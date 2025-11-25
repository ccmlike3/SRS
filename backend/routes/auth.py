from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db

bp = Blueprint('auth', __name__)

@bp.route('/api/login', methods=['POST'])
def login_or_register():
    print("\n==============================")
    print("🔥 /api/login 요청 도착")
    print("==============================")

    try:
        print("📌 요청 헤더 전체:")
        for k, v in request.headers.items():
            print(f"   {k}: {v}")
    except Exception as e:
        print("❌ 헤더 출력 중 오류:", e)

    try:
        auth_header = request.headers.get("Authorization")
        print(f"\n🔎 Authorization 헤더 값: {auth_header}")

        if not auth_header:
            print("❌ Authorization 없음 → 401")
            return jsonify({"error": "Authorization header missing"}), 401

        if not auth_header.startswith("Bearer "):
            print("❌ Authorization 형식 오류 → 401")
            return jsonify({"error": "Authorization header invalid"}), 401

        token = auth_header.split(" ", 1)[1]
        print(f"🔐 토큰 앞부분: {token[:20]}...")
    except Exception as e:
        print("❌ Authorization 처리 중 오류:", e)
        return jsonify({"error": "authorization error"}), 500

    try:
        data = request.get_json()
        print("\n📌 요청 Body(JSON):", data)

        if data is None:
            print("❌ JSON Body 없음 → 400")
            return jsonify({"error": "no json body"}), 400

        email = data.get("email")
        name = data.get("name")
        print(f"🔎 email: {email}, name: {name}")

        if not email:
            print("❌ email 누락 → 400")
            return jsonify({"error": "email is required"}), 400
    except Exception as e:
        print("❌ JSON 파싱 오류:", e)
        return jsonify({"error": "json parse error"}), 500

    try:
        print("\n🔍 DB에서 사용자 검색 중...")
        user = User.query.filter_by(email=email).first()
        print(f"🔎 검색 결과: {user}")
    except Exception as e:
        print("❌ DB 조회 중 오류:", e)
        return jsonify({"error": "database query error"}), 500

    try:
        if not user:
            print("🆕 DB에 사용자 없음 → 새로 생성")
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
            print(f"✅ 새 사용자 생성 완료 → ID={user.id}")
        else:
            print("✅ 기존 사용자 확인 → 로그인 성공")
    except Exception as e:
        print("❌ 사용자 생성/커밋 중 오류:", e)
        return jsonify({"error": "user create error"}), 500

    print("\n🎉 로그인 성공 → 응답 반환 중...")
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name
    })
