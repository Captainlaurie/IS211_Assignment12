-- Create Database:
CREATE SCHEMA IF NOT EXISTS studentschema;

-- Delete tables if they exist:
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

-- Create students table:    
CREATE table students (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name varchar(50),
    last_name varchar (50)
);

-- Create quizzes table:
CREATE table quizzes (
	q_id int NOT NULL PRIMARY KEY,
    subject varchar(100),
	num_questions int,
    date varchar(10)
    );
    
-- Create results table:    
CREATE table results (
    id int NOT NULL PRIMARY KEY,
	student int,
    quiz int,
	grade int,
    FOREIGN KEY (student) REFERENCES students(id), 
    FOREIGN KEY (quiz) REFERENCES quizzes(q_id)
    );
    
