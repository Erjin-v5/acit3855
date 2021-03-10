import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE order_request
          ''')

c.execute('''
          DROP TABLE delivery_request
          ''')

conn.commit()
conn.close()
