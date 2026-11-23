
import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 최상위 폴더
BASE_DIR = Path(__file__).resolve().parents[2]

# .env 파일 불러오기
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# API 키 존재 여부만 확인
api_key = os.getenv("OPENAI_API_KEY")

print("=" * 50)
print("STEP 6 - OpenAI API 키 설정 테스트")
print("=" * 50)

if api_key and api_key.startswith("sk-"):
    print("성공: OPENAI_API_KEY가 정상적으로 설정되었습니다.")
else:
    print("실패: OPENAI_API_KEY 설정을 확인하세요.")

print("=" * 50)
