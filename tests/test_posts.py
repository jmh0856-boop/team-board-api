import pytest


@pytest.fixture(scope="module")
def auth_token(client):
    """테스트용 유저 생성 및 토큰 반환"""
    client.post(
        "/users/",
        json={"email": "post_test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "post_test@example.com", "password": "password123"},
    )
    return response.json()["data"]["access_token"]


def test_create_post(client, auth_token):
    """게시글 생성 성공 테스트"""
    response = client.post(
        "/posts/",
        json={"title": "테스트 제목", "content": "테스트 내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "테스트 제목"
    assert data["data"]["content"] == "테스트 내용"
    assert data["message"] == "게시글 생성 성공"


def test_create_post_unauthorized(client):
    """비로그인 게시글 생성 실패 테스트"""
    response = client.post(
        "/posts/",
        json={"title": "테스트 제목", "content": "테스트 내용"},
    )
    assert response.status_code == 401


def test_get_posts(client):
    """게시글 목록 조회 테스트"""
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["message"] == "게시글 목록 조회 성공"


def test_get_post_detail(client, auth_token):
    """게시글 상세 조회 테스트"""
    create_response = client.post(
        "/posts/",
        json={"title": "상세 조회 테스트", "content": "내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    post_id = create_response.json()["data"]["post_id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["post_id"] == post_id
    assert data["data"]["view_count"] == 1


def test_update_post(client, auth_token):
    """게시글 수정 성공 테스트"""
    create_response = client.post(
        "/posts/",
        json={"title": "수정 전 제목", "content": "수정 전 내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    post_id = create_response.json()["data"]["post_id"]

    response = client.patch(
        f"/posts/{post_id}",
        json={"title": "수정 후 제목"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == "수정 후 제목"
    assert data["data"]["content"] == "수정 전 내용"


def test_delete_post(client, auth_token):
    """게시글 삭제 성공 테스트"""
    create_response = client.post(
        "/posts/",
        json={"title": "삭제 테스트", "content": "내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    post_id = create_response.json()["data"]["post_id"]

    response = client.delete(
        f"/posts/{post_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "게시글 삭제 성공"


def test_delete_post_forbidden(client, auth_token):
    """다른 유저 게시글 삭제 실패 테스트"""
    create_response = client.post(
        "/posts/",
        json={"title": "권한 테스트", "content": "내용"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    post_id = create_response.json()["data"]["post_id"]

    # 다른 유저 생성 및 토큰 발급
    client.post(
        "/users/",
        json={"email": "other@example.com", "password": "password123"},
    )
    other_token = client.post(
        "/auth/login",
        data={"username": "other@example.com", "password": "password123"},
    ).json()["data"]["access_token"]

    response = client.delete(
        f"/posts/{post_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403


def test_get_posts_pagination(client):
    """게시글 목록 페이지네이션 테스트"""
    response = client.get("/posts/?page=1&size=3")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) <= 3
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "total_pages" in data


def test_search_posts_by_keyword(client):
    """게시글 키워드 검색 테스트"""
    response = client.get("/posts/?keyword=테스트")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_search_posts_no_result(client):
    """존재하지 않는 키워드 검색 테스트"""
    response = client.get("/posts/?keyword=없는게시글12345")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 0
    assert data["total"] == 0
