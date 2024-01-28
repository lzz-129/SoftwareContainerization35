from utils import db

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.Text)
    title_year = db.Column(db.Integer)
    language = db.Column(db.Text)
    country = db.Column(db.Text)
    duration = db.Column(db.Integer)
    content_rating = db.Column(db.Text)
    movie_imdb_link = db.Column(db.Text)
    director_name = db.Column(db.Text)
    imdb_score = db.Column(db.Float)
    num_voted_users = db.Column(db.Integer)
    gross = db.Column(db.Float)

    # Relationship to Genre through the association table
    genres = db.relationship('Genre', secondary='movie_genre', back_populates='movies')
    # Relationship to Actor through the association table
    actors = db.relationship('Actor', secondary='movie_actor', back_populates='movies')

    # return as dict
    def to_dict(self):
        return{
            'id': self.id,
            'movie_title': self.movie_title,
            'title_year': self.title_year,
            'language': self.language,
            'country': self.country,
            'duration': self.duration,
            'content_rating': self.content_rating,
            'movie_imdb_link': self.movie_imdb_link,
            'director_name': self.director_name,
            'imdb_score': self.imdb_score,
            'num_voted_users': self.num_voted_users,
            'gross': self.gross,
            'genres': [genre.name for genre in self.genres],
            'actors': [actor.name for actor in self.actors]
        }

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    # Relationship to Movie through the association table
    movies = db.relationship('Movie', secondary='movie_genre', back_populates='genres')

class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    # Relationship to Movie through the association table
    movies = db.relationship('Movie', secondary='movie_actor', back_populates='actors')

class MovieActor(db.Model):
    __tablename__ = 'movie_actor'
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)






#TODO: users

