# app

from flask import Flask, request, jsonify
from flask_restx import Api, Resource

from models import Movie, Director, Genre, db
from schemas import movie_schema, movies_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JSON_SORT_KEYS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}


db.init_app(app)
api = Api(app)
movie_ns = api.namespace('movies')


@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        all_movies = db.session.query(Movie).all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        req = request.json
        new_movie = Movie(**req)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieViews(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            req_json = request.json

            movie.title = req_json.get('title')
            movie.description = req_json.get('description')
            movie.trailer = req_json.get('trailer')
            movie.year = req_json.get('year')
            movie.rating = req_json.get('rating')
            movie.genre_id = req_json.get('genre_id')
            movie.genre = req_json.get('genre')
            movie.director_id = req_json.get('director_id')
            movie.director = req_json.get('director')

            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def patch(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            req_json = request.json

            if 'title' in req_json:
                movie.title = req_json.get('title')
            if 'description' in req_json:
                movie.description = req_json.get('description')
            if 'trailer' in req_json:
                movie.trailer = req_json.get('trailer')
            if 'year' in req_json:
                movie.year = req_json.get('year')
            if 'rating' in req_json:
                movie.rating = req_json.get('rating')
            if 'genre_id' in req_json:
                movie.genre_id = req_json.get('genre_id')
            if 'genre' in req_json:
                movie.genre = req_json.get('genre')
            if 'director_id' in req_json:
                movie.director_id = req_json.get('director_id')
            if 'director' in req_json:
                movie.director = req_json.get('director')

            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, uid: int):
        try:
            book = db.session.query(Movie).get(uid)
            db.session.delete(book)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404


if __name__ == "__main__":
    app.run(debug=True)
