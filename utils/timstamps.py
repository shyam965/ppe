from datetime import datetime, timedelta
import pytz


def unique_timestamp():
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist)
    future_time = current_time + timedelta(hours=5, minutes=30)
    return str(future_time.timestamp() * 1000).split(".")[0]


print("unique_timestamp :- ", unique_timestamp())
