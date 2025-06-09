Assumptions made:

DB relations between different entities:

1. 1 fitness class can have multiple available slots
2. 1 fitness class can be booked by multiple users
3. There can be multiple fitness classes 
4. 1 user can book appointments in multiple classes
5. 1 user can book multiple available slots in a fitness class

Fitness_class fields:

1. Name
2. Date_time
3. Instructor
4. Available slots

User class fields: 

1. Name
2. Email id
3. Password
4. Booked_classes (for each fitness_class booked by the user - also show the number of available classes he booked)

___

Relationship between different entities in the DB:

1. FitnessClass ↔ AvailableSlot: One-to-many
2. FitnessClass ↔ User: Many-to-many with additional data (how many slots they booked) — requires a through model
3. User ↔ AvailableSlot: Many-to-many (a user can book multiple slots, and slots can be booked by different users theoretically — but there should be a limit later)

---

Booking model:

1. The Booking model acts as a through model between User and FitnessClass models, while also connecting with AvailableSlot to show which slots were booked
2. slots_booked in Booking model allows tracking which specific slots were booked