from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(40), unique=True)
    fname = db.Column(db.String(16))
    lname = db.Column(db.String(20))
    password_hash = db.Column(db.String(64))
    wallet_funds = db.Column(db.Float())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, email, fname, lname, password):
        user = User(username=username, email=email, fname=fname, lname=lname)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user

    # debugging string
    def __repr__(self):
        return '<User {0} {1} {2}>'.format(self.username, self.fname, self.lname)

class Stocks(db.Model):
    __tablename__ = 'stocklist'
    ticker = db.Column(db.String, primary_key=True)
    companyName = db.Column(db.String)
    sector = db.Column(db.String)
    description = db.Column(db.String)
    address = db.Column(db.String)
    assetType = db.Column(db.String)

class BrentOil(db.Model):
    __tablename__ = 'BrentOil'
    CommodityName = db.Column(db.String, primary_key=True)
    Unit = db.Column(db.String)
    Price =  db.Column(db.Float)
    time = db.Column(db.DateTime)

class Copper(db.Model):
    __tablename__ = 'Copper'
    CommodityName = db.Column(db.String, primary_key=True)
    Unit = db.Column(db.String)
    Price =  db.Column(db.Float)
    time = db.Column(db.DateTime)

class Coffee(db.Model):
    __tablename__ = 'Coffee'
    CommodityName = db.Column(db.String, primary_key=True)
    Unit = db.Column(db.String)
    Price =  db.Column(db.Float)
    time = db.Column(db.DateTime)

class TopGainers(db.Model):
    __tablename__ = 'TopGainers'
    ticker = db.Column(db.String, ForeignKey("stocklist.ticker"), primary_key=True)
    price = db.Column(db.Float)
    changeAmount = db.Column(db.Float)
    changePercentage = db.Column(db.Float)
    volume = db.Column(db.Float)

class TopLosers(db.Model):
    __tablename__ = 'TopLosers'
    ticker = db.Column(db.String, ForeignKey("stocklist.ticker"), primary_key=True)
    price = db.Column(db.Float)
    changeAmount = db.Column(db.Float)
    changePercentage = db.Column(db.Float)
    volume = db.Column(db.Float)

class Intraday(db.Model):
    __tablename__ = 'intraday'
    ticker = db.Column(db.String, ForeignKey("stocklist.ticker"), primary_key=True)
    interval = db.Column(db.String, primary_key=True)
    time = db.Column(db.DateTime)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    adjClose = db.Column(db.Float)
    volume = db.Column(db.Float)

class DailyAdj(db.Model):
    __tablename__ = 'DailyAdj'
    ticker = db.Column(db.String, ForeignKey("stocklist.ticker"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    adjClose = db.Column(db.Float)
    volume = db.Column(db.Float)

class MonthlyAdj(db.Model):
    __tablename__ = 'MonthlyAdj'
    ticker = db.Column(db.String, ForeignKey("stocklist.ticker"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    adjClose = db.Column(db.Float)
    volume = db.Column(db.Float)

class Settings(db.Model):
    __tablename__ = 'settings'
    userID = db.Column(db.Integer, ForeignKey("user.id"), primary_key=True)
    profilePic = db.Column(db.String)
    colourSchemeID = db.Column(db.Integer)
    font = db.Column(db.String)
    
class OrderType(db.Model):
    __tablename__ = 'ordertype'
    orderTypeID = db.Column(db.Integer, primary_key=True)
    orderType = db.Column(db.String)

class PurchaseHistory(db.Model):
    __tablename__ = 'purchasehistory'
    orderID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, ForeignKey("user.id"))
    stockID = db.Column(db.Integer, ForeignKey("stocklist.ticker"))
    orderTypeID = db.Column(db.Integer, ForeignKey("ordertype.orderTypeID"))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)

with app.app_context():
    db.create_all()