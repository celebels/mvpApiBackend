## fetching data üwü ##

import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
import yfinance as yf #finance api



from modulo_2_int.db import db
from modulo_2_int.models import TransactionModel, StockModel
from modulo_2_int.schemas import StockSchema
from modulo_3_ext.fetching_schemas import  FetchingSchema

bp = Blueprint("yfinances", __name__)



#print(stock_amazon.info)




#dolar cotacao -> transaction/user_id/stock_id/convertion_to_dollar 
#preco dos stocks -> stocks/stocks_id/price


@bp.route("/transactions/<int:user_id>/<int:stock_id>/convertions")
class TransactionConvertionDetail(MethodView): #since i just want to fetch and show, not store, no need for model
    @bp.response(200, FetchingSchema ) # need both to do checking TransactionSchema, StockSchema
    def get(self, user_id,stock_id):
        stocks = StockModel.query.filter_by(stock_id = stock_id).first_or_404() 
        transactions = TransactionModel.query.filter_by(user_id=user_id, stock_id=stock_id).first_or_404()
        
        
        try:
            ticker = yf.Ticker(stocks.stock_symbol)
            if ticker.info["currency"] != "USD":
                abort(400, message=f"Stock currency not supported or missing for {stocks.stock_symbol}.")
            if ticker.info["currency"] == "USD":
                rate = yf.Ticker("USDBRL=X").info["regularMarketPrice"] ##convertendo para real
                price = yf.Ticker(stocks.stock_symbol).info.get("regularMarketPrice")
                fetched_data = {
                    "user_id": user_id,
                    "stock_id": stock_id,
                    "stock_symbol" : stocks.stock_symbol,
                    "stock_price" : price,
                    "converted_value" : transactions.price_transacion * rate
                }
            return fetched_data
        except Exception as e:
            abort(500,message=f"error fetching financial data:{str(e)}")
       
        
@bp.route("/stocks/<int:stock_id>/price") #fetching price in real time, no need to store it
class AccountConvertionDetail(MethodView): 
    @bp.response(200, StockSchema ) 
    def get(self, stock_id):
        stocks = StockModel.query.filter_by(stock_id = stock_id).first_or_404() 
        ticker = yf.Ticker(stocks.stock_symbol)
        #stocks.stock_price = ticker.info["regularMarketPrice"]
        return {
            "stock_id":stocks.stock_id,
            "stock_symbol":stocks.stock_symbol,
            "sector":stocks.sector,
            "stock_price":ticker.info["regularMarketPrice"]
        }
        
        
        
              
        
            
  