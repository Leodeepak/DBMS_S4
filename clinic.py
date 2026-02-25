import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ================= DATABASE CONNECTION =================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="195047",   # <-- YOUR PASSWORD
    database="MultiClinicDB"
)
cursor = conn.cursor()

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Multi-Clinic Medical System")
root.geometry("600x500")
root.configure(bg="#E3F2FD")

title = tk.Label(root, text="Multi-Clinic Medical History System",
                 font=("Arial", 18, "bold"),
                 bg="#E3F2FD", fg="#0D47A1")
title.pack(pady=20)

# ================= PATIENT WINDOW =================
def patient_window():
    win = tk.Toplevel(root)
    win.title("Patient Management")
    win.geometry("800x600")
    win.configure(bg="white")

    tk.Label(win, text="Add Patient", font=("Arial", 14, "bold"),
             bg="white").pack(pady=10)

    form = tk.Frame(win, bg="white")
    form.pack()

    labels = ["Name", "DOB (YYYY-MM-DD)", "Gender",
              "Phone", "Address", "Blood Group"]

    entries = []

    for i, label in enumerate(labels):
        tk.Label(form, text=label, bg="white").grid(row=i, column=0, pady=5)
        if label == "Gender":
            entry = ttk.Combobox(form, values=["Male", "Female", "Other"])
        else:
            entry = tk.Entry(form)
        entry.grid(row=i, column=1, pady=5)
        entries.append(entry)

    def add_patient():
        query = """
        INSERT INTO Patient (name, dob, gender, phone, address, blood_group)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = tuple(e.get() for e in entries)
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Patient Added!")

    tk.Button(win, text="Add Patient", bg="#2E7D32", fg="white",
              command=add_patient).pack(pady=10)

    # Table
    tree = ttk.Treeview(win, columns=("ID", "Name", "DOB", "Gender",
                                      "Phone", "Address", "Blood"),
                        show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM Patient")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    tk.Button(win, text="Refresh Table", command=load_data).pack(pady=5)


# ================= DOCTOR WINDOW =================
def doctor_window():
    win = tk.Toplevel(root)
    win.title("Doctor Management")
    win.geometry("700x500")
    win.configure(bg="white")

    tk.Label(win, text="Add Doctor", font=("Arial", 14, "bold"),
             bg="white").pack(pady=10)

    form = tk.Frame(win, bg="white")
    form.pack()

    labels = ["Name", "Specialization", "Phone", "Clinic ID"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form, text=label, bg="white").grid(row=i, column=0, pady=5)
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, pady=5)
        entries.append(entry)

    def add_doctor():
        query = """
        INSERT INTO Doctor (name, specialization, phone, clinic_id)
        VALUES (%s, %s, %s, %s)
        """
        values = tuple(e.get() for e in entries)
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Doctor Added!")

    tk.Button(win, text="Add Doctor", bg="#1565C0", fg="white",
              command=add_doctor).pack(pady=10)

    tree = ttk.Treeview(win, columns=("ID", "Name", "Spec",
                                      "Phone", "ClinicID"),
                        show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM Doctor")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    tk.Button(win, text="Refresh Table", command=load_data).pack(pady=5)


# ================= VISIT WINDOW =================
def visit_window():
    win = tk.Toplevel(root)
    win.title("Visit Management")
    win.geometry("700x500")
    win.configure(bg="white")

    tk.Label(win, text="Add Visit", font=("Arial", 14, "bold"),
             bg="white").pack(pady=10)

    form = tk.Frame(win, bg="white")
    form.pack()

    labels = ["Patient ID", "Doctor ID", "Clinic ID",
              "Visit Date (YYYY-MM-DD)", "Symptoms", "Diagnosis"]

    entries = []

    for i, label in enumerate(labels):
        tk.Label(form, text=label, bg="white").grid(row=i, column=0, pady=5)
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, pady=5)
        entries.append(entry)

    def add_visit():
        query = """
        INSERT INTO Visit (patient_id, doctor_id, clinic_id,
                           visit_date, symptoms, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = tuple(e.get() for e in entries)
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Visit Added!")

    tk.Button(win, text="Add Visit", bg="#6A1B9A", fg="white",
              command=add_visit).pack(pady=10)


# ================= MEDICAL HISTORY =================
def history_window():
    win = tk.Toplevel(root)
    win.title("Medical History")
    win.geometry("900x500")
    win.configure(bg="white")

    tk.Label(win, text="Patient ID:",
             bg="white").pack(pady=5)

    entry = tk.Entry(win)
    entry.pack()

    tree = ttk.Treeview(win,
                        columns=("Patient", "Doctor",
                                 "Date", "Diagnosis"),
                        show="headings")

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    def load_history():
        for row in tree.get_children():
            tree.delete(row)

        query = """
        SELECT p.name, d.name, v.visit_date, v.diagnosis
        FROM Visit v
        JOIN Patient p ON v.patient_id = p.patient_id
        JOIN Doctor d ON v.doctor_id = d.doctor_id
        WHERE p.patient_id = %s
        """
        cursor.execute(query, (entry.get(),))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    tk.Button(win, text="Load History",
              command=load_history).pack(pady=10)


# ================= MAIN MENU BUTTONS =================
tk.Button(root, text="Patient Management",
          width=25, bg="#2E7D32", fg="white",
          command=patient_window).pack(pady=10)

tk.Button(root, text="Doctor Management",
          width=25, bg="#1565C0", fg="white",
          command=doctor_window).pack(pady=10)

tk.Button(root, text="Visit Management",
          width=25, bg="#6A1B9A", fg="white",
          command=visit_window).pack(pady=10)

tk.Button(root, text="View Medical History",
          width=25, bg="#EF6C00", fg="white",
          command=history_window).pack(pady=10)

tk.Button(root, text="Exit",
          width=25, bg="red", fg="white",
          command=root.destroy).pack(pady=20)

root.mainloop()
