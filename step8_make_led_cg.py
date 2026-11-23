"""AIJ-P1 STEP 8: 10-stage election broadcast LED graphics (FHD PNG).
Requires: pillow. Run from any directory: python step8_make_led_cg.py
All data are synthetic and are read from STEP2_Data/election_summary.json.
"""
import json
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'STEP2_Data' / 'election_summary.json'
OUT = ROOT / 'video' / 'charts' / 'led'
W, H = 1920, 1080
NAVY = '#07152F'
WHITE = '#F6FAFF'
MUTED = '#A7BCD7'
PALETTE = {'C01':'#488CF4', 'C02':'#FF626F', 'C03':'#30C49B'}
NAMES = {'C01':'이몽룡','C02':'심청','C03':'홍길동'}


def font(size, bold=False):
    locations = [
        ('C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'),
        ('/usr/share/fonts/truetype/nanum/NanumSquareB.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumSquareR.ttf'),
        '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf' if bold else '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    ]
    for item in locations:
        if Path(item).exists():
            return ImageFont.truetype(item, size)
    raise RuntimeError('한국어 폰트가 없습니다. Windows 맑은 고딕 설치를 확인하세요.')


def rect(draw,xy,fill,r=0,outline=None,width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def render(step):
    im = Image.new('RGB', (W,H), NAVY)
    d = ImageDraw.Draw(im)
    # Top bar
    rect(d,(0,0,W,146),'#112A53')
    d.text((88,37),'2026 한빛시 시장 선거',font=font(53,True),fill=WHITE)
    d.text((92,102),'AI 가상 개표 특집  |  교육용 시뮬레이션',font=font(26),fill='#BBD5F8')
    phase = step['step']
    stamp = datetime.fromisoformat(step['timestamp']).strftime('%Y.%m.%d  %H:%M')
    d.text((1450,49),f'제 {phase:02d} / 10 단계',font=font(39,True),fill='#F6FBFF')
    d.text((1470,105),f'집계 기준 {stamp}',font=font(21),fill='#C7D6EC')
    # Progress & status
    d.text((92,185),'개표 진행률',font=font(31),fill=MUTED)
    d.text((92,230),f"{step['count_progress_pct']:.2f}%",font=font(85,True),fill=WHITE)
    rect(d,(580,264,1765,286),'#29415E',r=9)
    rect(d,(580,264,580+int(1185*step['count_progress_pct']/100),286),'#56B1FF',r=9)
    d.text((92,352),'후보별 누적 득표 현황',font=font(37,True),fill=WHITE)
    # Candidate rows, sorted by rank
    results = sorted(step['candidate_results'], key=lambda x:x['rank'])
    for idx,c in enumerate(results):
        y = 425 + idx*164
        cid=c['candidate_id']; color=PALETTE[cid]
        rect(d,(90,y,1830,y+140),'#132643',r=16,outline='#284266',width=2)
        rect(d,(108,y+23,179,y+117),'#233B5C',r=12)
        d.text((127,y+44),str(idx+1),font=font(49,True),fill=WHITE)
        d.text((217,y+23),NAMES[cid],font=font(43,True),fill=WHITE)
        d.text((214,y+83),f"{c['votes']:,}표",font=font(27),fill=MUTED)
        # bar scaled to 100% for consistent comparison
        rect(d,(655,y+51,1455,y+86),'#27415F',r=12)
        fillw = max(1,int(800*c['vote_share_pct']/100))
        rect(d,(655,y+51,655+fillw,y+86),color,r=12)
        d.text((1485,y+43),f"{c['vote_share_pct']:.2f}%",font=font(47,True),fill=color)
    # Bottom left info - only current step known
    if phase == 10:
        announcement=f"개표 완료 · {NAMES[results[0]['candidate_id']]} 최종 1위"
    else:
        announcement=f"현재 1위 · {NAMES[results[0]['candidate_id']]}   |   1·2위 격차 {step['margin_votes']:,}표"
    d.text((93,952),announcement,font=font(34,True),fill='#EAF5FF')
    rect(d,(0,1010,W,H),'#0D2F5F')
    d.text((90,1023),'가상 선거 · 교육용 시뮬레이션 / 실제 선거 결과가 아닙니다',font=font(27,True),fill=WHITE)
    d.text((1430,1030),'자료: SYNTHETIC-STEP2-v1.0',font=font(19),fill='#BFD8FB')
    return im


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f'데이터 파일을 찾지 못했습니다: {SOURCE}')
    data=json.loads(SOURCE.read_text(encoding='utf-8-sig'))
    if not data.get('is_synthetic') or len(data.get('steps',[])) != 10:
        raise ValueError('교육용 가상 데이터 10단계가 아닙니다.')
    OUT.mkdir(parents=True,exist_ok=True)
    for s in sorted(data['steps'],key=lambda x:x['step']):
        target=OUT / f"led_count_step_{s['step']:02d}.png"
        render(s).save(target)
        print(f"생성 완료: {target.relative_to(ROOT)}")
    print('완료: LED 그래픽 10장 (각 1920x1080)')

if __name__=='__main__':
    main()
