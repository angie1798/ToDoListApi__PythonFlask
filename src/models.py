from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), unique=True, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.label

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done
            # do not serialize the password, its a security breach
        }
