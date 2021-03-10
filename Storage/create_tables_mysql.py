import mysql.connector
db_conn = mysql.connector.connect(host="acit3855-erjin.eastus2.cloudapp.azure.com", user="root", password="P@ssw0rd", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
     CREATE TABLE IF NOT EXISTS order_request(
        id INT NOT NULL AUTO_INCREMENT,
        customer_name VARCHAR(250) NOT NULL,
        device_id VARCHAR(250) NOT NULL,
        item VARCHAR(250) NOT NULL,
        quantity INTEGER NOT NULL,
        order_id VARCHAR(250) NOT NULL,
        store_id VARCHAR(250) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT order_request_pk PRIMARY KEY (id))
 ''')
db_cursor.execute('''
     CREATE TABLE IF NOT EXISTS delivery_request(
        id INT NOT NULL AUTO_INCREMENT,
        customer_name VARCHAR(250) NOT NULL,
        device_id VARCHAR(250) NOT NULL,
        driver_id INTEGER NOT NULL,
        item VARCHAR(250) NOT NULL,
        quantity INTEGER NOT NULL,
        order_id VARCHAR(250) NOT NULL,
        store_id VARCHAR(250) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT delivery_request_pk PRIMARY KEY (id))
 ''')

db_conn.commit()
db_conn.close()
