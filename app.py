import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load movie data and similarity matrix
movies = pickle.load(open("./movie_list.pkl", 'rb'))
similarity = pickle.load(open('./similarity.pkl', 'rb'))

def recommend(movie):
    if movie not in movies['title'].values:
        return None  # Movie not found
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie_name = data.get('movie_name')
    if not movie_name:
        return jsonify({"error": "No movie name provided"}), 400

    recommended_names = recommend(movie_name)
    if recommended_names is None:
        return jsonify({"error": "Movie not found"}), 404

    response = {
        "recommended_movies": recommended_names,
    }
    return jsonify(response)

# This is required to run the app on Vercel
if __name__ == '__main__':
    app.run()
