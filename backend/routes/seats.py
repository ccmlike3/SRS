from flask import Blueprint, jsonify
from models.seat import Seat
from .cleanup import expire_old_reservations  # 🔹 추가

bp = Blueprint('seats', __name__)

@bp.route('/api/seats', methods=['GET'])
def get_seats():
    # ✅ 먼저 지난 예약들을 정리
    expire_old_reservations()

    seats = Seat.query.all()
    result = [{"id": seat.id, "status": seat.status} for seat in seats]
    return jsonify(result)
