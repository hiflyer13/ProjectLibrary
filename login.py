from colorama import Fore, Back, Style
import enduser
import hashlib
import psycopg2


def main():
    # Connection details
    config = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
    }

    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = 'SELECT * FROM users'
                cursor.execute(query)
                rows = cursor.fetchall()

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    input_email_address = input(Fore.GREEN + "Email address: " + Style.RESET_ALL)
    input_password = input(Fore.GREEN + "Password: " + Style.RESET_ALL)

    # hashing the password
    # Create an SHA-256 hash object
    hash_object = hashlib.sha256()
    # Convert the password to bytes and hash it
    hash_object.update(input_password.encode())
    # Get the hex digest of the hash
    hash_password = hash_object.hexdigest()

    # Getting the email addresses only
    existing_email_addresses = []
    for i in rows:
        existing_email_addresses.append(i[1])

    # Checking the existence of the email address. If it does not exist, exit the program
    if input_email_address not in existing_email_addresses:
        print(Fore.RED + "Email address does not exist" + Style.RESET_ALL)
        exit()

    # Querying the values of password and login_attempts based on the input_email_address
    try:
        # Establish a connection to the PostgreSQL database using 'with' statement
        with psycopg2.connect(**config) as conn:
            # Create a cursor object within the 'with' block
            with conn.cursor() as cursor:
                # Query to select all rows from the specified table
                query = f"SELECT password FROM users WHERE email='{input_email_address}';"
                cursor.execute(query)
                query_password = cursor.fetchall()
                query_password_cleaned = query_password[0][0]
                query2 = f"SELECT login_attempts FROM users WHERE email='{input_email_address}';"
                cursor.execute(query2)
                query_login_attempt = cursor.fetchall()
                query_login_attempt_cleaned = query_login_attempt[0][0]

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    # Checking the login attempts.
    if query_login_attempt_cleaned >= 3:
        print(Fore.RED + "Your account is locked, please contact system administrator" + Style.RESET_ALL)
        exit()

    # Comparing the two hash passwords. If they do not match, then exit the program and increase the number in the
    # login_attempts table. If it reaches 3, then the user is in locked status.
    if hash_password != query_password_cleaned:
        print(Fore.RED + "Password is incorrect" + Style.RESET_ALL)
        try:
            # Establish a connection to the PostgreSQL database using 'with' statement
            with psycopg2.connect(**config) as conn:
                # Create a cursor object within the 'with' block
                with conn.cursor() as cursor:
                    # Query to select all rows from the specified table
                    query = f"SELECT login_attempts FROM users WHERE email='{input_email_address}';"
                    cursor.execute(query)
                    login_attempt = cursor.fetchall()
                    login_attempt_cleaned = login_attempt[0][0]
                    print(Fore.RED + f"Incorrect login attempts: {login_attempt_cleaned+1}" + Style.RESET_ALL)
                    query_set = f"UPDATE users SET login_attempts = '{login_attempt_cleaned+1}' WHERE email='{input_email_address}'"
                    cursor.execute(query_set)

        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    else:
        print("You are in")
        try:
            # Establish a connection to the PostgreSQL database using 'with' statement
            with psycopg2.connect(**config) as conn:
                # Create a cursor object within the 'with' block
                with conn.cursor() as cursor:
                    # Query to select all rows from the specified table
                    query = f"UPDATE users SET login_attempts = '0' WHERE email='{input_email_address}'"
                    cursor.execute(query)

        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

        enduser.main(input_email_address)

