# blueprint_routes/ppe_authorization.py
import os
import cv2
import base64
import threading
import time
from collections import deque
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import pymongo
import pygame

from flask import Blueprint, Response, render_template, current_app
from ultralytics import YOLO

# project config modules (must exist in your repo)
from configs_and_constants.db import db
from configs_and_constants.env import env

ppe_bp = Blueprint("ppe_authorization", __name__, template_folder="../templates")

# --------------------- Configs (env overrides) ---------------------
MODEL_PATH = env.get("MODEL_PATH", os.path.join(os.getcwd(), "yolo.pt"))
ALARM_SOUND = env.get("ALARM_SOUND", os.path.join(os.getcwd(), "preview.mp3"))
FPS = int(env.get("FPS", 20))
PRE_EVENT_SECONDS = float(env.get("PRE_EVENT_SECONDS", 2.5))
POST_EVENT_SECONDS = float(env.get("POST_EVENT_SECONDS", 2.5))
LINE_Y = int(env.get("LINE_Y", 400))
ALERT_IMAGE_DIR = env.get("ALERT_IMAGE_DIR", "alerts_images")
ALERT_VIDEO_DIR = env.get("ALERT_VIDEO_DIR", "alerts_videos")
ALERT_COOLDOWN_SECONDS = int(env.get("ALERT_COOLDOWN_SECONDS", 120))  # cooldown between alerts
MONGO_COLLECTION = env.get("MONGO_COLLECTION", "alerts")

ALERT_EMAIL_FROM = env.get("ALERT_EMAIL_FROM")
ALERT_EMAIL_PASSWORD = env.get("ALERT_EMAIL_PASSWORD")
ALERT_EMAIL_TO = env.get("ALERT_EMAIL_TO")

# Ensure folders exist
os.makedirs(ALERT_IMAGE_DIR, exist_ok=True)
os.makedirs(ALERT_VIDEO_DIR, exist_ok=True)

# --------------------- Globals ---------------------
# Load model (may take time at startup)
try:
    model = YOLO(MODEL_PATH)
    print(f"[YOLO] Loaded model from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"[YOLO ERROR] Failed to load model at {MODEL_PATH}: {e}")

frame_buffer_len = int(PRE_EVENT_SECONDS * FPS) + 5
frame_buffer = deque(maxlen=frame_buffer_len)

# Video writing control
video_recording_active = False
video_writer_object = None
video_frames_to_write_after_alert = 0
current_alert_video_path = None

# Alarm & cooldown
pygame_inited = False
active_alarm = False
LAST_ALERT_TIME = None

# Threaded email semaphore (limit concurrent)
email_semaphore = threading.BoundedSemaphore(value=2)

# Mongo collection handle
alerts_collection = db[MONGO_COLLECTION] if db is not None else None

# Colors & font
FONT = cv2.FONT_HERSHEY_SIMPLEX


# --------------------- Utility functions ---------------------
def init_pygame():
    global pygame_inited
    if not pygame_inited:
        try:
            pygame.mixer.init()
            pygame_inited = True
            print("[Pygame] mixer initialized")
        except Exception as e:
            print(f"[Pygame ERROR] mixer init failed: {e}")


def play_alarm():
    global active_alarm
    init_pygame()
    if not active_alarm and pygame_inited and os.path.exists(ALARM_SOUND):
        try:
            active_alarm = True
            pygame.mixer.music.load(ALARM_SOUND)
            pygame.mixer.music.play(loops=0)
            print("[ALARM] playing")
        except Exception as e:
            print(f"[ALARM ERROR] {e}")


def stop_alarm():
    global active_alarm
    if pygame_inited:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
    active_alarm = False


def insert_alert_to_mongo(reason, image_path=None, video_path=None, unauthorized_count=0, total_people=0):
    if alerts_collection is None:
        print("[MONGO ERROR] No collection configured")
        return
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "reason": reason,
        "status": "Open",
        "total_people": total_people,
        "unauthorized_count": unauthorized_count,
        "image_path": image_path,
        "video_path": video_path,
    }
    try:
        alerts_collection.insert_one(doc)
        print(f"[MONGO] Alert inserted: {reason}")
    except Exception as e:
        print(f"[MONGO ERROR] insert failed: {e}")


