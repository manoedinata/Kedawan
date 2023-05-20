# from pymongo import MongoClient

# from bson import json_util

# def dump_bson(data):
#     return json_util.dumps(data)

# # MongoDB
# mongo = MongoClient("mongodb+srv://manoedinata:0xbnqL9dbA9Emlih@cluster0.bozu48b.mongodb.net/?retryWrites=true&w=majority")

# # DB
# db = mongo.kedawan
# kedawanLinks = db.links

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.mysql import INTEGER

db = SQLAlchemy()

# FastLinks
# class FastLinks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     slug = db.Column(db.Text(10), unique=True, nullable=False)
#     url = db.Column(db.Text(255), nullable=False)
#     visitor = db.Column(db.Integer, default=0)
#     created_at = db.Column(db.DateTime, nullable=False)
#     expire = db.Column(db.DateTime, nullable=False)

#     @property
#     def serialize(self):
#         """Return object data in easily serializable format"""
#         """https://stackoverflow.com/a/7103486"""
#         # TODO: Add serialize property for created_at
#         # and expire
#         return {
#             "id": self.id,
#             "slug": self.slug,
#             "url": self.url,
#         }

#     def __repr__(self):
#         return f'<FastLinks {self.id}>'

class FastLinks(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    slug = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    expire = db.Column(db.DateTime, nullable=False)
    visitor = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        # TODO: Add serialize property for created_at
        # and expire
        return {
            "id": self.id,
            "slug": self.slug,
            "url": self.url,
            "visitor": self.visitor
        }

    def __repr__(self):
        return f'<FastLinks {self.id}>'

class Visitor(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    fast_links_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('fast_links.id'), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)

    fast_links = db.relationship('FastLinks', backref=db.backref('visitors', cascade='all, delete-orphan'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        # TODO: Add serialize property for created_at
        # and expire
        return {
            "id": self.id,
            "fast_links_id": self.fast_links_id,
            "country_code": self.country_code,
        }

    def __repr__(self):
        return f'<Visitor {self.fast_links_id}>'
