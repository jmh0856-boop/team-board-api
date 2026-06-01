import pytest


@pytest.fixture(scope="module")
def auth_token(client):
    """테스트용 유저 생성 및 토큰 반환"""
    client.post(
        "/users/",
        json={"email": "comment_test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "comment_test@example.com",
            "password": "password123",
        },
    )
    return response.json()["data"]["access_token"]


@pytest.fixture(scope="module")
def post_id(client, auth_token):
    """테스트용 게시글 생성 및 id 반환"""
    response = client.post(
        "/posts/",
        json={"title": "댓글 테스트 게시글", "content": "내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()["data"]["id"]


def test_create_comment(client, auth_token, post_id):
    """댓글 생성 성공 테스트"""
    response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "테스트 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["content"] == "테스트 댓글"
    assert data["message"] == "댓글 생성 성공"


def test_create_comment_unauthorized(client, post_id):
    """비로그인 댓글 생성 실패 테스트"""
    response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "테스트 댓글"},
    )
    assert response.status_code == 401


def test_get_comments(client, post_id):
    """댓글 목록 조회 테스트"""
    response = client.get(f"/posts/{post_id}/comments/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["message"] == "댓글 목록 조회 성공"


def test_update_comment(client, auth_token, post_id):
    """댓글 수정 성공 테스트"""
    create_response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "수정 전 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    comment_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/posts/{post_id}/comments/{comment_id}",
        json={"content": "수정 후 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["content"] == "수정 후 댓글"
    assert data["message"] == "댓글 수정 성공"


def test_delete_comment(client, auth_token, post_id):
    """댓글 삭제 성공 테스트 (소프트 삭제)"""
    create_response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "삭제 테스트 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    comment_id = create_response.json()["data"]["id"]

    response = client.delete(
        f"/posts/{post_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "댓글 삭제 성공"


def test_create_reply(client, auth_token, post_id):
    """대댓글 생성 성공 테스트"""
    create_response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "부모 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    comment_id = create_response.json()["data"]["id"]

    response = client.post(
        f"/posts/{post_id}/comments/{comment_id}/replies",
        json={"content": "대댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["content"] == "대댓글"
    assert data["data"]["parent_id"] == comment_id
    assert data["message"] == "대댓글 생성 성공"


def test_comment_like(client, auth_token, post_id):
    """댓글 좋아요 테스트"""
    create_response = client.post(
        f"/posts/{post_id}/comments/",
        json={"content": "좋아요 테스트 댓글"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    comment_id = create_response.json()["data"]["id"]

    response = client.post(
        f"/posts/{post_id}/comments/{comment_id}/like",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "좋아요를 눌렀습니다."
