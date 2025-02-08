from tkinter import *
from tkinter import ttk, messagebox
from plyer import notification
import threading
import time
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List with Notifications')
        self.root.geometry('750x500+300+150')
        self.root.config(bg='#2C3E50')

        # Style Configuration
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        style.configure("TLabel", font=("Arial", 14), background="#2C3E50", foreground="white")
        style.configure("TEntry", font=("Arial", 12))

        # Heading
        heading = Label(self.root, text='To-Do List 📋', font=('Arial', 24, 'bold'), bg='#1ABC9C', fg='white', pady=10)
        heading.pack(fill=X)

        # Frames for Better Layout
        frame1 = Frame(self.root, bg='#2C3E50')
        frame1.pack(pady=20)

        frame2 = Frame(self.root, bg='#2C3E50')
        frame2.pack()

        # Task Entry
        Label(frame1, text="Task:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.task_entry = Text(frame1, height=2, width=30, font=("Arial", 12))
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        # Time Entry
        Label(frame1, text="Set Time (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.time_entry = ttk.Entry(frame1, width=10)
        self.time_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Buttons
        ttk.Button(frame1, text="➕ Add Task", command=self.add_task).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(frame1, text="❌ Delete Task", command=self.delete_task).grid(row=2, column=1, padx=10, pady=10)

        # Task Listbox
        Label(frame2, text="📋 Your Tasks:").pack()
        self.tasks_listbox = Listbox(frame2, height=10, width=50, font=("Arial", 12), bg="#ECF0F1", bd=2)
        self.tasks_listbox.pack(pady=10)

        # Start Reminder Button
        ttk.Button(self.root, text="🔔 Start Reminders", command=self.start_reminder).pack(pady=10)

        # Load saved tasks
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get(1.0, END).strip()
        task_time = self.time_entry.get().strip()

        # Validate time format (HH:MM)
        try:
            datetime.strptime(task_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format!")
            self.time_entry.delete(0, END)
            return

        if task and task_time:
            task_entry = f"{task} - {task_time}"
            self.tasks_listbox.insert(END, task_entry)

            with open('tasks.txt', 'a') as file:
                file.write(task_entry + '\n')

            self.task_entry.delete(1.0, END)
            self.time_entry.delete(0, END)

    def delete_task(self):
        try:
            selected_task = self.tasks_listbox.curselection()[0]
            task_text = self.tasks_listbox.get(selected_task)

            with open('tasks.txt', 'r') as file:
                lines = file.readlines()

            with open('tasks.txt', 'w') as file:
                for line in lines:
                    if line.strip() != task_text:
                        file.write(line)

            self.tasks_listbox.delete(selected_task)
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete!")

    def load_tasks(self):
        try:
            with open('tasks.txt', 'r') as file:
                tasks = file.readlines()
                for task in tasks:
                    self.tasks_listbox.insert(END, task.strip())
        except FileNotFoundError:
            pass

    def send_notification(self):
        while True:
            now = datetime.now().strftime("%H:%M")  # Get current time in HH:MM format
            print(f"[DEBUG] Current System Time: {now}")  # Debugging log

            for i in range(self.tasks_listbox.size()):
                task_entry = self.tasks_listbox.get(i)
                task, task_time = task_entry.rsplit(" - ", 1)

                if task_time == now:
                    print(f"[NOTIFY] Task Reminder Triggered for: {task}")  # Debug log

                    notification.notify(
                        title="Task Reminder ⏰",
                        message=f"Don't forget: {task}",
                        app_name="To-Do List Notifier",
                        timeout=5
                    )

                    time.sleep(60)  # Avoid duplicate notifications within the same minute
            time.sleep(30)  # Check every 30 seconds

    def start_reminder(self):
        thread = threading.Thread(target=self.send_notification, daemon=True)
        thread.start()
        messagebox.showinfo("Reminders Started", "Task notifications will run in the background!")

def main():
    root = Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
