import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Todo List")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        # Data file
        self.data_file = "todos.json"
        self.todos = self.load_todos()
        
        # Colors
        self.colors = {
            "bg": "#f0f0f0",
            "entry_bg": "#ffffff",
            "button_bg": "#4CAF50",
            "button_fg": "#ffffff",
            "list_bg": "#ffffff",
            "completed": "#d4edda",
            "pending": "#fff3cd"
        }
        
        self.setup_ui()
        self.load_tasks_to_listbox()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="📝 TODO List", 
                              font=("Arial", 20, "bold"),
                              bg=self.colors["bg"], fg="#333333")
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.colors["bg"])
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 14),
                                  bg=self.colors["entry_bg"], relief="solid",
                                  width=30)
        self.task_entry.pack(side="left", padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(input_frame, text="Add Task", 
                           font=("Arial", 12, "bold"),
                           bg=self.colors["button_bg"],
                           fg=self.colors["button_fg"],
                           command=self.add_task,
                           relief="flat", padx=20)
        add_btn.pack(side="left")
        
        # Listbox with scrollbar
        list_frame = tk.Frame(self.root, bg=self.colors["bg"])
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(list_frame, font=("Arial", 12),
                                 bg=self.colors["list_bg"],
                                 selectbackground="#e3f2fd",
                                 yscrollcommand=scrollbar.set,
                                 height=15, selectmode="single")
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind double-click to toggle completion
        self.listbox.bind("<Double-Button-1>", self.toggle_task)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.colors["bg"])
        buttons_frame.pack(pady=20, padx=20)
        
        buttons = [
            ("✅ Complete", "#28a745", self.complete_task),
            ("✏️ Edit", "#ffc107", self.edit_task),
            ("🗑️ Delete", "#dc3545", self.delete_task),
            ("📊 Stats", "#17a2b8", self.show_stats),
            ("💾 Save", "#6c757d", self.save_todos)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(buttons_frame, text=text,
                          font=("Arial", 10, "bold"),
                          bg=color, fg="white",
                          command=command, padx=15, pady=8,
                          relief="flat")
            btn.pack(side="left", padx=5)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.todos.append({"task": task_text, "completed": False})
            self.task_entry.delete(0, tk.END)
            self.load_tasks_to_listbox()
            self.save_todos()
    
    def load_tasks_to_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, todo in enumerate(self.todos):
            status = "✓ " if todo["completed"] else "○ "
            task_text = f"{status} {todo['task']}"
            self.listbox.insert(tk.END, task_text)
            
            # Color based on completion status
            if todo["completed"]:
                self.listbox.itemconfig(idx, {'bg': self.colors["completed"]})
            else:
                self.listbox.itemconfig(idx, {'bg': self.colors["pending"]})
    
    def complete_task(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            self.todos[idx]["completed"] = True
            self.load_tasks_to_listbox()
            self.save_todos()
    
    def toggle_task(self, event):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            self.todos[idx]["completed"] = not self.todos[idx]["completed"]
            self.load_tasks_to_listbox()
            self.save_todos()
    
    def edit_task(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            current_task = self.todos[idx]["task"]
            
            # Create edit window
            edit_win = tk.Toplevel(self.root)
            edit_win.title("Edit Task")
            edit_win.geometry("400x150")
            edit_win.configure(bg=self.colors["bg"])
            
            tk.Label(edit_win, text="Edit Task:", 
                    font=("Arial", 12, "bold"),
                    bg=self.colors["bg"]).pack(pady=10)
            
            edit_entry = tk.Entry(edit_win, font=("Arial", 12),
                                 width=40)
            edit_entry.pack(pady=10, padx=20)
            edit_entry.insert(0, current_task)
            edit_entry.select_range(0, tk.END)
            edit_entry.focus()
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.todos[idx]["task"] = new_text
                    self.load_tasks_to_listbox()
                    self.save_todos()
                    edit_win.destroy()
            
            tk.Button(edit_win, text="Save", bg="#28a745", fg="white",
                     font=("Arial", 10, "bold"), command=save_edit,
                     padx=20, pady=5).pack(pady=10)
    
    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            if messagebox.askyesno("Confirm Delete", 
                                 "Are you sure you want to delete this task?"):
                del self.todos[idx]
                self.load_tasks_to_listbox()
                self.save_todos()
    
    def show_stats(self):
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["completed"])
        pending = total - completed
        percentage = (completed/total*100) if total > 0 else 0
        
        stats_text = f"""📊 Task Statistics:
        
Total Tasks: {total}
Completed: {completed}
Pending: {pending}
Completion: {percentage:.1f}%"""
        
        messagebox.showinfo("Statistics", stats_text)
    
    def save_todos(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def load_todos(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
