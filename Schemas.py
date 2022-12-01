from marshmallow import Schema, fields, validate

class ReadingSchemaPost(Schema):
    collection_id = fields.String(required=True)
    time = fields.DateTime(required=True)
    temp = fields.Float(required=True)
    humi = fields.Float(required=True)
    lumi = fields.Float(required=True)



