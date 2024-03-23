import psycopg2

# Connection details
config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}

# Table name to look up
table_name = 'books'  # Replace 'your_table_name' with the actual table name

try:
    # Establish a connection to the PostgreSQL database using 'with' statement
    with psycopg2.connect(**config) as conn:
        # Create a cursor object within the 'with' block
        with conn.cursor() as cursor:
            # Query to get columns of a specific table
            query = '''
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            AND table_catalog = %s;
            '''
            cursor.execute(query, (table_name, config['database']))
            columns = cursor.fetchall()

            # Print the columns of the specified table
            if columns:
                print("Columns of table '{}':".format(table_name))
                for col in columns:
                    print(f"Column Name: {col[0]}, Data Type: {col[1]}")
            else:
                print("Table '{}' not found in the database.".format(table_name))

except psycopg2.Error as e:
    print("Error connecting to the database:", e)
