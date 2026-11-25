
from fastapi import FastAPI

# FastAPI 웹 서버 생성
app = FastAPI(
    title="AIJ_P1 가상 선거 개표 대시보드",
    description="2026 한빛시 시장 선거 교육용 시뮬레이션",
    version="1.0.0"
)

# 기본 접속 화면
@app.get("/")
def home():
    return {
        "project": "AIJ_P1",
        "title": "2026 한빛시 시장 선거",
        "message": "FastAPI 서버 정상 작동",
        "mode": "교육용 가상 선거",
        "status": "success"
    }


from pathlib import Path
import pandas as pd

# STEP 2 데이터 파일 위치
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "STEP2_Data" / "election_results.csv"


# 가상 선거 데이터 조회 API
@app.get("/api/election-results")
def get_election_results():
    df = pd.read_csv(DATA_FILE)

    return {
        "election": "2026 한빛시 시장 선거",
        "mode": "교육용 가상 선거",
        "total_rows": len(df),
        "data": df.to_dict(orient="records")
    }


from fastapi.responses import HTMLResponse

# HTML 대시보드 화면
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html_file = Path(__file__).resolve().parent / "templates" / "index.html"

    return HTMLResponse(
        content=html_file.read_text(encoding="utf-8")
    )

from fastapi.staticfiles import StaticFiles

# CSS, JavaScript 등 정적 파일 연결
STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# ============================================
# STEP 5 - WebSocket 연결 기능
# ============================================

import sys

from fastapi import WebSocket, WebSocketDisconnect

# STEP5_WebSocket 폴더의 모듈을 불러오기 위한 경로 설정
sys.path.insert(0, str(BASE_DIR))

from STEP5_WebSocket.websocket_manager import manager



# STEP 5-13: 실제 개표 데이터 전송
from STEP5_WebSocket.election_stream import get_step_data



# STEP 5-15: 10단계 자동 개표 데이터 전송

import asyncio

from STEP5_WebSocket.election_stream import get_step_data



# STEP 5-17: WebSocket 재생 제어 기능

import asyncio
from contextlib import suppress

from STEP5_WebSocket.election_stream import get_step_data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    current_step = 0
    is_paused = False
    playback_task = None
    playback_lock = asyncio.Lock()

    async def play_election():
        nonlocal current_step, is_paused

        try:
            while current_step < 10:
                if is_paused:
                    await asyncio.sleep(0.1)
                    continue

                async with playback_lock:
                    if is_paused:
                        continue

                    next_step = current_step + 1
                    result = get_step_data(next_step)

                    await websocket.send_json(result)
                    current_step = next_step

                    print(f"개표 {current_step}/10 단계 전송 완료")

                if current_step < 10:
                    await asyncio.sleep(2)

            if current_step == 10:
                await websocket.send_json({
                    "type": "election_complete",
                    "message": "가상 선거 개표 완료",
                    "mode": "교육용 가상 선거"
                })

        except asyncio.CancelledError:
            raise

    async def stop_playback():
        nonlocal playback_task

        if playback_task and not playback_task.done():
            playback_task.cancel()
            with suppress(asyncio.CancelledError):
                await playback_task

        playback_task = None

    try:
        while True:
            command = await websocket.receive_text()
            command = command.strip().lower()

            if command == "start":
                await stop_playback()

                async with playback_lock:
                    current_step = 0
                    is_paused = False

                playback_task = asyncio.create_task(play_election())

            elif command == "pause":
                is_paused = True

                await websocket.send_json({
                    "type": "playback_status",
                    "status": "paused",
                    "step": current_step
                })

            elif command == "resume":
                is_paused = False

                if playback_task is None or playback_task.done():
                    if current_step < 10:
                        playback_task = asyncio.create_task(
                            play_election()
                        )

                await websocket.send_json({
                    "type": "playback_status",
                    "status": "playing",
                    "step": current_step
                })

            elif command == "reset":
                await stop_playback()

                async with playback_lock:
                    current_step = 0
                    is_paused = False

                await websocket.send_json({
                    "type": "playback_status",
                    "status": "reset",
                    "step": 0
                })

            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "지원하지 않는 명령입니다.",
                    "mode": "교육용 가상 선거"
                })

    except WebSocketDisconnect:
        print("WebSocket 연결 종료")

    finally:
        await stop_playback()
        manager.disconnect(websocket)


