from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy.orm import joinedload
from sqlalchemy import desc,text
from urllib.parse import quote_plus


from utils import db, cors
from models import Movie, Actor, Genre


app = Flask(__name__)
app.debug = True

# CORS
cors.init_app(app)

# sql database
db_user = 'db_user'
db_password = quote_plus('user@kube')  # URL encoded
db_host = '127.0.0.1'
db_name = 'kubedb'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # 关联 db 对象与 Flask 应用
# TODO content-rating: 'Not rated' 'Unrated' 不显示； 整合 passed, approved
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

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



film_view = FilmApi.as_view('film_api')
app.add_url_rule('/films', view_func=film_view, methods=['GET', ])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
