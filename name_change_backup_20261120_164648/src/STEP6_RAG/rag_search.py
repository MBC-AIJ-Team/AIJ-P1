
import re

from document_loader import load_documents


# 가상 후보 이름과 검색에 사용할 핵심 단어
KEYWORDS = {
    "이몽룡": ["이몽룡", "교통", "광역교통망", "도시개발"],
    "심청이": ["심청이", "주거", "청년", "복지"],
    "홍길동": ["홍길동", "소상공인", "지역경제", "일자리"],
}

STOPWORDS = {
    "후보", "공약", "정책", "주요", "무엇인가",
    "무엇", "알려줘", "설명해줘", "어떤", "대한",
}


def tokenize(text):
    """질문에서 검색에 사용할 단어를 추출한다."""
    words = re.findall(r"[가-힣A-Za-z0-9]+", text.lower())
    return [word for word in words if word not in STOPWORDS]


def search_documents(query, top_k=3):
    """질문과 관련된 RAG 문서를 검색한다."""

    documents = load_documents()
    query_words = tokenize(query)

    if not query_words:
        return []

    # 질문에 명시된 후보 이름을 우선 확인
    target_candidates = [
        name for name in KEYWORDS if name in query
    ]

    results = []

    for document in documents:
        content = (
            document["title"] + " " + document["text"]
        ).lower()

        score = 0

        for word in query_words:
            if word in content:
                score += 1

        # 후보 이름이 명시된 질문은 해당 후보 문서를 우선
        for candidate in target_candidates:
            if candidate in content:
                score += 10

        if score > 0:
            results.append({
                "document_id": document["document_id"],
                "title": document["title"],
                "text": document["text"],
                "source_id": document["source_id"],
                "citation_label": document["citation_label"],
                "score": score,
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]


if __name__ == "__main__":
    questions = [
        "심청이 후보의 주요 공약은?",
        "이몽룡 후보의 교통 정책은?",
        "홍길동 후보의 소상공인 지원 정책은?",
    ]

    for question in questions:
        print("\n" + "=" * 60)
        print(f"질문: {question}")

        results = search_documents(question, top_k=1)

        if not results:
            print("검색된 근거 문서가 없습니다.")
            continue

        for result in results:
            print(f"근거 ID: {result['document_id']}")
            print(f"문서 제목: {result['title']}")
            print(f"근거 내용: {result['text']}")
            print(f"출처: {result['citation_label']}")
