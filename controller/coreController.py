from flask import render_template, request
from fuzzywuzzy import process
from initiar import cbRecommendation, movies

class CoreController:
    def __init__(self):
        self.movies_df = movies  # Assume DataFrame with 'title' column

    def search(self):
        if request.method == "POST":
            movie_query = request.form.get("query")
            all_titles = self.movies_df['title'].tolist()

            # Find close matches using fuzzy search
            close_matches = process.extract(movie_query, all_titles, limit=5)
            best_match_title = close_matches[0][0] if close_matches else None

            # Whether it's an exact match or not, get recommendations using the best match
            if best_match_title:
                recommendations_df = cbRecommendation(best_match_title, self.movies_df, top_n=5)
                recommendations = recommendations_df.to_dict(orient='records')
            else:
                recommendations = []

            return render_template(
                "search.html",
                movieName=movie_query,
                matchedName=best_match_title if movie_query != best_match_title else None,
                recommendations=recommendations
            )

        # GET request fallback
        return render_template("search.html", movieName=None, matchedName=None, recommendations=[])
