import pytest


@pytest.fixture(scope="module")
def auth_token(client):
    """테스트용 유저 생성 및 토큰 반환"""
    client.post(
        "/users/",
        json={"email": "tag_test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "tag_test@example.com", "password": "password123"},
    )
    return response.json()["data"]["access_token"]


@pytest.fixture(scope="module")
def post_id(client, auth_token):
    """테스트용 게시글 생성 및 id 반환"""
    response = client.post(
        "/posts/",
        json={"title": "태그 테스트 게시글", "content": "내용", "tag_names": ["태그1"]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()["data"]["id"]


def test_create_post_with_tags(client, auth_token):
    """게시글 생성 시 태그 등록 테스트"""
    response = client.post(
        "/posts/",
        json={
            "title": "태그 포함 게시글",
            "content": "내용",
            "tag_names": ["테스트", "태그"],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["tags"]) == 2


def test_set_post_tags(client, auth_token, post_id):
    """태그 등록 테스트"""
    response = client.post(
        f"/posts/{post_id}/tags/",
        json={"names": ["태그1", "태그2"]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["message"] == "태그 등록 성공"


def test_update_post_tags(client, auth_token, post_id):
    """태그 수정 테스트 (전체 교체)"""
    response = client.patch(
        f"/posts/{post_id}/tags/",
        json={"names": ["새태그"]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "새태그"
    assert data["message"] == "태그 수정 성공"


def test_filter_by_tag(client, post_id):
    """태그 필터링 테스트"""
    response = client.get(
        f"/posts/{post_id}/tags/filter?tag_name=새태그",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["message"] == "태그 필터링 성공"


def test_filter_by_nonexistent_tag(client, post_id):
    """존재하지 않는 태그 필터링 실패 테스트"""
    response = client.get(
        f"/posts/{post_id}/tags/filter?tag_name=없는태그",
    )
    assert response.status_code == 404
