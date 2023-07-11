from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate



# Initialize the database
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate=Migrate()
