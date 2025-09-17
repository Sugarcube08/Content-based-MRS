from flask import Blueprint, render_template,request
from initiar import movies
MOVIES_PER_PAGE = 20

class HomeController:
    def __init__(self):
        self.movies = movies.to_dict(orient='records')

    def index(self, page=1):
        all_movies = self.movies
        page = request.args.get('page', 1, type=int)
        perpage = 8
        start = (page - 1) * MOVIES_PER_PAGE
        end = start + MOVIES_PER_PAGE
        paged_movies = self.movies[start:end]

        total_pages = (len(self.movies) + MOVIES_PER_PAGE - 1) // MOVIES_PER_PAGE

        return render_template(
            'home.html',
            movies=paged_movies,
            current_page=page,
            total_pages=total_pages
        )
    
    def create(self):
        pass

    def store(self):
        pass

    def show(self, id):
        pass

    def edit(self, id):
        pass

    def update(self, id):
        pass

    def destroy(self, id):
        pass
