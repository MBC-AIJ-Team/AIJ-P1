# AIJ-P1 | RAG 기반 가상 선거 개표 및 AI 뉴스 보도 시스템

## 1. 프로젝트 소개
AI 데이터 저널리즘 교육을 위한 가상 선거 보도 프로젝트입니다.

가상의 후보 3명과 가상 개표 데이터를 활용하여 실시간 개표 현황을 시각화하고, RAG 기반 AI 기사를 생성·검증한 후 뉴스 영상으로 제작합니다.

> 본 프로젝트의 선거, 후보, 정당, 개표 결과는 모두 교육용 가상 데이터이며 실제 선거와 관계없습니다.

## 2. 프로젝트 목표
- Python을 이용한 가상 선거 데이터 생성 및 분석
- WebSocket 기반 실시간 개표 시뮬레이션
- 후보별·지역별 득표 현황 웹 대시보드
- RAG 기반 근거 검색 및 AI 기사 생성
- 수치 오류 자동 검증 및 편집자 승인
- 10분 이내 FHD AI 뉴스 영상 제작

## 3. 가상 선거 개요
- 선거명: 2026 한빛시 시장 선거 (가상)
- 후보: 이몽룡, 심청, 홍길동
- 지역: 중앙구, 동부구, 서부구, 남부구, 북부구
- 선거인 수: 500,000명
- 예상 투표자 수: 350,000명
- 개표 시뮬레이션: 10단계

## 4. 개발 환경
- OS: Windows 11
- Editor: VS Code
- Language: Python 3.14.7 (패키지 호환성 확인 필요)
- Data: pandas, CSV, JSON, SQLite
- Backend: FastAPI, WebSocket
- Visualization: Plotly
- AI: RAG, LLM
- Version Control: Git, GitHub
- Video: AI 영상 도구, CapCut 또는 Premiere Pro

## 5. 시스템 처리 흐름
1. 가상 선거 데이터 생성
2. 데이터 정제 및 분석
3. FastAPI 서버에서 데이터 제공
4. WebSocket 실시간 개표 시뮬레이션
5. RAG 검색 및 AI 기사 초안 생성
6. 데이터·근거 기반 오류 검증
7. 편집자 최종 승인
8. 승인된 기사로 뉴스 영상 제작

## 6. 프로젝트 개발 단계
- STEP 1: 프로젝트 기획
- STEP 2: 가상 데이터 생성
- STEP 3: Python 데이터 분석
- STEP 4: 웹 대시보드 개발
- STEP 5: WebSocket 구현
- STEP 6: RAG 및 AI 기사 생성
- STEP 7: 기사 검증 및 승인
- STEP 8: FHD 뉴스 영상 제작
- STEP 9: 통합 테스트 및 발표

## 7. 실행 방법

### 개발 환경
- Windows 11
- Python 3.12.10
- VS Code

### 최초 실행 준비
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### FastAPI 서버 실행
프로젝트 최상위 폴더에서 실행합니다.

```powershell
.\run_server.ps1
```

### 접속 주소
- 대시보드: http://127.0.0.1:8000/dashboard
- 선거 데이터 API: http://127.0.0.1:8000/api/election-results
- WebSocket: ws://127.0.0.1:8000/ws

### 서버 종료
서버 실행 터미널에서 Ctrl + C를 누릅니다.

> 본 프로젝트의 모든 선거 데이터는 교육용 가상 데이터입니다.

## 8. 테스트

2026-11-23 기준 Windows 11 · VS Code에서 사용자가 수행한 테스트와 캡처 화면을 통해 아래 항목을 확인했습니다.

| 항목 | 확인 결과 |
|---|---|
| FastAPI 시작 | `Application startup complete` 확인 |
| 개표 데이터 조회 | `/api/election-results`에서 가상 개표 데이터 150행 반환 |
| WebSocket 재생 | 1~10단계 자동 진행 및 완료 |
| 재생 제어 | 4단계 일시정지, 이어서 10단계 완료, 초기화 0/10 확인 |
| AI 기사 조회 | 기사 본문·상태·근거 ID·기준시각 화면 출력 |
| 정상 기사 검증 | 기본·원본 데이터·RAG 근거 3종 검사 통과 |
| 오류 기사 검증 | 득표수·득표율·1·2위 격차 오류 검출 |
| 승인 차단 | 오류 기사 승인 시도 차단 및 로그 추가 확인 (2026-11-23 12:38:06+09:00) |
| 승인 기사 해시 | 승인 로그의 SHA-256과 원본 기사 파일 해시 일치 |
| STEP 8 대본 | TTS 텍스트 대본 20장면과 원본 가상 선거 자료 대조 완료 |

> 테스트의 '통과'는 실제 확인한 조건에 한정합니다. 전체 예외·부하 테스트, 최종 MP4의 실제 음성·자막·CG 검수는 완료되지 않았습니다.

