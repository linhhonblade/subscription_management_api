from . import db

class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())