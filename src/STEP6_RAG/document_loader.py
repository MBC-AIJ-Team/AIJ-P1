
import json
from pathlib import Path


# 프로젝트 최상위 폴더
BASE_DIR = Path(__file__).resolve().parents[2]

# STEP 2에서 만든 RAG 문서
DOCUMENT_PATH = BASE_DIR / "data" / "STEP2_Data" / "policy_documents.json"


def load_documents():
    """가상 선거 정책 문서를 불러온다."""

    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(
            f"문서 파일을 찾을 수 없습니다: {DOCUMENT_PATH}"
        )

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("문서 데이터는 JSON 배열이어야 합니다.")

    required_fields = {"document_id", "title", "text"}

    for document in documents:
        if not isinstance(document, dict):
            raise ValueError("각 문서는 JSON 객체여야 합니다.")

        if not required_fields.issubset(document):
            raise ValueError(
                f"필수 필드가 누락되었습니다: {document}"
            )

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print("=" * 50)
    print("STEP 6 - RAG 문서 불러오기 테스트")
    print("=" * 50)

    print(f"불러온 문서 수: {len(documents)}개")

    for document in documents:
        print(
            f"[{document['document_id']}] "
            f"{document['title']}"
        )

    print("=" * 50)
    print("RAG 문서 불러오기 완료")
