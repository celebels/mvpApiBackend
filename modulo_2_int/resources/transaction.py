import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort


from modulo_2_int.db import db
from modulo_2_int.models import TransactionModel
from modulo_2_int.schemas import TransactionSchema, UpdateTransactionSchema

bp = Blueprint("transactions", __name__,description="transactions in accounts X stocks")

@bp.route("/transactions/<int:user_id>/<int:stock_id>")
class TransactionDetail(MethodView):
    @bp.response(200, TransactionSchema)
    def get(self, user_id,stock_id):
        return TransactionModel.query.filter_by(user_id=user_id, stock_id=stock_id).first_or_404()
            
    def delete(self, transaction_id):
        transacation = TransactionModel.query.get_or_404(transaction_id)
        db.session.delete(transacation)
        db.session.commit()
        return {"message":"transacation deleted"}
            
            
    @bp.arguments(UpdateTransactionSchema)
    @bp.response(201,TransactionSchema)
    def put(self,transaction_data, transaction_id):
        transaction = TransactionModel.query.get(transaction_id)
        if transaction:
            transaction.type_of_transaction = transaction_data["type_of_transaction"]
            transaction.price_transacion = transaction_data["price_transacion"]
    
        else:
            transaction = TransactionModel(transaction_id = transaction_id, **transaction_data)
        
        db.session.add(transaction)
        db.session.commit() #commitment is not part of db charcater arc :/
        
        return transaction



@bp.route("/transactions/<int:user_id>")
class TransactionListUser(MethodView):
    @bp.response(200, TransactionSchema(many=True))
    def get(self,user_id):
        return TransactionModel.query.filter_by(user_id=user_id).all()
    
    
  
        
       
       
@bp.route("/transactions")
class TransactionListGeneral(MethodView): 
    @bp.response(200, TransactionSchema(many=True))
    def get(self):
        return TransactionModel.query.all()
    
    @bp.arguments(TransactionSchema) #gives a validation dictionary
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data):
        transaction = TransactionModel(**transaction_data)
        
        try:
            db.session.add(transaction)
            db.session.commit() # save in db
        except SQLAlchemyError:
            abort(500, message="error whilst inserting new transaction")
            
        return transaction