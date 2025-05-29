from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# Database Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Request parser for input validation
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# Output formatting
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# Resource class
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    class User(Resource):
        @marshal_with(user_fields)
        def get(self ,id):
            user = UserModel.query.filter_by(id = id).first()
            if not user:
                abort(404,"user not found")
                return user
        @marshal_with(user_fields)
        def patch(self ,id):
            args =user_args.parse_args()
            user = UserModel.query.filter_by(id = id).first()
            if not user:
                abort(404,"user not found")
                user.name = args["name"]
                user.email =args["email"]
                db.session.commit

                return user   
        @marshal_with(user_fields)
        def delete(self ,id):
           
            user = UserModel.query.filter_by(id = id).first()
            if not user:
                abort(404,"user not found")
                db.session.delete(user)
                db.session.commit()
                users =UserModel.query.all()
                return users ,204

# Register the resource
api.add_resource(user, '/api/users/')
api.add_resource(user,'/api/users/<int:id>')
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(debug=True)
