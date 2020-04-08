from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Horoscope(db.Model):
    """Model for the horoscope table"""
    __tablename__ = 'horoscope'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    text = db.Column(db.String(255))
    sign = db.Column(db.String(50))
    download_date = db.Column(db.DateTime)

    def __init__(self, text, sign, download_date):
        self.text = text
        self.sign = sign
        self.download_date = download_date