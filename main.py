from flask import Flask, jsonify, request
from app.routes.task_routes import task_bp
from app.routes.auth_routes import auth_bp

app = Flask(__name__)
app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "OK"}

@app.route("/")
def home():
    return {"message": "TaskFlow API is live on Railway 🚀"}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