def send_email_with_media(to_email, subject, body, image_path=None, video_path=None):
    """Sends an email synchronously (called inside a daemon thread)."""
    if not ALERT_EMAIL_FROM or not ALERT_EMAIL_PASSWORD or not to_email:
        print("[EMAIL] Missing email config; skipping send")
        return

    msg = MIMEMultipart()
    msg["From"] = ALERT_EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(image_path)}"')
                msg.attach(part)

        # Optional: attach video only if small / enabled
        # if video_path and os.path.exists(video_path):
        #     with open(video_path, "rb") as f:
        #         part = MIMEBase("application", "octet-stream")
        #         part.set_payload(f.read())
        #         encoders.encode_base64(part)
        #         part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(video_path)}"')
        #         msg.attach(part)

        with email_semaphore:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(ALERT_EMAIL_FROM, ALERT_EMAIL_PASSWORD)
                server.sendmail(ALERT_EMAIL_FROM, to_email, msg.as_string())
                print(f"[EMAIL] Sent to {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")


def send_email_with_media_async(to_email, subject, body, image_path=None, video_path=None):
    thread = threading.Thread(
        target=lambda: send_email_with_media(to_email, subject, body, image_path, video_path),
        daemon=True,
    )
    thread.start()


# --------------------- Detection & frame processing ---------------------
def process_frame(frame):
    """
    Detect PPE and unauthorized persons below the LINE_Y.
    Returns annotated frame and detection summary.
    """
    global video_recording_active, video_writer_object, video_frames_to_write_after_alert, current_alert_video_path, LAST_ALERT_TIME

    if model is None:
        # If model not loaded, just return frame
        return frame, {"person_count": 0, "unauthorized_count": 0, "vest_count": 0, "hardhat_count": 0, "unauthorized": []}

    h, w, _ = frame.shape
    # store for pre-event buffering
    frame_buffer.append(frame.copy())

    # Run YOLO prediction (adjust conf as needed)
    results = model.predict(frame, conf=0.45, show=False, verbose=False)[0]

    boxes = results.boxes.xyxy.cpu().numpy() if getattr(results, "boxes", None) is not None else []
    classes = results.boxes.cls.cpu().numpy() if getattr(results, "boxes", None) is not None else []

    names = results.names  # mapping of class id -> name

    person_boxes = [box for box, cls in zip(boxes, classes) if names[int(cls)] == "person"]
    vest_boxes = [box for box, cls in zip(boxes, classes) if names[int(cls)] == "vest"]
    hardhat_boxes = [box for box, cls in zip(boxes, classes) if names[int(cls)] == "hardhat"]

    unauthorized_persons = []
    authorized_count = 0

    # Draw the 2m line
    cv2.line(frame, (0, LINE_Y), (w, LINE_Y), (255, 0, 0), 2)
    cv2.putText(frame, "2m Zone", (10, LINE_Y - 10), FONT, 0.6, (255, 0, 0), 2)

    # helper to test overlap
    def overlaps(b1, b2):
        x1, y1, x2, y2 = b1
        X1, Y1, X2, Y2 = b2
        return not (x2 < X1 or X2 < x1 or y2 < Y1 or Y2 < y1)

    for idx, (px1, py1, px2, py2) in enumerate(person_boxes):
        # person considered if below the line (entering restricted zone)
        if py2 > LINE_Y:
            has_vest = any(overlaps((px1, py1, px2, py2), vbox) for vbox in vest_boxes)
            has_hardhat = any(overlaps((px1, py1, px2, py2), hbox) for hbox in hardhat_boxes)

            if has_vest and has_hardhat:
                auth_status = "Authorized"
                authorized_count += 1
                color = (0, 255, 0)
            else:
                auth_status = "Unauthorized"
                color = (0, 0, 255)
                if not has_vest and not has_hardhat:
                    reason = "Missing vest and hardhat"
                elif not has_vest:
                    reason = "Missing vest"
                else:
                    reason = "Missing hardhat"
                unauthorized_persons.append({
                    "bbox": (float(px1), float(py1), float(px2), float(py2)),
                    "label": f"Person {idx+1}",
                    "reason": reason
                })

            cv2.rectangle(frame, (int(px1), int(py1)), (int(px2), int(py2)), color, 2)
            cv2.putText(frame, f"Person {idx+1}: {auth_status}", (int(px1), int(py1) - 10), FONT, 0.45, color, 1)

    alert_triggered = len(unauthorized_persons) > 0

    # Cooldown check
    current_time = datetime.utcnow()
    cooldown_elapsed = (current_time - LAST_ALERT_TIME).total_seconds() if LAST_ALERT_TIME else float("inf")

    if alert_triggered and cooldown_elapsed > ALERT_COOLDOWN_SECONDS:
        # Trigger alarm + save screenshot + build video (start with buffer)
        play_alarm()
        LAST_ALERT_TIME = current_time

        timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_filename = f"unauthorized_ppe_{timestamp_str}.jpg"
        screenshot_path = os.path.join(ALERT_IMAGE_DIR, screenshot_filename)
        cv2.imwrite(screenshot_path, frame)
        print(f"[FILE] Screenshot saved: {screenshot_path}")

        # Prepare video writer
        video_filename = f"unauthorized_ppe_{timestamp_str}.avi"
        current_alert_video_path = os.path.join(ALERT_VIDEO_DIR, video_filename)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        vw = cv2.VideoWriter(current_alert_video_path, fourcc, FPS, (w, h))

        # write buffer frames (pre-event)
        for bf in frame_buffer:
            vw.write(bf)

        # mark global writer so subsequent frames are appended for POST_EVENT_SECONDS
        global video_writer_object, video_recording_active, video_frames_to_write_after_alert
        video_writer_object = vw
        video_recording_active = True
        video_frames_to_write_after_alert = int(POST_EVENT_SECONDS * FPS)

        # Insert to Mongo
        reasons_summary = "; ".join([f"{p['label']}: {p['reason']}" for p in unauthorized_persons])
        insert_alert_to_mongo(reasons_summary, image_path=screenshot_path, video_path=current_alert_video_path,
                              unauthorized_count=len(unauthorized_persons),
                              total_people=authorized_count + len(unauthorized_persons))

        # Send email async
        subject = "Unauthorized PPE Alert Detected"
        body = f"An unauthorized PPE event was detected.\n\nReason:\n{reasons_summary}\n\nTime: {timestamp_str}"
        send_email_with_media_async(ALERT_EMAIL_TO, subject, body, image_path=screenshot_path, video_path=current_alert_video_path)

    # If currently recording, write current frame until post-event frames exhausted
    if video_recording_active:
        if video_frames_to_write_after_alert > 0:
            if video_writer_object is not None:
                video_writer_object.write(frame)
            video_frames_to_write_after_alert -= 1
        else:
            # finish and release writer
            if video_writer_object is not None:
                try:
                    video_writer_object.release()
                    print(f"[VIDEO] Saved: {current_alert_video_path}")
                except Exception:
                    pass
            video_writer_object = None
            video_recording_active = False
            # stop the alarm once clip done (optional)
            stop_alarm()

    summary = {
        "person_count": len(person_boxes),
        "unauthorized_count": len(unauthorized_persons),
        "vest_count": len(vest_boxes),
        "hardhat_count": len(hardhat_boxes),
        "unauthorized": unauthorized_persons
    }
    return frame, summary


