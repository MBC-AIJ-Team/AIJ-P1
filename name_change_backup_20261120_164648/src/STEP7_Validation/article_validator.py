
import json
import re
from pathlib import Path
from datetime import datetime
from xml.parsers.expat import errors

# 프로젝트 최상위 경로
ROOT = Path(__file__).resolve().parents[2]

ARTICLE_PATH = ROOT / "rag" / "articles" / "ai_article_step_10.json"

CANDIDATES = ["심청이", "이몽룡", "홍길동"]


def validate_article():
    with open(ARTICLE_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    article = data.get("article", "")
    errors = []
    checks = []

    global VALIDATION_ERRORS
    VALIDATION_ERRORS = []

    # 1. 교육용 가상 선거 표시
    if data.get("is_synthetic") is True and "교육용 시뮬레이션" in article:
        checks.append("가상 선거 표시 확인")
    else:
        errors.append("가상 선거 표시 누락")

    # 2. 개표 단계 확인
    if data.get("step") == 10:
        checks.append("개표 단계 확인")
    else:
        errors.append("개표 단계 불일치")

    # 3. 후보별 득표수 및 득표율 추출
    results = {}

    for name in CANDIDATES:
        pattern = rf"{name} 후보(?:는|가)?\s*(\d[\d,]*)표\s*\(([\d.]+)%\)"
        match = re.search(pattern, article)

        if match:
            votes = int(match.group(1).replace(",", ""))
            rate = float(match.group(2))
            results[name] = (votes, rate)
        else:
            errors.append(f"{name} 후보 득표 정보 확인 실패")

    # 4. 기사 내부 득표율 계산 확인
    if len(results) == 3:
        total = sum(votes for votes, rate in results.values())

        for name, (votes, rate) in results.items():
            calculated = round(votes / total * 100, 2) if total else 0

            if abs(calculated - rate) > 0.01:
                errors.append(f"{name} 득표율 계산 오류")

        if not any("득표율 계산 오류" in e for e in errors):
            checks.append("기사 내부 득표율 계산 일치")

        # 5. 1위와 2위 격차 확인
        sorted_votes = sorted(
            [votes for votes, rate in results.values()],
            reverse=True
        )
        gap = sorted_votes[0] - sorted_votes[1]

        gap_match = re.search(r"득표 차이는\s*([\d,]+)표", article)

        if gap_match and int(gap_match.group(1).replace(",", "")) == gap:
            checks.append("득표 차이 계산 일치")
        else:
            errors.append("득표 차이 불일치")

    # 6. RAG 근거 ID 형식 확인
    evidence_ids = data.get("evidence_ids", [])

    if evidence_ids and all(eid in article for eid in evidence_ids):
        checks.append("기사 내 근거 ID 표기 확인")
    else:
        errors.append("근거 ID 누락 또는 불일치")

    # 7. 기준시각 형식 확인
    try:
        datetime.fromisoformat(data["timestamp"])
        checks.append("기준시각 형식 확인")
    except (KeyError, ValueError, TypeError):
        errors.append("기준시각 형식 오류")

    print("\n===== STEP 7 기사 기본 검증 =====")

    for check in checks:
        print("[PASS]", check)

    for error in errors:
        print("[FAIL]", error)
        VALIDATION_ERRORS.extend(errors)

    print("\n검사 오류 수:", len(errors))

    if errors:
        print("결과: 검증 실패 / 승인 차단")
        return False
    else:
        print("결과: 기본 검사 통과 / 원본 데이터 대조 필요")
        return True



def validate_against_source():
    """AI 기사와 STEP 2 원본 개표 데이터 비교"""

    summary_path = ROOT / "data" / "STEP2_Data" / "election_summary.json"

    with open(ARTICLE_PATH, "r", encoding="utf-8-sig") as f:
        article_data = json.load(f)

    with open(summary_path, "r", encoding="utf-8-sig") as f:
        source_data = json.load(f)

    article = article_data["article"]
    step_number = article_data["step"]

    errors = []

    # 같은 개표 단계의 데이터 검색
    source_step = next(
        (s for s in source_data["steps"] if s["step"] == step_number),
        None
    )

    if source_step is None:
        print("[FAIL] 원본 개표 단계 없음")
        return False

    print("\n===== STEP 7 원본 데이터 교차검증 =====")

    # 1. 데이터 출처 확인
    if article_data["source_id"] == source_data["source_id"]:
        print("[PASS] 데이터 출처 일치")
    else:
        errors.append("데이터 출처 불일치")

    # 2. 개표 기준시각 확인
    if article_data["timestamp"] == source_step["timestamp"]:
        print("[PASS] 개표 기준시각 일치")
    else:
        errors.append("기준시각 불일치")

    # 3. 후보별 득표수와 득표율 확인
    for candidate in source_step["candidate_results"]:
        name = candidate["name"]
        votes = candidate["votes"]
        rate = candidate["vote_share_pct"]

        pattern = rf"{name} 후보(?:는|가)?\s*([\d,]+)표\s*\(([\d.]+)%\)"
        match = re.search(pattern, article)

        if match is None:
            errors.append(f"{name} 기사 데이터 누락")
            continue

        article_votes = int(match.group(1).replace(",", ""))
        article_rate = float(match.group(2))

        if article_votes == votes:
            print(f"[PASS] {name} 득표수 일치")
        else:
            errors.append(f"{name} 득표수 불일치")

        if abs(article_rate - rate) <= 0.0051:
            print(f"[PASS] {name} 득표율 일치")
        else:
            errors.append(f"{name} 득표율 불일치")

    # 4. 1위와 2위 득표 차이 확인
    gap_match = re.search(r"득표 차이는\s*([\d,]+)표", article)

    if gap_match:
        article_gap = int(gap_match.group(1).replace(",", ""))

        if article_gap == source_step["margin_votes"]:
            print("[PASS] 1·2위 득표 차이 일치")
        else:
            errors.append("득표 차이 불일치")
    else:
        errors.append("득표 차이 정보 누락")

    # 5. 개표율 확인
    progress_match = re.search(r"개표율은\s*([\d.]+)%", article)

    if progress_match:
        article_progress = float(progress_match.group(1))

        if abs(article_progress - source_step["count_progress_pct"]) <= 0.0051:
            print("[PASS] 개표율 일치")
        else:
            errors.append("개표율 불일치")
    else:
        errors.append("개표율 정보 누락")

    # 결과 출력
    for error in errors:
        print("[FAIL]", error)

    VALIDATION_ERRORS.extend(errors)

    if errors:
        print("\n결과: 원본 데이터 검증 실패 / 승인 차단")
        return False

    print("\n결과: 원본 데이터 교차검증 통과")
    return True


if __name__ == "__main__":
    validate_article()
    validate_against_source()



def validate_rag_evidence():
    """기사의 RAG 근거 ID와 실제 정책 문서 비교"""

    policy_path = (
        ROOT / "data" / "STEP2_Data" / "policy_documents.json"
    )

    with open(ARTICLE_PATH, "r", encoding="utf-8-sig") as f:
        article_data = json.load(f)

    with open(policy_path, "r", encoding="utf-8-sig") as f:
        documents = json.load(f)

    article = article_data["article"]
    evidence_ids = article_data.get("evidence_ids", [])
    source_id = article_data.get("source_id")

    # 현재 가상 선거의 후보별 공약 기준
    expected = {
        "DOC-002": ("C01", "이몽룡", "광역교통망 확충"),
        "DOC-003": ("C02", "심청이", "청년 주거 지원"),
        "DOC-004": ("C03", "홍길동", "소상공인 지원"),
    }

    doc_map = {
        doc["document_id"]: doc
        for doc in documents
    }

    errors = []

    print("\n===== STEP 7 RAG 근거 자동 검증 =====")

    if not evidence_ids:
        errors.append("기사에 연결된 RAG 근거가 없습니다.")

    for evidence_id in evidence_ids:

        if evidence_id not in doc_map:
            errors.append(f"{evidence_id}: 근거 문서 없음")
            continue

        doc = doc_map[evidence_id]

        if evidence_id not in article:
            errors.append(f"{evidence_id}: 기사 내 인용 누락")
            continue

        if doc.get("source_id") != source_id:
            errors.append(f"{evidence_id}: 데이터 출처 불일치")
            continue

        if evidence_id in expected:
            candidate_id, name, policy = expected[evidence_id]

            if doc.get("candidate_id") != candidate_id:
                errors.append(f"{evidence_id}: 후보 ID 불일치")
                continue

            if name not in doc.get("text", ""):
                errors.append(f"{evidence_id}: 후보 이름 불일치")
                continue

            if policy not in doc.get("text", ""):
                errors.append(f"{evidence_id}: 근거 문서 공약 불일치")
                continue

            # 후보·공약·근거 ID가 기사에서 함께 연결되는지 확인
            pattern = (
                rf"{re.escape(name)} 후보"
                rf"(?:(?![.!?\n]).)*?"
                rf"{re.escape(policy)}"
                rf"(?:(?![.!?\n]).)*?"
                rf"\({re.escape(evidence_id)}\)"
            )

            if not re.search(pattern, article):
                errors.append(
                    f"{evidence_id}: 기사 내 후보·공약·근거 연결 불일치"
                )
                continue

        print(f"[PASS] {evidence_id}: 근거 문서 확인")

    # 기사에 인용된 정책 근거가 목록에서 빠졌는지 확인
    cited_ids = set(re.findall(r"\(DOC-\d+\)", article))
    cited_ids = {item.strip("()") for item in cited_ids}

    if cited_ids != set(evidence_ids):
        errors.append("기사의 근거 ID와 evidence_ids 목록 불일치")

    # 현재 기사는 후보 3명의 공약을 모두 소개하므로
    # 세 가지 정책 근거가 모두 필요한지 확인
    if article_data.get("step") == 10:
        missing = set(expected) - set(evidence_ids)

        if missing:
            errors.append(
                "최종 기사 정책 근거 누락: " + ", ".join(sorted(missing))
            )

    for error in errors:
        print("[FAIL]", error)

    if errors:
        print("\n결과: RAG 근거 검증 실패 / 승인 차단")
        return False

    print("\n결과: RAG 근거 검증 통과")
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        ARTICLE_PATH = Path(sys.argv[1]).resolve()

    validate_article()
    validate_against_source()
    validate_rag_evidence()