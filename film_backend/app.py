from flask import Flask, request, jsonify, url_for, redirect, flash
from flask.views import MethodView
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus
import conf


from utils import db, cors
from models import Movie, Actor, Genre, User, MovieUser


app = Flask(__name__)

# CORS
cors.init_app(app)

# sql database
db_user = conf.DBUSER
db_password = quote_plus(conf.DBPW)  # URL encoded
db_host = conf.DBADDR
db_name = conf.DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app) # 关联 db 对象与 Flask 应用

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class FilmApi(MethodView):
    def get(self):
        # 获取查询参数
        movie_title = request.args.get('movie_title')
        title_year = request.args.get('title_year')
        language = request.args.get('language')
        country = request.args.get('country')
        content_rating = request.args.get('content_rating')
        imdb_score_low = request.args.get('imdb_score_low', type=float) # range
        imdb_score_high = request.args.get('imdb_score_high', type=float) # range
        director_name = request.args.get('director_name')
        genre = request.args.get('genre')
        actor = request.args.get('actor')

        try:
            query = Movie.query # basic query
            # filter by paras
            if movie_title:
                query = query.filter(Movie.movie_title.ilike(f'%{movie_title}%'))
            if title_year:
                query = query.filter(Movie.title_year == title_year)
            if language:
                query = query.filter(Movie.language.ilike(f'%{language}%'))
            if country:
                query = query.filter(Movie.country.ilike(f'%{country}%'))
            if content_rating:
                query = query.filter(Movie.content_rating.ilike(f'%{content_rating}%')) # TODO: select box

            # TODO: 大小 range
            if imdb_score_low:
                query = query.filter(Movie.imdb_score >= imdb_score_low)
            if imdb_score_high:
                query = query.filter(Movie.imdb_score <= imdb_score_high)

            if director_name:
                query = query.filter(Movie.director_name.ilike(f'%{director_name}%'))
            if genre:
                # 假设存在一个名为 'name' 的字段在 Genre 模型中
                query = query.join(Movie.genres).filter(Genre.name.ilike(f'%{genre}%')) # TODO: select box
            if actor:
                # 假设存在一个名为 'name' 的字段在 Actor 模型中
                query = query.join(Movie.actors).filter(Actor.name.ilike(f'%{actor}%'))

            #TODO: order by

            # execute query and return
            movies = query.options(joinedload(Movie.genres), joinedload(Movie.actors)).all()
            if not movies:
                return jsonify({'status': 'not found',
                                'message': 'No movies found matching the criteria'
                                }), 404
            else:
                return jsonify({'status': 'success',
                            'message': 'Search success',
                            'data': [movie.to_dict() for movie in movies]
                            }), 200

        except ValueError as e:
            # This might happen if the type conversion for imdb_score_low/high fails, for example
            return jsonify({'status': 'error',
                            'message': 'Invalid input: ' + str(e)
                            }), 400
        except Exception as e:
            # Catch all for any other unexpected errors
            return jsonify({'status': 'error',
                            'message': 'Something wrong: ' + str(e)
                            }), 500


class RegisterApi(MethodView):
    def post(self):
        user_name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        query = User.query

        # 检查用户名是否已存在
        if query.filter((User.user_name==user_name) | (User.email == email)).first():
            #print('user name has been taken', 'warning')
            response = jsonify({'message': 'User name or email has been taken', 'category': 'warning'})
            return response, 409
        try:
            #hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(user_name=user_name, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            response = jsonify({'message': 'Register Success! Please log in', 'category': 'success'})
            return response, 200
        except Exception as e:
                db.session.rollback()
                response = jsonify({'message': 'Register failed due to an error: ' + str(e), 'category': 'danger'})
                return response, 500  # 500 表示服务器内部错误

class LoginApi(MethodView):
    def post(self):
        user_name = request.form['username']
        password = request.form['password']
        #email = request.form['email']
        query = User.query

        # 检查用户名是否已存在
        user = query.filter(User.user_name==user_name, User.password== password).first()
        if user:
            login_user(user, remember=True)
            response = jsonify({'message': 'Login Success!', 'category': 'success'})
            return response, 200
        else:
            response = jsonify({'message': 'User name or password is wrong', 'category': 'warning'})
            return response, 409

class RatingApi(MethodView):
    decorators = [login_required]

    def post(self):
        user_id = request.form['user_id']
        movie_title = request.form['movie_title']
        rating = request.form['rating']
        comment = request.form['comment']

        query = MovieUser.query
        user_movie = query.filter(MovieUser.user_id == user_id, \
                                            MovieUser.movie_title == movie_title).first()
        if user_movie:
            response = jsonify({'message':'You have commented and rated this moive','category':'warning'})
            return response, 409
        else:
            new_cr = MovieUser(user_id=user_id, \
                               movie_title = movie_title, \
                               rating=rating, \
                               comment = comment)
            db.session.add(new_cr)
            db.session.commit()
            response = jsonify({'message':'Comment Post Successfully','category':'success'})
            return response

    def put(self):
        user_id = request.form['user_id']
        movie_title = request.form['movie_title']
        rating = request.form['rating']
        comment = request.form['comment']

        query = MovieUser.query
        user_movie = query.filter(MovieUser.user_id == user_id, MovieUser.movie_title == movie_title).first()
        if user_movie:
            #new_cr = MovieUser(user_id=user_id, movie_title=movie_title, rating=rating, comment=comment)
            #db.session.add(new_cr)
            user_movie.rating = rating
            user_movie.comment = comment
            db.session.commit()
            response = jsonify({'message': 'Comment Modified Successfully', 'category': 'success'})
            return response
        else:
            response = jsonify({'message': 'Your Movie NOT found', 'category': 'warning'})
            return response,404






film_view = FilmApi.as_view('film_api')
register_view = RegisterApi.as_view('register_api')
login_view = LoginApi.as_view('login_api')
rate_view = RatingApi.as_view(('rate_api'))
app.add_url_rule('/films', view_func=film_view, methods=['GET', ])
app.add_url_rule('/register', view_func=register_view, methods=['POST'])
app.add_url_rule('/login', view_func=login_view, methods=['POST'])
app.add_url_rule('/rates', view_func=rate_view, methods=['PUT','POST'])


if __name__ == '__main__':
    app.run(host=conf.HOST, port=conf.PORT, debug=True)
