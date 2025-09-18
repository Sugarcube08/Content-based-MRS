from flask import render_template, request
from fuzzywuzzy import process, fuzz
from initiar import cbRecommendation, movies  

class CoreController:
    def __init__(self):
        self.movies_df = movies
        self.all_titles = [t.lower() for t in self.movies_df['title'].tolist()]
        genre_strings = self.movies_df['genre_string'].dropna().tolist()
        self.all_genres = list(set(
            g.lower()
            for gs in genre_strings
            for g in gs.split()
        ))

    def search(self):
        if request.method == "POST":
            movie_query = request.form.get("query", "").strip()
            if not movie_query:
                return render_template("search.html", movieName=None, matchedName=None, recommendations=[])

            query_lower = movie_query.lower()
            title_match = process.extractOne(query_lower, self.all_titles, scorer=fuzz.WRatio)
            best_title, title_score = title_match if title_match else (None, 0)
            query_tokens = query_lower.split()
            matched_genres = set()
            for token in query_tokens:
                genre_match = process.extractOne(token, self.all_genres, scorer=fuzz.WRatio)
                if genre_match and genre_match[1] >= 70: 
                    matched_genres.add(genre_match[0])

            recommendations = []
            matched_name = None

            max_genre_score = 100 if matched_genres else 0  
            if best_title and title_score >= 70 and title_score >= max_genre_score:
                original_title = self.movies_df['title'].iloc[self.all_titles.index(best_title)]
                recommendations_df = cbRecommendation(original_title, self.movies_df)
                recommendations = recommendations_df.to_dict(orient='records')
                matched_name = original_title if movie_query.lower() != best_title else None

            elif matched_genres:
                filtered_movies = self.movies_df[
                    self.movies_df['genre_string'].apply(
                        lambda genres: all(genre.lower() in genres.lower() for genre in matched_genres)
                    )
                ]
                recommendations = filtered_movies.to_dict(orient='records')
                matched_name = ', '.join(matched_genres) if len(matched_genres) > 1 else list(matched_genres)[0]

            else:
                matched_name = None
                recommendations = []

            return render_template(
                "search.html",
                movieName=movie_query,
                matchedName=matched_name,
                recommendations=recommendations
            )

        return render_template("search.html", movieName=None, matchedName=None, recommendations=[])
