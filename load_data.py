from mongoengine import connect
import json
from models import Author, Quote

def load_authors(filename):
    with open(filename, 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

def load_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            quote = Quote(
                author=author,
                tags=quote_data['tags'],
                quote=quote_data['quote']
            )
            quote.save()

if __name__ == '__main__':
    connect(db='My_Data', username='Siia', password='Dartiana95', host='mongodb+srv://Siia:Dartiana95@mycluster.39vlnle.mongodb.net/My_Data')
    load_authors('authors.json')
    load_quotes('quotes.json')
