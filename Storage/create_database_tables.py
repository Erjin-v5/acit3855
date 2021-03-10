import sqlite3

conn = sqlite3.connect("readings.sqlite")

c = conn.cursor()

c.execute('''
        CREATE TABLE order_request(
        id INTEGER PRIMARY KEY ASC,
        customer_name VARCHAR(250) NOT NULL,
        device_id VARCHAR(250) NOT NULL,
        item VARCHAR(250) NOT NULL,
        quantity INTEGER NOT NULL,
        order_id VARCHAR(250) NOT NULL,
        store_id VARCHAR(250) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL)
        ''')

c.execute('''
        CREATE TABLE delivery_request(
        id INT NOT NULL AUTO_INCREMENT,
        customer_name VARCHAR(250) NOT NULL,
        device_id VARCHAR(250) NOT NULL,
        driver_id INTEGER NOT NULL,
        item VARCHAR(250) NOT NULL,
        quantity INTEGER NOT NULL,
        order_id VARCHAR(250) NOT NULL,
        store_id VARCHAR(250) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL
        CONSTRAINT delivery_request_pk PRIMARY KEY (id))
        ''')

conn.commit()
conn.close()