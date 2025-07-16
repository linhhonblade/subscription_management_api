from flask import Flask
from routers.v1 import blueprints as v1_blueprints
from routers.v1 import prefix as v1_prefix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
from models.base import db
db.init_app(app)
with app.app_context():
    db.create_all()

# Init blueprints
for bp in v1_blueprints:
    app.register_blueprint(bp, url_prefix=f"{v1_prefix}{bp.url_prefix}")


if __name__ == '__main__':
    app.run(debug=True)
