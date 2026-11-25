
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

VIDEO_PATH = ROOT / "video/clips/studio_v5_male_motion_loop_10s.mp4"
DATA_PATH = ROOT / "data/STEP2_Data/election_summary.json"
OUTPUT_DIR = ROOT / "video/clips"

W, H = 1920, 1080
FPS = 30
DURATION = 10
ANIMATION_DURATION = 2
TOTAL_FRAMES = FPS * DURATION

FONT_PATH = "C:/Windows/Fonts/malgunbd.ttf"

COLORS = {
    "C01": (60, 150, 255, 255),
    "C02": (65, 204, 168, 255),
    "C03": (245, 105, 145),
}


def X(value):
    return round(value * W / 1376)


def Y(value):
    return round(value * H / 768)


def font(size):
    return ImageFont.truetype(FONT_PATH, X(size))


def write_text(draw, xy, value, size, color="white"):
    draw.text(
        xy,
        str(value),
        font=font(size),
        fill=color,
        stroke_width=3,
        stroke_fill=(5, 12, 35, 230),
    )


# 1. 원본 데이터 검사
with open(DATA_PATH, encoding="utf-8-sig") as f:
    data = json.load(f)

if data.get("is_synthetic") is not True:
    raise ValueError("가상 선거 데이터 여부를 확인하세요.")

steps = sorted(data["steps"], key=lambda s: s["step"])

if [s["step"] for s in steps] != list(range(1, 11)):
    raise ValueError("개표 단계가 1~10단계인지 확인하세요.")


# 2. 앵커 원본 영상 확인
cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise FileNotFoundError(f"앵커 영상 없음: {VIDEO_PATH}")

source_fps = cap.get(cv2.CAP_PROP_FPS)
source_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

if source_fps <= 0 or source_frames / source_fps < DURATION:
    cap.release()
    raise ValueError("앵커 영상의 길이가 10초 미만입니다.")

cap.release()


# 3. 개표 단계별 그래픽 생성
def make_overlay(step, progress):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    write_text(
        draw,
        (X(570), Y(65)),
        data["election"],
        37,
    )

    write_text(
        draw,
        (X(570), Y(135)),
        f"개표 {step['step']}단계  |  "
        f"개표율 {step['count_progress_pct']:.2f}%",
        28,
        (170, 215, 255, 255),
    )

    results = sorted(
        step["candidate_results"],
        key=lambda c: c["rank"],
    )

    for i, candidate in enumerate(results):
        y = 225 + i * 115
        rate = candidate["vote_share_pct"]
        color = COLORS[candidate["candidate_id"]]

        write_text(
            draw,
            (X(570), Y(y)),
            candidate["name"],
            32,
        )

        label = f"{rate:.2f}%"
        bbox = draw.textbbox(
            (0, 0), label, font=font(33)
        )
        label_width = bbox[2] - bbox[0]

        write_text(
            draw,
            (X(1250) - label_width, Y(y)),
            label,
            33,
        )

        x1, x2 = X(570), X(1250)
        y1, y2 = Y(y + 52), Y(y + 75)

        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=Y(10),
            fill=(55, 75, 120, 190),
        )

        bar_width = round(
            (x2 - x1) * rate / 100 * progress
        )

        if bar_width > 0:
            draw.rounded_rectangle(
                (
                    x1,
                    y1,
                    x1 + bar_width,
                    y2,
                ),
                radius=min(Y(10), bar_width // 2),
                fill=color,
            )

    # 가상 선거 고지
    draw.rounded_rectangle(
        (X(15), Y(725), X(470), Y(760)),
        radius=X(8),
        fill=(5, 16, 46, 210),
    )

    draw.text(
        (X(30), Y(730)),
        data["disclaimer"],
        font=font(23),
        fill="white",
    )

    return overlay



# 개표 10단계 최종 그래프 PNG 추출
step10 = next(s for s in steps if s["step"] == 10)

png_path = (
    ROOT / "video/charts/led_transparent/"
    "led_overlay_step_10_male_exact.png"
)

png_path.parent.mkdir(parents=True, exist_ok=True)

# 기존 애니메이션과 동일한 그래픽 생성
make_overlay(step10, 1.0).save(png_path)

print(f"[PNG 저장 완료] {png_path}")

# MP4를 다시 생성하지 않고 종료
raise SystemExit(0)



png_path = (
    ROOT / "video/charts/led_transparent/"
    "led_overlay_step_05_male_exact.png"
)

png_path.parent.mkdir(parents=True, exist_ok=True)

# 기존 MP4와 동일한 그래픽 함수 사용
make_overlay(step5, 1.0).save(png_path)

print(f"[PNG 저장 완료] {png_path}")

# MP4 영상은 다시 생성하지 않음
raise SystemExit(0)


# 4. 개표 2~10단계 영상 생성
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for step in steps[1:]:
    number = step["step"]

    output_path = (
        OUTPUT_DIR
        / f"scene03_step{number:02d}_LED_animation_10s.mp4"
    )

    cap = cv2.VideoCapture(str(VIDEO_PATH))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        str(output_path),
        fourcc,
        FPS,
        (W, H),
    )

    if not cap.isOpened() or not out.isOpened():
        cap.release()
        out.release()
        raise RuntimeError("입력 또는 출력 영상을 열 수 없습니다.")

    print(f"[START] 개표 {number}단계 제작")

    try:
        for frame_no in range(TOTAL_FRAMES):
            # 원본 앵커 프레임 읽기
            source_frame_no = round(
                frame_no * source_fps / FPS
            )
            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                source_frame_no,
            )

            ok, frame = cap.read()

            if not ok:
                raise RuntimeError(
                    f"{number}단계 {frame_no}프레임 읽기 실패"
                )

            frame = cv2.resize(frame, (W, H))
            frame_rgb = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )
            image = Image.fromarray(frame_rgb).convert("RGBA")

            # 처음 2초만 그래프가 채워짐
            t = min(
                1.0,
                (frame_no + 1)
                / (FPS * ANIMATION_DURATION),
            )

            progress = t * t * (3 - 2 * t)

            overlay = make_overlay(step, progress)

                        # 개표 4단계 완성 그래프를 투명 PNG로 저장
            if number == 4 and frame_no == FPS * ANIMATION_DURATION:
                png_path = (
                    ROOT / "video/charts/led_transparent/"
                    "led_overlay_step_04_male_exact.png"
                )
                png_path.parent.mkdir(parents=True, exist_ok=True)
                overlay.save(png_path)
                print(f"[PNG 저장 완료] {png_path}")

            result = Image.alpha_composite(
                image, overlay
            ).convert("RGB")

            output_frame = cv2.cvtColor(
                np.array(result),
                cv2.COLOR_RGB2BGR,
            )

            out.write(output_frame)

    finally:
        cap.release()
        out.release()

    print(f"[SUCCESS] {output_path.name}")

print("\n전체 개표 2~10단계 영상 생성 완료!")
print(f"저장 위치: {OUTPUT_DIR}")
