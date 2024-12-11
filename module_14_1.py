import sqlite3

contec = sqlite3.connect("not_telegram.db")
cursor = contec.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

#for i in range(1, 11):
   # cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (f"User{i}", f'example{i}@gmail.com', f'{i*10}', '1000'))
#for i in range(1, 11):
    #if i%2 == 1:
        #cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", ('500', f"User{i}"))

#t=0
#for i in range(1, 11):
    #t= t+1
    #if t == 1 or t == 4 or t == 7 or t == 10:
       # cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))
#cursor.execute('SELECT username, email, age, balance FROM Users WHERE age!=?', (60,))
#users = cursor.fetchall()
#for i in users:
  #  for g in range(len(i)):
    #    print(f"Имя: {i[g]} | Почта: {i[g+1]} | Возраст: {i[g+2]} | Баланс: {i[g+3]}")
      #  break
#cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{6}",))

cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchall()[0][0]
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchall()[0][0]
print(all_balances/total_users)
contec.commit()
contec.close()



