# Creating all the different functions for each value in the user registration form.
# At the end, put them into correspondent variables and add them to the database.

from colorama import Fore, Back, Style
import datetime
import hashlib
import psycopg2
import re


class AlreadyExists(Exception):
    pass


class InvalidEmail(Exception):
    pass


class InvalidPassword(Exception):
    pass


class TooLong(Exception):
    pass


# Connection details
config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}


def get_email():
    # Table name to query
    table_name = 'users'
    existing_email_addresses = []
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = 'SELECT email FROM {};'.format(table_name)
                cursor.execute(query)
                rows = cursor.fetchall()
                for i in rows:
                    existing_email_addresses.append(i[0])

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    while True:
        try:
            email_address = input(Fore.GREEN + "Email address: " + Style.RESET_ALL)

            def isvalid(email):
                email_pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
                if re.fullmatch(email_pattern, email):
                    valid = True
                else:
                    valid = False

                return valid

            if not isvalid(email_address):
                raise InvalidEmail

            if len(email_address) > 255:
                raise TooLong

            if email_address in existing_email_addresses:
                raise AlreadyExists

        except InvalidEmail:
            print(Fore.RED + "Invalid email address" + Style.RESET_ALL)
        except TooLong:
            print(Fore.RED + "Email address is too long, character limit is 255" + Style.RESET_ALL)
        except AlreadyExists:
            print(Fore.RED + "Email address already exists" + Style.RESET_ALL)
        else:
            return email_address
        # Later we need to check if it exists in the database. If it does, we need to return an error.


def get_first_name():
    while True:
        try:
            input_first_name = input(Fore.GREEN + "First Name: " + Style.RESET_ALL)
            if len(input_first_name) > 255:
                raise TooLong
        except TooLong:
            print(Fore.RED + "First name is too long, character limit is 255" + Style.RESET_ALL)
        else:
            return input_first_name


def get_family_name():
    while True:
        try:
            input_family_name = input(Fore.GREEN + "Family Name: " + Style.RESET_ALL)
            if len(input_family_name) > 255:
                raise TooLong
        except TooLong:
            print(Fore.RED + "Family name is too long, character limit is 255" + Style.RESET_ALL)
        else:
            return input_family_name


def get_birthdate():
    while True:
        try:
            birthdate_input = input(Fore.GREEN + "Birth date (YYYYMMDD): " + Style.RESET_ALL)
            format_input = "%Y%m%d"
            datetime_object = datetime.datetime.strptime(birthdate_input, format_input)
            datetime_object_string = datetime_object.strftime("%Y-%m-%d")
        except ValueError:
            print(Fore.RED + "Invalid Birth Date" + Style.RESET_ALL)
        else:
            return datetime_object_string


def get_password():
    while True:
        try:
            input_password = input(Fore.GREEN + "Password: " + Style.RESET_ALL)
            digits_pattern = r'[0-9]'
            upper_pattern = r'[A-Z]'
            lower_pattern = r'[a-z]'
            numbers = re.findall(digits_pattern, input_password)
            upper_case = re.findall(upper_pattern, input_password)
            lower_case = re.findall(lower_pattern, input_password)
            if len(input_password) < 8 or not numbers or not upper_case or not lower_case:
                raise InvalidPassword
        except InvalidPassword:
            print(Fore.RED + """Password rules:
            - Must contain at least 8 characters
            - Must contain at least 1 digit
            - Must contain at least 1 lower case letter
            - Must contain at least 1 upper case letter""" + Style.RESET_ALL)
        else:
            # hashing the password
            # Create an SHA-256 hash object
            hash_object = hashlib.sha256()
            # Convert the password to bytes and hash it
            hash_object.update(input_password.encode())
            # Get the hex digest of the hash
            hash_password = hash_object.hexdigest()
            return hash_password


def main():
    email = get_email()
    first_name = get_first_name()
    family_name = get_family_name()
    birthdate = get_birthdate()
    password = get_password()
    my_dict = {
        "input_email": email,
        "input_first_name": first_name,
        "input_family_name": family_name,
        "input_birthdate": birthdate,
        "input_read": '1',
        "input_change": '0',
        "input_admin": '0',
        "input_login_attempts": '0',
        "input_password": password
    }
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                create_user = '''
                    INSERT INTO users (
                    email, first_name, family_name, birthdate, read, change, admin, login_attempts, password)
                    VALUES
                    (
                    %(input_email)s,
                    %(input_first_name)s,
                    %(input_family_name)s,
                    %(input_birthdate)s,
                    %(input_read)s,
                    %(input_change)s,
                    %(input_admin)s,
                    %(input_login_attempts)s,
                    %(input_password)s)
                '''
                cursor.execute(create_user, my_dict)
                conn.commit()
                print(Fore.GREEN + "User created successfully" + Style.RESET_ALL)

    except psycopg2.Error as e:
        print(Fore.RED + "Error connecting to the database:" + Style.RESET_ALL, e)


#main()
