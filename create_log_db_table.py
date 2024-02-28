import sqlite3
conn = sqlite3.connect('user_responses_log.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE logs
    (timestamp TEXT, tabindex TEXT, userClickedValue TEXT, userQuestion TEXT, responseApiUniqueValue TEXT)
''')
conn.commit()
