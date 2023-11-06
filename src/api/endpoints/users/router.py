from flask import Blueprint, jsonify, request
from apifairy import body, response

from .schemas import UserSchema, ArrayUserScheme
from ...composers import UserComposer

users_bp = Blueprint('Users', __name__, url_prefix = '/api/v1/users')
create_schema = UserSchema()
array_schema = ArrayUserScheme()


@users_bp.post('')
@body(create_schema)
@response(create_schema, status_code = 200)
def register(query_body: UserSchema):
    r = UserComposer.save(request, params = {})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status


@users_bp.get('/<string:user_id>')
@response(create_schema, status_code = 200)
def get_user(user_id: str):
    r = UserComposer.get(request, {"user_id": user_id})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status


@users_bp.get('/<int:skip>/<int:limit>')
@response(array_schema, status_code = 200)
def get_users_by_pagination(skip: int, limit: int):
    r = UserComposer.pagination(request, {"skip": skip, "limit": limit})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status
