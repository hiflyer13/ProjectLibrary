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
            create_admin_user = '''
                INSERT INTO users (
                email, first_name, family_name, birthdate, read, change, admin, login_attempts, password)
                VALUES ('admin@admin.com', 'admin', 'admin', '2000-01-01', '1', '1', '1', '0', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
            '''
            cursor.execute(create_admin_user)
            conn.commit()
            print("User created successfully")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

