from flask import Flask
from dotenv import load_dotenv
import os

from blueprint_routes.user import users_bp
from blueprint_routes.ppe_authorization import ppe_bp
load_dotenv()

app = Flask(__name__)



# register blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(ppe_bp, url_prefix="/ppe")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
