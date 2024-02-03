from utils import db

class Movie(db.Model):
    __tablename__ = 'movies'
    #id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String, primary_key=True)
    title_year = db.Column(db.Integer)
    language = db.Column(db.String)
    country = db.Column(db.String)
    duration = db.Column(db.Numeric)
    content_rating = db.Column(db.String)
    movie_imdb_link = db.Column(db.String)
    director_name = db.Column(db.String)
    imdb_score = db.Column(db.Numeric)
    num_voted_users = db.Column(db.Integer)
    gross = db.Column(db.Numeric)

    # Relationship to Genre through the association table
    genres = db.relationship('Genre', secondary='movie_genres', back_populates='movies')
    # Relationship to Actor through the association table
    actors = db.relationship('Actor', secondary='movie_actors', back_populates='movies')
    # Relationship to Users through the association table
    users = db.relationship('MovieUser', back_populates='movie')

    # return as dict
    def to_dict(self):
        return{
            #'id': self.id,
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
            'genres': [genre.genre_type for genre in self.genres],
            'actors': [actor.actor_name for actor in self.actors],
            'users': [
                {
                    'user_id': movie_user.user.user_id,
                    'user_name': movie_user.user.user_name,
                    'rating': movie_user.rating,
                    'comment': movie_user.comment
                }
                for movie_user in self.users
            ]
        }

class Genre(db.Model):
    __tablename__ = 'genres'
    #id = db.Column(db.Integer, primary_key=True)
    genre_type = db.Column(db.String, primary_key=True)

    # Relationship to Movie through the association table
    movies = db.relationship('Movie', secondary='movie_genres', back_populates='genres')

class Actor(db.Model):
    __tablename__ = 'actors'
    #id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String, primary_key=True)

    # Relationship to Movie through the association table
    movies = db.relationship('Movie', secondary='movie_actors', back_populates='actors')

class MovieActor(db.Model):
    __tablename__ = 'movie_actors'
    movie_title = db.Column(db.String, db.ForeignKey('movies.movie_title'), primary_key=True)
    actor_name = db.Column(db.String, db.ForeignKey('actors.actor_name'), primary_key=True)

class MovieGenre(db.Model):
    __tablename__ = 'movie_genres'
    movie_title = db.Column(db.Integer, db.ForeignKey('movies.movie_title'), primary_key=True)
    genre_type = db.Column(db.Integer, db.ForeignKey('genres.genre_type'), primary_key=True)

#TODO: users
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    com_movies = db.relationship('MovieUser', back_populates='user')
    def get_id(self):
        # 假设 User 模型有一个类型为 int 的 id 字段
        return str(self.user_id)

    def to_dict(self):
        return{
            #'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,
            'com_movies': [
                {
                    'movie_title': movie_user.movie.movie_title,
                    'comment': movie_user.comment,
                    'rating': movie_user.rating
                }
                for movie_user in self.com_movies
            ]
        }

    # def is_active(self):
    #     # 在这里，您应该编写逻辑来检查用户是否处于活跃状态。
    #     # 这只是一个简单的例子：
    #     return True
    #
    # def is_authenticated(self):
    #     # 假设每个注册的用户默认都是通过身份验证的
    #     return True
    #
    # def is_anonymous(self):
    #     # 默认情况下，已注册用户不是匿名用户
    #     return False



class MovieUser(db.Model):
    __tablename__ = 'movie_users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    movie_title = db.Column(db.String, db.ForeignKey('movies.movie_title'), primary_key=True)
    rating = db.Column(db.Integer, db.CheckConstraint('rating >= 1 AND rating <= 5'))
    comment = db.Column(db.Text)

    user = db.relationship('User', back_populates='com_movies')
    movie = db.relationship('Movie', back_populates='users')
