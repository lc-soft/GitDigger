from flask_restful import fields

voter_fields = {
    'id': fields.Integer,
    'value': fields.Integer,
    'target_id': fields.Integer,
    'target_type': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.DateTime('iso8601')
}
topic_fields = {
    'id': fields.Integer,
    'group': fields.String,
    'description': fields.String,
    'issues_count': fields.Integer,
    'followers_count': fields.Integer,
    'repositories_count': fields.Integer
}
