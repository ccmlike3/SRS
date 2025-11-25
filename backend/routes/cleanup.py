from datetime import datetime
from extensions import db
from models.reservation import Reservation
from models.seat import Seat

TIME_FORMAT = "%Y-%m-%d %H:%M"

def expire_old_reservations():
    """끝난 예약들을 찾아서 status를 'expired'로 바꾸고 좌석을 비워준다."""
    now = datetime.now()
    active = Reservation.query.filter_by(status='reserved').all()

    changed = False
    for r in active:
        try:
            end_dt = datetime.strptime(r.end_time, TIME_FORMAT)
        except ValueError:
            continue

        if end_dt <= now:
            r.status = 'expired'
            seat = Seat.query.get(r.seat_id)
            if seat and seat.status == 'reserved':
                seat.status = 'available'
            changed = True

    if changed:
        db.session.commit()
