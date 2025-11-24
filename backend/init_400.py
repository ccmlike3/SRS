# backend/init_seats_400.py

from app import app
from extensions import db
from models.seat import Seat

with app.app_context():
    print("⚠ 기존 좌석 데이터를 삭제하지 않고, 부족한 번호만 채웁니다.")
    
    created = 0
    for i in range(1, 401):
        if not Seat.query.get(i):
            db.session.add(Seat(id=i, status="available"))
            created += 1

    db.session.commit()

    print(f"✅ 좌석 생성 완료: {created}개 생성됨 (1~400 중 기존에 없던 좌석만 생성)")
