import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort


from modulo_2_int.db import db
from modulo_2_int.models import AccountModel
from modulo_2_int.schemas import AccountSchema, UpdateAccountSchema

bp = Blueprint("accounts", __name__,description="operations in accounts")

@bp.route("/accounts/<string:user_id>")
class AccountDetail(MethodView):
    @bp.response(200, AccountSchema)
    def get(self, user_id):
        account = AccountModel.query.get_or_404(user_id)
        return account
        
    def delete(self, user_id):
       
        account = AccountModel.query.get_or_404(user_id)
        db.session.delete(account)
        db.session.commit()
        return {"message":"account deleted"}
            
            
    @bp.arguments(UpdateAccountSchema)
    @bp.response(201,AccountSchema)
    def put(self,account_data, user_id):
        account = AccountModel.query.get(user_id)
        if account:
            account.type_of_account = account_data["type_of_account"]
            account.amount = account_data["amount"]
        else:
            account = AccountModel(user_id = user_id, **account_data)
        
        db.session.add(account)
        db.session.commit()
        
        return account
            

@bp.route("/accounts")
class AccountList(MethodView):
    @bp.response(200, AccountSchema(many=True))
    def get(self):
        return AccountModel.query.all()
    
    
    @bp.arguments( AccountSchema) #gives a validation dictionary
    @bp.response(201, AccountSchema)
    def post(self, account_data):
        account = AccountModel(**account_data)
        
        try:
            db.session.add(account)
            db.session.commit() # save in db
        except SQLAlchemyError:
            abort(500, message="error whilst inserting new acocunt")
            
        return account
        