from flask import Flask, request, jsonify
import pika
import json
import os

app = Flask(__name__)
carts = []

RABBIT_HOST = os.environ.get("RABBIT_HOST", "rabbitmq")

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue='cart_updated')

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    carts.append(data)
    # Publish event
    channel.basic_publish(exchange='',
                          routing_key='cart_updated',
                          body=json.dumps(data))
    return jsonify({"message": "Item added to cart and event sent!"})

@app.route('/cart', methods=['GET'])
def get_cart():
    return jsonify(carts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
