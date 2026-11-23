"""AIJ-P1 선거 특집: Google Cloud WaveNet 장면별 TTS MP3 생성.

사용: python generate_step8_tts.py --key 'C:/private/google_tts_key.json'
사전 설치: python -m pip install google-cloud-texttospeech
키는 Git 프로젝트 밖에 보관하세요. 이 스크립트는 키를 복사하거나 출력하지 않습니다.
"""
import argparse
import json
from pathlib import Path

VOICE_NAMES = {"male": "ko-KR-Wavenet-C", "female": "ko-KR-Wavenet-A"}
RATES = {"male": 0.96, "female": 1.0}
PER_RUN_LIMIT = 100_000  # 사고 방지용 실행당 상한. 월별 사용량은 콘솔에서 별도 확인.


def main():
    parser = argparse.ArgumentParser(description="한빛시 교육용 개표방송 TTS")
    parser.add_argument("--key", required=True, type=Path, help="서비스 계정 키의 로컬 경로")
    parser.add_argument("--script", type=Path, default=Path(__file__).with_name("step8_tts_segments.json"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("video") / "audio")
    parser.add_argument("--dry-run", action="store_true", help="과금 없이 텍스트와 설정만 검사")
    args = parser.parse_args()

    if not args.script.is_file():
        parser.error(f"대본 파일을 찾을 수 없습니다: {args.script}")
    data = json.loads(args.script.read_text(encoding="utf-8"))
    segments = data["audio_segments"]
    if not isinstance(segments, list) or not segments:
        parser.error("대본이 비어 있습니다")
    total_chars = sum(len(str(s["text"])) for s in segments)
    if total_chars > PER_RUN_LIMIT:
        parser.error(f"실행당 안전 상한 초과: {total_chars:,}자")
    for s in segments:
        if s["role"] not in VOICE_NAMES or not s["text"].strip():
            parser.error(f"장면 설정 오류: {s}")
    print(f"장면 수: {len(segments)}, 요청 문자 수(대략): {total_chars:,}자")
    if args.dry_run:
        print("DRY RUN 완료: API 호출 없음, 과금 없음")
        return
    if not args.key.is_file():
        parser.error("서비스 계정 키 파일이 없습니다. --key 경로를 확인하세요")

    from google.cloud import texttospeech
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file(str(args.key))
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    args.output.mkdir(parents=True, exist_ok=True)
    for s in segments:
        name = s["id"]
        out = args.output / f"{name}.mp3"
        if out.exists():
            print(f"SKIP (기존 파일): {out.name}")
            continue
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=s["text"]),
            voice=texttospeech.VoiceSelectionParams(
                language_code="ko-KR", name=VOICE_NAMES[s["role"]]
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=RATES[s["role"]],
            ),
        )
        out.write_bytes(response.audio_content)
        print(f"완료: {out.name} ({len(response.audio_content):,} bytes)")
    print("완료: 생성된 MP3를 편집기 오디오 트랙에 배치하세요.")


if __name__ == "__main__":
    main()
