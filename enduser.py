# This file contains all the actions a user can do with the books table.
# Query, save, add, delete, etc based on the the value of the change address value.

from colorama import Fore, Style
import admin
import pandas as pd
import psycopg2


class InvalidSelection(Exception):
    pass


class TooLong(Exception):
    pass


config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}


def add_book():
    # Getting all the input values for the new book
    while True:  # Author
        try:
            input_author = input(Fore.GREEN + "Author(s): " + Style.RESET_ALL)
            if len(input_author) > 255:
                raise TooLong
        except TooLong:
            print(Fore.RED + "Character limit is 255." + Style.RESET_ALL)
        else:
            break

    while True:  # Title
        try:
            input_title = input(Fore.GREEN + "Title: " + Style.RESET_ALL)
            if len(input_author) > 255:
                raise TooLong
        except TooLong:
            print(Fore.RED + "Character limit is 255." + Style.RESET_ALL)
        else:
            break

    while True:  # Language
        try:
            input_language = input(Fore.GREEN + "Language (e.g. EN, HU, FR, DE, etc): " + Style.RESET_ALL)
            if len(input_language) > 2:
                raise TooLong
        except TooLong:
            print(Fore.RED + "Character limit is 2." + Style.RESET_ALL)
        else:
            break

    while True:  # Number of pages
        try:
            input_pages = int(input(Fore.GREEN + "Number of pages: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Please enter a whole number." + Style.RESET_ALL)
        else:
            break

    while True:  # ISBN
        try:
            input_isbn = int(input(Fore.GREEN + "ISBN: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Please enter a whole number." + Style.RESET_ALL)
        else:
            break

    while True:  # Year
        try:
            input_year = int(input(Fore.GREEN + "Year: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Please enter a whole number." + Style.RESET_ALL)
        else:
            break

    print(input_author)
    print(input_title)
    print(input_language)
    print(input_pages)
    print(input_isbn)
    print(input_year)

    my_dict = {
        "input_author": input_author,
        "input_title": input_title,
        "input_language": input_language,
        "input_pages": input_pages,
        "input_isbn": input_isbn,
        "input_year": input_year
    }

    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                create_book = '''
                    INSERT INTO books (
                    author, title, language, pages, isbn, year)
                    VALUES
                    (
                    %(input_author)s,
                    %(input_title)s,
                    %(input_language)s,
                    %(input_pages)s,
                    %(input_isbn)s,
                    %(input_year)s
                    )
                '''
                cursor.execute(create_book, my_dict)
                conn.commit()
                print(Fore.GREEN + "Book added successfully" + Style.RESET_ALL)

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)


def check_permissions(username):
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = f"SELECT admin FROM users WHERE email='{username}';"
                cursor.execute(query)
                result_admin = cursor.fetchall()
                query2 = f"SELECT change FROM users WHERE email='{username}';"
                cursor.execute(query2)
                result_change = cursor.fetchall()

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    return int(result_admin[0][0]), int(result_change[0][0])


def load_all_books():
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = 'SELECT author, title, language, pages, isbn, year from books'
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convert fetched rows into a Pandas DataFrame
                if rows:
                    pd.set_option('display.width', 200)
                    df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                    pd.set_option('display.max_rows', None)
                    pd.set_option('display.max_columns', None)
                    print("DataFrame for the books table")
                    print(df)
                else:
                    print("No data found in the books table")

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    return df


def read_menu():
    print("1 - Load all books")
    print("2 - Search for books")
    while True:
        try:
            selection = int(input(Fore.GREEN + "Select from the above options: " + Style.RESET_ALL))
            if selection not in range(1, 3):
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid Selection" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Value Error" + Style.RESET_ALL)
        else:
            if selection == 1:
                load_all_books()
            else:
                pass  # TODO


def change_manu():
    print("1 - Load all books")
    print("2 - Search for books")
    print("3 - Add book")
    while True:
        try:
            selection = int(input(Fore.GREEN + "Select from the above options: " + Style.RESET_ALL))
            if selection not in range(1, 4):
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid Selection" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Value Error" + Style.RESET_ALL)
        else:
            if selection == 1:
                load_all_books()
            elif selection == 2:
                pass  # TODO
            else:
                add_book()
                break


def main(username):
    admin_change_access = check_permissions(username)
    print("Admin: ", admin_change_access[0])
    print("Change: ", admin_change_access[1])
    if admin_change_access[0] == 1:
        admin.main()
    else:
        if admin_change_access[1] == 0:
            read_menu()
        else:
            change_manu()

"""
# This is only for testing purposes. Remove it when it's linked with the login file.
email_address_test = input("Email address: ")
main(email_address_test)
"""

