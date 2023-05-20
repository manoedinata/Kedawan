from flask import Blueprint

from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse

from datetime import datetime
from datetime import timedelta
from pytz import timezone

from kedawan.db import db
from kedawan.db import FastLinks
from kedawan.api.utils import generateSlug

fastadd_api_bp = Blueprint("fastadd_api", __name__)
fastadd_api = Api(fastadd_api_bp)

jakartaTz = timezone("Asia/Jakarta") 

class FastAddAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

        super().__init__()

    def get(self):
        fastlinks = FastLinks.query.all()
        return [f.serialize for f in fastlinks]
    
    def post(self):
        self.parser.add_argument("url", type=str, help="Target URL", required=True)
        self.parser.add_argument("slug", type=str, help="Target slug", default=generateSlug(), required=False)
        parser = self.parser.parse_args()
        print(parser)

        currentDate = datetime.now(jakartaTz)
        addedDate = currentDate + timedelta(days=2)

        try:
            fastlinks = FastLinks(
                slug=parser["slug"],
                url=parser["url"],
                created_at=currentDate,
                expire=addedDate
            )

            db.session.add(fastlinks)
            db.session.commit()

            return fastlinks.serialize

        except Exception as e:
            db.session.rollback()

            return {"error": str(e)}

fastadd_api.add_resource(FastAddAPI, "/fastadd")
