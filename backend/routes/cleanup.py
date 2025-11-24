# backend/routes/cleanup.py
from datetime import datetime
from extensions import db
from models.reservation import Reservation
from models.seat import Seat

TIME_FORMAT = "%Y-%m-%d %H:%M"  # 프론트에서 넘어오는 문자열 형식

def expire_old_reservations():
    """끝난 예약들을 찾아서 status를 'expired'로 바꾸고 좌석을 비워준다."""
    now = datetime.now()
    # 아직 'reserved' 상태인 예약들만 조회
    active = Reservation.query.filter_by(status='reserved').all()

    changed = False
    for r in active:
        try:
            end_dt = datetime.strptime(r.end_time, TIME_FORMAT)
        except ValueError:
            # 혹시 형식이 깨진 데이터가 있으면 그냥 건너뜀
            continue

        # 종료 시간이 현재 시각보다 과거이면 만료 처리
        if end_dt <= now:
            r.status = 'expired'
            # 해당 좌석을 다시 available로 돌려줌
            seat = Seat.query.get(r.seat_id)
            if seat and seat.status == 'reserved':
                seat.status = 'available'
            changed = True

    if changed:
        db.session.commit()
