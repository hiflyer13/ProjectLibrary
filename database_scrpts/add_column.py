import psycopg2

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
            # Create a sample table
            create_column = '''
            UPDATE users
            SET login_attempts='0';
            '''
            cursor.execute(create_column)
            conn.commit()
            print("Table created successfully.")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