- [AIJ_P1_통합테스트_결과서_v1.0.docx](reports/AIJ_P1_%ED%86%B5%ED%95%A9%ED%85%8C%EC%8A%A4%ED%8A%B8_%EA%B2%B0%EA%B3%BC%EC%84%9C_v1.0.docx)
- [AIJ_P1_AI_성능_평가_보고서_v1.0.docx](reports/AIJ_P1_AI_%EC%84%B1%EB%8A%A5_%ED%8F%89%EA%B0%80_%EB%B3%B4%EA%B3%A0%EC%84%9C_v1.0.docx)

## 9. 최종 산출물

- 설계 문서: [docs/](docs/) — 기획서, 요구사항 정의서, ERD, 화면 설계서, API 명세서, RAG·프롬프트 설계서
- 프로그램 및 데이터: [src/](src/), [data/](data/), [rag/](rag/) — Python, FastAPI, WebSocket, 기사 생성·검증·승인
- 평가 및 테스트: [reports/](reports/) — 데이터셋, 성능 평가, 통합 테스트, 대본 수치 검증
- 영상 자산: [video/](video/) — TTS, 차트, LED 그래픽, 개표 영상 클립
- 미완료 제출물: 최종 뉴스 영상, 시스템 시연 영상, 발표 PPT, 최종 보고서

## 10. 프로젝트 운영
- Organization: MBC-AIJ-Team
- Repository: AIJ-P1
- 개발 형태: 1인 개발 (향후 팀 협업 가능)
- 프로젝트 기간: 2026.11.18 ~ 2026.11.27

## 11. AI 활용 및 보도 윤리
- 실제 선거로 오인되지 않도록 가상 선거임을 명시합니다.
- AI 생성 기사는 근거와 수치를 검증합니다.
- 승인되지 않은 기사는 최종 뉴스에 사용하지 않습니다.
- AI 이미지·영상·음성 사용 여부를 표시합니다.

## 12. 프로젝트 산출물 관리 현황

**기준일: 2026-11-23.** '문서 등록'은 GitHub에서 파일 존재를 확인한 상태로, 모든 기능과 내용의 검증이 완료되었다는 뜻은 아닙니다.

### 12.1 핵심 산출물 8종

| 번호 | 산출물 | 상태 | 문서/코드 |
|---|---|---|---|
| 1 | 기획서 | 등록 | [AIJ_P1_프로젝트 기획서.docx](docs/AIJ_P1_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B8%B0%ED%9A%8D%EC%84%9C.docx) |
| 2 | 요구사항 정의서 | 등록 | [AIJ_P1_요구사항_정의서_v1.0.docx](docs/AIJ_P1_%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD_%EC%A0%95%EC%9D%98%EC%84%9C_v1.0.docx) |
| 3 | ERD | 등록 | [AIJ_P1_ERD_설계서_v1.0.docx](docs/AIJ_P1_ERD_%EC%84%A4%EA%B3%84%EC%84%9C_v1.0.docx) · [AIJ_P1_ERD_설계_v1.0.md](docs/AIJ_P1_ERD_%EC%84%A4%EA%B3%84_v1.0.md) |
| 4 | 화면 설계서 | 등록 | [AIJ_P1_화면_설계서_v1.0.docx](docs/AIJ_P1_%ED%99%94%EB%A9%B4_%EC%84%A4%EA%B3%84%EC%84%9C_v1.0.docx) |
| 5 | API 명세서 | 등록 | [AIJ_P1_API_명세서_v1.0.docx](docs/AIJ_P1_API_%EB%AA%85%EC%84%B8%EC%84%9C_v1.0.docx) |
| 6 | 소스코드 | 핵심 기능 구현·테스트 | [src/](src/) |
| 7 | 발표 PPT | 제작 예정 | [presentation/](presentation/) |
| 8 | 시연 영상 | 제작 예정 | [video/](video/) (현재는 뉴스 영상 제작 자산 보관) |

### 12.2 AI 프로젝트 추가 산출물

