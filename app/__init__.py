# from flask import Flask
# from app.config import Config
# from app.database import db, migrate
# from flask_mail import Mail
# from app.auth.routes import auth_bp

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     Mail(app)
    
#     # Register blueprints
#     app.register_blueprint(auth_bp)
    
#     return app