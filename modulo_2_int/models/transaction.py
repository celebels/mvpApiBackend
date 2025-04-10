from modulo_2_int.db import db



class TransactionModel(db.Model): #mapping between a row in a table to a python class
    __tablename__ = "transactions"
    
    #storing transactions from accounts to stock, different than accountStock that is a join table
    
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.user_id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.stock_id'), nullable=False)
    type_of_transaction = db.Column(db.String(3), unique=False, nullable=False)
    price_transacion = db.Column(db.Float(), unique=False, nullable=False)
    
  
  #  account = db.relationship("AccountModel", backref="transactions", lazy=True)
  
'''
      {
        "user_id":"3",
        "stock_id":"1",
        "type_of_transaction":"UVC",
        "price_transacion":49.99
    }
  
  '''