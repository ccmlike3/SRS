from .seats import bp as seats_bp
from .reserve import bp as reserve_bp
from .reservation import bp as reservation_bp
from .cancel import bp as cancel_bp
from .auth import bp as auth_bp

def register_routes(app):
    print("🔗 register_routes() 함수 진입")
    app.register_blueprint(seats_bp)
    app.register_blueprint(reserve_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(cancel_bp)
    app.register_blueprint(auth_bp)
    print("✅ seats_bp 등록 완료")