| 산출물 | 상태 | 설명 및 위치 |
|---|---|---|
| AI 모델 파일(.pkl, .h5) | 별도 학습 모델 없음 | 기존 LLM API 사용, 임의 모델 파일 만들지 않음 |
| 학습·평가 데이터셋 | 가상 원본·평가셋 등록 | [data/](data/), [AIJ_P1_RAG_평가데이터셋_v1.0.csv](reports/AIJ_P1_RAG_%ED%8F%89%EA%B0%80%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B_v1.0.csv), [AIJ_P1_기사검증_평가데이터셋_v1.0.csv](reports/AIJ_P1_%EA%B8%B0%EC%82%AC%EA%B2%80%EC%A6%9D_%ED%8F%89%EA%B0%80%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B_v1.0.csv) |
| 성능 평가 보고서 | 등록 | [AIJ_P1_AI_성능_평가_보고서_v1.0.docx](reports/AIJ_P1_AI_%EC%84%B1%EB%8A%A5_%ED%8F%89%EA%B0%80_%EB%B3%B4%EA%B3%A0%EC%84%9C_v1.0.docx), [AIJ_P1_평가결과_v1.0.json](reports/AIJ_P1_%ED%8F%89%EA%B0%80%EA%B2%B0%EA%B3%BC_v1.0.json) |
| 프롬프트 설계서 | 등록 | [AIJ_P1_프롬프트_설계서_v1.0.docx](docs/AIJ_P1_%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8_%EC%84%A4%EA%B3%84%EC%84%9C_v1.0.docx) |
| RAG 문서·벡터 DB 설계서 | 검색 구조 설계서 등록 | [AIJ_P1_RAG_문서_검색구조_설계서_v1.0.docx](docs/AIJ_P1_RAG_%EB%AC%B8%EC%84%9C_%EA%B2%80%EC%83%89%EA%B5%AC%EC%A1%B0_%EC%84%A4%EA%B3%84%EC%84%9C_v1.0.docx) — 현행 구현에서 벡터 DB는 미사용 |

### 12.3 추가 자료

- [통합 시스템 설계서 v0.1.docx](docs/%ED%86%B5%ED%95%A9%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%EC%84%9C%20v0.1.docx) — 통합 설계 초안
- [AIJ_P1_통합테스트_결과서_v1.0.docx](reports/AIJ_P1_%ED%86%B5%ED%95%A9%ED%85%8C%EC%8A%A4%ED%8A%B8_%EA%B2%B0%EA%B3%BC%EC%84%9C_v1.0.docx) — 수동 통합 테스트 결과
- [AIJ_P1_STEP8_뉴스대본_수치검증_결과서_v1.0.docx](reports/AIJ_P1_STEP8_%EB%89%B4%EC%8A%A4%EB%8C%80%EB%B3%B8_%EC%88%98%EC%B9%98%EA%B2%80%EC%A6%9D_%EA%B2%B0%EA%B3%BC%EC%84%9C_v1.0.docx) — STEP 8 대본 원본 수치 대조
- [AIJ_P1_STEP8_대본20개_검증표_v1.0.csv](reports/AIJ_P1_STEP8_%EB%8C%80%EB%B3%B820%EA%B0%9C_%EA%B2%80%EC%A6%9D%ED%91%9C_v1.0.csv) — 장면 20개별 체크표
- WBS·사용자 매뉴얼·최종 보고서: 제출 기준에 따라 추가 정리 예정

## 13. RAG 및 AI 모델 구현 범위

현재 `src/STEP6_RAG/rag_search.py`는 `data/STEP2_Data/policy_documents.json`의 **가상 정책·규칙 문서 6개**를 키워드 점수 방식으로 검색하고 문서 ID를 반환합니다.

- **실제 구현:** 키워드 기반 검색, 문서 근거 ID, 규칙 기반 기사 초안, LLM API로 문장 작성, 수치·원본·근거 검사, 사람 승인
- **미구현:** 문서 임베딩·벡터 DB, 별도 학습 모델 파일
- **확인 필요:** 코드에 적힌 LLM 모델명과 실제 API 이용 가능 여부, 광범위한 시스템 성능

소규모 평가셋의 성적을 전체 모델의 보편적 정확도로 해석하지 않습니다.

## 14. STEP 8 뉴스 영상 제작 현황

| 항목 | 현재 확인 결과 | 상태 |
|---|---|---|
| TTS 텍스트 대본 | 20개, 개표율·득표수·공약·근거 ID 대조 | 검증 완료 |
| TTS MP3 | 20개, ffprobe 실측 **388.82초(6분 28.82초)** | 파일·길이 확인; 실제 음성 발화 내용 미검증 |
| 개표 영상 | `video/clips/hanbit_counting_10steps.mp4`, 30초, FHD 1920×1080, 30fps, H.264 | 규격 확인 |
| 차트·LED | 득표율 차트 10개, LED 이미지 10개 | 파일 존재 확인 |
| 편집 제작표 | 목표 길이 8분 30초, 계획상 추가 화면 121.18초 | 제작표 준비; GitHub 등록 여부 별도 확인 |
| 최종 뉴스 MP4 | 편집·렌더링·최종 QC | 미완료 |

> **8분 30초는 제작 목표값**입니다. 완성한 뉴스 영상의 실측 길이로 기재하지 않습니다.

## 15. 남은 작업

1. STEP 8 뉴스 영상 편집 및 MP3 발화·자막·CG 수치 검수
2. 최종 FHD MP4의 길이·해상도·고지 문구 확인
3. 시스템 시연 영상 제작
4. 발표 PPT 및 최종 보고서 작성
5. README와 제출물의 최종 정합성 확인
