import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

import traceback 


from modulo_2_int.db import db
from modulo_2_int.models import StockModel
from modulo_2_int.schemas import StockSchema


bp = Blueprint("stocks", __name__,description="operations in stock")

@bp.route("/stocks/<int:stock_id>") #get and put specific stock no account
class StockDetail(MethodView):
    @bp.response(200, StockSchema)
    def get(self, stock_id):
        stock = StockModel.query.get_or_404(stock_id)
        return stock
    def delete(self, stock_id):
        stock = StockModel.query.get_or_404(stock_id)
        db.session.delete(stock)
        db.session.commit()
        return {"message": f"Stock with ID {stock_id} deleted."}, 200
            
            
  
            
   
@bp.route("/stocks") #get all stocks
class StockList(MethodView):
    @bp.response(200, StockSchema(many=True))
    def get(self):
        return StockModel.query.all()
    
    @bp.arguments( StockSchema) #gives a validation dictionary
    @bp.response(201, StockSchema)
    def post(self, stock_data):
        stock = StockModel(**stock_data)
        
        try:
            db.session.add(stock)
            db.session.commit() # save in db
        except SQLAlchemyError:
            traceback.print_exc()
            abort(500, message="error whilst inserting new stock")
            
        return stock
        
    