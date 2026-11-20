
# AIJ-P1 FastAPI 서버 실행 스크립트
Set-Location $PSScriptRoot

# 프로젝트 가상환경의 Python 사용
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "가상환경이 없습니다. .venv를 먼저 생성하세요."
    exit 1
}

# Python 모듈 검색 경로 설정
$env:PYTHONPATH = "src;src\STEP4_Dashboard"

# FastAPI 서버 실행
& $python -m uvicorn main:app --app-dir src/STEP4_Dashboard --reload
