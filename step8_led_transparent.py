
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

DATA_PATH = ROOT / "data/STEP2_Data/election_summary.json"
OUT_DIR = ROOT / "video/charts/led_transparent"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/malgunbd.ttf"

# CapCut 최종 영상 해상도
W, H = 1920, 1080

# 기존 1376x768 디자인 좌표를 FHD로 변환
def X(x):
    return round(x * W / 1376)

def Y(y):
    return round(y * H / 768)

def font(size):
    return ImageFont.truetype(FONT_PATH, X(size))

COLORS = {
    "C01": (60, 150, 255, 255),   # 이몽룡
    "C02": (65, 204, 168, 255),   # 심청
    "C03": (245, 105, 145, 255),  # 홍길동
}

with open(DATA_PATH, encoding="utf-8-sig") as f:
    data = json.load(f)

assert data["is_synthetic"] is True
assert len(data["steps"]) == 10

def text(draw, xy, value, size, color="white"):
    draw.text(
        xy,
        value,
        font=font(size),
        fill=color,
        stroke_width=2,
        stroke_fill=(5, 12, 35, 230)
    )

for step in sorted(data["steps"], key=lambda s: s["step"]):
    n = step["step"]
    results = sorted(
        step["candidate_results"],
        key=lambda c: c["rank"]
    )

    # 투명 배경(RGBA)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 제목과 개표율
    text(
        draw, (X(570), Y(65)),
        data["election"], 37
    )

    text(
        draw, (X(570), Y(135)),
        f"개표 {n}단계  |  개표율 {step['count_progress_pct']:.2f}%",
        28, (170, 215, 255, 255)
    )

    for i, c in enumerate(results):
        y = 225 + i * 115
        rate = c["vote_share_pct"]

        text(
            draw, (X(570), Y(y)),
            c["name"], 32
        )

        label = f"{rate:.2f}%"
        label_font = font(33)
        bbox = draw.textbbox((0, 0), label, font=label_font)

        text_width = bbox[2] - bbox[0]

        text(
            draw,
            (X(1250) - text_width, Y(y)),
            label, 33
        )

        # 그래프
        x1, x2 = X(570), X(1250)
        y1, y2 = Y(y + 52), Y(y + 75)

        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=Y(10),
            fill=(55, 75, 120, 190)
        )

        draw.rounded_rectangle(
            (
                x1, y1,
                x1 + round((x2 - x1) * rate / 100),
                y2
            ),
            radius=Y(10),
            fill=COLORS[c["candidate_id"]]
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

    output = OUT_DIR / f"led_overlay_step_{n:02d}.png"
    img.save(output)

    print(f"[SUCCESS] {output.name}")

print("\n완료: 투명 LED 그래픽 10장 생성")
print(f"저장 위치: {OUT_DIR}")
