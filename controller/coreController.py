from flask import Blueprint, render_template

class CoreController:
    def cbRecommendation(title, movies_df, cosine_sim_matrix, titleToIndex, top_n=5):
        if title not in titleToIndex:
            return f"Movie '{title}' not found in the dataset."

        idx = titleToIndex[title]
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))

        # Sort by similarity score in descending order, accessing the scalar value
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Skip the first movie (itself) and get top_n results
        sim_scores = sim_scores[1:top_n+1]

        movie_indices = [i[0] for i in sim_scores]
        similarity_scores = [i[1] for i in sim_scores]

        recommendations = pd.DataFrame({
            'Title': movies_df['title'].iloc[movie_indices].values,
            'Similarity Score': similarity_scores,
            'Genre': movies_df['genre_string'].iloc[movie_indices].values
        })

        return recommendations.reset_index(drop=True)