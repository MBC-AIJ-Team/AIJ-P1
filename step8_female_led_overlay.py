
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent

source = ROOT / "video/charts/led_transparent/led_overlay_step_02.png"
output = ROOT / "video/charts/led_transparent/led_overlay_step_02_female.png"

img = Image.open(source).convert("RGBA")

# 원본과 같은 크기의 투명 캔버스
result = Image.new("RGBA", img.size, (0, 0, 0, 0))

# 기존 오른쪽 LED 그래픽만 잘라 왼쪽으로 이동
# 텍스트와 막대그래프가 함께 이동하므로 글자는 뒤집히지 않음
graphic = img.crop((770, 55, 1810, 985))
result.alpha_composite(graphic, (80, 55))

# 하단의 가상 선거 고지는 원래 위치에 유지
notice = img.crop((0, 1010, 680, 1080))
result.alpha_composite(notice, (0, 1010))

result.save(output)

print("[SUCCESS] 여자 앵커용 개표 그래픽 생성 완료")
print(output)