# --------------------- Frame generator ---------------------
def find_working_camera(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap is not None and cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None


def generate_frames(camera_index=None):
    # open camera
    cam_index = camera_index if camera_index is not None else find_working_camera()
    if cam_index is None:
        raise RuntimeError("No working camera found.")

    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame, summary = process_frame(frame)

        # attempt to emit via Flask-SocketIO if initialized
        try:
            # emit on default namespace; this will only work if SocketIO instance is running
            from flask_socketio import emit
            emit("update", {
                "frame": base64.b64encode(cv2.imencode(".jpg", annotated_frame)[1]).decode("utf-8"),
                "person_count": summary["person_count"],
                "unauthorized_count": summary["unauthorized_count"],
                "vest_count": summary["vest_count"],
                "hardhat_count": summary["hardhat_count"]
            }, namespace="/", broadcast=True)
        except Exception:
            # not fatal — it just means SocketIO isn't initialized here
            pass

        _, buffer = cv2.imencode(".jpg", annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
    cap.release()


# --------------------- Routes ---------------------
@ppe_bp.route("/")
def index():
    # render a simple template (create templates/index.html in your project)
    # For minimal usage you can return a tiny html here or create a templates file.
    try:
        return render_template("index.html")
    except Exception:
        # fallback small page
        return """
        <html><body>
        <h3>PPE Monitoring</h3>
        <img src="/ppe/test_authorized" style="max-width:100%;"/>
        </body></html>
        """


@ppe_bp.route("/test_authorized")
def test_authorized():
    """MJPEG stream route: visit /ppe/test_authorized"""
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
