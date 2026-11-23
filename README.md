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
개발 진행 후 작성 예정

## 9. 최종 산출물
- 프로젝트 기획서 및 데이터셋
- Python 분석 코드 및 웹 대시보드
- RAG 기사 생성 및 팩트체크 시스템
- 검증·승인 이력
- 10분 이내 FHD 뉴스 영상
- README 및 발표 PPT

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
