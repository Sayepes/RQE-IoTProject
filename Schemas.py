from marshmallow import Schema, fields, validate

class ReadingSchemaPost(Schema):
    collection_id = fields.String(required=True)
    time = fields.DateTime(required=True)
    temp = fields.Double(required=True)
    humi = fields.Double(required=True)
    lumi = fields.Double(required=True)



