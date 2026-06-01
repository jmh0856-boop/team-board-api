def test_create_user(client):
    """회원가입 성공 테스트"""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"
    assert "id" in data["data"]
    assert data["message"] == "회원가입 성공"


def test_create_user_duplicate_email(client):
    """이메일 중복 회원가입 실패 테스트"""
    client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400


def test_login(client):
    """로그인 성공 테스트"""
    client.post(
        "/users/",
        json={"email": "login@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["message"] == "로그인 성공"


def test_login_wrong_password(client):
    """잘못된 비밀번호 로그인 실패 테스트"""
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_refresh_token(client):
    """Refresh Token으로 Access Token 재발급 테스트"""
    client.post(
        "/users/",
        json={"email": "refresh@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "refresh@example.com", "password": "password123"},
    )
    refresh_token = login_response.json()["data"]["refresh_token"]

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["message"] == "토큰 재발급 성공"


def test_refresh_token_invalid(client):
    """유효하지 않은 Refresh Token 테스트"""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token"},
    )
    assert response.status_code == 401
