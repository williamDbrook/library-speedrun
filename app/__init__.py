from flask import Flask
from app.models import User

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'your-secret-key-change-this'
    
    from app.routes import auth_bp, library_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(admin_bp)
    
    # Add helper function to templates
    @app.context_processor
    def inject_user():
        def get_user(username):
            return User.find_by_username(username)
        return dict(get_user=get_user)
    
    return app
