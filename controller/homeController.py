from flask import Blueprint, render_template

class HomeController:
    def __init__(self):
        pass

    def index(self):
        return render_template('home.html')
    
    
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
