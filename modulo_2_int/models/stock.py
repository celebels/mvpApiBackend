from modulo_2_int.db import db


class StockModel(db.Model): #mapping between a row in a table to a python class
    __tablename__ ="stocks"
    stock_id = db.Column(db.Integer,  primary_key=True, nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False, unique=False) # TSLA, GOOGL etc
   
    sector = db.Column(db.String(),  nullable=False) ## carS or tech etc
     
    accounts = db.relationship("AccountModel", back_populates="stocks",secondary="account_stocks")
    
    '''
  {
        "stock_symbol": "TSLA",
        "sector" : "automotive"
    }
    '''