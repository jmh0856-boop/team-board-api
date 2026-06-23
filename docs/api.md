# 팀 공지 게시판 API 명세서

## 프로젝트 정보

| 항목 | 내용 |
|------|------|
| 프로젝트명 | 팀 공지 게시판 API (미니 프로젝트) |
| 기술 스택 | Python 3.12+, FastAPI, SQLite, SQLAlchemy, PyJWT, passlib |
| 담당자 | BE_17_정명호 |
| 개발 방식 | GitHub 조직 레포지토리 협업 (Branch 전략 기반, PR 및 코드 리뷰 필수) |

---

## 공통 응답 형식

### ✅ 성공 응답
```json
{
  "success": true,
  "data": {},
  "message": "요청 성공"
}
```

### ❌ 실패 응답
```json
{
  "success": false,
  "message": "에러 메시지"
}
```

---

## 상태 코드 정의

| 상태 코드 | 설명 |
|-----------|------|
| 200 | 요청 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 409 | 충돌 (중복 등) |
| 422 | 유효성 검사 실패 |

---

## 전체 API 목록

| ID | 도메인 | 기능명 | Method | URL | 인증 필요 |
|----|--------|--------|--------|-----|-----------|
| API-01 | 인증 | 회원가입 | POST | /users/ | X |
| API-02 | 인증 | 사용자 로그인 | POST | /auth/login | X |
| API-03 | 인증 | Access Token 재발급 | POST | /auth/refresh | X |
| API-04 | 게시글 | 게시글 작성 | POST | /posts/ | O |
| API-05 | 게시글 | 게시글 목록 조회 | GET | /posts/ | X |
| API-06 | 게시글 | 게시글 상세 조회 | GET | /posts/{post_id} | X |
| API-07 | 게시글 | 게시글 수정 | PATCH | /posts/{post_id} | O |
| API-08 | 게시글 | 게시글 삭제 | DELETE | /posts/{post_id} | O (관리자/작성자) |
| API-09 | 좋아요 | 좋아요 등록/취소 | POST | /posts/{post_id}/like | O |
| API-10 | 좋아요 | 싫어요 등록/취소 | POST | /posts/{post_id}/dislike | O |
| API-11 | 댓글 | 댓글 작성 | POST | /posts/{post_id}/comments/ | O |
| API-12 | 댓글 | 댓글 수정 | PATCH | /posts/{post_id}/comments/{comment_id} | O |
| API-13 | 댓글 | 댓글 삭제 | DELETE | /posts/{post_id}/comments/{comment_id} | O (관리자/작성자) |
| API-14 | 댓글 | 대댓글 작성 | POST | /posts/{post_id}/comments/{comment_id}/replies | O |
| API-15 | 댓글 | 대댓글 목록 조회 | GET | /posts/{post_id}/comments/{comment_id}/replies | X |
| API-16 | 댓글 | 댓글 좋아요 등록/취소 | POST | /posts/{post_id}/comments/{comment_id}/like | O |
| API-17 | 댓글 | 댓글 싫어요 등록/취소 | POST | /posts/{post_id}/comments/{comment_id}/dislike | O |
| API-18 | 게시판 | 게시판 생성 | POST | /admin/boards/ | O (관리자) |
| API-19 | 게시판 | 게시판 목록 조회 | GET | /boards/ | X |
| API-20 | 게시판 | 게시판 상세 조회 | GET | /boards/{board_id} | X |
| API-21 | 게시판 | 게시판 수정 | PATCH | /admin/boards/{board_id} | O (관리자) |
| API-22 | 게시판 | 게시판 삭제 | DELETE | /admin/boards/{board_id} | O (관리자) |
| API-23 | 게시판 | 게시판 게시글 목록 조회 | GET | /boards/{board_id}/posts | X |
| API-24 | 태그 | 태그 등록 | POST | /posts/{post_id}/tags/ | O |
| API-25 | 태그 | 태그 수정 | PATCH | /posts/{post_id}/tags/ | O |
| API-26 | 태그 | 태그 필터링 | GET | /posts/{post_id}/tags/filter?tag_name=태그명 | X |
| API-27 | 인기글 | 조회수 기준 인기글 | GET | /posts/popular?sort_type=views&limit=N | X |
| API-28 | 인기글 | 좋아요 기준 인기글 | GET | /posts/popular?sort_type=likes&limit=N | X |
| API-29 | 게시글 | 게시글 검색/페이지네이션 | GET | /posts/?keyword=검색어&page=1&size=10&board_id=1 | X |

---

## 상세 API 명세

### 인증

#### API-01 회원가입
- **Method:** POST
- **URL:** `/users/`
- **인증:** X

