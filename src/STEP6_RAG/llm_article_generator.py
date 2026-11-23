
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from article_generator import generate_article


# 1. 프로젝트 경로 및 API 키 설정
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

client = OpenAI(api_key=api_key)


# 2. AI 기사 생성 함수
def generate_ai_article(step_number=10):

    # 기존 STEP 6-6에서 만든 근거 기반 기사
    source_article = generate_article(step_number)

    # AI에 전달할 작성 지침
    instructions = """
당신은 교육용 가상 선거 뉴스 기자입니다.

다음 규칙을 반드시 지키세요.

1. 입력 자료에 있는 사실만 사용합니다.
2. 득표수, 득표율, 후보명, 기준시각을 변경하지 않습니다.
3. 없는 정보나 후보 발언을 만들어내지 않습니다.
4. 특정 후보를 지지하거나 비방하지 않습니다.
5. 기사 첫머리에 '가상 선거·교육용 시뮬레이션'을 표시합니다.
6. 객관적이고 자연스러운 한국어 뉴스 문체로 작성합니다.
7. 제목과 본문을 작성합니다.
8. 후보 공약을 언급할 때 근거 문서 ID를 표시합니다.
9. 당선 확정 여부는 입력 자료에 명시되지 않았다면 단정하지 않습니다.
10. 입력 자료에 없는 원인 분석이나 예측을 추가하지 않습니다.

분량은 제목을 제외하고 약 400~600자로 작성하세요.
"""

    user_input = f"""
다음 자료를 바탕으로 뉴스 기사 초안을 작성하세요.

[원본 기사 제목]
{source_article['title']}

[원본 기사 본문 및 RAG 근거]
{source_article['body']}

[개표 기준시각]
{source_article['timestamp']}

[근거 문서 ID]
{', '.join(source_article['evidence_ids'])}

위 자료에 포함된 수치와 근거만 사용하세요.
"""

    # 3. OpenAI API 호출
  
    # 3. OpenAI API 호출
    response = client.responses.create(
        model="gpt-6-luna",
        instructions=instructions,
        input=user_input,
        max_output_tokens=1200,
        store=False,
    )

    if not response.output_text:
        raise ValueError("AI 기사 생성 결과가 비어 있습니다.")


    # 4. 결과 정리
    result = {
        "article": response.output_text,
        "step": source_article["step"],
        "timestamp": source_article["timestamp"],
        "source_id": source_article["source_id"],
        "evidence_ids": source_article["evidence_ids"],
        "status": "검토 필요",
        "is_synthetic": True,
        "generation_method": "openai_llm",
        "model": "gpt-6-luna",
    }

    return result


# 5. 실행 테스트

def save_ai_article(result):
    """생성한 AI 기사 초안을 JSON 파일로 저장한다."""

    output_dir = BASE_DIR / "rag" / "articles"
    output_dir.mkdir(parents=True, exist_ok=True)

    step_number = result["step"]
    output_path = output_dir / f"ai_article_step_{step_number:02d}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    return output_path


if __name__ == "__main__":

    print("=" * 60)
    print("STEP 6 - OpenAI RAG 뉴스 기사 생성")
    print("=" * 60)

    try:
        result = generate_ai_article(step_number=10)

        saved_path = save_ai_article(result)
        print(f"\n기사 저장 완료: {saved_path}")


        print("\n[AI 생성 기사]")
        print(result["article"])

        print("\n[기사 정보]")
        print("개표 단계:", result["step"])
        print("기준시각:", result["timestamp"])
        print("근거 ID:", result["evidence_ids"])
        print("검토 상태:", result["status"])
        print("사용 모델:", result["model"])

    except Exception as error:
        print(f"\n기사 생성 실패: {type(error).__name__}")
        print(str(error))
