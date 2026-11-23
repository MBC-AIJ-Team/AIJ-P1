# AIJ_P1 ERD — 논리 데이터 모델 v1.0

> **설계 문서**: 현재 구현은 CSV/JSON/JSONL 파일 저장 방식입니다. 아래 테이블과 관계는 SQLite 전환 시 사용할 **제안 논리 모델**이며, 현재 DB에 생성된 테이블이 아닙니다.

```mermaid
erDiagram
    CANDIDATES ||--o{ ELECTION_RESULTS : "candidate_id"
    REGIONS ||--o{ ELECTION_RESULTS : "region_id"
    COUNT_STEPS ||--o{ ELECTION_RESULTS : "step"
    CANDIDATES o|--o{ RAG_DOCUMENTS : "candidate_id nullable"
    COUNT_STEPS ||--o{ ARTICLES : "step"
    ARTICLES ||--o{ ARTICLE_EVIDENCE : "article_id"
    RAG_DOCUMENTS ||--o{ ARTICLE_EVIDENCE : "document_id"
    ARTICLES ||--o{ APPROVAL_EVENTS : "article_id"
    CANDIDATES {
        string candidate_id PK
        string name
        int age
        string party
        string primary_policy
        string policy_focus
        string color
    }
    REGIONS {
        string region_id PK
        string region
        int electorate
        int voters
        float turnout_rate
    }
    COUNT_STEPS {
        int step PK
        string timestamp
        int counted_ballots
        int valid_votes
        int invalid_votes
        float count_progress_pct
        string source_id
    }
    ELECTION_RESULTS {
        string row_id PK
        int step FK
        string region_id FK
        string candidate_id FK
        int votes
        float vote_share_pct
        int valid_votes
        int invalid_votes
        int counted_ballots
        int total_ballots
        float count_progress_pct
    }
    RAG_DOCUMENTS {
        string document_id PK
        string title
        string document_type
        string publisher
        string published_at
        string source_id
        string source_url
        string candidate_id FK_nullable
        string text
    }
    ARTICLES {
        string article_id PK
        int step FK
        string title
        string body
        string timestamp
        string source_id
        string status
        string generation_method
        string article_hash
    }
    ARTICLE_EVIDENCE {
        string article_id PK,FK
        string document_id PK,FK
    }
    APPROVAL_EVENTS {
        int event_id PK
        string article_id FK
        string editor
        string status
        string reason
        string timestamp
        boolean basic_validation
        boolean source_validation
        boolean rag_validation
    }
```

## 구현 기준 파일과 매핑

| 논리 테이블 | 현재 저장소 파일 | 비고 |
|---|---|---|
| CANDIDATES | `data/STEP2_Data/candidates.csv` | 실제 필드 그대로 |
| REGIONS | `data/STEP2_Data/regions.csv` | 실제 필드 그대로 |
| COUNT_STEPS | `data/STEP2_Data/election_summary.json` → `steps[]` | 단계 집계 데이터 분리 제안 |
| ELECTION_RESULTS | `data/STEP2_Data/election_results.csv` | 기존 `row_id` 고유 식별자 |
| RAG_DOCUMENTS | `data/STEP2_Data/policy_documents.json` | 후보가 없는 공통 문서도 존재 |
| ARTICLES | `rag/articles/*.json`, `rag/approved/*.json` | 기사 식별자 신규 제안; 원본에 일관된 ID 없음 |
| ARTICLE_EVIDENCE | 각 기사 `evidence_ids` 배열 | 다대다 연결용 신규 테이블 제안 |
| APPROVAL_EVENTS | `rag/approval_log.jsonl` | 이벤트 ID 신규 제안; 기록마다 필드 차이 있음 |

## 핵심 제약조건

- 후보 ID(`C01` 등), 지역 ID(`R01` 등), 문서 ID(`DOC-001` 등)를 유지합니다.
- 각 개표 행은 `row_id`가 고유해야 하며, `step+region_id+candidate_id` 조합도 중복될 수 없습니다.
- 누적 개표는 10단계이고 같은 지역·후보의 누적 득표수는 감소하면 안 됩니다.
- 각 단계·지역에서 후보 득표수 합계는 `valid_votes`와 일치해야 합니다. `counted_ballots = valid_votes + invalid_votes`입니다.
- RAG 공통 문서는 `candidate_id`가 `null`일 수 있습니다.
- 기사 원본과 승인 기록은 수정 이력을 위해 덮어쓰지 않고 연결합니다.
- 현 저장소 후보 데이터에는 `심청`, 기획서에는 `심청이`가 등장합니다. 영상·검증 코드와 표기를 통일해야 합니다.

## 구현 상태

- **확인됨:** CSV/JSON/JSONL 파일, 후보·지역·시점·RAG 근거·승인 로그의 데이터 구조
- **설계 제안:** 8개 논리 테이블과 PK/FK 관계, SQLite 스키마 전환
- **미확인:** 실제 SQLite DB 파일 및 테이블 생성 여부, 실행 기반 무결성 테스트
