#  CodeAlpha Task 1 - Data Redundancy Removal System

##  Project Description
This project is a cloud-based system that prevents duplicate and invalid data from being stored in a database.  
It validates user input and ensures only unique and verified data is saved.

---

##  Features
-  Email and phone validation  
   Duplicate data detection  
-  Only unique records stored  
-  Cloud database integration (Firebase)

---

##  Tech Stack
- Python (Flask)
- Firebase Firestore
- Postman

---

##  How It Works
1. User sends data using API  
2. System validates email and phone number  
3. Checks if data already exists  
4. If duplicate → rejected  
5. If unique → stored in Firebase  

---

##  API Endpoint

### POST `/add`

### Request Body:
```json
{
  "name": "Anshu",
  "email": "test@gmail.com",
  "phone": "9876543210"
}
