CREATE DATABASE multi_clinic_db;
USE multi_clinic_db;
CREATE TABLE Patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    dob DATE,
    gender VARCHAR(10),
    phone VARCHAR(15)
);

CREATE TABLE Clinic (
    clinic_id INT PRIMARY KEY AUTO_INCREMENT,
    clinic_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    specialization VARCHAR(100),
    clinic_id INT,
    FOREIGN KEY (clinic_id) REFERENCES Clinic(clinic_id)
);

CREATE TABLE Visit (
    visit_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    visit_date DATE,
    diagnosis VARCHAR(200),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE Prescription (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    visit_id INT,
    medicine_name VARCHAR(100),
    dosage VARCHAR(50),
    FOREIGN KEY (visit_id) REFERENCES Visit(visit_id)
);
DELIMITER //

CREATE PROCEDURE add_patient(
    IN p_name VARCHAR(100),
    IN p_dob DATE,
    IN p_gender VARCHAR(10),
    IN p_phone VARCHAR(15)
)
BEGIN
    INSERT INTO Patient(name, dob, gender, phone)
    VALUES(p_name, p_dob, p_gender, p_phone);
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE add_visit(
    IN p_patient_id INT,
    IN p_doctor_id INT,
    IN p_visit_date DATE,
    IN p_diagnosis VARCHAR(200)
)
BEGIN
    INSERT INTO Visit(patient_id, doctor_id, visit_date, diagnosis)
    VALUES(p_patient_id, p_doctor_id, p_visit_date, p_diagnosis);
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE view_medical_history(
    IN p_patient_id INT
)
BEGIN
    SELECT p.name,
           v.visit_date,patient
           v.diagnosis,
           pr.medicine_name,
           pr.dosage
    FROM Patient p
    JOIN Visit v ON p.patient_id = v.patient_id
    LEFT JOIN Prescription pr ON v.visit_id = pr.visit_id
    WHERE p.patient_id = p_patient_id;
END //

DELIMITER ;
SELECT * FROM Patient;
