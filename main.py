import tkinter as tk
from tkinter import messagebox
import os

# Класс Task определяет задачу с описанием, сроком выполнения и статусом
class Task:
    def __init__(self, description, due_date, status=False):
        self.description = description  # Описание задачи
        self.due_date = due_date  # Срок выполнения задачи
        self.status = status  # Статус задачи (по умолчанию невыполнено)

    def mark_as_done(self):
        self.status = True  # Метод для отметки задачи как выполненной

    def __str__(self):
        # Форматированная строка для представления задачи
        return f"{self.description} (срок: {self.due_date}) - {'Выполнено' if self.status else 'Не выполнено'}"

    def to_string(self):
        # Строка для сохранения в файл
        return f"{self.description};{self.due_date};{self.status}"

    @staticmethod
    def from_string(task_str):
        # Создание объекта Task из строки
        description, due_date, status = task_str.split(';')
        return Task(description, due_date, status == 'True')

# Класс TaskManager управляет списком задач
class TaskManager:
    def __init__(self, file_name='tasks.txt'):
        self.tasks = []  # Список задач
        self.file_name = file_name  # Имя файла для сохранения задач
        self.load_tasks()  # Загрузка задач из файла

    def add_task(self, task):
        self.tasks.append(task)  # Добавление задачи в список

    def list_tasks(self):
        return self.tasks  # Возвращает список всех задач

    def list_pending_tasks(self):
        return [task for task in self.tasks if not task.status]  # Возвращает список невыполненных задач

    def mark_task_as_done(self, task_index):
        self.tasks[task_index].mark_as_done()  # Отметка задачи как выполненной

    def save_tasks(self):
        with open(self.file_name, 'w') as file:
            for task in self.tasks:
                file.write(task.to_string() + '\n')  # Сохранение задач в файл

    def load_tasks(self):
        if not os.path.exists(self.file_name):
            open(self.file_name, 'w').close()  # Создание файла, если его нет
        else:
            with open(self.file_name, 'r') as file:
                for line in file:
                    self.tasks.append(Task.from_string(line.strip()))  # Загрузка задач из файла

# Класс TaskManagerApp создает графический интерфейс для менеджера задач
class TaskManagerApp:
    def __init__(self, root):
        self.manager = TaskManager()  # Создание экземпляра TaskManager

        self.root = root
        self.root.title("Менеджер задач")  # Заголовок окна
        self.root.geometry("600x400")  # Размеры окна

        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Расположение рамки с отступом

        # Метки и поля ввода для описания задачи и срока выполнения
        self.description_label = tk.Label(self.frame, text="Описание задачи:")
        self.description_label.grid(row=0, column=0, sticky=tk.W)
        self.description_entry = tk.Entry(self.frame)
        self.description_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)

        self.due_date_label = tk.Label(self.frame, text="Срок выполнения:")
        self.due_date_label.grid(row=1, column=0, sticky=tk.W)
        self.due_date_entry = tk.Entry(self.frame)
        self.due_date_entry.grid(row=1, column=1, padx=5, sticky=tk.EW)

        # Кнопка для добавления задачи
        self.add_button = tk.Button(self.frame, text="Добавить задачу", command=self.add_task)
        self.add_button.grid(row=2, column=1, pady=5, sticky=tk.E)

        # Список для отображения всех задач
        self.task_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.NSEW)

        # Кнопка для отметки задачи как выполненной
        self.mark_done_button = tk.Button(self.frame, text="Отметить выполненной", command=self.mark_as_done)
        self.mark_done_button.grid(row=4, column=1, pady=5, sticky=tk.E)

        # Настройка адаптивного интерфейса
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.update_task_list()  # Обновление списка задач при запуске

    def add_task(self):
        description = self.description_entry.get()  # Получение описания задачи из поля ввода
        due_date = self.due_date_entry.get()  # Получение срока выполнения из поля ввода
        if description and due_date:
            task = Task(description, due_date)  # Создание новой задачи
            self.manager.add_task(task)  # Добавление задачи в менеджер задач
            self.manager.save_tasks()  # Сохранение задач в файл
            messagebox.showinfo("Успех", "Задача успешно добавлена")  # Показ сообщения об успешном добавлении
            self.description_entry.delete(0, tk.END)  # Очистка поля ввода описания
            self.due_date_entry.delete(0, tk.END)  # Очистка поля ввода срока выполнения
            self.update_task_list()  # Обновление списка задач
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")  # Показ сообщения об ошибке

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)  # Очистка списка задач
        for task in self.manager.list_tasks():
            self.task_listbox.insert(tk.END, str(task))  # Добавление задач в список
        self.color_tasks()  # Обновление цветов задач

    def color_tasks(self):
        for i in range(self.task_listbox.size()):
            task_str = self.task_listbox.get(i)
            if 'Выполнено' in task_str:
                self.task_listbox.itemconfig(i, {'bg': 'green', 'fg': 'white'})  # Выполненные задачи - зеленым цветом
            else:
                self.task_listbox.itemconfig(i, {'bg': 'red', 'fg': 'white'})  # Невыполненные задачи - красным цветом

    def mark_as_done(self):
        selected_index = self.task_listbox.curselection()  # Получение индекса выделенной задачи
        if selected_index:
            index = selected_index[0]
            self.manager.mark_task_as_done(index)  # Отметка задачи как выполненной в менеджере задач
            self.manager.save_tasks()  # Сохранение изменений в файл
            messagebox.showinfo("Успех", f"Задача '{self.manager.list_tasks()[index].description}' отмечена как выполненная")  # Показ сообщения об успешной отметке
            self.update_task_list()  # Обновление списка задач
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите задачу для отметки как выполненной")  # Показ сообщения об ошибке

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
