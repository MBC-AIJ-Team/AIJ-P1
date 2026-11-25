
import json
import cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

VIDEO_PATH = (
    ROOT / "video/clips/studio_v5_female_motion_loop_10s.mp4"
)

DATA_PATH = (
    ROOT / "data/STEP2_Data/election_summary.json"
)

OUTPUT_PATH = (
    ROOT / "video/clips/scene04_step08_female_LED_animation_10s.mp4"
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
FPS = 30
DURATION = 10
ANIMATION_DURATION = 2

TOTAL_FRAMES = FPS * DURATION

FONT = "C:/Windows/Fonts/malgunbd.ttf"

def X(v):
    return round(v * W / 1376)

# 여자 앵커용 LED 그래픽의 가로 위치 이동
def LED_X(v):
    return X(v - 490)

def Y(v):
    return round(v * H / 768)

def font(size):
    return ImageFont.truetype(FONT, X(size))

# JSON 원본 읽기
with open(DATA_PATH, encoding="utf-8-sig") as f:
    data = json.load(f)

if data.get("is_synthetic") is not True:
    raise ValueError("가상 선거 데이터가 아닙니다.")

step = next(
    s for s in data["steps"] if s["step"] == 8
)

results = sorted(
    step["candidate_results"],
    key=lambda c: c["rank"]
)

if sum(c["votes"] for c in results) != step["valid_votes"]:
    raise ValueError("후보별 득표수 합계 오류")

COLORS = {
    "C01": (60, 150, 255, 255),
    "C02": (65, 204, 168, 255),
    "C03": (245, 105, 145, 255)
}

# 원본 앵커 영상 열기
cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise FileNotFoundError(
        f"영상 파일을 확인하세요: {VIDEO_PATH}"
    )

source_fps = cap.get(cv2.CAP_PROP_FPS)
source_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

if source_fps <= 0 or source_frames < source_fps * DURATION:
    raise ValueError("원본 영상이 2초보다 짧거나 FPS 정보가 없습니다.")

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    str(OUTPUT_PATH), fourcc, FPS, (W, H)
)

if not out.isOpened():
    raise RuntimeError("영상 출력 파일을 열 수 없습니다.")

def write_text(draw, xy, value, size, color="white"):
    draw.text(
        xy,
        value,
        font=font(size),
        fill=color,
        stroke_width=3,
        stroke_fill=(5, 12, 35, 230)
    )

try:
    for frame_no in range(TOTAL_FRAMES):

        # 원본 동영상을 출력 시각에 맞춰 읽기
        source_frame_no = round(
            frame_no * source_fps / FPS
        )

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            source_frame_no
        )

        ok, frame = cap.read()

        if not ok:
            raise RuntimeError(
                f"{frame_no}번째 프레임 읽기 실패"
            )

        frame = cv2.resize(frame, (W, H))
        frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame).convert("RGBA")

        overlay = Image.new(
            "RGBA", (W, H), (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(overlay)

        # 그래프는 처음 2초 동안만 채워짐
        t = min(
            1.0,
        (frame_no + 1) / (FPS * ANIMATION_DURATION)
        )

        # 부드러운 가속·감속
        progress = t * t * (3 - 2 * t)

        # 제목
        write_text(
            draw, (LED_X(570), Y(65)),
            data["election"], 37
        )

        write_text(
            draw, (LED_X(570), Y(135)),
            f"개표 {step['step']}단계  |  개표율 "
            f"{step['count_progress_pct']:.2f}%",
            28, (170, 215, 255, 255)
        )

        for i, candidate in enumerate(results):

            y = 225 + i * 115
            rate = candidate["vote_share_pct"]
            color = COLORS[candidate["candidate_id"]]

            write_text(
                draw, (LED_X(570), Y(y)),
                candidate["name"], 32
            )

            label = f"{rate:.2f}%"

            bbox = draw.textbbox(
                (0, 0), label, font=font(33)
            )

            width = bbox[2] - bbox[0]

            write_text(
                draw,
                (LED_X(1250) - width, Y(y)),
                label, 33
            )

            x1, x2 = LED_X(570), LED_X(1250)
            y1, y2 = Y(y + 52), Y(y + 75)

            draw.rounded_rectangle(
                (x1, y1, x2, y2),
                radius=Y(10),
                fill=(55, 75, 120, 190)
            )

            # 최종 득표율만큼 2초 동안 표시
            bar_width = round(
                (x2 - x1) * rate / 100 * progress
            )

            if bar_width > 0:
                draw.rounded_rectangle(
                    (
                        x1, y1,
                        x1 + bar_width, y2
                    ),
                    radius=min(Y(10), bar_width // 2),
                    fill=color
                )

        # 가상 선거 고지
        draw.rounded_rectangle(
            (X(15), Y(725), X(470), Y(760)),
            radius=X(8),
            fill=(5, 16, 46, 210)
        )

        draw.text(
            (X(30), Y(730)),
            data["disclaimer"],
            font=font(23),
            fill="white"
        )
            # 개표 2단계 완성 그래프를 투명 PNG로 저장
        if frame_no == FPS * ANIMATION_DURATION:
            png_path = (
                ROOT / "video/charts/led_transparent/"
                "led_overlay_step_08_female_exact.png"
            )
            png_path.parent.mkdir(parents=True, exist_ok=True)
            overlay.save(png_path)
            print(f"[PNG 저장 완료] {png_path}")

        # 앵커 영상과 투명 그래픽 합성
        result = Image.alpha_composite(
            image, overlay
        ).convert("RGB")

        output_frame = cv2.cvtColor(
            cv2_mat := __import__("numpy").array(result),
            cv2.COLOR_RGB2BGR
        )

        out.write(output_frame)

finally:
    cap.release()
    out.release()

print("[SUCCESS] 개표 6단계 여자 앵커 애니메이션 생성 완료")
print(f"파일: {OUTPUT_PATH}")
print(f"해상도: {W}x{H}")
print(f"길이: {DURATION}초")
