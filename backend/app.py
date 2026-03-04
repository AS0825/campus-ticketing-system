from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import uuid
import time

app = Flask(__name__)
CORS(app)  # 🔥 Allow frontend (port 3000) to access backend

# ✅ Wait for MySQL to be ready (Docker safe)
while True:
    try:
        db = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="campus"
        )
        print("✅ Connected to MySQL")
        break
    except mysql.connector.Error as err:
        print("⏳ Waiting for MySQL...", err)
        time.sleep(5)

# -----------------------------------------
# BOOK TICKET (Multiple Seats + No Duplicate)
# -----------------------------------------
@app.route('/book', methods=['POST'])
def book_ticket():
    try:
        data = request.json
        ticket_id = str(uuid.uuid4())[:8]

        cursor = db.cursor()
        booked_seats = []

        for seat in data['seats']:

            # Check if seat already booked
            cursor.execute(
                "SELECT * FROM tickets WHERE event=%s AND seat=%s",
                (data['event'], seat)
            )
            existing = cursor.fetchone()

            if not existing:
                cursor.execute(
                    "INSERT INTO tickets (ticket_id, name, email, event, seat) VALUES (%s,%s,%s,%s,%s)",
                    (ticket_id, data['name'], data['email'], data['event'], seat)
                )
                booked_seats.append(seat)

        db.commit()

        return jsonify({
            "success": True,
            "ticket_id": ticket_id,
            "seats_confirmed": booked_seats
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------------
# GET BOOKED SEATS
# -----------------------------------------
@app.route('/booked-seats', methods=['GET'])
def booked_seats():
    try:
        event = request.args.get("event")
        cursor = db.cursor()
        cursor.execute("SELECT seat FROM tickets WHERE event=%s", (event,))
        results = cursor.fetchall()

        booked = [row[0] for row in results]

        return jsonify({"booked": booked})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------
# VALIDATE TICKET
# -----------------------------------------
@app.route('/validate/<ticket_id>', methods=['GET'])
def validate(ticket_id):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=%s", (ticket_id,))
        result = cursor.fetchone()

        if result:
            return jsonify({"status": "Valid Ticket"})
        else:
            return jsonify({"status": "Invalid Ticket"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)