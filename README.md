# AIJ-P1 | RAG 기반 가상 선거 개표 및 AI 뉴스 보도 시스템

**2026 한빛시 시장 선거 — AI 가상 개표 특집**

### 최종 AI 뉴스 영상 시청

[▶ 최종 뉴스 영상 시청하기 (Google Drive)](https://drive.google.com/file/d/1_a4BQ9g78F7yzgqDbPreUeiyYi9aAZip/view?usp=sharing)

| 재생 시간 | 해상도 | 화면 비율 | 프레임 속도 | 형식 | 용량 |
|---|---|---|---|---|---|
| 6분 50초 | FHD 1920 × 1080 | 16:9 | 30fps | MP4 | 약 372.3 MB |

> 교육용 가상 선거 프로젝트입니다. 후보·정당·지역·개표 결과는 창작 설정이며 실제 선거와 무관합니다. 생성형 AI를 활용했으며, AI 생성 기사는 사람의 검토와 승인 없이 최종 보도에 사용하지 않습니다.

- 과정: MBC 미디어캠퍼스 AI 기반 데이터 저널리스트 양성 과정
- 개발 형태: 개인 프로젝트(1인 개발)
- 개발자: 조남수
- 과제 수행 기간: 2026.11.18~11.27 (기관 일정)
- 대표 통합 테스트: 2026.11.25 (8개 항목 통과)
- STEP 10 추가 기능 검증: 2026.11.27 (24개 항목 통과, PC 및 대표 기사 화면 검증 범위)

## 1. 프로젝트 소개

빠르게 바뀌는 개표 데이터를 정확하게 전달하기 위해 가상 선거 데이터 생성·분석, 실시간 웹 시각화, RAG 근거 검색, 기사 생성, 자동 팩트체크, 편집자 승인, AI 뉴스 영상 제작을 하나의 작업 흐름으로 연결한다. 실제 선거 API 대신 사전 제작한 교육용 데이터를 사용한다.

핵심 보도 질문: 개표 진행에 따라 선두 후보와 격차가 어떻게 달라지고 지역별 결과가 최종 순위에 어떤 영향을 주는가?

## 2. 가상 선거 설정과 최종 결과

| 항목 | 내용 |
|---|---|
| 선거 | 2026 한빛시 시장 선거 |
| 가상 선거일 | 2026.11.20 |
| 지역 | 중앙구, 동부구, 서부구, 남부구, 북부구 |
| 선거인 / 투표자 | 500,000명 / 350,000명 |
| 투표율 | 70.00% |
| 개표 단계 | 10단계 |
| 최종 개표율 | 100.00% |
| 유효 / 무효투표수 | 346,500표 / 3,500표 |
| 데이터 출처 ID | `SYNTHETIC-STEP2-v1.0` |
| 최종 집계 기준시각(가상) | 2026.11.20 23:30 KST |

| 순위 | 후보 | 득표수 | 득표율 | 주요 공약 | 근거 ID |
|---|---|---:|---:|---|---|
| 1 | 심청 | 131,000 | 37.81% | 청년 주거 지원 | DOC-003 |
| 2 | 이몽룡 | 128,000 | 36.94% | 광역교통망 확충 | DOC-002 |
| 3 | 홍길동 | 87,500 | 25.25% | 소상공인 지원 | DOC-004 |

1·2위 격차는 3,000표(표시 득표율 기준 0.87%p)이다. 득표율의 분모는 유효투표수이며 개별 반올림에 따라 합계가 100%와 소폭 다를 수 있다. 개표 초반 이몽룡이 선두였으며 최종 단계에는 심청이 선두로 바뀌었다. 이는 교육용 시나리오이며 실제 정치적 전망이 아니다.

## 3. 핵심 기능

- 개표 단계별 데이터 조회, 후보별·지역별 득표 현황 및 Plotly 득표율 추이 시각화
- WebSocket 10단계 JSON 전송(약 2초 간격), 재생·일시정지·재개·초기화 및 잘못된 명령 처리
- RAG 근거 문서 검색, 문서 ID와 공약 연결, 규칙 기반 및 OpenAI LLM 기반 기사 생성
- 기본 검증, 원본 데이터 교차검증, RAG 근거 검증
- 편집자 검토·승인·반려, 검증 실패 시 승인 차단, 승인 파일 덮어쓰기 방지
- JSONL 감사 로그 및 원본 기사 SHA-256 기록
- 승인 기사를 기준으로 AI 앵커·음성·CG·자막을 결합한 뉴스 영상 제작

### STEP 10 — 통합 AI 뉴스룸 고도화

- 수동 조회 및 실시간 개표에 연동된 1~10단계 저장 기사 자동 갱신
- 기사 단계, RAG 근거 ID, 모델명, 승인자·시각·사유 표시
- 요청 ID 기반 비동기 응답 보호(기사, 후보별, 지역별, 그래프)
- 공통 초기화 함수로 0단계 화면 복구 및 기사 조회 차단
- WebSocket 자동 재연결 및 0단계 상태 동기화
- 재생 상태에 따른 제어 버튼 활성화 관리
- PC 중심 통합 뉴스룸 UI


### 초기 개표 화면 — 1단계

![1단계 초기 개표 화면](docs/screenshots/dashboard_step01.png)

- 개표율 9.94%
- 이몽룡 후보 61.30%로 선두
- 초기 개표 데이터와 AI 뉴스 기사 연동

### 중간 개표 화면 — 5단계

![5단계 중간 개표 화면](docs/screenshots/dashboard_step05.png)

- 개표율 49.85%
- 후보별 득표율 변화 및 지역별 개표 현황
- RAG 기반 AI 뉴스 기사와 승인 정보 표시

### 최종 개표 화면 — 10단계

![10단계 최종 개표 화면](docs/screenshots/dashboard_step10.png)

- 개표율 100.00%
- 심청 후보 131,000표(37.81%)로 1위
- 최종 개표 결과 및 편집자 승인 기사 표시

※ 모든 화면은 AI 데이터 저널리즘 교육용 가상 선거
시뮬레이션이며 실제 선거 결과가 아닙니다.


## 4. 기술 스택

| 영역 | 기술 | 버전 또는 설명 |
|---|---|---|
| 개발 환경 | Windows 11, VS Code, PowerShell, .venv | Python 3.12.10 |
| 백엔드 | FastAPI, Uvicorn | 0.162.5 / 0.54.0 |
| 실시간 통신 | websockets, asyncio | 17.4 / Python 내장 |
| 데이터 분석 | pandas, NumPy | 3.1.1 / 2.5.4 |
| 프런트엔드 | HTML, CSS, JavaScript, Jinja2 | Jinja2 3.1.6 |
| 시각화 | Plotly | Python 패키지 7.1.0 |
| 데이터 검증 | Pydantic | 2.14.3 |
| 환경변수 | python-dotenv | 1.2.4 |
| 데이터·기록 | CSV, JSON, JSONL, SHA-256 | 파일 기반 |
| 기사 생성 | Python 규칙 기반 생성, RAG, OpenAI SDK | openai 3.57.0 설치 확인 |
| 영상 | AI 앵커·립싱크·음성, 데이터 CG, CapCut | 별도 영상 편집 |
| 형상관리 | Git, GitHub | — |

Python 및 OpenAI SDK 버전은 로컬 실행 출력 기준이며, 나머지 패키지 버전은 `requirements.txt` 기록 기준이다. 2026.11.27 `python -m pip check` 결과는 `No broken requirements found.`이다. 새 가상환경에서 전체 설치 재현성은 아직 검증하지 않았다. 기사에 기록된 모델명은 `GPT-6.2`, `gpt-6-luna` 등이 있으며 실제 API 모델 식별자는 요청 기록 확인이 필요하다.

## 5. 시스템 아키텍처

```mermaid
flowchart TD
    A[교육용 가상 개표 데이터] --> B[FastAPI]
    B --> C[HTTP API 및 통합 뉴스룸]
    B --> D[WebSocket /ws]
    D --> C
    A --> E[기사 생성]
    F[교육용 근거 문서] --> G[RAG 검색]
    G --> E
    E --> H[규칙 기반 또는 LLM 기사 초안]
    H --> I[기본·원본·RAG 검증]
    I -->|통과| J[편집자 직접 검토]
    I -->|실패| K[승인 차단]
    J -->|승인| L[승인 기사 별도 저장]
    J -->|반려| M[수정 및 재검증]
    M --> I
    K --> N[감사 로그]
    L --> N
    J --> N
    L --> Q[기사 조회 API 및 승인 상태 확인]
    H --> Q
    N --> Q
    Q --> C
    L --> O[뉴스 대본·CG·음성·영상 제작]
    O --> P[FHD 뉴스 MP4]
```

대시보드는 저장된 기사와 승인 상태를 조회한다. 단계가 바뀔 때마다 LLM을 새로 호출하는 방식은 아니다. 영상 제작은 별도의 편집 작업이며 완전 자동 영상 생성 파이프라인을 의미하지 않는다.

## 6. 주요 파일 구조

Git 관리 파일 목록 기준의 축약 구조이며 영상 제작 스크립트와 세부 산출물 일부는 생략했다.

```text
AIJ-P1/
├── README.md
├── requirements.txt
├── run_server.ps1
├── .gitignore
├── AIJ_P1_Final_Report.docx
├── AIJ_P1_Final_Report.pdf
├── AIJ_P1_Presentation.pptx
├── STEP9_Integration_Test.md
├── data/STEP2_Data/
│   ├── candidates.csv
│   ├── regions.csv
│   ├── election_results.csv
│   ├── election_summary.json
│   ├── policy_documents.json
│   ├── data_dictionary.csv
│   ├── article_log.json
│   ├── generate_election_data.py
│   └── validate_data.py
├── src/
│   ├── STEP3_Analysis/
│   │   ├── analyze_election.py
│   │   └── output/
│   ├── STEP4_Dashboard/
│   │   ├── main.py
│   │   ├── static/dashboard.js
│   │   ├── static/style.css
│   │   └── templates/index.html
│   ├── STEP5_WebSocket/
│   │   ├── election_stream.py
│   │   └── websocket_manager.py
│   ├── STEP6_RAG/
│   │   ├── document_loader.py
│   │   ├── rag_search.py
│   │   ├── article_generator.py
│   │   ├── llm_article_generator.py
│   │   └── test_api_key.py
│   └── STEP7_Validation/
│       ├── article_validator.py
│       └── article_approval.py
├── rag/
│   ├── articles/     # 01~10단계 기사 및 검증용 파일
│   ├── approved/     # 01~10단계 승인 기사 및 별도 수정본
│   └── approval_log.jsonl
├── docs/
├── reports/
├── presentation/
├── tests/
└── video/
    ├── audio/
    ├── charts/
    └── images/
```

## 7. 설치 및 실행

프로젝트 루트에서 Windows PowerShell을 사용한다. 새 환경에서는 Python 3.12.10을 권장하며, 아래 설치 절차의 새 환경 재현성은 미검증이다.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
.\run_server.ps1
```

기존 가상환경에서 검증된 서버 실행 명령은 `.\run_server.ps1`이다. 이 스크립트는 프로젝트 루트와 가상환경 Python을 사용하고 `PYTHONPATH`를 설정한 후 `uvicorn main:app --app-dir src/STEP4_Dashboard --reload`를 실행한다. `Application startup complete.`를 확인한다. 종료는 서버 터미널에서 `Ctrl+C`.

| 페이지 | 주소 |
|---|---|
| 서버 상태 | http://127.0.0.1:8000/ |
| 개표 대시보드 | http://127.0.0.1:8000/dashboard |
| Swagger UI | http://127.0.0.1:8000/docs |

대시보드는 최초 접속 시 개표 대기 상태로 시작한다. 조회 단계 메뉴로 수동 조회하거나 상단 실시간 개표 재생 버튼을 사용한다. 재연결 시 0단계로 돌아간다. 저장 기사 조회와 LLM 신규 기사 생성은 구분한다. LLM API 키는 개인 환경 설정으로 관리하고 저장소에 공개하지 않는다. `requirements.txt`에 `openai==3.57.0`이 반영되어 있는지 확인한다. 실제 키 설정명 및 `.env.example` 존재 여부는 별도 확인 대상이다.

## 8. API 명세

| 방식 | 경로 | 기능 |
|---|---|---|
| GET | `/` | 서버 상태 JSON |
| GET | `/api/election-results` | 개표 데이터 조회 |
| GET | `/dashboard` | 개표 대시보드 |
| GET | `/api/ai-article?step=10` | 저장된 AI 기사 조회 (정수 1~10, 기본값 10) 및 승인 상태 확인 |
| WebSocket | `/ws` | 개표 데이터 순차 전송 및 재생 제어 |

WebSocket 명령: `start`, `pause`, `resume`, `reset`. 단계별 `election_update`, 상태 변경 `playback_status`, 완료 `election_complete`, 미지원 명령 `error` 메시지를 사용한다. Swagger UI에는 WebSocket 경로가 표시되지 않는다. 기사 조회 시 원본 해시, 승인 파일 및 감사 로그를 이용해 승인 상태를 확인한다. 0단계는 화면 초기화 상태로 기사 조회 대상이 아니다.

## 9. RAG 기사 생성 및 검증 실행

별도 터미널에서 프로젝트 루트 및 가상환경을 유지한다.

```powershell
python .\src\STEP6_RAG\rag_search.py
python .\src\STEP6_RAG\article_generator.py
python .\src\STEP7_Validation\article_validator.py
```

LLM 기사 재생성은 API 비용과 기존 초안 갱신 가능성이 있으므로 필요할 때만 실행한다.

```powershell
python .\src\STEP6_RAG\llm_article_generator.py
```

승인 대상은 기본 기사 또는 실행 인자로 지정한 JSON 파일이다. 편집자가 직접 검토한 경우에만 승인한다. 이미 승인된 출력 파일은 덮어쓰지 않는다.

```powershell
python .\src\STEP7_Validation\article_approval.py
# 의도적으로 오류가 있는 교육용 테스트 기사
python .\src\STEP7_Validation\article_approval.py .\rag\articles\ai_article_step_10_error.json
python .\src\STEP7_Validation\article_approval.py .\rag\articles\ai_article_step_10_no_evidence.json
Get-Content .\rag\approval_log.jsonl -Encoding UTF8 -Tail 1
```

오류 기사에서 승인 메뉴 `1`을 선택하더라도 승인 차단되어야 한다. 승인/차단 실행은 감사 로그에 기록될 수 있다.

최종 영상 검증에 사용한 승인 기사: `rag/approved/approved_ai_article_step_10_name_corrected_pending.json` (파일명에 pending이 남아 있지만 기존 검증 기록상 내부 status는 승인). 대시보드의 정규 10단계 기사와 별도 파일이다. 기존 승인 원본 SHA-256 확인:

```powershell
Get-FileHash .\rag\articles\ai_article_step_10_name_corrected_pending.json -Algorithm SHA256
```

기존 검증 기대값: `941c362f75ce3739fece11571a6dbc95fe6af29df79d1213a78f0f0470a5c7a1`

## 10. 대표 통합 테스트 결과

### STEP 9 — 2026.11.25

사용자 실행 화면·터미널 출력·기존 승인 로그에 근거한 수동 통합 테스트이다.

| ID | 항목 | 결과 |
|---|---|---|
| TC-01 | 서버 실행 | PASS |
| TC-02 | 기본 HTTP/JSON 응답 및 기사 조회 | PASS |
| TC-03 | 대시보드 및 수동 개표 단계 변경 | PASS |
| TC-04 | WebSocket 10단계 전송, 콘솔 재생 제어, UI 완료 표시 | PASS |
| TC-05 | RAG 3개 질문 검색, 규칙·LLM 기사 생성 및 저장 | PASS |
| TC-06 | 정상 기사 및 수치 오류·근거 누락 검출 | PASS |
| TC-07 | 기존 승인 기록, 중복 승인 방지, 오류 차단, 감사 로그, 승인 원본 해시 | PASS |
| TC-08 | 영상 규격 및 사용자 직접 재생·내용 검토 | PASS |

| 검사 | 정상 기사 | 수치 오류 | 근거 누락 |
|---|---|---|---|
| 기본 | PASS | FAIL | FAIL |
| 원본 교차검증 | PASS | FAIL | PASS |
| RAG | PASS | PASS | FAIL |
| 승인 | 가능(기존 승인 이력 확인) | 차단 | 차단 |
| 테스트 판정 | PASS | PASS | PASS |

정상 기사 대표 검사 19개(기본 6, 원본 10, RAG 3). 수치 오류 기사에서 5개 오류를 검출했고 근거 누락 기사에서는 수치가 정확해도 승인을 차단했다. 상세 결과는 [통합 테스트 결과서](STEP9_Integration_Test.md) 참조.

### STEP 10 — 2026.11.27

사용자 실행 확인 및 제공된 화면을 기준으로 집계한 PC 기능 테스트 24개 항목이다. 자동화 테스트 결과나 전체 원본 데이터 검증을 의미하지 않는다.

| ID | 검증 항목 | 결과 |
|---|---|---|
| S10-01 | FastAPI 서버 실행 | PASS |
| S10-02 | 최초 접속 및 화면 초기화 | PASS |
| S10-03 | WebSocket 실시간 연결 | PASS |
| S10-04 | 1~10단계 자동 개표 | PASS |
| S10-05 | 수동 개표 단계 조회 | PASS |
| S10-06 | 후보별 득표 현황 | PASS |
| S10-07 | 지역별 개표 현황 | PASS |
| S10-08 | Plotly 득표율 그래프 | PASS |
| S10-09 | 일시정지 및 이어서 재생 | PASS |
| S10-10 | 개표 초기화 | PASS |
| S10-11 | 비동기 요청 보호(시험 범위) | PASS |
| S10-12 | WebSocket 자동 재연결 | PASS |
| S10-13 | 화면 상태 일관성 | PASS |
| S10-14 | PC 화면 레이아웃 | PASS |
| S10-15 | 개표 단계별 AI 기사 연동 | PASS |
| S10-16 | AI 기사 자동 갱신 | PASS |
| S10-17 | 0단계 기사 조회 차단 | PASS |
| S10-18 | 1단계 기사 주요 화면 수치 일치 | PASS |
| S10-19 | 5단계 기사 주요 화면 수치 일치 | PASS |
| S10-20 | 10단계 기사 주요 화면 수치 일치 | PASS |
| S10-21 | RAG 근거 ID 표시 | PASS |
| S10-22 | AI 생성 모델 정보 표시 | PASS |
| S10-23 | 편집자 승인 정보 표시 | PASS |
| S10-24 | 교육용 가상 선거 명시 | PASS |

### 대표 단계 화면 검산

| 단계 | 개표율 | 누적 개표수 | 이몽룡 | 심청 | 홍길동 |
|---|---:|---:|---:|---:|---:|
| 1 | 9.94% | 34,805 | 21,120 (61.30%) | 4,585 (13.31%) | 8,750 (25.40%) |
| 5 | 49.85% | 174,460 | 87,040 (50.40%) | 41,920 (24.27%) | 43,750 (25.33%) |
| 10 | 100.00% | 350,000 | 128,000 (36.94%) | 131,000 (37.81%) | 87,500 (25.25%) |

각 대표 화면의 지역별 합계, 후보별 득표수 및 기사에 보이는 주요 수치와 순위를 비교했다. 기사 전체 본문 및 근거 원문 대조는 이 화면 검증에 포함되지 않는다. 모바일·태블릿 테스트는 생략했다.

## 11. 최종 뉴스 영상

파일(로컬 산출물): `video/output/AIJ_P1_2026_한빛시_시장선거_AI가상개표특집_final.mp4`

| 항목 | 기존 검증 결과 |
|---|---|
| 길이 | 6분 50초 |
| 해상도 | 1920 × 1080 (FHD, 16:9) |
| 프레임 속도 | 30fps |
| 파일 크기 | 372,304,248 bytes (약 372.3 MB) |
| 오디오 | 스테레오, 44.1 kHz |
| 내용 검토 | 사용자 직접 재생 및 10개 항목 확인 완료 |

대용량 영상은 일반 Git 커밋 대신 별도 제출 파일 또는 [Google Drive 공유 링크](https://drive.google.com/file/d/1_a4BQ9g78F7yzgqDbPreUeiyYi9aAZip/view?usp=sharing)로 제공한다. 외부 사용자 접근 권한은 제출 전 별도 확인한다.

## 12. 한계 및 개선 방향

- 실제 선거 API가 아닌 내부 교육용 창작 데이터를 사용하며 외부 공식 원문 URL은 없다.
- RAG 검색은 세 가지 대표 질문에서 확인했으며 전체 검색 성능이나 의미적 사실 검증 정확도를 측정한 것은 아니다.
- STEP 10에서 단계별 UI 갱신, UI 재생 제어 및 연결 복구를 사용자 실행으로 확인했다. 재연결 시 진행 상태를 복원하지 않고 0단계에서 다시 시작한다.
- 비동기 요청 보호는 이전 응답의 반영을 차단하지만 이미 시작된 Plotly 렌더링까지 취소하지는 않는다. 모든 충돌 가능성의 제거 여부는 미확인이다.
- 1·5·10단계 기사 화면 주요 수치를 검증했으며 전체 10단계 기사 본문·CSV·JSON·RAG 근거 원문 직접 대조는 추가 검증 대상이다.
- 기사 모델명 `GPT-6.2`와 `gpt-6-luna`의 실제 생성 기록 및 식별자를 확인할 필요가 있다.
- AI 보조 판정과 규칙 판정 불일치 처리, 새 환경 설치 재현성, API 키 없는 전체 데모 재현은 별도 확인이 필요하다.
- 승인 원본 해시는 기존 대표 테스트에서 일치했으나 승인 결과 파일 전체의 무결성을 검증한 것은 아니다. 11월 25일 재생성 초안은 기존 승인본과 구분한다.
- 중복 승인 차단 경로에서 로그 저장 전에 반환하는 기존 코드가 확인되었다. 해당 시도도 감사 로그에 남기도록 개선할 수 있다.
- 가상 집계 기준시각과 실제 편집 승인 시각은 다른 의미이다. 후보명 수정 전후 자료를 구분한다.
- PC 화면 중심으로 검증했으며 모바일·태블릿 반응형 검증은 생략했다. favicon.ico 404는 확인된 기능 동작에 영향을 주지 않았다.
- 공개 전 API 키, 개인정보, 저작권, 영상 공유 권한, `.gitignore` 및 과거 Git 이력을 점검한다.

## 13. 개발 기여 및 참고 자료

개인 프로젝트로 기획, 데이터 처리, 웹서비스, RAG·기사 생성, 검증·승인, 영상 제작 및 통합 테스트를 수행했다. AI 도구는 코드 및 콘텐츠 제작을 보조하며 최종 검토 책임은 사람에게 있다.

### 제출 산출물

- [최종 보고서 (DOCX)](AIJ_P1_Final_Report.docx)
- [최종 보고서 (PDF)](AIJ_P1_Final_Report.pdf)
- [프로젝트 발표자료 (PPTX)](AIJ_P1_Presentation.pptx)
- [STEP 9 통합 테스트 결과서](STEP9_Integration_Test.md)
- [최종 AI 뉴스 영상 (Google Drive)](https://drive.google.com/file/d/1_a4BQ9g78F7yzgqDbPreUeiyYi9aAZip/view?usp=sharing)

참고: 기관 「RAG 모델 기반의 선거 보도 구성하기」 작업지시서, STEP 1 프로젝트 기획서(2026.11.11), 2026.11.25 실행 증빙 및 승인 기록, 2026.11.27 STEP 10 사용자 실행 및 화면 검증 기록.
