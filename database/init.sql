-- users

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INSERT INTO users (user_name, password, email) VALUES
-- ('johndoe', 'johnssecurepassword', 'johndoe@example.com'),
-- ('janedoe', 'janessecurepassword', 'janedoe@example.com');

-- movies
CREATE TABLE IF NOT EXISTS movies (
    movie_title VARCHAR(255) PRIMARY KEY,
    title_year INT,
    language VARCHAR(50),
    country VARCHAR(50),
    duration DECIMAL(10, 1),
    content_rating VARCHAR(50),
    movie_imdb_link VARCHAR(255),
    director_name VARCHAR(255),
    imdb_score DECIMAL(3, 1),
    num_voted_users INT,
    gross DECIMAL(15, 2)
);

COPY movies FROM '/csvs/movies.csv'
DELIMITER ','
CSV HEADER;

-- actors 
CREATE TABLE IF NOT EXISTS actors (
    actor_name VARCHAR(255) PRIMARY KEY
);

COPY actors FROM '/csvs/actors.csv'
DELIMITER ','
CSV HEADER;



-- genres
CREATE TABLE IF NOT EXISTS genres (
    genre_type VARCHAR(255) PRIMARY KEY
);

COPY genres FROM '/csvs/genres.csv'
DELIMITER ','
CSV HEADER;

-- movie_actor
CREATE TABLE IF NOT EXISTS movie_actors (
    movie_title VARCHAR(255) REFERENCES movies(movie_title),
    actor_name VARCHAR(255) REFERENCES actors(actor_name),
    PRIMARY KEY (movie_title, actor_name)
);

COPY movie_actors FROM '/csvs/movie_actors.csv'
DELIMITER ','
CSV HEADER;

-- movie_genres
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_title VARCHAR(255) REFERENCES movies(movie_title),
    genre_type VARCHAR(255) REFERENCES genres(genre_type),
    PRIMARY KEY (movie_title, genre_type)
);

COPY movie_genres FROM '/csvs/movie_genres.csv'
DELIMITER ','
CSV HEADER;


-- movie_user
CREATE TABLE IF NOT EXISTS movie_users (
    user_id INT REFERENCES users(user_id),
    movie_title VARCHAR(255) REFERENCES movies(movie_title),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    PRIMARY KEY (user_id, movie_title)
);

-- INSERT INTO movie_users (user_id, movie_title, rating, comment)
-- VALUES
-- (1, 'Avatar', 4, 'Epic conclusion to the Pirates saga. A must-watch!'),
-- (1, 'Spectre', 3, 'Spectre was visually stunning but lacked the punch of previous Bond films.');





