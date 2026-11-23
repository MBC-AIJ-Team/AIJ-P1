
import json
from pathlib import Path

from rag_search import search_documents


# 프로젝트 최상위 경로
BASE_DIR = Path(__file__).resolve().parents[2]

SUMMARY_PATH = (
    BASE_DIR / "data" / "STEP2_Data"
    / "election_summary.json"
)


def generate_article(step_number=10):
    """개표 데이터와 RAG 근거로 기사 초안을 생성한다."""

    with open(SUMMARY_PATH, "r", encoding="utf-8") as file:
        election = json.load(file)

    steps = election["steps"]

    # 요청한 개표 단계 선택
    step = next(
        (item for item in steps
         if item["step"] == step_number),
        None
    )

    if step is None:
        raise ValueError("존재하지 않는 개표 단계입니다.")

    # 득표수 기준 정렬
    results = sorted(
        step["candidate_results"],
        key=lambda item: item["votes"],
        reverse=True,
    )

    first = results[0]
    second = results[1]
    third = results[2]

    # 원본 득표율 및 격차 사용
    progress = step["count_progress_pct"]
    margin = first["votes"] - second["votes"]

    # 후보별 RAG 근거 검색
    evidence = []

    for candidate in results:
        query = f"{candidate['name']} 후보 정책 소개"
        matches = search_documents(query, top_k=1)

        if not matches:
            raise ValueError(
                f"{candidate['name']} 후보의 근거가 없습니다."
            )

        doc = matches[0]

        # 다른 후보 문서가 검색되었는지 확인
        if candidate["name"] not in doc["text"]:
            raise ValueError(
                f"{candidate['name']} 근거 문서가 일치하지 않습니다."
            )

        evidence.append(doc)

    # 개표 단계에 따른 제목
    if progress == 100:
        headline = (
            f"[가상 선거] 한빛시 개표 완료…"
            f"{first['name']} 1위"
        )
    else:
        headline = (
            f"[가상 선거] 개표율 {progress:.1f}%…"
            f"{first['name']} 선두"
        )

    body = (
        f"{election['election']}의 "
        f"{step_number}단계 개표 결과, "
        f"{first['name']} 후보가 "
        f"{first['votes']:,}표"
        f"({first['vote_share_pct']:.2f}%)로 "
        f"1위를 기록했다.\n\n"

        f"2위 {second['name']} 후보는 "
        f"{second['votes']:,}표"
        f"({second['vote_share_pct']:.2f}%), "
        f"3위 {third['name']} 후보는 "
        f"{third['votes']:,}표"
        f"({third['vote_share_pct']:.2f}%)를 "
        f"기록했다.\n\n"

        f"1위와 2위의 득표 차이는 "
        f"{margin:,}표이며, "
        f"현재 개표율은 {progress:.2f}%다.\n\n"

        f"후보별 주요 정책은 다음과 같다.\n"
    )

    for doc in evidence:
        body += f"\n[{doc['document_id']}] {doc['text']}\n"

    body += (
        "\n이 기사는 가상 선거 데이터를 활용한 "
        "교육용 시뮬레이션이며, "
        "실제 선거 결과가 아니다."
    )

    article = {
        "title": headline,
        "body": body,
        "step": step_number,
        "timestamp": step["timestamp"],
        "source_id": election["source_id"],
        "evidence_ids": [
            doc["document_id"] for doc in evidence
        ],
        "status": "검토 필요",
        "is_synthetic": True,
        "generation_method": "rule_based_draft",
    }

    return article


if __name__ == "__main__":
    article = generate_article(step_number=10)

    print("=" * 60)
    print("STEP 6 - 근거 기반 뉴스 기사 생성 테스트")
    print("=" * 60)

    print("\n[기사 제목]")
    print(article["title"])

    print("\n[기사 본문]")
    print(article["body"])

    print("\n[기사 정보]")
    print("개표 단계:", article["step"])
    print("기준시각:", article["timestamp"])
    print("근거 ID:", article["evidence_ids"])
    print("기사 상태:", article["status"])
    print("생성 방식:", article["generation_method"])
