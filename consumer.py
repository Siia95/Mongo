import pika
import json
from mongoengine import connect, Document, StringField, BooleanField

# З'єднання з MongoDB
connect(db='My_Data', username='Siia', password='Dartiana95', host='mongodb+srv://Siia:Dartiana95@mycluster.39vlnle.mongodb.net/My_Data')


class Contact(Document):
    full_name = StringField()
    email = StringField()
    message_sent = BooleanField(default=False)


# З'єднання з RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


def process_contact(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']

    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Симуляція надсилання повідомлення
        print(f"Sending message to: {contact.full_name}")
        contact.message_sent = True
        contact.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)


# Підписка на чергу та обробка повідомлень
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='contact_queue', on_message_callback=process_contact)

print("Consumer is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
