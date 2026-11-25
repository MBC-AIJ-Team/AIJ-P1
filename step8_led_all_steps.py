
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

DATA_PATH = (
    ROOT / "data" / "STEP2_Data" / "election_summary.json"
)

IMAGE_PATH = (
    ROOT / "video" / "images"
    / "studio_v5_male_LED_analysis_final.jpg"
)

OUTPUT_DIR = ROOT / "video" / "charts" / "led_steps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/malgunbd.ttf"

COLORS = {
    "C01": (60, 150, 255, 255),
    "C02": (65, 204, 168, 255),
    "C03": (245, 105, 145, 255),
}

# 원본 JSON 읽기
with open(DATA_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# 가상 선거 데이터 확인
if data.get("is_synthetic") is not True:
    raise ValueError("가상 선거 데이터가 아닙니다.")

steps = data["steps"]

if len(steps) != 10:
    raise ValueError("개표 단계가 10개가 아닙니다.")

if sorted(s["step"] for s in steps) != list(range(1, 11)):
    raise ValueError("개표 단계 번호를 확인하세요.")

# 데이터 기본 검증
for step in steps:
    results = step["candidate_results"]

    if len(results) != 3:
        raise ValueError("후보 수 오류")

    votes_sum = sum(c["votes"] for c in results)

    if votes_sum != step["valid_votes"]:
        raise ValueError(
            f"{step['step']}단계 득표수 불일치"
        )

    for candidate in results:
        calculated = (
            candidate["votes"] / step["valid_votes"] * 100
        )

        if abs(calculated - candidate["vote_share_pct"]) > 0.01:
            raise ValueError("득표율 검증 실패")

    progress = (
        step["counted_ballots"] / data["total_ballots"] * 100
    )

    if abs(progress - step["count_progress_pct"]) > 0.01:
        raise ValueError("개표율 검증 실패")

# 배경 이미지
background = Image.open(IMAGE_PATH).convert("RGBA")
W, H = background.size

def X(value):
    return round(W * value / 1376)

def Y(value):
    return round(H * value / 768)

def font(size):
    return ImageFont.truetype(
        FONT_PATH,
        max(12, X(size))
    )

def draw_text(draw, position, text, size, color):
    draw.text(
        position,
        text,
        font=font(size),
        fill=color,
        stroke_width=max(1, X(2)),
        stroke_fill=(5, 12, 35, 230)
    )

for step_data in sorted(steps, key=lambda s: s["step"]):

    step_num = step_data["step"]
    progress = step_data["count_progress_pct"]

    # 매 단계에서 원본 이미지 새로 사용
    image = background.copy()

    overlay = Image.new(
        "RGBA", image.size, (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    # 방송 제목
    draw_text(
        draw,
        (X(570), Y(65)),
        data["election"],
        37,
        "white"
    )

    # 단계와 개표율
    draw_text(
        draw,
        (X(570), Y(135)),
        f"개표 {step_num}단계  |  개표율 {progress:.2f}%",
        28,
        (170, 215, 255, 255)
    )

    # 후보별 득표율 - 실제 순위로 정렬
    results = sorted(
        step_data["candidate_results"],
        key=lambda c: c["rank"]
    )

    for i, candidate in enumerate(results):

        y = 225 + i * 115
        name = candidate["name"]
        rate = candidate["vote_share_pct"]
        color = COLORS[candidate["candidate_id"]]

        draw_text(
            draw,
            (X(570), Y(y)),
            name,
            32,
            "white"
        )

        rate_text = f"{rate:.2f}%"
        rate_font = font(33)

        bbox = draw.textbbox(
            (0, 0),
            rate_text,
            font=rate_font
        )

        text_width = bbox[2] - bbox[0]

        draw_text(
            draw,
            (X(1250) - text_width, Y(y)),
            rate_text,
            33,
            "white"
        )

        # 막대그래프
        x1 = X(570)
        y1 = Y(y + 52)
        x2 = X(1250)
        y2 = Y(y + 75)

        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=Y(10),
            fill=(55, 75, 120, 190)
        )

        bar_width = round(
            (x2 - x1) * rate / 100
        )

        draw.rounded_rectangle(
            (x1, y1, x1 + bar_width, y2),
            radius=Y(10),
            fill=color
        )

    # 가상 선거 안내
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

    # 합성 및 저장
    result = Image.alpha_composite(
        image, overlay
    ).convert("RGB")

    output_path = (
        OUTPUT_DIR / f"led_count_step_{step_num:02d}.png"
    )

    result.save(output_path)

    print(
        f"[SUCCESS] {step_num}단계: "
        f"개표율 {progress:.2f}%"
    )

print("\n완료: LED 개표 그래픽 10장 생성")
print(f"저장 위치: {OUTPUT_DIR}")
