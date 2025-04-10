from marshmallow import Schema, fields

##plain to evade problems of undefined Schemas
class PlainAccountSchema(Schema):
    id=fields.Int(dump_only=True)
    user_full_name = fields.Str(required=True)
    
class PlainStockSchema(Schema):
    id=fields.Int(dump_only=True)
    stock_symbol = fields.Str(required=True)


#accounts
class AccountSchema(PlainAccountSchema):
    user_id= fields.Str(dump_only = True)
    user_full_name = fields.Str(required = True)
    type_of_account = fields.Str(required = True)
    amount = fields.Float(required=True)
    stocks = fields.List(fields.Nested(PlainStockSchema()), dump_only=True)
    
class UpdateAccountSchema(Schema):
    #äcan change both type of account and amount, but not the name nor id
    type_of_account = fields.Str()
    amount = fields.Float()
    
        
        
#stocks
class StockSchema(PlainStockSchema):
    stock_id= fields.Str(dump_only = True)
    stock_symbol = fields.Str(required = True)
    stock_price = fields.Float()
    sector = fields.Str(required = True)
    accounts = fields.List(fields.Nested(PlainAccountSchema()), dump_only=True)
    
        
        

        
        
        
#transaction join table
class TransactionSchema(Schema):
    transaction_id= fields.Str(dump_only = True)
    user_id=fields.Int(required = True)
    stock_id = fields.Int(required = True)
    type_of_transaction = fields.Str(required = True)
    price_transacion =fields.Float(required = True)
    
class UpdateTransactionSchema(Schema):
    #äcan change both type of account and amount, but not the name nor id
    type_of_transaction = fields.Str()
    price_transacion =fields.Float()
    

#stock_account -> join table
class AccountStocksSchema(Schema):
    account=fields.Nested(AccountSchema)
    stock= fields.Nested(StockSchema)