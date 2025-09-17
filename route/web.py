from controller import HomeController
from controller import CoreController
core_controller = CoreController()
home_controller = HomeController()

def setupRoute(app):
    app.add_url_rule('/',             endpoint='home',         view_func=home_controller.index,        methods=['GET'])
    app.add_url_rule('/search',      endpoint='search',       view_func=core_controller.search,       methods=['POST'])
    