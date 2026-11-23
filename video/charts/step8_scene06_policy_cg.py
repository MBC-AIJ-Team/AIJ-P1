from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
W,H=1920,1080
FONT_BOLD='/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'
FONT_REG='/usr/share/fonts/truetype/nanum/NanumSquareR.ttf'
if not Path(FONT_BOLD).exists():
    FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(sz,bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,sz)

def center_text(draw, xy, text, ft, fill):
    b=draw.textbbox((0,0),text,font=ft)
    draw.text((xy[0]-(b[2]-b[0])/2,xy[1]),text,font=ft,fill=fill)

CANDIDATES=[
    dict(name='이몽룡', party='한빛미래당', policy='광역교통망 확충', evidence='DOC-002', accent=(55,143,245), index='01', sub='교통 · 도시개발'),
    dict(name='심청', party='시민혁신당', policy='청년 주거 지원', evidence='DOC-003', accent=(237,95,115), index='02', sub='주거 · 복지'),
    dict(name='홍길동', party='무소속', policy='소상공인 지원', evidence='DOC-004', accent=(50,190,151), index='03', sub='지역경제 · 일자리'),
]

def draw_frame(focus):
    img=Image.new('RGB',(W,H))
    d=ImageDraw.Draw(img)
    for y in range(H):
        t=y/H
        d.line((0,y,W,y), fill=(int(7+7*t),int(16+17*t),int(41+37*t)))
    # studio LED screen stage lighting
    d.ellipse((-650,-125,780,350),outline=(34,69,146),width=6)
    d.ellipse((1170,-170,2450,450),outline=(44,86,174),width=6)
    d.line((70,245,1850,245), fill=(62,98,165), width=3)
    d.text((79,48),'HANBIT 2026   |   AI NEWS SIMULATION',font=font(28,True),fill=(136,177,235))
    d.text((75,105),'2026 한빛시 시장 선거',font=font(37,True),fill=(222,238,255))
    d.text((74,158),'후보별 주요 공약 비교',font=font(76,True),fill=(255,255,255))
    # all policy cards appear, only focused card brighter
    start_x=75; gap=24; cw=574; top=313; bottom=873
    for idx,c in enumerate(CANDIDATES):
        x=start_x+idx*(cw+gap);active=(idx==focus)
        fill=(26,49,99) if active else (15,32,68)
        border=c['accent'] if active else (63,81,117)
        d.rounded_rectangle((x,top,x+cw,bottom),radius=28,fill=fill,outline=border,width=5 if active else 2)
        if active:
            d.rounded_rectangle((x+20,top+22,x+cw-20,top+36),radius=7,fill=c['accent'])
        d.text((x+37,top+66),'후보 '+c['index'],font=font(30,True),fill=(174,202,240))
        d.text((x+35,top+136),c['name'],font=font(82,True),fill=(255,255,255))
        d.text((x+39,top+251),c['party'],font=font(38),fill=(211,228,255))
        d.line((x+35,top+328,x+cw-35,top+328),fill=(80,113,167),width=2)
        d.text((x+35,top+356),'주요 공약',font=font(28),fill=(166,189,224))
        d.text((x+35,top+408),c['policy'],font=font(43,True),fill=(255,255,255))
        d.text((x+36,top+487),f"근거 {c['evidence']}",font=font(29),fill=(176,204,243))
    # ticker / disclosure
    d.rounded_rectangle((75,924,1845,1023),radius=18,fill=(7,25,58),outline=(80,119,186),width=2)
    d.rounded_rectangle((93,940,730,1007),radius=12,fill=(27,75,149))
    d.text((118,952),'가상 선거·교육용 시뮬레이션',font=font(35,True),fill=(255,255,255))
    d.text((766,950),'공약 자료: 교육용 가상 정책 문서  |  결과·득표율 미표시',font=font(30),fill=(200,220,245))
    return img

paths=[]
for i,c in enumerate(CANDIDATES):
    path=OUT/f'AIJ_P1_SCENE06_policy_{i+1:02d}_{c["evidence"]}.png'
    draw_frame(i).save(path,optimize=True)
    paths.append(path)
    print('PNG:',path.name)
# encode 12-sec muted video using concat demuxer
concat=OUT/'scene06_policy_concat.txt'
concat.write_text(''.join(f"file '{p.name}'\nduration 4\n" for p in paths)+f"file '{paths[-1].name}'\n",encoding='utf-8')
mp4=OUT/'AIJ_P1_SCENE06_policy_cards_12s.mp4'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,format=yuv420p','-t','12','-c:v','libx264','-preset','veryfast','-crf','18','-movflags','+faststart',str(mp4)]
subprocess.run(cmd,check=True,cwd=OUT)
print('MP4:',mp4.name)
