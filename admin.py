# Admin functions to manipulate users in the database

from colorama import Fore, Back, Style
import hashlib
import pandas as pd
import psycopg2
import re


class InvalidPassword(Exception):
    pass


class InvalidSelection(Exception):
    pass


# Connection details
config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}

# Table name to query
table_name = 'users'


def load_users():
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = 'SELECT email, read, change, admin, locked FROM {};'.format(table_name)
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convert fetched rows into a Pandas DataFrame
                if rows:
                    df = pd.DataFrame(rows, columns=['email', 'read', 'change', 'admin', 'locked'])
                    print("DataFrame for the '{}' table:".format(table_name))
                    print(df)
                else:
                    print("No data found in the '{}' table.".format(table_name))

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    return df


def user_choice():
    while True:
        try:
            selection = int(input(Fore.GREEN + "Type the index of the user who you want to work with: " + Style.RESET_ALL))
            if selection not in range(1, len(users)):
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid Selection" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Value Error" + Style.RESET_ALL)
        else:
            user_to_work_with = users["email"].loc[selection]
            print(f"Your choice: {Fore.YELLOW + user_to_work_with + Style.RESET_ALL}")
            return user_to_work_with


def user_choice_2():
    print(Fore.GREEN + "ADMIN OPTIONS:" + Style.RESET_ALL)
    print(Fore.GREEN + "1 - Delete User" + Style.RESET_ALL)
    print(Fore.GREEN + "2 - Unlock User" + Style.RESET_ALL)
    print(Fore.GREEN + "3 - Reset Password" + Style.RESET_ALL)
    print(Fore.GREEN + "4 - Add change permission" + Style.RESET_ALL)
    print(Fore.GREEN + "5 - Remove change permission" + Style.RESET_ALL)

    while True:
        try:
            selection = int(input(Fore.GREEN +
                                  "Type the index of the user who you want to work with (except the admin): "
                                  + Style.RESET_ALL))
            if selection not in range(1, 6):
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid Selection" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Value Error" + Style.RESET_ALL)
        else:
            print(selection)
            return selection


def password():
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


def admin_actions(the_user, the_action):
    print(the_user)
    my_dict = {
        "input_email": the_user,
    }
    match the_action:
        case 1:
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        action = '''
                            DELETE FROM users
                            WHERE email = %(input_email)s;
                        '''
                        cursor.execute(action, my_dict)
                        conn.commit()
                        print("User deleted successfully")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

        case 2:
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        action = '''
                            UPDATE users
                            SET locked = '0'
                            WHERE email = %(input_email)s;
                        '''
                        cursor.execute(action, my_dict)
                        conn.commit()
                        print("User is unlocked")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

        case 3:

            input_password = password()
            my_dict = {
                "input_password": input_password,
                "input_email": the_user
            }
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        action = '''
                            UPDATE users
                            SET password = %(input_password)s
                            WHERE email = %(input_email)s;
                        '''
                        cursor.execute(action, my_dict)
                        conn.commit()
                        print(Fore.GREEN + "Password is reset" + Style.RESET_ALL)

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)

        case 4:
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        action = '''
                            UPDATE users
                            SET change = '1'
                            WHERE email = %(input_email)s;
                        '''
                        cursor.execute(action, my_dict)
                        conn.commit()
                        print("Change access is granted")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)
        case 5:
            try:
                # Establish a connection to the PostgreSQL database using 'with' statement
                with psycopg2.connect(**config) as conn:
                    # Create a cursor object within the 'with' block
                    with conn.cursor() as cursor:
                        action = '''
                            UPDATE users
                            SET change = '0'
                            WHERE email = %(input_email)s;
                        '''
                        cursor.execute(action, my_dict)
                        conn.commit()
                        print("Change access is revoked")

            except psycopg2.Error as e:
                print("Error connecting to the database:", e)


press_a_key = input(Fore.GREEN + "Press enter to load the users: " + Style.RESET_ALL)


# Call the function to load and print the DataFrame
users = load_users()

your_choice = user_choice()
action_you_want = user_choice_2()
admin_actions(your_choice, action_you_want)