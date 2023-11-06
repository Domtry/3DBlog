from typing import Any

from flask import Blueprint, jsonify, request
from apifairy import body, response

from .schemas import Model3dSchema, ArrayModel3dSchema
from ...composers import Model3dComposer

model_3d_bp = Blueprint('Model3Ds', __name__, url_prefix = '/api/v1/model3ds')
create_schema = Model3dSchema()
array_schema = ArrayModel3dSchema()


@model_3d_bp.post('')
@body(create_schema)
@response(create_schema, status_code = 200)
def register(query_body: Model3dSchema):
    r = Model3dComposer.save(request, params = {})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status


@model_3d_bp.get('/<string:model_3d_id>')
@response(create_schema, status_code = 200)
def get_model_3d(model_3d_id: str):
    r = Model3dComposer.get(request, {"model_3d_id": model_3d_id})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status


@model_3d_bp.get('/<int:skip>/<int:limit>')
@response(array_schema, status_code = 200)
def get_model_3d_by_pagination(skip: int, limit: int):
    r = Model3dComposer.pagination(request, {"skip": skip, "limit": limit})
    return jsonify({
        "data": r.data,
        "message": r.message,
        "success": r.success}
    ), r.code_status
