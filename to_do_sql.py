import sqlite3
from datetime import datetime

class Database:

    def __init__(self, db_name = "todos.db"):

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS todos
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                             date TEXT NOT NULL,
                             todo TEXT NOT NULL,
                             deadline TEXT NOT NULL
                             )
                            """)
        
        self.connection.commit()
    
    def add_todo_db(self,date, text, deadline):
        try:
            self.cursor.execute("""INSERT INTO todos(date, todo, deadline)
                                VALUES(?,?,?)""", (date, text, deadline))
            self.connection.commit()
            print("ახალი შესასრულებელი სამუშაო წარმატებით დაემატა სიაში!")
        except sqlite3.Error as e:
            print(F"შეცდომა მონაცემის დამატებისას: {e}!")

    
    def show_todos(self):
            self.cursor.execute("SELECT * FROM todos")
            return self.cursor.fetchall()
        
    
    def replace_todo_db(self, todo_id, new_text, new_deadline):
        try:
            self.cursor.execute("""UPDATE todos SET todo = ?,
                                deadline = ? WHERE ID = ? """ , (new_text, new_deadline,todo_id))
            self.connection.commit()
            print("შესასრულებელი სამუშაო წარმატებით შეიცვალა!")

        except sqlite3.Error as e:
            print(F"შეცდომა მონაცემის შეცვლისას: {e}!")

    def delete_todo_db(self, todo_id):
        try:
            self.cursor.execute("DELETE FROM todos WHERE ID = ?", (todo_id,))
            self.connection.commit()
            print("შესასრულებელი სამუშაო წარმატებით ამოიშალა სიიდან!")

        except sqlite3.Error as e:
            print(F"შეცდომა მონაცემის წაშლისას: {e}!")


    def close(self):
        self.cursor.close()
        self.connection.close()


class Manager:

    def __init__(self, database):
        self.database = database

    def add(self,text, deadline):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.database.add_todo_db(date,text, deadline)
        
    def showAll(self,):
        data = self.database.show_todos()
        if data:
            for todo in data:
                print(f"{'-'*25} {todo[0]} {'-'*25}")
                print(f"თარიღი: {todo[1]}")
                print(f"შესასრულებელი სამუშაო: {todo[2]}")
                print(f"ბოლო ვადა: {todo[3]}")
                print("-"*53)
        else:
            print("შესასრულებელი სამუშაოების სია ცარიელია!")
    
    def replace_todo(self, todo_id, new_text, new_deadline):
        self.database.replace_todo_db(todo_id, new_text, new_deadline)

    def delete_todo(self, todo_id):
        self.database.delete_todo_db(todo_id)
    

    def todo_checker(self, database):

        if not self.database.show_todos():   # ცარიელი ბაზის დროს თუ მომხმარებელი შეცვლას ან წაშლას ითხოვს
            return None

        while True:
            self.database.cursor.execute("SELECT MIN(ID), MAX(ID) FROM todos")
            data = self.database.cursor.fetchone()
            min_id, max_id = data[0], data[1]
            todo_id = input(f"შეიტანეთ წასაშლელი ან შესაცვლელი სამუშაოს ID ({min_id}-{max_id} დიაპაზონში): ").strip()

            if not todo_id.isdigit():
                print("გთხოვთ, შეიყვანეთ რიცხვითი მნიშვნელობა!")
                continue

            todo_id = int(todo_id)

            if todo_id < min_id or todo_id > max_id:
                print(f"გთხოვთ, შეიყვანოთ სწორი ID დიაპაზონში ({min_id}-{max_id})!")
                continue

            return todo_id
            

def menu():
    choice = None
    database = Database()
    manager = Manager(database)

    while choice != "გ":
        print("\nმენიუ")
        print("დ - დამატება;")
        print("ჩ - ჩვენება;")
        print("შ - შეცვლა;")
        print("წ - წაშლა;")
        print("გ - პროგრამიდან გასვლა;")

        choice = input("მიუთითეთ რომელი მოქმედების განხორციელება გსურთ: ").strip()

        if choice == "დ":
            text = input("შეიტანეთ შესასრულებელი სამუშაოს დასახელება: ").strip()
            deadline = input("შეიტანეთ სამუშაოს შესრულების ბოლო თარიღი: ").strip()
            manager.add(text, deadline)

        elif choice == "ჩ":
            manager.showAll()

        elif choice == "შ":
            manager.showAll()
            todo_id = manager.todo_checker(database)  
            if todo_id: 
                new_text = input("შეიტანეთ შესასრულებელი სამუშაოს ახალი დასახელება: ").strip()
                new_deadline = input("შეიტანეთ ახალი შესასრულებელი სამუშაოს ბოლო ვადა: ").strip()
                manager.replace_todo(todo_id, new_text, new_deadline)

        elif choice == "წ":
            manager.showAll()
            todo_id = manager.todo_checker(database)  
            if todo_id: 
                manager.delete_todo(todo_id)

        elif choice == "გ":
            print("პროგრამა დაიხურა.")
            database.close()
        else:
            print("ოპერაციის არასწორი დასახელება, გთხოვთ სცადეთ ხელახლა!")


menu()