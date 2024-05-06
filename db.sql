create database moviemgmt;
drop database moviemgmt;
use moviemgmt;
select * from movies;

-- MOVIES
CREATE TABLE movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    release_date INT,
    ratings FLOAT,
    review TEXT
);
drop table movies;
select * from movies;
DELETE m1 FROM movies m1
JOIN movies m2 ON m1.title = m2.title AND m1.movie_id > m2.movie_id;

-- ACTORS
CREATE TABLE actors (
    actor_id INT PRIMARY KEY AUTO_INCREMENT,
    actor_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50)
);
select * from actors;

-- ACTORS2
select * from actors2;
CREATE TABLE actors2(
	actor_name VARCHAR(50),
    movie_name VARCHAR(50)
);

ALTER TABLE actors2
ADD FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);

-- USERS
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL
);
alter table users add type varchar(20);
desc users;
select * from users;
SELECT username, password, type FROM users WHERE username = "user1" AND password = "password1";
UPDATE users
SET type = 'admin'
WHERE user_id = 1;
insert into users(username,password,type) values ('Aditya','Myproject@2023','admin');
insert into users(username,password,type) values ('Navdeep','Myproject@2023','admin');
insert into users(username,password,type) values ('user1','root','user');

-- AWARDS
CREATE TABLE awards (
    award_id INT PRIMARY KEY AUTO_INCREMENT,
    award_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    year INT,
    movie_id INT,
    actor_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);
select * from awards;

-- REVIEWS
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    movie_id INT,
    rating FLOAT,
    comment TEXT,
    review_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- Insert sample data into movies table
INSERT INTO movies (title, genre, release_date, ratings, review)
VALUES
    ('Inception', 'Sci-Fi', 2010, 8.7, 'Mind-bending thriller with stunning visuals.'),
    ('The Shawshank Redemption', 'Drama', 1994, 9.3, 'Classic tale of hope and redemption.'),
    ('The Dark Knight', 'Action', 2008, 9.0, 'Epic superhero film with a brilliant performance by Heath Ledger.');

-- Insert sample data into actors table
drop table actors;
select * from users;
INSERT INTO actors (actor_name, nationality)
VALUES
    ('Leonardo DiCaprio', 'American'),
    ('Morgan Freeman', 'American'),
    ('Christian Bale', 'British'),
    ('Tom Holland', 'UK');

-- Insert sample data into users table
INSERT INTO users (username, password)
VALUES
	('Atharv','123'),
    ('user1','password1'),
    ('user2','password2'),
    ('user3','password3');

-- Insert sample data into awards table
INSERT INTO awards (award_name, category, year, movie_id, actor_id)
VALUES
    ('Oscar', 'Best Picture', 2011, 1, 1),
    ('Golden Globe', 'Best Actor', 1995, 2, 2),
    ('BAFTA', 'Best Supporting Actor', 2009, 3, 3);

-- Insert sample data into reviews table
INSERT INTO reviews (user_id, movie_id, rating, comment, review_date)
VALUES
    (1, 1, 9.0, 'Amazing movie! Loved the plot twists.', '2023-01-01'),
    (2, 2, 9.5, 'One of the best movies ever made.', '2023-01-02'),
    (3, 3, 8.5, 'Great performance by Christian Bale.', '2023-01-03');
    
    
    
-- procedure to show all data in the movies table
delimiter //
create procedure show_data(in movie_id int)
begin
select *from movies;
end//


-- trigger to delete duplicate movie data
DELIMITER //

CREATE TRIGGER delete_duplicates
BEFORE INSERT ON movies
FOR EACH ROW
BEGIN
    DECLARE movie_count INT;
    SET movie_count = (SELECT COUNT(*) FROM movies WHERE title = NEW.title);
    IF movie_count > 1 THEN
        DELETE FROM movies WHERE title = NEW.title LIMIT 1;
    END IF;
END;
//

DELIMITER ;

