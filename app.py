from models import (Base, session, Book, engine)
import datetime
import csv
import time


def clean_date(date):
    try:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        date_list = date.split(' ')
        month = int(months.index(date_list[0]) + 1)
        day = int(date_list[1].split(',')[0]) 
        year = int(date_list[2])
        return_date = datetime.date(year, month, day)
        
    except ValueError:
            input('''
                \r***Date Erorr***
                \rThe Date format is invalid
                \rPlease input the date in Month Day, Year
                \rExample: October 26, 2020
                \rPlease hit enter and try again
                \r****************''')
            return
    return return_date
    
def clean_price(price):
    try:
        cleaned_price = float(price)
        new_price = int(cleaned_price * 100)
    except ValueError:   
        input('''
              \r***Price Erorr***
              \rThe Price format is invalid
              \rPrice should be dollar and cents with no currency symbol
              \rExample: 29.99
              \rPlease hit enter and try again
              \r****************''')
        return
    return new_price
    
def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile) 
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
                session.commit()


def menu():
    while True:
        print('''
            \nProgramming Books
            \r1) Add Book
            \r2) View All Books
            \r3) Search 
            \r4) Book Analysis
            \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ['1','2','3','4','5']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above
                  \rSelect and option 1-5
                  \rPress enter to continue''')
            
            
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Date Published (Ex. October 22, 2019): ')
                date_fixed = clean_date(date)
                if type(date_fixed) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex. 9.99): ')
                fixed_price = clean_price(price)
                if type(fixed_price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date_fixed, price=fixed_price)
            session.add(new_book)
            session.commit()
            print(f'{title} was successfully added!')
            time.sleep(1.5)        
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input("Press enter to return to main menu...")
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        else:
            print('goodbye')
            app_running = False
    
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
 