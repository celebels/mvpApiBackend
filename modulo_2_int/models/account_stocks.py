
from modulo_2_int.db import db

##pure secondary table that has both IDs ##

class AccountStocksModel(db.Model):
    __tablename__="account_stocks"
    id=db.Column(db.Integer, primary_key = True)    
    user_id = db.Column(db.Integer, db.ForeignKey("accounts.user_id"))
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.stock_id"))
    
