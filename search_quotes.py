from mongoengine import connect
from mongoengine.queryset.visitor import Q
from models import Author, Quote

def search_by_name(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.quote)
    else:
        print("Author not found.")

def search_by_tag(tag):
    quotes = Quote.objects(tags__icontains=tag)
    for quote in quotes:
        print(quote.quote)

def search_by_tags(tags_str):
    tags = tags_str.split(',')
    query = Q()
    for tag in tags:
        query |= Q(tags__icontains=tag)
    quotes = Quote.objects(query)
    for quote in quotes:
        print(quote.quote)

if __name__ == '__main__':
    connect(db='My_Data', username='Siia', password='Dartiana95', host='mongodb+srv://Siia:Dartiana95@mycluster.39vlnle.mongodb.net/My_Data')

    while True:
        command = input("Enter command: ")
        if command == 'exit':
            break
        else:
            action, value = command.split(':')
            if action == 'name':
                search_by_name(value)
            elif action == 'tag':
                search_by_tag(value)
            elif action == 'tags':
                search_by_tags(value)
            else:
                print("Invalid command.")
