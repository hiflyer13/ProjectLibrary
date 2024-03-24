# This file contains all the actions a user can do with the books table.
# Query, save, add, delete, etc based on the the value of the change address value.

from colorama import Fore, Style
import admin
import datetime
import os
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

    while True:
        try:
            selection = input(Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
            if selection not in ["s", "e"]:
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
        else:
            if selection == "s":
                current_time = datetime.datetime.now()
                current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{current_time_cleaned}.xlsx"
                path = os.path.join("search_results", filename)
                df.to_excel(path, index=False)
                break
            else:
                exit()


def search_books():
    print("Search by:")
    print("1 - Author")
    print("2 - Title")
    print("3 - Language")
    print("4 - Year")
    print("5 - ISBN")

    while True:
        try:
            selection = int(input(Fore.GREEN + "Your choice: " + Style.RESET_ALL))
            if selection not in range(1, 6):
                raise InvalidSelection
        except ValueError:
            print(Fore.RED + "Enter a whole number" + Style.RESET_ALL)
        except InvalidSelection:
            print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
        else:
            break

    match selection:

        case 1:  # Author
            search_by = input(Fore.GREEN + "Search by author: " + Style.RESET_ALL)
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        # Query to select all rows from the specified table
                        query = "SELECT author, title, language, pages, isbn, year from books WHERE author LIKE '%%{}%'".format(
                            search_by)

                        cursor.execute(query)
                        rows = cursor.fetchall()

                        # Convert fetched rows into a Pandas DataFrame
                        if rows:
                            pd.set_option('display.width', 200)
                            df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                            pd.set_option('display.max_rows', None)
                            pd.set_option('display.max_columns', None)
                            print("Search results:")
                            print(df)
                        else:
                            print("No data found in the books table")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

            while True:
                try:
                    selection = input(
                        Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
                    if selection not in ["s", "e"]:
                        raise InvalidSelection
                except InvalidSelection:
                    print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                else:
                    if selection == "s":
                        current_time = datetime.datetime.now()
                        current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{current_time_cleaned}.xlsx"
                        path = os.path.join("search_results", filename)
                        df.to_excel(path, index=False)
                        break
                    else:
                        exit()

        case 2:  # Title
            search_by = input(Fore.GREEN + "Search by title: " + Style.RESET_ALL)
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        # Query to select all rows from the specified table
                        query = "SELECT author, title, language, pages, isbn, year from books WHERE title LIKE '%%{}%'".format(
                            search_by)

                        cursor.execute(query)
                        rows = cursor.fetchall()

                        # Convert fetched rows into a Pandas DataFrame
                        if rows:
                            pd.set_option('display.width', 200)
                            df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                            pd.set_option('display.max_rows', None)
                            pd.set_option('display.max_columns', None)
                            print("Search results:")
                            print(df)
                        else:
                            print("No data found in the books table")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

            while True:
                try:
                    selection = input(
                        Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
                    if selection not in ["s", "e"]:
                        raise InvalidSelection
                except InvalidSelection:
                    print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                else:
                    if selection == "s":
                        current_time = datetime.datetime.now()
                        current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{current_time_cleaned}.xlsx"
                        path = os.path.join("search_results", filename)
                        df.to_excel(path, index=False)
                        break
                    else:
                        exit()

        case 3:  # Language
            search_by = input(Fore.GREEN + "Search by language: " + Style.RESET_ALL)
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        # Query to select all rows from the specified table
                        query = "SELECT author, title, language, pages, isbn, year from books WHERE language LIKE '%%{}%'".format(
                            search_by)

                        cursor.execute(query)
                        rows = cursor.fetchall()

                        # Convert fetched rows into a Pandas DataFrame
                        if rows:
                            pd.set_option('display.width', 200)
                            df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                            pd.set_option('display.max_rows', None)
                            pd.set_option('display.max_columns', None)
                            print("Search results:")
                            print(df)
                        else:
                            print("No data found in the books table")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

            while True:
                try:
                    selection = input(
                        Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
                    if selection not in ["s", "e"]:
                        raise InvalidSelection
                except InvalidSelection:
                    print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                else:
                    if selection == "s":
                        current_time = datetime.datetime.now()
                        current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{current_time_cleaned}.xlsx"
                        path = os.path.join("search_results", filename)
                        df.to_excel(path, index=False)
                        break
                    else:
                        exit()

        case 4:  # Year
            search_by = input(Fore.GREEN + "Search by year: " + Style.RESET_ALL)
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        # Query to select all rows from the specified table
                        query = "SELECT author, title, language, pages, isbn, year from books WHERE year = '{}'".format(
                            search_by)

                        cursor.execute(query)
                        rows = cursor.fetchall()

                        # Convert fetched rows into a Pandas DataFrame
                        if rows:
                            pd.set_option('display.width', 200)
                            df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                            pd.set_option('display.max_rows', None)
                            pd.set_option('display.max_columns', None)
                            print("Search results:")
                            print(df)
                        else:
                            print("No data found in the books table")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

            while True:
                try:
                    selection = input(
                        Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
                    if selection not in ["s", "e"]:
                        raise InvalidSelection
                except InvalidSelection:
                    print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                else:
                    if selection == "s":
                        current_time = datetime.datetime.now()
                        current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{current_time_cleaned}.xlsx"
                        path = os.path.join("search_results", filename)
                        df.to_excel(path, index=False)
                        break
                    else:
                        exit()

        case 5:  # ISBN
            search_by = input(Fore.GREEN + "Search by ISBN: " + Style.RESET_ALL)
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        # Query to select all rows from the specified table
                        query = "SELECT author, title, language, pages, isbn, year from books WHERE isbn LIKE '%%{}%'".format(
                            search_by)

                        cursor.execute(query)
                        rows = cursor.fetchall()

                        # Convert fetched rows into a Pandas DataFrame
                        if rows:
                            pd.set_option('display.width', 200)
                            df = pd.DataFrame(rows, columns=['author', 'title', 'language', 'pages', 'isbn', 'year'])
                            pd.set_option('display.max_rows', None)
                            pd.set_option('display.max_columns', None)
                            print("Search results:")
                            print(df)
                        else:
                            print("No data found in the books table")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

            while True:
                try:
                    selection = input(
                        Fore.GREEN + "Press 's' to save the results in a file or 'e' to exit program. " + Style.RESET_ALL)
                    if selection not in ["s", "e"]:
                        raise InvalidSelection
                except InvalidSelection:
                    print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                else:
                    if selection == "s":
                        current_time = datetime.datetime.now()
                        current_time_cleaned = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"{current_time_cleaned}.xlsx"
                        path = os.path.join("search_results", filename)
                        df.to_excel(path, index=False)
                        break
                    else:
                        exit()


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
                break
            else:
                search_books()
                break


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
                break
            elif selection == 2:
                search_books()
                break
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
