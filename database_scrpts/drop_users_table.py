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
                DROP table books;
            '''
            cursor.execute(create_table_query)
            conn.commit()
            print("Table removed successfully.")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)