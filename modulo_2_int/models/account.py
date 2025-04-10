from modulo_2_int.db import db


class AccountModel(db.Model): #mapping between a row in a table to a python class
    __tablename__ = "accounts"
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_full_name = db.Column(db.String(90), unique=True, nullable=False)
    type_of_account = db.Column(db.String(3), unique=False, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)


    transactions = db.relationship("TransactionModel", backref="account", lazy=True)
    stocks = db.relationship("StockModel", back_populates="accounts",secondary="account_stocks")
    
    
    
    
    
    '''
    
    {
        "user_full_name":"julien solomita",
        "type_of_account":"SAV",
        "amount":19.99
    }
    
    '''