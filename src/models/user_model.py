from src.databases.conection import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'token': self.token
        }