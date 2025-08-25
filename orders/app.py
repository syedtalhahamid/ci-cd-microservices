from flask import Flask, jsonify
import pika
import json
import os

app = Flask(__name__)
orders = []

RABBIT_HOST = os.environ.get("RABBIT_HOST", "rabbitmq")

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue='cart_updated')
channel.queue_declare(queue='order_created')

def process_cart(ch, method, properties, body):
    data = json.loads(body)
    order = {"order_id": len(orders)+1, "items": data}
    orders.append(order)
    # Publish order created event
    channel.basic_publish(exchange='',
                          routing_key='order_created',
                          body=json.dumps(order))
    print(f"Processed cart to order: {order}")

channel.basic_consume(queue='cart_updated', on_message_callback=process_cart, auto_ack=True)

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == "__main__":
    print("Waiting for cart events...")
    channel.start_consuming()
