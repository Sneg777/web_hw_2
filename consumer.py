import pika
import json
import sys
import os
from bson import ObjectId
from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='HW_08 events message', exchange_type='fanout')
    q = channel.queue_declare(queue="")
    name_q = q.method.queue
    channel.queue_bind(exchange='HW_08 events message', queue=name_q)

    def send_email(contact_id):
        contact = Contact.objects(id=ObjectId(contact_id)).first()
        if contact and not contact.sent:
            print(f"Sending email to: {contact.fullname} with ({contact.email})")

            contact.sent = True
            contact.save()

            print(f"Email sent to: {contact.fullname}")
        else:
            print(f"Contact {contact_id} not found or already sent")

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        contact_id = data["contact_id"]
        send_email(contact_id)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=name_q, on_message_callback=callback, auto_ack=False)
    print("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
