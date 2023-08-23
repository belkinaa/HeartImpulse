from heart_imp_app import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.TEXT, unique=True, nullable=False)


    def __repr__(self):
        return f"{self.__tablename__}: {self.id},{self.email},{self.pulse}"

class UsersPulse(db.Model):
    __tablename__ = "users_pulse"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'))
    pulse = db.Column(db.INTEGER, unique=False, nullable=False)
    date = db.Column(db.TIMESTAMP, unique=False, nullable=False)

    def __repr__(self):
        return f"{self.__tablename__}: {self.date},{self.pulse}"