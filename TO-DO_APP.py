import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

# This file will store your tasks so you won't lose them
TASK_FILE = "tasks.txt"

# Load all tasks saved in the file when you open the app
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for line in file:
                task_list.insert(tk.END, line.strip())

# Save all your tasks to a file when you close the app
def save_tasks():
    with open(TASK_FILE, "w") as file:
        tasks = task_list.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")

# Add a new task, and let you include an optional due date
def add_task(event=None):  # Pressing Enter will also add the task
    task = task_entry.get().strip()
    if task:
        due_date = simpledialog.askstring("Due Date", "When is this task due? (YYYY-MM-DD) or leave blank:")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Check if the date format is correct
                task += f" (Due: {due_date})"
            except ValueError:
                messagebox.showerror("Error", "Oops! Please use the format YYYY-MM-DD for the date.")
                return
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)  # Clear the input field
    else:
        messagebox.showwarning("Warning", "Don't forget to type your task first!")

# Delete the selected task from the list
def delete_task():
    selected_task = task_list.curselection()
    if selected_task:
        task_list.delete(selected_task)
    else:
        messagebox.showwarning("Warning", "Please select a task you want to delete!")

# Mark a task as completed by adding a checkmark
def complete_task():
    selected_task = task_list.curselection()
    if selected_task:
        task = task_list.get(selected_task)
        task_list.delete(selected_task)
        task_list.insert(tk.END, f"{task} ✅")
    else:
        messagebox.showwarning("Warning", "Pick a task to mark as complete!")

# Search for tasks that match your input
def search_tasks(event=None):  # Pressing Enter will also search
    search_term = search_entry.get().lower()
    if search_term:
        tasks = task_list.get(0, tk.END)
        matching_tasks = [task for task in tasks if search_term in task.lower()]
        task_list.delete(0, tk.END)
        for task in matching_tasks:
            task_list.insert(tk.END, task)
        if not matching_tasks:
            messagebox.showinfo("Search", "Couldn't find anything that matches your search.")
    else:
        messagebox.showinfo("Search", "Type something to search!")

# Restore all tasks after a search, bringing back the full list
def restore_tasks():
    task_list.delete(0, tk.END)
    load_tasks()

# Switch between light and dark mode to suit your preference
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        app.configure(bg="#2c2c2c")
        header.configure(bg="#2c2c2c", fg="white")
        for widget in [task_entry, search_entry, task_list]:
            widget.configure(bg="#3c3c3c", fg="white", insertbackground="white")
        for button in buttons:
            button.configure(bg="#444444", fg="white", relief=tk.FLAT)
    else:
        app.configure(bg="SystemButtonFace")
        header.configure(bg="SystemButtonFace", fg="black")
        for widget in [task_entry, search_entry, task_list]:
            widget.configure(bg="white", fg="black", insertbackground="black")
        for button in buttons:
            button.configure(bg="SystemButtonFace", fg="black", relief=tk.RAISED)

# Create the main app window
app = tk.Tk()
app.title("Ribas' To-Do App")
app.geometry("500x700")
app.resizable(False, False)
app.configure(bg="#f8f9fa")  # Light background to keep it clean and simple

# Create the app's title
header = tk.Label(app, text="Ribas' To-Do App", font=("Helvetica", 28, "bold"), bg="#f8f9fa", fg="#212529")
header.pack(pady=20)

# Input field for adding new tasks
task_entry = tk.Entry(app, font=("Helvetica", 16), bg="white", fg="black", relief=tk.FLAT, bd=5)
task_entry.pack(pady=10, padx=20, fill=tk.X)
task_entry.bind("<Return>", add_task)  # Press Enter to add a task

# Search bar and related buttons
search_frame = tk.Frame(app, bg="#f8f9fa")
search_frame.pack(pady=10, padx=20, fill=tk.X)

search_entry = tk.Entry(search_frame, font=("Helvetica", 16), bg="white", fg="black", relief=tk.FLAT, bd=5)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
search_entry.bind("<Return>", search_tasks)  # Press Enter to search

search_button = tk.Button(search_frame, text="Search", command=search_tasks, bg="#17a2b8", fg="white", relief=tk.FLAT, padx=10, pady=5)
search_button.pack(side=tk.LEFT, padx=5)

restore_button = tk.Button(search_frame, text="Restore", command=restore_tasks, bg="#6c757d", fg="white", relief=tk.FLAT, padx=10, pady=5)
restore_button.pack(side=tk.LEFT)

# Buttons for adding, deleting, completing tasks, and toggling dark mode
button_frame = tk.Frame(app, bg="#f8f9fa")
button_frame.pack(pady=20)

add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#28a745", fg="white", relief=tk.FLAT, padx=10, pady=5, width=12)
add_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, bg="#dc3545", fg="white", relief=tk.FLAT, padx=10, pady=5, width=12)
delete_button.grid(row=0, column=1, padx=10)

complete_button = tk.Button(button_frame, text="Complete Task", command=complete_task, bg="#007bff", fg="white", relief=tk.FLAT, padx=10, pady=5, width=12)
complete_button.grid(row=0, column=2, padx=10)

dark_mode_button = tk.Button(button_frame, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#ffc107", fg="black", relief=tk.FLAT, padx=10, pady=5, width=12)
dark_mode_button.grid(row=1, column=1, pady=10)

buttons = [add_button, delete_button, complete_button, dark_mode_button, search_button, restore_button]

# A scrollable area to display all tasks
task_list_frame = tk.Frame(app, bg="#f8f9fa")
task_list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

task_list_scrollbar = tk.Scrollbar(task_list_frame, orient=tk.VERTICAL)
task_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(task_list_frame, font=("Helvetica", 14), bg="white", fg="black", yscrollcommand=task_list_scrollbar.set, selectmode=tk.SINGLE, relief=tk.FLAT, bd=5)
task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

task_list_scrollbar.config(command=task_list.yview)

# Load tasks from the file at startup
load_tasks()

# Save tasks when you close the app
app.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), app.destroy()])

# Initialize dark mode
dark_mode = False

# Run the app
app.mainloop()
