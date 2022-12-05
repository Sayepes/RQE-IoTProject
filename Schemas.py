from marshmallow import Schema, fields, validate


# Validation Schema for reading Post requests
class ReadingSchemaPost(Schema):
    collection_id = fields.String(required=True)
    temp = fields.Float(required=True)
    humi = fields.Float(required=True)
    lumi = fields.Float(required=True)


# Validation Schema for compare Post
class CompareSchemaPost(Schema):
    temp = fields.Float(required=True)
    humi = fields.Float(required=True)
    lumi = fields.Float(required=True)

