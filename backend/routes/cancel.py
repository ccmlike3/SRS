from flask import Blueprint, request, jsonify
from models.reservation import Reservation
from models.seat import Seat
from extensions import db

bp = Blueprint('cancel', __name__)

@bp.route('/api/cancel', methods=['POST'])
def cancel_reservation():
    data = request.get_json()
    reservation_id = data.get('reservation_id')

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "해당 예약을 찾을 수 없습니다."}), 404

    if reservation.status == 'cancelled':
        return jsonify({"error": "이미 취소된 예약입니다."}), 400

    reservation.status = 'cancelled'

    seat = Seat.query.get(reservation.seat_id)
    if seat:
        seat.status = 'available'

    db.session.commit()

    return jsonify({"message": "예약이 취소되었습니다."})
