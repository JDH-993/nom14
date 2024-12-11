import sqlite3
def initiate_db():
   contec = sqlite3.connect("Products.db")
   cursor = contec.cursor()

   cursor.execute('''
   CREATE TABLE IF NOT EXISTS Prod(
   id INTEGER PRIMARY KEY,
   title TEXT NOT NULL,
   description TEXT,
   price INTEGER NOT NULL
   )
   ''')
   cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Prod (title)")

   #for i in range(4):
      #cursor.execute("INSERT INTO Prod (title, description, price) VALUES (?, ?, ?)", (f"{input()}", f'{input()}', f"{int(input())}"))
   cursor.execute("SELECT * FROM Prod")
   produ = cursor.fetchall()
   o = []
   for i in produ:
      a = []
      for j in i:
         a.append(j)
      o.append(a)

   contec.commit()
   contec.close()
   return o
initiate_db()
def get_all_products():
   o = initiate_db()
   return o




fd= sqlite3.connect("Users.db")
cr = fd.cursor()

cr.execute('''
CREATE TABLE IF NOT EXISTS Users(
username TEXT PRIMARY KEY NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cr.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
def  is_included(username):

   o1 = fd.cursor()
   o1.execute("SELECT * FROM Users")
   o = o1.fetchall()
   l=0
   for i in o:
      for d in i:
         if i[0] == username:
            l = 1
            return False
      else:
         l = 0
   if l==0:
      return True

def add_user(username, email, age, balance):
   cr.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (f"{username}", f'{email}', f"{int(age)}", f"{int(balance)}"))
   fd.commit()
   cr.close()
