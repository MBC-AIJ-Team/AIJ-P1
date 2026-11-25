
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

IMAGE_PATH = (
    ROOT / "video" / "images"
    / "studio_v5_male_LED_analysis_final.jpg"
)

OUTPUT_DIR = ROOT / "video" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = (
    OUTPUT_DIR / "scene03_step01_LED_composite_v4.png"
)

# 원본 이미지 읽기
image = Image.open(IMAGE_PATH).convert("RGBA")
W, H = image.size

# 1376×768 기준 상대 좌표
def X(value):
    return round(W * value / 1376)

def Y(value):
    return round(H * value / 768)

font_path = "C:/Windows/Fonts/malgunbd.ttf"

def font(size):
    return ImageFont.truetype(
        font_path,
        max(12, X(size))
    )

# 투명 그래픽 레이어 생성
overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# 오른쪽 반투명 LED 그래픽 패널
# draw.rounded_rectangle(
    # (X(530), Y(35), X(1310), Y(595)),
    # radius=X(20),
    # fill=(7, 19, 56, 205),
    # outline=(75, 142, 245, 220),
    # width=max(2, X(2))
# )

# 상단 타이틀
draw.text(
    (X(570), Y(65)),
    "2026 한빛시 시장 선거",
    font=font(37),
    fill=(255, 255, 255, 255),
    stroke_width=2,
    stroke_fill=(5, 12, 35, 230)
)

draw.text(
    (X(570), Y(175)),
    "개표 1단계  |  개표율 9.94%",
    font=font(28),
    fill=(170, 215, 255, 255),
    stroke_width=2,
    stroke_fill=(5, 12, 35, 230)
)

# 기존 가상 선거 데이터
candidates = [
    ("이몽룡", 61.30, (60, 150, 255, 255)),
    ("홍길동", 25.40, (245, 105, 145, 255)),
    ("심청", 13.31, (65, 204, 168, 255)),
]

# 후보별 그래프
for i, (name, rate, color) in enumerate(candidates):

    y = 225 + i * 115

    draw.text(
        (X(570), Y(y)),
        name,
        font=font(32),
        fill="white"
    )

    # 득표율 오른쪽 정렬
    rate_text = f"{rate:.2f}%"

    box = draw.textbbox(
        (0, 0),
        rate_text,
        font=font(33)
    )

    rate_width = box[2] - box[0]

    draw.text(
        (X(1250) - rate_width, Y(y)),
        rate_text,
        font=font(33),
        fill="white"
    )

    # 그래프 배경
    x1 = X(570)
    y1 = Y(y + 52)
    x2 = X(1250)
    y2 = Y(y + 75)

    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=Y(10),
        fill=(55, 75, 120, 190)
    )

    # 득표율 그래프
    bar_width = round((x2 - x1) * rate / 100)

    draw.rounded_rectangle(
        (x1, y1, x1 + bar_width, y2),
        radius=Y(10),
        fill=color
    )

# 하단 가상 선거 안내
draw.rounded_rectangle(
    (X(15), Y(725), X(470), Y(760)),
    radius=X(8),
    fill=(5, 16, 46, 210)
)

draw.text(
    (X(30), Y(730)),
    "가상 선거 · 교육용 시뮬레이션",
    font=font(23),
    fill=(245, 250, 255, 255)
)

# 이미지와 그래픽 합성
result = Image.alpha_composite(image, overlay)

# RGB 변환 후 PNG 저장
result = result.convert("RGB")
result.save(OUTPUT_PATH)

print("[SUCCESS] LED 합성 v2 완료")
print(f"저장 위치: {OUTPUT_PATH}")
print(f"이미지 크기: {W} x {H}")
