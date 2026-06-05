import pytest


@pytest.fixture(scope="module")
def auth_token(client):
    """테스트용 유저 생성 및 토큰 반환"""
    client.post(
        "/users/",
        json={"email": "popular_test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "popular_test@example.com",
            "password": "password123",
        },
    )
    return response.json()["data"]["access_token"]


@pytest.fixture(scope="module")
def post_id(client, auth_token):
    """테스트용 게시글 생성 및 id 반환"""
    response = client.post(
        "/posts/",
        json={"title": "인기글 테스트", "content": "내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()["data"]["id"]


def test_popular_by_views(client):
    """조회수 기준 인기글 조회 테스트"""
    response = client.get("/posts/popular?type=views&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["message"] == "인기글 조회 성공"


def test_popular_by_likes(client, auth_token, post_id):
    """좋아요 기준 인기글 조회 테스트"""
    # 좋아요 추가
    client.post(
        f"/posts/{post_id}/like",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.get("/posts/popular?type=likes&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1
    assert data["message"] == "인기글 조회 성공"


def test_popular_default_type(client):
    """기본 type(views) 인기글 조회 테스트"""
    response = client.get("/posts/popular")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "인기글 조회 성공"


def test_popular_with_limit(client):
    """limit 파라미터 테스트"""
    response = client.get("/posts/popular?type=views&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) <= 3
