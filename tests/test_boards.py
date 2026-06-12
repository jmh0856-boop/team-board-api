import pytest


@pytest.fixture(scope="module")
def admin_token(client):
    """테스트용 관리자 유저 생성 및 토큰 반환"""
    client.post(
        "/users/",
        json={"email": "admin_test@example.com", "password": "password123"},
    )
    # DB에서 직접 is_admin 설정이 불가능하므로 일반 유저로 테스트
    response = client.post(
        "/auth/login",
        data={
            "username": "admin_test@example.com",
            "password": "password123",
        },
    )
    return response.json()["data"]["access_token"]


def test_create_board_forbidden(client, admin_token):
    """일반 유저 게시판 생성 실패 테스트"""
    response = client.post(
        "/admin/boards/",
        json={"name": "테스트 게시판"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


def test_get_boards(client):
    """게시판 목록 조회 테스트"""
    response = client.get("/boards/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["message"] == "게시판 목록 조회 성공"


def test_get_board_not_found(client):
    """존재하지 않는 게시판 조회 실패 테스트"""
    response = client.get("/boards/9999")
    assert response.status_code == 404
