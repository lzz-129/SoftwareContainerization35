from flask import Flask
import pandas as pd

from utils import db


app = Flask(__name__)

# sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # 关联 db 对象与 Flask 应用
# TODO: data validation
movie = pd.read_csv('/static/movie_metadata.csv')
movie.to_sql('movies', db.engine, if_exists='replace', index=False)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
