import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

def init_db():
    conn = sqlite3.connect('tours.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def seed_db():

    tours = [
        ("Пляжный отпуск", "Наслаждайтесь солнечным отдыхом на пляже.", 299.99, "2023-08-01"),
        ("Горное приключение", "Походы и кемпинг в горах.", 199.99, "2023-09-15"),
        ("Экскурсия по Москве", "Откройте для себя исторические достопримечательности столицы.", 150.00, "2023-07-01"),
        ("Романтический уикенд", "Проведите романтический уикенд в культурной столице.", 350.00, "2023-06-20"),
        ("Круиз по Волге", "Наслаждайтесь живописными пейзажами во время круиза.", 400.00, "2023-07-15")
    ]
    conn = sqlite3.connect('tours.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tours")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO tours (title, description, price, date) VALUES (?, ?, ?, ?)", tours)
        conn.commit()
    conn.close()

class TourManagementApp:

    def __init__(self, master):

        self.master = master
        master.title("Система управления турами")

        self.load_button = tk.Button(master, text="Загрузить туры", command=self.load_tours)
        self.load_button.pack(pady=10)

        self.tour_listbox = tk.Listbox(master, width=50)
        self.tour_listbox.pack(pady=10)
        self.tour_listbox.bind("<Double-Button-1>", self.on_tour_select)

        self.add_button = tk.Button(master, text="Добавить новый тур", command=self.add_tour)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(master, text="Редактировать тур", command=self.edit_tour, state=tk.DISABLED)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(master, text="Удалить тур", command=self.delete_tour, state=tk.DISABLED)
        self.delete_button.pack(pady=5)

        self.selected_tour_id = None

    def load_tours(self):

        self.tour_listbox.delete(0, tk.END)
        conn = sqlite3.connect('tours.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tours")
        tours = cursor.fetchall()
        for tour in tours:
            self.tour_listbox.insert(tk.END, f'ID: {tour[0]}, Название: {tour[1]}, Цена: {tour[3]}, Дата: {tour[4]}')
        conn.close()
        self.disable_edit_delete_buttons()

    def add_tour(self):
        title = simpledialog.askstring("Название", "Введите название тура:")
        description = simpledialog.askstring("Описание", "Введите описание тура:")
        price = simpledialog.askfloat("Цена", "Введите цену тура:")
        date = simpledialog.askstring("Дата", "Введите дату начала тура (YYYY-MM-DD):")

        if title and description and price and date:
            conn = sqlite3.connect('tours.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tours (title, description, price, date) VALUES (?, ?, ?, ?)",
                           (title, description, price, date))
            conn.commit()
            conn.close()
            self.load_tours()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")

    def edit_tour(self):
        if self.selected_tour_id is None:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите тур для редактирования.")
            return

        title = simpledialog.askstring("Название", "Введите название тура:")
        description = simpledialog.askstring("Описание", "Введите описание тура:")
        price = simpledialog.askfloat("Цена", "Введите цену тура:")
        date = simpledialog.askstring("Дата", "Введите дату начала тура (YYYY-MM-DD):")

        if title and description and price and date:
            conn = sqlite3.connect('tours.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE tours SET title=?, description=?, price=?, date=? WHERE id=?",
                           (title, description, price, date, self.selected_tour_id))
            conn.commit()
            conn.close()
            self.load_tours()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")

    def delete_tour(self):
        if self.selected_tour_id is None:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите тур для удаления.")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот тур?"):
            conn = sqlite3.connect('tours.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tours WHERE id=?", (self.selected_tour_id,))
            conn.commit()
            conn.close()
            self.load_tours()

    def on_tour_select(self, event):
        selection = self.tour_listbox.curselection()
        if selection:
            selected_tour = self.tour_listbox.get(selection[0])
            self.selected_tour_id = int(selected_tour.split(',')[0].split(':')[1].strip())
            self.enable_edit_delete_buttons()
        else:
            self.disable_edit_delete_buttons()

    def enable_edit_delete_buttons(self):
        self.edit_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)

    def disable_edit_delete_buttons(self):
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.selected_tour_id = None

if __name__ == "__main__":
    init_db()
    seed_db()
    root = tk.Tk()
    app = TourManagementApp(root)
    root.mainloop()