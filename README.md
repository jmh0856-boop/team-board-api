# Team Board API

본 프로젝트는 팀 협업을 위한 게시판 API 서비스입니다.

## 🗂 Database Design (ERD)

\`\`\`mermaid
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
    }

    LIKES {
        int id PK
        int user_id FK
        int post_id FK
        boolean is_like
    }

    COMMENT_LIKES {
        int id PK
        int user_id FK
        int comment_id FK
        boolean is_like
    }

    COMMENTS {
        int id PK
        string content
        int parent_id FK
        int post_id FK
        int author_id FK
        boolean is_deleted
    }
\`\`\`

## 주요 설계 원칙
1. **정규화 및 관계 정의**: USERS, BOARDS, POSTS, COMMENTS 엔티티 간의 관계를 명확히 정의하여 데이터 중복을 최소화했습니다.
2. **확장 가능한 게시판 구조**: BOARDS 테이블을 분리하여 향후 게시판 유형이 추가되어도 시스템 구조 변경 없이 유연하게 확장 가능합니다.
3. **데이터 무결성 (CASCADE)**: POSTS 삭제 시 관련 COMMENTS가 고아 데이터로 남지 않도록 CASCADE 옵션을 적용하였습니다.
4. **대댓글 및 좋아요 기능**:
   - Self-referencing: COMMENTS 테이블 내 parent_id를 통해 계층형 대댓글 구조를 구현했습니다.
   - Soft Delete: 댓글 삭제 시 물리적 삭제 대신 본문만 초기화하여 대화 맥락을 유지하도록 설계했습니다.
   - 중복 방지: LIKES 및 COMMENT_LIKES 테이블에 복합 유니크 제약을 설정하여 사용자당 좋아요/싫어요 1회 제한 정책을 강제했습니다.
