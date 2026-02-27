from flask import Flask, request, jsonify
import mysql.connector
import uuid

app = Flask(__name__)

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="campus"
)

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.json

    ticket_id = str(uuid.uuid4())[:8]

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tickets (ticket_id, name, email, event, seat) VALUES (%s,%s,%s,%s,%s)",
        (ticket_id, data['name'], data['email'], data['event'], data['seat'])
    )
    db.commit()

    return jsonify({
        "message": "Booking successful",
        "ticket_id": ticket_id
    })

@app.route('/validate/<ticket_id>', methods=['GET'])
def validate(ticket_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id=%s", (ticket_id,))
    result = cursor.fetchone()

    if result:
        return jsonify({"status": "Valid Ticket"})
    else:
        return jsonify({"status": "Invalid Ticket"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)