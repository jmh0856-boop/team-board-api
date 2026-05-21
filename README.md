# Team Board API

본 프로젝트는 팀 협업을 위한 게시판 API 서비스입니다.

## 🗂 Database Design (ERD)

```mermaid
erDiagram
    USERS ||--o{ POSTS : writes
    USERS ||--o{ COMMENTS : writes
    USERS ||--o{ LIKES : "presses(Post)"
    USERS ||--o{ COMMENT_LIKES : "presses(Comment)"
    POSTS ||--o{ COMMENTS : has
    POSTS ||--o{ LIKES : "receives"
    BOARDS ||--o{ POSTS : contains
    COMMENTS ||--o{ COMMENTS : replies
    COMMENTS ||--o{ COMMENT_LIKES : "receives"

    USERS {
        int id PK
        string email
        string password
        string phone_number
        boolean is_active
        datetime created_at
    }

    BOARDS {
        int id PK
        string name
    }

    POSTS {
        int id PK
        string title
        string content
        int views
        int owner_id FK
        int board_id FK
        datetime created_at
        datetime updated_at
    }

    LIKES {
        int id PK
        int user_id FK
        int post_id FK
        boolean is_like
        datetime created_at
    }

    COMMENT_LIKES {
        int id PK
        int user_id FK
        int comment_id FK
        boolean is_like
        datetime created_at
    }

    COMMENTS {
        int id PK
        string content
        int parent_id FK
        int post_id FK
        int author_id FK
        boolean is_deleted
        string deleted_by
        datetime created_at
    }
```

---

## 주요 설계 원칙
1. **정규화 및 관계 정의**: USERS, BOARDS, POSTS, COMMENTS 엔티티 간의 관계를 명확히 정의하여 데이터 중복을 최소화했습니다.
2. **확장 가능한 게시판 구조**: BOARDS 테이블을 분리하여 향후 게시판 유형이 추가되어도 시스템 구조 변경 없이 유연하게 확장 가능합니다.
3. **데이터 무결성 (CASCADE)**: POSTS 삭제 시 관련 COMMENTS가 고아 데이터로 남지 않도록 CASCADE 옵션을 적용하였습니다.
4. **대댓글 및 좋아요 기능**:
   - Self-referencing: COMMENTS 테이블 내 parent_id를 통해 계층형 대댓글 구조를 구현했습니다.
   - Soft Delete: 댓글 삭제 시 물리적 삭제 대신 `deleted_by` 필드로 삭제 주체(작성자/관리자)를 기록하여 대화 맥락을 유지하도록 설계했습니다.
   - 중복 방지: LIKES 및 COMMENT_LIKES 테이블에 복합 유니크 제약을 설정하여 사용자당 좋아요/싫어요 1회 제한 정책을 강제했습니다.


---

## 📋 Table Definition (테이블 정의서)

### USERS
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 사용자 고유 ID |
| email | VARCHAR | UNIQUE, NOT NULL | 이메일 (로그인 ID) |
| hashed_password | VARCHAR | NOT NULL | 암호화된 비밀번호 |
| phone_number | VARCHAR | NULL | 전화번호 |
| is_active | BOOLEAN | DEFAULT TRUE | 계정 활성화 여부 |
| created_at | DATETIME | DEFAULT NOW | 가입일시 |

---

### BOARDS (구현 예정)
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 게시판 고유 ID |
| name | VARCHAR | NOT NULL | 게시판 이름 |

---

### POSTS
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 게시글 고유 ID |
| title | VARCHAR(200) | NOT NULL | 게시글 제목 |
| content | TEXT | NOT NULL | 게시글 내용 |
| user_id | INTEGER | FK(USERS.id), NOT NULL | 작성자 ID |
| view_count | INTEGER | DEFAULT 0 | 조회수 |
| created_at | DATETIME | DEFAULT NOW | 작성일시 |
| updated_at | DATETIME | NULL | 수정일시 |

---

### COMMENTS
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 댓글 고유 ID |
| content | TEXT | NOT NULL | 댓글 내용 |
| user_id | INTEGER | FK(USERS.id), NOT NULL | 작성자 ID |
| post_id | INTEGER | FK(POSTS.id), NOT NULL | 게시글 ID |
| parent_id | INTEGER | FK(COMMENTS.id), NULL | 부모 댓글 ID (대댓글인 경우) |
| is_deleted | BOOLEAN | DEFAULT FALSE | 삭제 여부 |
| deleted_by | VARCHAR | NULL | 삭제 주체 (user/admin) |
| created_at | DATETIME | DEFAULT NOW | 작성일시 |

---

### LIKES
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 좋아요 고유 ID |
| user_id | INTEGER | FK(USERS.id), NOT NULL | 사용자 ID |
| post_id | INTEGER | FK(POSTS.id), NOT NULL | 게시글 ID |
| is_like | BOOLEAN | NOT NULL | 좋아요(TRUE) / 싫어요(FALSE) |
| created_at | DATETIME | DEFAULT NOW | 생성일시 |

> UNIQUE(user_id, post_id) — 한 사용자가 한 게시글에 한 번만 가능

---

### COMMENT_LIKES
| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 좋아요 고유 ID |
| user_id | INTEGER | FK(USERS.id), NOT NULL | 사용자 ID |
| comment_id | INTEGER | FK(COMMENTS.id), NOT NULL | 댓글 ID |
| is_like | BOOLEAN | NOT NULL | 좋아요(TRUE) / 싫어요(FALSE) |
| created_at | DATETIME | DEFAULT NOW | 생성일시 |

> UNIQUE(user_id, comment_id) — 한 사용자가 한 댓글에 한 번만 가능
