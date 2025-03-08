from flask import Flask, g
from app.db.database import SessionLocal, engine
from app.db.models import Base

def create_app():
    app = Flask(__name__)

    Base.metadata.create_all(bind=engine)

    @app.before_request
    def create_session():
        g.session = SessionLocal()


    @app.teardown_request
    def remove_session(exception=None):
        session = g.pop('session', None)
        if session is not None:
            session.close()

    from app.endpoints.symbols import symbols_bp
    from app.endpoints.quotes import quotes_bp
    app.register_blueprint(symbols_bp)
    app.register_blueprint(quotes_bp)

    return app