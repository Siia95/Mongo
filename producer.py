import pika
import json
import random
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField

fake = Faker()

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

# Генерація фейкових контактів
num_contacts = 10
contacts = []
for _ in range(num_contacts):
    contact = Contact(full_name=fake.name(), email=fake.email())
    contact.save()
    contacts.append(contact)

# Надсилання повідомлень до черги
for contact in contacts:
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='contact_queue', body=json.dumps(message))
    print(f"Sent message for contact: {contact.full_name}")

connection.close()
