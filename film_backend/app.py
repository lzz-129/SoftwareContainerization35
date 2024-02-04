from functools import wraps
from urllib.parse import quote_plus
import jwt
import os

from flask import Flask, request, jsonify, g
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

import conf
from utils import db, cors
from models import Movie, Actor, Genre, User, MovieUser
from auth import generate_token, decode_token

app = Flask(__name__)
# Session configuration
app.config['SECRET_KEY'] = conf.SECRET_KEY  # Make sure to set this to a secure key in your conf file

# CORS
cors.init_app(app, supports_credentials=True)  # 允许跨域携带凭证

# sql database


db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_host = 'postgres-service'  # 这里是你的 PostgreSQL 服务的名称
db_name = os.environ.get('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # 关联 db 对象与 Flask 应用

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # try to extract token from hearder
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split()  # 分割"Bearer"和实际的token
            if token_parts[0].lower() == "bearer" and len(token_parts) == 2:
                token = token_parts[1]
            else:
                return jsonify({'message': 'Invalid token header'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            current_user = decode_token(token)
            g.current_user = current_user
            if not isinstance(current_user, str):  # 如果 decode_token 返回的是响应对象
                return current_user  # 返回错误响应
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


class FilmApi(MethodView):
    def get(self):
        # 获取查询参数
        movie_title = request.args.get('movie_title')
        title_year = request.args.get('title_year')
        language = request.args.get('language')
        country = request.args.get('country')
        content_rating = request.args.get('content_rating') # TODO:
        imdb_score_low = request.args.get('imdb_score_low', type=float) # range
        imdb_score_high = request.args.get('imdb_score_high', type=float) # range
        director_name = request.args.get('director_name')
        genre = request.args.get('genre') # TODO:
        actor = request.args.get('actor')
        # 获取分页参数
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        # 获取sort参数
        sort_by = request.args.get('sort_by')
        sort_order = request.args.get('sort_order')

        try:
            query = Movie.query.options(joinedload(Movie.genres), joinedload(Movie.actors)) # basic query
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
            if sort_order:
                if sort_order == 'ascending':
                    query = query.order_by(getattr(Movie, sort_by))
                elif sort_order == 'descending':
                    query = query.order_by(desc(getattr(Movie, sort_by)))

            # execute query and return
            movies = query.offset(offset).limit(limit).all()
            if not movies:
                return jsonify({'status': 'not found',
                                'message': 'No movies found matching the criteria'
                                }), 404
            else:
                total = query.count()
                return jsonify({'status': 'success',
                            'message': 'Search success',
                            'data': [movie.to_dict() for movie in movies],
                            'total': total
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

        if (user_name and password and email):
            # 检查用户名是否已存在
            if query.filter((User.user_name==user_name) | (User.email == email)).first():
                #print('user name has been taken', 'warning')
                response = jsonify({'message': 'User name or email has been taken', 'category': 'warning'})
                return response, 409

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            try:
                new_user = User(user_name=user_name, password=hashed_password, email=email)
                db.session.add(new_user)
                db.session.commit()
                response = jsonify({'message': 'Register Success! Please log in', 'category': 'success'})
                return response, 201 #created successful

            except Exception as e:
                db.session.rollback()
                response = jsonify({'message': 'Register failed due to an error: ' + str(e), 'category': 'danger'})
                return response, 500  # 500 表示服务器内部错误
        else:
            response = jsonify({'message': 'Incomplement message', 'category': 'warning'})
            return response, 400

class LoginApi(MethodView):
    def post(self):
        user_name = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(user_name=user_name).first()

        # 如果用户存在，那么检查密码是否匹配
        if user and check_password_hash(user.password, password):
            token = generate_token(user_name)
            response = jsonify({'message': 'Login Success!', 'token':token,'category': 'success'})
            return response, 200
        else:
            response = jsonify({'message': 'User name or password is wrong', 'category': 'warning'})
            return response, 401

class UserApi(MethodView):
    decorators = [token_required]
    def get(self):
        user_name = request.args.get('username')
        query = User.query
        user = query.filter(User.user_name == user_name).first()

        current_user = g.get('current_user', None)
        if not current_user:
            return jsonify({'message': 'Unauthorized'}), 401

        if user:
            response = jsonify({'message': 'found', 'category': 'success', \
                                'data': user.to_dict()})
            return response, 200
        else:
            response = jsonify({'message': 'not found', 'category': 'warning'})
            return response, 404


class RatingApi(MethodView):
    decorators = [token_required]

    def get(self):
        user_id = request.args.get('user_id')
        movie_title = request.args.get('movie_title')

        query = MovieUser.query
        mv_u = query.filter(MovieUser.user_id == user_id, MovieUser.movie_title == movie_title).first()

        if mv_u:
            data = {'rating':mv_u.rating,'comment': mv_u.comment}
            response = jsonify({'message': 'found', 'category': 'success', \
                                'data': data})
            return response, 200
        else:
            response = jsonify({'message': 'not found', 'category': 'warning'})
            return response, 404



    def post(self):
        #user_id = request.form['user_id']
        current_user = g.get('current_user', None)
        user = User.query.filter(User.user_name == current_user).first()
        user_id = user.user_id
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
            response = jsonify({'message':'Comment Post Successfully','category':'success', 'username':current_user})
            return response,200

    # def put(self):
    #     user_id = request.form['user_id']
    #     movie_title = request.form['movie_title']
    #     rating = request.form['rating']
    #     comment = request.form['comment']
    #
    #     query = MovieUser.query
    #     user_movie = query.filter(MovieUser.user_id == user_id, MovieUser.movie_title == movie_title).first()
    #     if user_movie:
    #         user_movie.rating = rating
    #         user_movie.comment = comment
    #         db.session.commit()
    #         response = jsonify({'message': 'Comment Modified Successfully', 'category': 'success'})
    #         return response
    #     else:
    #         response = jsonify({'message': 'Your Movie NOT found', 'category': 'warning'})
    #         return response,404






film_view = FilmApi.as_view('film_api')
register_view = RegisterApi.as_view('register_api')
login_view = LoginApi.as_view('login_api')
rate_view = RatingApi.as_view('rate_api')
user_view = UserApi.as_view('user_api')
app.add_url_rule('/films', view_func=film_view, methods=['GET', ])
app.add_url_rule('/register', view_func=register_view, methods=['POST'])
app.add_url_rule('/login', view_func=login_view, methods=['POST'])
app.add_url_rule('/rates', view_func=rate_view, methods=['GET','PUT','POST'])
app.add_url_rule('/user', view_func=user_view, methods=['GET'])

if __name__ == '__main__':
    app.run(host=conf.HOST, port=conf.PORT, debug=True)
