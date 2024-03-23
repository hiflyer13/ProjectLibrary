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
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                family_name VARCHAR(255) NOT NULL,
                birthdate DATE NOT NULL,
                read BIT NOT NULL,
                change BIT NOT NULL,
                admin BIT NOT NULL,
                login_attempts INT NOT NULL,
                password VARCHAR NOT NULL
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully.")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

