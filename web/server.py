# web/server.py
import os
from flask import Flask, request, jsonify
from database.db import init_db, get_session
from database.models import Deposit, User
from decimal import Decimal

app = Flask(__name__)

# Initialize DB tables on startup (safe for Railway)
init_db()

TASKER_SECRET = os.getenv("TASKER_SECRET_KEY", "change_me")
BOT_WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # if using webhooks later

@app.route("/")
def index():
    return "Bingo Web Server Running"

@app.route("/tasker-deposit", methods=["POST"])
def tasker_deposit():
    # Basic security: require Authorization header with TASKER_SECRET
    auth = request.headers.get("Authorization", "")
    if auth != TASKER_SECRET:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json or {}
    # Expected fields: sender_phone, amount, transaction_id
    sender = data.get("sender_phone")
    amount = data.get("amount")
    txid = data.get("transaction_id")

    if not sender or not amount or not txid:
        return jsonify({"error": "missing_fields"}), 400

    # map sender phone to user (if previously assigned)
    session = get_session()
    try:
        user = session.query(User).filter(User.phone_number == sender).first()
        # create deposit record (pending)
        deposit = Deposit(user_id=user.id if user else None,
                          amount=Decimal(str(amount)),
                          transaction_id=txid,
                          sender_phone=sender,
                          status="pending")
        session.add(deposit)
        session.commit()

        # You might want to notify the telegram user via the bot
        return jsonify({"status":"ok","deposit_id": deposit.id}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": "server_error", "detail": str(e)}), 500
    finally:
        session.close()

@app.route("/admin/health")
def admin_health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
