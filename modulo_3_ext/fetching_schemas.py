from marshmallow import Schema, fields
        
        
#stocks
class FetchingSchema(Schema):
    user_id= fields.Int(dump_only = True)
    stock_id= fields.Int(dump_only = True)
    stock_symbol = fields.Str(required = True)
    stock_price = fields.Float(required=True)
    converted_value = fields.Float()
    
        