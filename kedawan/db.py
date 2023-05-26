from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func
from sqlalchemy.dialects.mysql import VARBINARY

db = SQLAlchemy()

class FastLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Text, nullable=False, unique=True)
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
    id = db.Column(db.Integer, primary_key=True)
    fast_links_id = db.Column(db.Integer, db.ForeignKey('fast_links.id'), nullable=False)
    ip_address_id = db.Column(db.Integer, db.ForeignKey('ip_address_log.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)

    fast_links = db.relationship('FastLinks', backref=db.backref('visitors', cascade='all, delete-orphan'))
    ip_address = db.relationship('IPAddressLog', backref=db.backref('visitors', cascade='all, delete-orphan'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "fast_links_id": self.fast_links_id,
            "ip_address_id": self.ip_address_id,
        }

    def __repr__(self):
        return f'<Visitor {self.fast_links_id}>'

class IPAddressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(VARBINARY(16), nullable=False, unique=True)
    country_code = db.Column(db.String(2), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "ip_address": str(func.inet6_ntoa(self.ip_address)),
            "country_code": self.country_code,
        }

    def __repr__(self):
        return f'<IPAddressLog {str(func.inet6_ntoa(self.ip_address))}>'
