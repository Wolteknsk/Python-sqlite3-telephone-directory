import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3    

def create_table():
  conn = sqlite3.connect('phonebook.db')
  cursor = conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT,
      phone_number TEXT NOT NULL UNIQUE,
      email TEXT
    )
  ''')
  conn.commit()
  conn.close()

def add_contact():
  def save_new_contact():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()

    if not first_name or not phone_number:
      messagebox.showerror("Ошибка", "Пожалуйста, введите имя и номер телефона.")
      return

    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    try:
      cursor.execute("SELECT * FROM contacts WHERE phone_number = ?", (phone_number,))
      if cursor.fetchone():
        messagebox.showerror("Ошибка", "Контакт с таким номером телефона уже существует")
        return

      cursor.execute("INSERT INTO contacts (first_name, last_name, phone_number, email) VALUES (?, ?, ?, ?)",
              (first_name, last_name, phone_number, email))
      conn.commit()
      messagebox.showinfo("Успех", "Контакт добавлен!")
      add_window.destroy()
    except sqlite3.Error as e:
      messagebox.showerror("Ошибка базы данных", f"Произошла ошибка: {e}")
      conn.rollback()
    finally:
      conn.close()

  add_window = tk.Toplevel(root)
  add_window.title("Добавить контакт")

  first_name_label = ttk.Label(add_window, text="Имя:", style="TLabel")
  first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
  first_name_entry = ttk.Entry(add_window, style="TEntry")
  first_name_entry.grid(row=0, column=1, padx=5, pady=5)

  last_name_label = ttk.Label(add_window, text="Фамилия:", style="TLabel")
  last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
  last_name_entry = ttk.Entry(add_window, style="TEntry")
  last_name_entry.grid(row=1, column=1, padx=5, pady=5)

  phone_number_label = ttk.Label(add_window, text="Номер телефона:", style="TLabel")
  phone_number_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
  phone_number_entry = ttk.Entry(add_window, style="TEntry")
  phone_number_entry.grid(row=2, column=1, padx=5, pady=5)

  email_label = ttk.Label(add_window, text="Email:", style="TLabel")
  email_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
  email_entry = ttk.Entry(add_window, style="TEntry")
  email_entry.grid(row=3, column=1, padx=5, pady=5)

  save_button = ttk.Button(add_window, text="Сохранить", command=save_new_contact, style="TButton")
  save_button.grid(row=4, column=0, columnspan=2, pady=10)

def find_contact():
    def show_results():
        search_term = search_entry.get()
        conn = sqlite3.connect('phonebook.db')
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, phone_number, email FROM contacts WHERE first_name LIKE ? OR last_name LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%"))
        results = cursor.fetchall()
        conn.close()

        if results:
            result_text = "Найденные контакты:\n"
            for first_name, last_name, phone_number, email in results:
                result_text += f"Имя: {first_name}, Фамилия: {last_name or ''}\n"
                result_text += f"Телефон: {phone_number}, Email: {email or 'Не указан'}\n\n"
            messagebox.showinfo("Результаты поиска", result_text)
        else:
            messagebox.showinfo("Результаты поиска", "Контакты не найдены.")
        find_window.destroy()

    find_window = tk.Toplevel(root)
    find_window.title("Найти контакт")

    search_label = ttk.Label(find_window, text="Введите имя или фамилию:", style="TLabel")
    search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    search_entry = ttk.Entry(find_window, style="TEntry")
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    search_button = ttk.Button(find_window, text="Найти", command=show_results, style="TButton")
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

def delete_contact():
    def confirm_delete():
        phone_number = phone_number_entry.get()
        conn = sqlite3.connect('phonebook.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE phone_number = ?", (phone_number,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        if rows_affected > 0:
            messagebox.showinfo("Успех", "Контакт удален!")
        else:
            messagebox.showerror("Ошибка", "Контакт не найден.")
        delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Удалить контакт")

    phone_number_label = ttk.Label(delete_window, text="Введите номер телефона контакта:", style="TLabel")
    phone_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    phone_number_entry = ttk.Entry(delete_window, style="TEntry")
    phone_number_entry.grid(row=0, column=1, padx=5, pady=5)

    delete_button = ttk.Button(delete_window, text="Удалить", command=confirm_delete, style="TButton")
    delete_button.grid(row=1, column=0, columnspan=2, pady=10)

def show_all_contacts():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, phone_number, email FROM contacts")
    contacts = cursor.fetchall()
    conn.close()

    if contacts:
        result = "Все контакты:\n"
        for first_name, last_name, phone_number, email in contacts:
            result += f"Имя: {first_name}, Фамилия: {last_name or ''}, Телефон: {phone_number}, Email: {email or 'Не указан'}\n"
        messagebox.showinfo("Все контакты", result)
    else:
        messagebox.showinfo("Все контакты", "Телефонная книга пуста.")
 
# Стиль
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", background="lavender", foreground="violet", font=("Arial", 12), padding=6)
style.configure("TLabel", background="lavender")

root = tk.Tk()
root.title("Телефонный справочник")
root.configure(bg="black")
root.geometry("1000x500")


add_button = ttk.Button(root, text="Добавить контакт", command=add_contact, style="TButton")
add_button.pack(pady=10)

find_button = ttk.Button(root, text="Найти контакт", command=find_contact, style="TButton")
find_button.pack(pady=10)

delete_button = ttk.Button(root, text="Удалить контакт", command=delete_contact, style="TButton")
delete_button.pack(pady=10)

show_all_button = ttk.Button(root, text="Показать все контакты", command=show_all_contacts, style="TButton")
show_all_button.pack(pady=10)

create_table()
root.mainloop()