import pika
import json
import time

from faker import Faker
from models import Contact

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW_08 events message', exchange_type='fanout')




def main():
    for _ in range(10):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()
        message = json.dumps({"contact_id": str(contact.id)})

        channel.basic_publish(
            exchange="HW_08 events message",
            routing_key="",
            body=message.encode()
        )
        print(f"Added to queue: {contact.fullname} ({contact.email})")

        time.sleep(1)

    connection.close()


if __name__ == '__main__':
    main()
