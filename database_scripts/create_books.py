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
            create_table_query = '''
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                author VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                language VARCHAR(2) NOT NULL,
                pages INT NOT NULL,
                isbn VARCHAR NOT NULL,
                year INT NOT NULL
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully.")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)


# ISBN  must be a varchar instead of an int because it's a very long sequence of numbers and I believe
# it's handled more efficiently when it's handled as a string.