**Request Body**
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**성공 응답**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "email": "test@example.com"
  },
  "message": "회원가입 성공"
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 400 | 이미 사용 중인 이메일입니다. |

---

#### API-02 로그인
- **Method:** POST
- **URL:** `/auth/login`
- **인증:** X

**Request Body**
```json
{
  "username": "test@example.com",
  "password": "password123"
}
```

**성공 응답**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  },
  "message": "로그인 성공"
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 401 | 이메일 또는 비밀번호가 올바르지 않습니다. |

---

#### API-03 Access Token 재발급
- **Method:** POST
- **URL:** `/auth/refresh`
- **인증:** X

**Request Body**
```json
{
  "refresh_token": "eyJ..."
}
```

**성공 응답**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  },
  "message": "토큰 재발급 성공"
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 401 | 유효하지 않은 토큰입니다. |

---

### 게시글

#### API-04 게시글 작성
- **Method:** POST
- **URL:** `/posts/`
- **인증:** O

**Request Body**
```json
{
  "title": "게시글 제목",
  "content": "게시글 내용",
  "board_id": 1,
  "tag_names": ["태그1", "태그2"]
}
```

**성공 응답**
```json
{
  "success": true,
  "data": {
    "post_id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용",
    "author": { "user_id": 1, "email": "test@example.com" },
    "board": { "board_id": 1, "name": "게시판명" },
    "tags": [{ "tag_id": 1, "name": "태그1" }],
    "like_count": 0,
    "dislike_count": 0,
    "view_count": 0,
    "created_at": "2026-06-23T00:00:00",
    "updated_at": null
  },
  "message": "게시글 생성 성공"
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 401 | 인증이 필요합니다. |
| 404 | 존재하지 않는 게시판입니다. |

---

#### API-05 게시글 목록 조회 / 검색 / 페이지네이션
- **Method:** GET
- **URL:** `/posts/`
- **인증:** X

**Query Parameters**
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| keyword | string | X | 검색어 (제목/내용/작성자 이메일) |
| board_id | integer | X | 게시판 ID 필터 |
| page | integer | X | 페이지 번호 (기본값: 1) |
| size | integer | X | 페이지당 게시글 수 (기본값: 10) |

**성공 응답**
```json
{
  "success": true,
  "data": [
    {
      "post_id": 1,
      "title": "게시글 제목",
      "author": { "user_id": 1, "email": "test@example.com" },
      "board": { "board_id": 1, "name": "게시판명" },
      "tags": [],
      "created_at": "2026-06-23T00:00:00"
    }
  ],
  "total": 10,
  "page": 1,
  "size": 10,
  "total_pages": 1,
  "message": "게시글 목록 조회 성공"
}
```

---

#### API-06 게시글 상세 조회
- **Method:** GET
- **URL:** `/posts/{post_id}`
- **인증:** X

**성공 응답**
```json
{
  "success": true,
  "data": {
    "post_id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용",
    "author": { "user_id": 1, "email": "test@example.com" },
    "board": { "board_id": 1, "name": "게시판명" },
    "tags": [],
    "like_count": 0,
    "dislike_count": 0,
    "view_count": 1,
    "created_at": "2026-06-23T00:00:00",
    "updated_at": null
  },
  "message": "게시글 상세 조회 성공"
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 404 | 존재하지 않는 게시글입니다. |

---

#### API-07 게시글 수정
- **Method:** PATCH
- **URL:** `/posts/{post_id}`
- **인증:** O (작성자)

**Request Body**
```json
{
  "title": "수정된 제목",
  "content": "수정된 내용",
  "board_id": 1
}
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 401 | 인증이 필요합니다. |
| 403 | 권한이 없습니다. |
| 404 | 존재하지 않는 게시글입니다. |

---

#### API-08 게시글 삭제
- **Method:** DELETE
- **URL:** `/posts/{post_id}`
- **인증:** O (작성자/관리자)

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 401 | 인증이 필요합니다. |
| 403 | 권한이 없습니다. |
| 404 | 존재하지 않는 게시글입니다. |

---

### 좋아요/싫어요

#### API-09 게시글 좋아요 등록/취소
- **Method:** POST
- **URL:** `/posts/{post_id}/like`
- **인증:** O

**성공 응답**
```json
{ "success": true, "message": "좋아요를 눌렀습니다." }
{ "success": true, "message": "좋아요가 취소되었습니다." }
```

**실패 응답**
| 상태 코드 | 메시지 |
|-----------|--------|
| 409 | 싫어요 상태에서 다른 반응을 누를 수 없습니다. |

---

#### API-10 게시글 싫어요 등록/취소
- **Method:** POST
- **URL:** `/posts/{post_id}/dislike`
- **인증:** O

---

### 댓글

#### API-11 댓글 작성
- **Method:** POST
- **URL:** `/posts/{post_id}/comments/`
- **인증:** O

**Request Body**
```json
{ "content": "댓글 내용" }
```

**성공 응답**
```json
{
  "success": true,
  "data": {
    "comment_id": 1,
    "content": "댓글 내용",
    "author": { "user_id": 1, "email": "test@example.com" },
    "post_id": 1,
    "parent_id": null,
    "is_deleted": false,
    "like_count": 0,
    "dislike_count": 0,
    "replies": [],
    "created_at": "2026-06-23T00:00:00"
  },
  "message": "댓글 생성 성공"
}
```

---

#### API-12 댓글 수정
- **Method:** PATCH
- **URL:** `/posts/{post_id}/comments/{comment_id}`
- **인증:** O (작성자)

**Request Body**
```json
{ "content": "수정된 댓글" }
```

---

#### API-13 댓글 삭제
- **Method:** DELETE
- **URL:** `/posts/{post_id}/comments/{comment_id}`
- **인증:** O (작성자/관리자)

> 소프트 삭제 — 삭제 주체에 따라 다른 메시지 표시
> - 작성자 삭제: "사용자에 의해 삭제된 댓글입니다."
> - 관리자 삭제: "관리자에 의해 삭제된 댓글입니다."

---

#### API-14 대댓글 작성
- **Method:** POST
- **URL:** `/posts/{post_id}/comments/{comment_id}/replies`
- **인증:** O

**Request Body**
```json
{ "content": "대댓글 내용" }
```

---

#### API-15 대댓글 목록 조회
- **Method:** GET
- **URL:** `/posts/{post_id}/comments/{comment_id}/replies`
- **인증:** X

---

#### API-16 댓글 좋아요 등록/취소
- **Method:** POST
- **URL:** `/posts/{post_id}/comments/{comment_id}/like`
- **인증:** O

---

#### API-17 댓글 싫어요 등록/취소
- **Method:** POST
- **URL:** `/posts/{post_id}/comments/{comment_id}/dislike`
- **인증:** O

---

### 게시판

#### API-18 게시판 생성
- **Method:** POST
- **URL:** `/admin/boards/`
- **인증:** O (관리자)

**Request Body**
```json
{ "name": "게시판 이름" }
```

---

#### API-19 게시판 목록 조회
- **Method:** GET
- **URL:** `/boards/`
- **인증:** X

---

#### API-20 게시판 상세 조회
- **Method:** GET
- **URL:** `/boards/{board_id}`
- **인증:** X

---

#### API-21 게시판 수정
- **Method:** PATCH
- **URL:** `/admin/boards/{board_id}`
- **인증:** O (관리자)

**Request Body**
```json
{ "name": "수정된 게시판 이름" }
```

---

#### API-22 게시판 삭제
- **Method:** DELETE
- **URL:** `/admin/boards/{board_id}`
- **인증:** O (관리자)

---

#### API-23 게시판 게시글 목록 조회
- **Method:** GET
- **URL:** `/boards/{board_id}/posts`
- **인증:** X

**Query Parameters**
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| page | integer | X | 페이지 번호 (기본값: 1) |
| size | integer | X | 페이지당 게시글 수 (기본값: 10) |

---

### 태그

#### API-24 태그 등록
- **Method:** POST
- **URL:** `/posts/{post_id}/tags/`
- **인증:** O (작성자)

**Request Body**
```json
{ "names": ["태그1", "태그2"] }
```

---

#### API-25 태그 수정
- **Method:** PATCH
- **URL:** `/posts/{post_id}/tags/`
- **인증:** O (작성자)

**Request Body**
```json
{ "names": ["새태그1", "새태그2"] }
```

> 전체 교체 방식 — 기존 태그 삭제 후 새 태그 등록

---

#### API-26 태그 필터링
- **Method:** GET
- **URL:** `/posts/{post_id}/tags/filter`
- **인증:** X

**Query Parameters**
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| tag_name | string | O | 태그 이름 |

---

### 인기글

#### API-27 조회수 기준 인기글
- **Method:** GET
- **URL:** `/posts/popular?sort_type=views&limit=N`
- **인증:** X

**Query Parameters**
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| sort_type | string | X | views 또는 likes (기본값: views) |
| limit | integer | X | 조회할 게시글 수 (기본값: 10) |

---

#### API-28 좋아요 기준 인기글
- **Method:** GET
- **URL:** `/posts/popular?sort_type=likes&limit=N`
- **인증:** X