# ============================================
# STEP 6 - RAG 기반 AI 기사 조회 API
# ============================================


import json
import hashlib
from fastapi import HTTPException


# AI 기사 및 승인 기사 저장 경로
ARTICLE_DIR = BASE_DIR / "rag" / "articles"
APPROVED_DIR = BASE_DIR / "rag" / "approved"
APPROVAL_LOG_PATH = BASE_DIR / "rag" / "approval_log.jsonl"


def get_valid_approved_article(article_file, article, article_hash):
    """현재 기사에 대한 유효한 승인 기록을 확인한다."""

    approved_file = (
        APPROVED_DIR / f"approved_{article_file.stem}.json"
    )

    if not approved_file.is_file():
        return None

    if not APPROVAL_LOG_PATH.is_file():
        return None

    try:
        with open(approved_file, "r", encoding="utf-8-sig") as file:
            approved = json.load(file)

        if not isinstance(approved, dict):
            return None

        # 1. 승인 상태 확인
        if approved.get("status") != "승인":
            return None

        # 2. 현재 기사와 승인 당시 기사 해시 비교
        if approved.get("source_article_hash") != article_hash:
            return None

        # 3. 승인 기사와 현재 초안의 데이터 비교
        for key, value in article.items():
            if key != "status" and approved.get(key) != value:
                return None

        # 4. 해당 기사의 최신 처리 이력 확인
        latest_record = None

        with open(APPROVAL_LOG_PATH, "r", encoding="utf-8-sig") as file:
            for line in file:
                if not line.strip():
                    continue

                record = json.loads(line)

                if record.get("article_file") == article_file.name:
                    latest_record = record

        if latest_record is None:
            return None

        if latest_record.get("status") != "승인":
            return None

        if latest_record.get("article_hash") != article_hash:
            return None

        # 5. 자동 검증 결과 확인
        for key in (
            "basic_validation",
            "source_validation",
            "rag_validation",
        ):
            if latest_record.get(key) is not True:
                return None

        if latest_record.get("validation_errors") != []:
            return None

        # 6. 편집자 승인 정보 일치 확인
        approval_fields = {
            "approved_by": "editor",
            "approved_at": "timestamp",
            "approval_reason": "reason",
        }

        for approved_key, log_key in approval_fields.items():
            value = approved.get(approved_key)

            if not value or value != latest_record.get(log_key):
                return None

        return approved

    except (OSError, ValueError, TypeError, AttributeError):
        return None


@app.get("/api/ai-article")
def get_ai_article(step: int = 10):
    """현재 개표 단계의 기사와 승인 상태를 조회한다."""

    # 개표 단계는 1~10 사이만 허용
    if not 1 <= step <= 10:
        raise HTTPException(
            status_code=400,
            detail="개표 단계는 1~10 사이여야 합니다."
        )

    article_file = (
        ARTICLE_DIR / f"ai_article_step_{step:02d}.json"
    )

    if not article_file.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"{step}단계 AI 기사가 아직 생성되지 않았습니다."
        )

    try:
        # 동일한 파일 내용으로 JSON 해석과 해시 계산
        article_bytes = article_file.read_bytes()
        article = json.loads(article_bytes.decode("utf-8-sig"))

        article_hash = hashlib.sha256(
            article_bytes
        ).hexdigest()

    except (OSError, ValueError):
        raise HTTPException(
            status_code=500,
            detail="AI 기사 파일을 읽을 수 없습니다."
        )

    if not isinstance(article, dict):
        raise HTTPException(
            status_code=500,
            detail="AI 기사 데이터 형식이 올바르지 않습니다."
        )

    if article.get("step") != step:
        raise HTTPException(
            status_code=500,
            detail="요청 단계와 기사 단계가 일치하지 않습니다."
        )

    # 유효한 승인 기사 확인
    approved = get_valid_approved_article(
        article_file,
        article,
        article_hash
    )

    if approved is not None:
        article = approved
    else:
        article["status"] = "검토 필요"

        # 유효하지 않은 승인 정보 제거
        for key in (
            "approved_by",
            "approved_at",
            "approval_reason",
            "source_article_hash",
        ):
            article.pop(key, None)

    # 기존 API 반환 구조 유지
    return {
        "project": "AIJ_P1",
        "mode": "가상 선거·교육용 시뮬레이션",
        "article": article
    }
