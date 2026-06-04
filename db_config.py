import mysql.connector

print("MYSQL MODULE LOADED")

def get_database_connection():

    print("TRYING DATABASE CONNECTION")

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root@1234",
        database="student_task_manager",
        connection_timeout=5,
        use_pure=True
    )

    print("DATABASE CONNECTION SUCCESSFUL")

    return connection