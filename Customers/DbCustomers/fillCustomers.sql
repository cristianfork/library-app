CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    mail VARCHAR(100) NOT NULL
);

INSERT INTO customers (id, name, surname, mail) VALUES
(1, 'Name 1', 'Surname 1', 'Mail 1'),
(2, 'Name 2', 'Surname 2', 'Mail 2'),
(3, 'Name 3', 'Surname 3', 'Mail 3'),
(4, 'Name 4', 'Surname 4', 'Mail 4'),
(5, 'Name 5', 'Surname 5', 'Mail 5'),
(6, 'Name 6', 'Surname 6', 'Mail 6'),
(7, 'Name 7', 'Surname 7', 'Mail 7'),
(8, 'Name 8', 'Surname 8', 'Mail 8'),
(9, 'Name 9', 'Surname 9', 'Mail 9'),
(10, 'Name 10', 'Surname 10', 'Mail 10');