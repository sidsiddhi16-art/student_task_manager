import mysql.connector

print("Starting...")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root@1234",
        database="student_task_manager",
        use_pure=True,
        connection_timeout=5
    )

    print("Connected Successfully")

except Exception as e:
    print("Error:", e)

print("Finished")