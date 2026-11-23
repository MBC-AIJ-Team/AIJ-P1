
import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from article_validator import (
    validate_article,
    validate_against_source,
    validate_rag_evidence,
)

import article_validator


# 프로젝트 경로
ROOT = Path(__file__).resolve().parents[2]

ARTICLE_PATH = (
    ROOT / "rag" / "articles" / "ai_article_step_10.json"
)

LOG_PATH = ROOT / "rag" / "approval_log.jsonl"
APPROVED_DIR = ROOT / "rag" / "approved"

KST = ZoneInfo("Asia/Seoul")


def current_time():
    """한국시간 반환"""
    return datetime.now(KST).isoformat(timespec="seconds")


def save_log(record):
    """승인 및 반려 기록 저장"""

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    # 실행할 기사 파일 선택
    article_path = ARTICLE_PATH

    if len(sys.argv) > 1:
        article_path = Path(sys.argv[1]).resolve()

    if not article_path.is_file():
        print("[ERROR] 기사 파일을 찾을 수 없습니다.")
        return

    # 기사 읽기
    try:
        with open(article_path, "r", encoding="utf-8-sig") as f:
            article_data = json.load(f)
    except (OSError, ValueError) as e:
        print("[ERROR] 기사 읽기 실패:", e)
        return

    # 검사 대상 파일을 검증기에 전달
    article_validator.ARTICLE_PATH = article_path

    print("\n===== STEP 7 기사 승인 관리 =====")

    # 기존 두 가지 검증 실행
    # 오류가 발생하면 검증 실패로 처리
    basic_pass = False
    source_pass = False
    rag_pass = False

    try:
        basic_pass = validate_article()
    except Exception as e:
        print("[FAIL] 기본 검증 실행 오류:", e)

    try:
        source_pass = validate_against_source()
    except Exception as e:
        print("[FAIL] 원본 교차검증 실행 오류:", e)

    try:
        rag_pass = validate_rag_evidence()
    except Exception as e:
        print("[FAIL] RAG 근거 검증 실행 오류:", e)

    verified = (
    basic_pass is True
    and source_pass is True
    and rag_pass is True
)

    print("\n===== 최종 자동 검증 상태 =====")

    if verified:
        print("[PASS] 기본·원본·RAG 근거 검증 모두 통과")
        print("사람 검토 후 승인할 수 있습니다.")
    else:
        print("[FAIL] 검증 실패")
        print("기사 승인이 차단되었습니다.")

    # 편집자 정보
    editor = input("\n편집자 이름: ").strip()

    if not editor:
        print("[ERROR] 편집자 이름은 필수입니다.")
        return

    print("\n1. 기사 승인")
    print("2. 기사 반려")

    choice = input("선택 (1/2): ").strip()

    if choice not in ("1", "2"):
        print("[ERROR] 잘못된 선택입니다.")
        return

    # 승인 요청
    
    if choice == "1":
        if not verified:
            blocked_record = {
                "article_file": article_path.name,
                "step": article_data.get("step"),
                "source_id": article_data.get("source_id"),
                "editor": editor,
                "status": "승인 차단",
                "basic_validation": basic_pass,
                "source_validation": source_pass,
                "rag_validation": rag_pass,
                "reason": "자동 검증 실패로 승인 차단",
                "timestamp": current_time(),
                "validation_errors": list(
    dict.fromkeys(article_validator.VALIDATION_ERRORS)
),
            }

            save_log(blocked_record)

            print("\n[BLOCKED] 검증 실패 기사는 승인할 수 없습니다.")
            print("[LOG] 승인 차단 이력 저장 완료")
            return


        print("\n사람 검토 체크리스트")
        print("- 기사 내용과 원본 수치 확인")
        print("- RAG 근거 문서와 공약 내용 직접 확인")
        print("- 후보·지역·시각·중립성 확인")
        print("- 가상 선거 및 AI 활용 고지 확인")

        confirm = input(
            "\n위 항목을 직접 검토했습니까? (yes/no): "
        ).strip().lower()

        if confirm not in ("y", "yes"):
            print("[BLOCKED] 사람 검토가 완료되지 않았습니다.")
            return

        reason = input("승인 사유: ").strip()

        if not reason:
            print("[ERROR] 승인 사유는 필수입니다.")
            return

        status = "승인"

    # 반려 요청
    else:
        reason = input("반려 사유: ").strip()

        if not reason:
            print("[ERROR] 반려 사유는 필수입니다.")
            return

        status = "반려"

    # 기사 원본의 SHA-256 해시값
    # 승인 기록과 기사 내용을 연결
    article_hash = hashlib.sha256(
        article_path.read_bytes()
    ).hexdigest()

    record = {
        "article_file": article_path.name,
        "article_hash": article_hash,
        "step": article_data.get("step"),
        "source_id": article_data.get("source_id"),
        "editor": editor,
        "status": status,
        "basic_validation": basic_pass,
        "source_validation": source_pass,
        "rag_validation": rag_pass,
        "reason": reason,
        "timestamp": current_time(),
        "validation_errors": list(
    dict.fromkeys(article_validator.VALIDATION_ERRORS)
),
    }

    # 승인된 기사는 별도 저장
    if status == "승인":
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)

        approved_article = article_data.copy()
        approved_article["status"] = "승인"
        approved_article["approved_by"] = editor
        approved_article["approved_at"] = record["timestamp"]
        approved_article["approval_reason"] = reason
        approved_article["source_article_hash"] = article_hash

        output_path = (
            APPROVED_DIR / f"approved_{article_path.stem}.json"
        )

        # 기존 승인 파일을 덮어쓰지 않도록 처리
        if output_path.exists():
            print("[BLOCKED] 이미 승인된 출력 파일이 있습니다.")
            print("기존 승인 기록을 확인하세요.")
            return

        with open(output_path, "x", encoding="utf-8") as f:
            json.dump(
                approved_article,
                f,
                ensure_ascii=False,
                indent=2,
            )

        print("\n[SUCCESS] 기사 승인 완료")
        print("승인 기사:", output_path)

    else:
        print("\n[REJECTED] 기사 반려 완료")

    # 처리 이력 기록
    save_log(record)

    print("승인·반려 로그:", LOG_PATH)
    print("최종 상태:", status)


if __name__ == "__main__":
    main()
