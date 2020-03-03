/* create_db.sql

WARNING: This script will drop the tables at the beginning. Do not run if you have data that is not 
backed up!!!

This script will build the tables and seed some of the inital data.

*/



-- Preliminary DROPS 
DROP TABLE post; 
DROP TABLE lab_step; 
DROP TABLE lab; 
DROP TABLE user_account; 
DROP TABLE term; 
DROP TABLE account_type;


-- CREATE TABLES
CREATE TABLE account_type 
( account_type_id 	SERIAL 			PRIMARY KEY 
, name 				VARCHAR(30)		NOT NULL
, code 				VARCHAR(5)		NOT NULL
, admin_login		INT				NOT NULL 	DEFAULT 0);

CREATE TABLE term 
( term_id 			SERIAL 			PRIMARY KEY 
, name 				VARCHAR(20)		NOT NULL 
, code 				VARCHAR(20) 	NOT NULL
, start_date		DATE			NOT NULL 
, end_date 			DATE );


CREATE TABLE user_account
( user_account_id 	SERIAL 			PRIMARY KEY
, first_name		VARCHAR(30)		NOT NULL
, last_name			VARCHAR(30)		NOT NULL
, email				VARCHAR(60)		NOT NULL
, password			VARCHAR(250)	NOT NULL
, token 			VARCHAR(250)
, force_pass_reset	INT 			NOT NULL 	DEFAULT 0
, enabled			INT				NOT NULL 	DEFAULT 1
, date_created		TIMESTAMP 		NOT NULL	DEFAULT CURRENT_TIMESTAMP
, account_type 		INT 			NOT NULL 	DEFAULT 1
, term_id			INT
, FOREIGN KEY (account_type) REFERENCES account_type(account_type_id)
, FOREIGN KEY (term_id) REFERENCES term(term_id));

CREATE TABLE lab 
( lab_id 			SERIAL 			PRIMARY KEY 
, name 				VARCHAR(30)		NOT NULL
, number 			INT 			NOT NULL 
, description		TEXT
, instructions		TEXT 
, archived 			INT 			NOT NULL 	DEFAULT 0);


CREATE TABLE lab_step 
( lab_step_id 		SERIAL 			PRIMARY KEY 
, lab_id 			INT 			NOT NULL
, name 				VARCHAR(20)		NOT NULL 
, number 			INT 			NOT NULL 
, instruction 		TEXT
, FOREIGN KEY (lab_id) REFERENCES lab(lab_id));


CREATE TABLE post 
( post_id 			SERIAL 			PRIMARY KEY 
, user_account_id	INT 			NOT NULL 
, lab_step_id		INT 			NOT NULL 
, title 			VARCHAR(30)		NOT NULL 
, content 			TEXT 			NOT NULL 
, date_posted		TIMESTAMP		NOT NULL 	DEFAULT CURRENT_TIMESTAMP
, approved 			INT 			NOT NULL 	DEFAULT 1
, likes 			INT 			NOT NULL 	DEFAULT 0
, FOREIGN KEY (user_account_id) REFERENCES user_account(user_account_id) 
, FOREIGN KEY (lab_step_id) REFERENCES lab_step(lab_step_id));


-- Seed basic data 

INSERT INTO account_type 
( name 
, code 
, admin_login)
VALUES
  ( 'Administrator', 'ADMIN', 1 )
, ('Student', 'STUD', 0)
, ('Teaching Assistant', 'TA', 0)
, ('Alumni', 'ALUM', 0);

INSERT INTO term 
( name 
, code
, start_date 
, end_date )
VALUES 
( 'Winter 2020', 'WINTER2020', '01/01/2020', NULL);


-- Insert labs the hard way
INSERT INTO lab 
( name 
, number )
VALUES 
  ('Lab 1', 1)
, ('Lab 2', 2)
, ('Lab 3', 3)
, ('Lab 4', 4)
, ('Lab 5', 5)
, ('Lab 6', 6)
, ('Lab 7', 7)
, ('Lab 8', 8)
, ('Lab 9', 9)
, ('Lab 10', 10)
, ('Lab 11', 11)
, ('Lab 12', 12)
, ('Lab 13', 13)
, ('Lab 14', 14)
, ('General', 50);


-- Insert Steps 1-4 for each lab (Showing a shortcut)

INSERT INTO lab_step 
( lab_id 
, name 
, number )
SELECT 
  lab.lab_id 
, CONCAT('Step ', step.step) AS name
, step.step AS number
FROM lab CROSS JOIN
(SELECT 1 AS step
UNION 
SELECT 2 AS step
UNION 
SELECT 3 AS step
UNION 
SELECT 4 AS step) step;