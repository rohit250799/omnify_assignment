    Setup: (all commands mentioned are for Ubuntu users)

1. Fork the repo and clone it to your local system
2. Create a virtual environment using the command: python3 -m venv env (env=name of virtual environment, also python should be installed before this)
3. Once env is ready, activate it using the command: source env/bin/activate
4. Once env is activated, install all necessary requirements mentioned in the requirements.txt file (from inside the bookerProject directory) using command: pip install -r requirements.txt

5. When requirements are installed, run the dev server using: python3 manage.py runserver
6. To check the API endpoints, first create a few model entities from the Django admin panel for FitnessClass, Users etc. (seed data provided for unit tests)
7. Use Postman / any other alternative to hit the api endpoints mentioned below. Responses will be returned accordingly
8. To perform unit testing, separate instructions have been included underneath


Assumptions made:

    How different entities are related:

1. 1 fitness class can have multiple available slots
2. 1 fitness class can be booked by multiple users
3. There can be multiple fitness classes 
4. 1 user can book appointments in multiple classes
5. 1 user can book multiple available slots in a fitness class

---

    Relationship between different entities in the DB:

1. FitnessClass ↔ AvailableSlot: One-to-many
2. FitnessClass ↔ User: Many-to-many with additional data (how many slots they booked) — requires a through model
3. User ↔ AvailableSlot: Many-to-many (a user can book multiple slots, and slots can be booked by different users theoretically — but there should be a limit later)

---
All models have been defined in the classes/models.py file

    Booking model:

1. The Booking model acts as a through model between User and FitnessClass models, while also connecting with AvailableSlot to show which slots were booked
2. slots_booked in Booking model allows tracking which specific slots were booked

---

Testing:

1. Used pytest-django for unit testing - needs to be installed in the virtual environment
2. All tests are written in the tests/ directory inside the classes app
3. Once pytest.ini is set - start unit testing using the command: pytest

---

API Endpoints:
1. GET request on http://127.0.0.1:8000/classes/ -> returns a list of all upcoming fitness classes

2. POST request on http://127.0.0.1:8000/book-class/{user_id}/{fitness_class_id}/ -> books a fitness class with fitness class id for user user_id ({
  "slot_ids": [2],
  "quantity": 2
} - adding this in body, values can be altered)

3. GET request on http://127.0.0.1:8000/class/bookings/?email={mail_id} -> returns a list of all fitness classes booked with the mail id