-- Insert sample data into movies table
INSERT INTO movies (title, genre, release_date, ratings, review)
VALUES
    ('Avatar', 'Sci-Fi', 2009, 7.8, 'Visually stunning film with a captivating storyline.'),
    ('The Godfather', 'Crime', 1972, 9.2, 'Timeless classic depicting the Italian-American Mafia.'),
    ('Pulp Fiction', 'Crime', 1994, 8.9, 'Quirky and non-linear narrative with memorable characters.'),
    ('Titanic', 'Romance', 1997, 7.8, 'Epic romance set against the backdrop of the ill-fated Titanic.'),
    ('La La Land', 'Musical', 2016, 8.0, 'A modern musical with beautiful cinematography and music.'),
    ('Sholay', 'Action', 1975, 8.2, 'Iconic Bollywood film with memorable characters like Jai and Veeru.'),
    ('Dilwale Dulhania Le Jayenge', 'Romance', 1995, 8.1, 'Romantic drama that became a cultural phenomenon.'),
    ('The Matrix', 'Action', 1999, 8.7, 'Groundbreaking sci-fi action film with mind-bending visuals.'),
    ('Gone with the Wind', 'Drama', 1939, 8.1, 'Classic epic set during the American Civil War.'),
    ('Casablanca', 'Romance', 1942, 8.5, 'Timeless love story set in wartime Morocco.'),
    ('Jurassic Park', 'Adventure', 1993, 8.1, 'Dinosaur-themed adventure with groundbreaking special effects.'),
    ('Dangal', 'Biography', 2016, 8.4, 'Inspiring story of a father training his daughters in wrestling.'),
    ('The Revenant', 'Adventure', 2015, 8.0, 'Intense survival drama with a stellar performance by Leonardo DiCaprio.'),
    ('Baahubali: The Beginning', 'Action', 2015, 8.1, 'Epic fantasy film with grand visuals and a captivating story.'),
    ('Forrest Gump', 'Drama', 1994, 8.8, 'Heartwarming tale of a man with a low IQ navigating through life.');

-- Add more actors data
INSERT INTO actors (actor_name, nationality)
VALUES
    ('Sam Worthington', 'Australian'),
    ('Marlon Brando', 'American'),
    ('John Travolta', 'American'),
    ('Leonardo DiCaprio', 'American'),
    ('Ryan Gosling', 'Canadian'),
    ('Amitabh Bachchan', 'Indian'),
    ('Shah Rukh Khan', 'Indian'),
    ('Keanu Reeves', 'Canadian'),
    ('Clark Gable', 'American'),
    ('Humphrey Bogart', 'American'),
    ('Tom Hanks', 'American'),
    ('Aamir Khan', 'Indian'),
    ('Leonardo DiCaprio', 'American'),
    ('Prabhas', 'Indian'),
    ('Tom Hanks', 'American');

-- Add more awards data
INSERT INTO awards (award_name, category, year, movie_id, actor_id)
VALUES
    ('Golden Globe', 'Best Director', 2010, 1, 1),
    ('Oscar', 'Best Actor', 1973, 2, 2),
    ('BAFTA', 'Best Original Screenplay', 1995, 3, 3),
    ('Golden Globe', 'Best Original Song', 1998, 4, 4),
    ('Oscar', 'Best Original Song', 1998, 4, 4),
    ('IIFA', 'Best Actor', 1999, 6, 6),
    ('Filmfare', 'Best Actor', 1996, 7, 7),
    ('Oscar', 'Best Film Editing', 2000, 8, 8),
    ('Oscar', 'Best Actress', 1940, 9, 9),
    ('Oscar', 'Best Picture', 1943, 10, 10),
    ('Oscar', 'Best Visual Effects', 1994, 11, 11),
    ('Filmfare', 'Best Film', 2017, 12, 12),
    ('Oscar', 'Best Actor in a Leading Role', 2016, 13, 13),
    ('National Film Awards', 'Best Feature Film', 2016, 14, 14),
    ('Oscar', 'Best Actor', 1995, 15, 15);

-- Add more reviews data
INSERT INTO reviews (user_id, movie_id, rating, comment, review_date)
VALUES
    (1, 5, 8.0, 'Great performance by Sam Worthington.', '2023-03-15'),
    (2, 6, 9.5, 'Marlon Brandos acting is legendary.', '2023-03-16'),
    (2, 7, 8.7, 'John Travolta steals the show in Pulp Fiction.', '2023-03-17'),
    (2, 8, 9.2, 'Leonardo DiCaprio delivers another outstanding performance.', '2023-03-18'),
    (1, 9, 8.0, 'La La Land is a visually stunning musical.', '2023-03-19'),
    (2, 10, 8.5, 'Amitabh Bachchan shines in Sholay.', '2023-03-20'),
    (2, 11, 8.8, 'Dilwale Dulhania Le Jayenge is a classic romance.', '2023-03-21'),
    (1, 12, 9.0, 'Keanu Reeves excels in The Matrix.', '2023-03-22'),
    (2, 13, 8.3, 'Clark Gables performance in Gone with the Wind is iconic.', '2023-03-23'),
    (1, 14, 8.5, 'Casablanca is a timeless love story.', '2023-03-24'),
    (1, 15, 8.2, 'Jurassic Parks special effects are groundbreaking.', '2023-03-25'),
    (1, 16, 9.1, 'Dangal is an inspiring story of perseverance.', '2023-03-26'),
    (1, 17, 8.7, 'The Revenant showcases Leonardo DiCaprios talent.', '2023-03-27'),
    (1, 18, 8.4, 'Baahubali: The Beginning is an epic fantasy.', '2023-03-28'),
    (1, 19, 9.0, 'Forrest Gump is a heartwarming journey.', '2023-03-29');


