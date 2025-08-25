from flask import Flask, jsonify
import pika
import json
import os

app = Flask(__name__)
payments = []

RABBIT_HOST = os.environ.get("RABBIT_HOST", "rabbitmq")

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue='order_created')

def process_order(ch, method, properties, body):
    order = json.loads(body)
    payment = {"order_id": order["order_id"], "status": "paid"}
    payments.append(payment)
    print(f"Processed payment: {payment}")

channel.basic_consume(queue='order_created', on_message_callback=process_order, auto_ack=True)

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(payments)

if __name__ == "__main__":
    print("Waiting for orders to process payment...")
    channel.start_consuming()
