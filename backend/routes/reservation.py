from flask import Blueprint, jsonify
from models.reservation import Reservation
from .cleanup import expire_old_reservations  # 🔹 추가

bp = Blueprint('reservation', __name__)

@bp.route('/api/user/<int:user_id>/reservations', methods=['GET'])
def get_user_reservations(user_id):
    # ✅ 조회 전에 먼저 지난 예약들을 정리
    expire_old_reservations()

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "seat_id": r.seat_id,
            "start_time": r.start_time,
            "end_time": r.end_time,
            "status": r.status
        })

    return jsonify(result)
