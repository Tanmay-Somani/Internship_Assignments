import tkinter as tk
import mysql.connector
from tkinter import messagebox
conn = mysql.connector.connect(
    host='localhost', user='root', password='root', database='employee_db'
)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    position VARCHAR(100),
                    salary FLOAT
                )''')
conn.commit()

def add_employee():
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()

    if name and position and salary:
        salary = float(salary)  # Convert to float
        cursor.execute("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)", 
                       (name, position, salary))
        conn.commit()
        messagebox.showinfo("Success", "Employee Added Successfully")
    else:
        messagebox.showerror("Error", "All fields are required")

def promote_employee():
    emp_id = entry_id.get()
    new_position = entry_position.get()
    new_salary = entry_salary.get()

    if emp_id and (new_position or new_salary):
        update_query = "UPDATE employees SET "
        values = []
        
        if new_position:
            update_query += "position = %s, "
            values.append(new_position)
        if new_salary:
            update_query += "salary = %s, "
            values.append(float(new_salary))  # Convert to float
        
        update_query = update_query.rstrip(', ') + " WHERE id = %s"
        values.append(emp_id)
        
        cursor.execute(update_query, tuple(values))
        conn.commit()
        messagebox.showinfo("Success", "Employee Promoted Successfully")
    else:
        messagebox.showerror("Error", "Employee ID and at least one update field required")

def remove_employee():
    emp_id = entry_id.get()
    if emp_id:
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        conn.commit()
        messagebox.showinfo("Success", "Employee Removed Successfully")
    else:
        messagebox.showerror("Error", "Employee ID is required")

def display_employees():
    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()
    display_text.delete(1.0, tk.END)
    for record in records:
        display_text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Position: {record[2]}, Salary: {record[3]}\n")

def on_closing():
    conn.close()
    root.destroy()

root = tk.Tk()
root.title("Employee Management System")
root.geometry("800x500")
tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()
tk.Label(root, text="Position").pack()
entry_position = tk.Entry(root)
entry_position.pack()
tk.Label(root, text="Salary").pack()
entry_salary = tk.Entry(root)
entry_salary.pack()
tk.Label(root, text="Employee ID").pack()
entry_id = tk.Entry(root)
entry_id.pack()
tk.Button(root, text="Add Employee", command=add_employee).pack()
tk.Button(root, text="Remove Employee", command=remove_employee).pack()
tk.Button(root, text="Promote Employee", command=promote_employee).pack()
tk.Button(root, text="Display Employees", command=display_employees).pack()
display_text = tk.Text(root, height=10, width=50)
display_text.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
