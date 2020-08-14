from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User, Coupon, Restaurant, Employee, Achievements

# The way of deploying it to host comes from
# https://www.youtube.com/watch?v=pmRT8QQLIqk

# The way to connect to PostgreSQL comes from
# https://www.youtube.com/watch?v=FKy21FnjKS0

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
