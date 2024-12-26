CREATE DATABASE todo_db;
Drop DATABASE todo_db;

SHOW DATABASES;

show tables;
use todo_db;

SHOW tables;
drop table todo_usertoken;

SELECT* FROM todo_task;

INSERT INTO todo_task (user_id, title, description, created_at, updated_at)
VALUES
(1, 'Buy groceries', 'Milk, bread, and eggs', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Finish project', 'Complete by Friday', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Call plumber', 'Fix the kitchen sink', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Prepare meeting', 'Prepare slides for Monday', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

SELECT * FROM auth_user;
drop table auth_user;

SHOW COLUMNS FROM auth_user;

INSERT INTO todo_task (user_id, title) VALUES (1, 'Sample Task 1');
INSERT INTO todo_task (user_id, title) VALUES (1, 'Sample Task 2');

DESCRIBE todo_task;
SELECT * from todo_task;

-- Insert Task with user_id=1, title='Sample Task 1'
INSERT INTO todo_task (user_id, title, created_at, updated_at) 
VALUES (1, 'Sample Task 1', NOW(), NOW());

-- Insert Task with user_id=1, title='Sample Task 2'
INSERT INTO todo_task (user_id, title, created_at, updated_at) 
VALUES (1, 'Sample Task 2', NOW(), NOW());

SELECT * FROM auth_user WHERE username = 'fidel';
SELECT * FROM todo_usertoken WHERE user_id = (SELECT id FROM auth_user WHERE username = 'fidel');

SELECT * FROM todo_task WHERE user_id = (SELECT id FROM auth_user WHERE username = 'fidel');

select * from todo_CustomUser;












