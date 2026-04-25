from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import re
import os

app = Flask(__name__)

print("🚀 Starting Flask server...")

# -----------------------------
# DEBUG: Check files in folder
# -----------------------------
print("📂 Files in current folder:", os.listdir())

# -----------------------------
# Firebase Initialization
# -----------------------------
db = None

try:
    firebase_path = r"C:\Users\shubh\OneDrive\Documents\data-redundancy-project\firebase_key.json"
    cred = credentials.Certificate(firebase_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase connected successfully")
except Exception as e:
    print("❌ Firebase connection failed:", e)

# -----------------------------
# Validation Functions
# -----------------------------
def is_valid_email(email):
    return bool(email and re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone(phone):
    return bool(phone and phone.isdigit() and len(phone) == 10)

# -----------------------------
# API ROUTE
# -----------------------------
@app.route("/add", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No JSON data"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    # Validation
    if not name or not email or not phone:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if not is_valid_email(email) or not is_valid_phone(phone):
        return jsonify({"status": "false_positive"})

    # Normalize
    email = email.strip().lower()
    phone = phone.strip()

    if db is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 500

    # Use email as UNIQUE document ID
    user_ref = db.collection("users").document(email)

    # Duplicate check
    if user_ref.get().exists:
        return jsonify({"status": "duplicate"})

    # Save data
    user_ref.set({
        "name": name.strip(),
        "email": email,
        "phone": phone,
        "status": "verified"
    })

    return jsonify({"status": "added"})

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return "🚀 Data Redundancy System Running Successfully!"

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)