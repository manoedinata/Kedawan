from flask import Blueprint

from flask_restful import Api
from flask_restful import Resource

main_api_bp = Blueprint("main_api", __name__)
main_api = Api(main_api_bp)

class MainAPI(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        return {"message": "Hello, World!"}

main_api.add_resource(MainAPI, "/")
