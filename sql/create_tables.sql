
-- PostgreSQL üzerinden manuel aşağıdaki kod ile oluşturuldu.


-- users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    country VARCHAR(5),
    device_type VARCHAR(10),
    signup_source VARCHAR(20),
    register_date DATE,
    user_level INT,
    is_paying_user BOOLEAN
);

-- events table
DROP TABLE IF EXISTS events;
CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    event_name VARCHAR(50),
    timestamp TIMESTAMP,
    event_params JSONB
);
