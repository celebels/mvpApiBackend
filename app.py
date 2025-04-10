import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from modulo_2_int.resources.account import bp as AccountBlueprint
from modulo_2_int.resources.stock import bp as StockBlueprint
from modulo_2_int.resources.transaction import bp as TransactionBlueprint
from modulo_2_int.resources.account_stocks import blp as AccountStocksBlueprint

from modulo_3_ext.resources.fetching_data import bp as FetchingBlueprint #fetching

from modulo_2_int.db import db
from flask_jwt_extended import JWTManager


import modulo_2_int.models




def create_app(db_url = None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db") #stores in server instead of code
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)




    api = Api(app) # connect flasksmoresxt ext to the app
    app.config["JWT_SECRET_KEY"] = "isabel"
    with app.app_context():
        db.create_all() #create table as first thing to do
        


    api.register_blueprint(AccountBlueprint)
    api.register_blueprint(StockBlueprint)
    api.register_blueprint(TransactionBlueprint)
    api.register_blueprint(AccountStocksBlueprint)
    api.register_blueprint(FetchingBlueprint)
    
    return app