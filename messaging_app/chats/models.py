  user_id (Primary Key, UUID, Indexed)
    first_name (VARCHAR, NOT NULL)
    last_name (VARCHAR, NOT NULL)
    email (VARCHAR, UNIQUE, NOT NULL)
    password_hash (VARCHAR, NOT NULL)
    phone_number (VARCHAR, NULL)
    role (ENUM: 'guest', 'host', 'admin', NOT NULL)
    created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
 message_id (Primary Key, UUID, Indexed)
    sender_id (Foreign Key, references User(user_id))
    message_body (TEXT, NOT NULL)
    sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
conversation_id (Primary Key, UUID, Indexed)
participants_id (Foreign Key, references User(user_id)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
                  User Table: Unique constraint on email, non-null constraints on required fields.
    Property Table: Foreign key constraint on host_id, non-null constraints on essential attributes.
    Booking Table: Foreign key constraints on property_id and user_id, status must be one of pending, confirmed, or canceled.
    Payment Table: Foreign key constraint on booking_id, ensuring payment is linked to valid bookings.
    Review Table: Constraints on rating values and foreign keys for property_id and user_id.
    Message Table: Foreign key constraints on sender_id and recipient_id.
**Primary Keys:** Indexed automatically.
**Additional Indexes:** Indexes on email (User), property_id (Property and Booking), and booking_id (Booking and Payment)
