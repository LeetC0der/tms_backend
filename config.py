import os


class Config:
    SECRET_KEY = 'be984bf2-5050-426d-a998-5ebbf46e8cd4'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sagpenty@localhost/TMS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
