import mysql.connector

db_conn = mysql.connector.connect(host="acit3855-erjin.eastus2.cloudapp.azure.com", user="root", password="P@ssw0rd", database="events")
db_cursor = db_conn.cursor()

db_cursor.execute('''
    DROP TABLE IF EXISTS order_request, delivery_request
''')

db_conn.commit()
db_conn.close()