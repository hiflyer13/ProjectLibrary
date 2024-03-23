import psycopg2

# Connection details
config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}

# Table name to query
table_name = 'users'

try:
    # Establish a connection to the PostgreSQL database using 'with' statement
    with psycopg2.connect(**config) as conn:
        # Create a cursor object within the 'with' block
        with conn.cursor() as cursor:
            # Query to select all rows from the specified table
            query = 'SELECT * FROM {};'.format(table_name)
            cursor.execute(query)
            rows = cursor.fetchall()

            # Print the rows of the specified table
            if rows:
                print("All values in the '{}' table:".format(table_name))
                print(type(rows[0]))
                for row in rows:
                    print(row)
            else:
                print("No data found in the '{}' table.".format(table_name))

except psycopg2.Error as e:
    print("Error connecting to the database:", e)
