class Config():
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='verysecret'
    SESSION_TYPE='filesystem'