import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort


from modulo_2_int.db import db
from modulo_2_int.models import StockModel, AccountModel, AccountStocksModel
from modulo_2_int.schemas import AccountStocksSchema


blp = Blueprint("account_stocks", "account_stocks", description="operations on the join table")

@blp.route("/accounts/<string:user_id>/stocks/<string:stock_id>") 
#specific stocks based on specific user oh god why 
class AccountStocks(MethodView):
    @blp.response(200, AccountStocksSchema)
    def post(self, user_id, stock_id):
        print(f"Received request to add stock {stock_id} to account {user_id}")  # Debugging
        stock = StockModel.query.get_or_404(stock_id)
        account = AccountModel.query.get_or_404(user_id)
        
        account.stocks.append(stock)
        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error occured whilst inserting new stock into user")
            
        return stock
        
    def delete(self, user_id, stock_id):
        stock = StockModel.query.get_or_404(stock_id)
        account = AccountModel.query.get_or_404(user_id)
        
        account.stocks.remove(stock)
        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error occured whilst deleting new stock into user")
            
        return {"message":"stock deleted from account"}
            
    def get(self,  user_id):
        account = AccountModel.query.get_or_404(user_id)
        return account.stocks