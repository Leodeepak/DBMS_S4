import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8262", 
    database="multi_clinic_db"
)

cursor = conn.cursor()

def add_patient():
    name = input("Enter patient name: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")

    cursor.callproc('add_patient', [name, dob, gender, phone])
    conn.commit()
    print("Patient added successfully!\n")

def add_visit():
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    visit_date = input("Enter visit date (YYYY-MM-DD): ")
    diagnosis = input("Enter diagnosis: ")

    cursor.callproc('add_visit', [patient_id, doctor_id, visit_date, diagnosis])
    conn.commit()
    print("Visit added successfully!\n")

def add_prescription():
    visit_id = int(input("Enter visit ID: "))
    medicine = input("Enter medicine name: ")
    dosage = input("Enter dosage: ")

    cursor.callproc('add_prescription', [visit_id, medicine, dosage])
    conn.commit()
    print("Prescription added successfully!\n")

def view_history():
    patient_id = int(input("Enter patient ID: "))
    cursor.callproc('view_medical_history', [patient_id])

    for result in cursor.stored_results():
        records = result.fetchall()
        for row in records:
            print(row)
    print()

while True:
    print("====== Multi-Clinic Medical System ======")
    print("1. Add Patient")
    print("2. Add Visit")
    print("3. Add Prescription")
    print("4. View Medical History")
    print("5. Exit")

    choice = input("Select an option: ")

    if choice == '1':
        add_patient()
    elif choice == '2':
        add_visit()
    elif choice == '3':
        add_prescription()
    elif choice == '4':
        view_history()
    elif choice == '5':
        print("Exiting system...")
        break
    else:
        print("Invalid choice! Try again.\n")

cursor.close()
conn.close()