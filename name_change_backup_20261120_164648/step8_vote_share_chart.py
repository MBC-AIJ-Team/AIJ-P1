"""STEP 8-7A: Generate 10 broadcast-ready progressive election charts.
Run at the root of AIJ-P1: python step8_vote_share_chart.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent

SOURCES = [
    ROOT / "data" / "STEP2_Data" / "election_summary.json",
    ROOT / "data" / "election_summary.json",
    ROOT / "election_summary.json",
]

SOURCE = next((p for p in SOURCES if p.exists()), None)
if SOURCE is None:
    raise FileNotFoundError('election_summary.json 파일을 AIJ-P1/data 또는 AIJ-P1 최상위 폴더에 저장하세요.')

with SOURCE.open('r', encoding='utf-8-sig') as f:
    payload = json.load(f)
assert payload.get('is_synthetic') is True, '교육용 가상 데이터인지 확인하세요.'
steps = sorted(payload['steps'], key=lambda row: row['step'])
assert len(steps) == 10 and [s['step'] for s in steps] == list(range(1, 11)), '1~10단계 데이터가 필요합니다.'

if any(f.name == 'Malgun Gothic' for f in font_manager.fontManager.ttflist):
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    for font in ('NanumGothic', 'Noto Sans CJK KR', 'DejaVu Sans'):
        if any(f.name == font for f in font_manager.fontManager.ttflist):
            plt.rcParams['font.family'] = font
            break
plt.rcParams['axes.unicode_minus'] = False

names = ['이몽룡', '심청이', '홍길동']
colors = {'이몽룡': '#4A91FF', '심청이': '#FA6577', '홍길동': '#45CBA7'}
xs = np.array([r['step'] for r in steps])
series = {name: np.array([next(c['vote_share_pct'] for c in r['candidate_results'] if c['name'] == name) for r in steps]) for name in names}
output = ROOT / 'video' / 'charts'
output.mkdir(parents=True, exist_ok=True)

for upto in range(1, 11):
    current = steps[upto - 1]
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor='#10192F')  # 1920x1080
    ax = fig.add_axes([0.10, 0.20, 0.77, 0.59], facecolor='#10192F')
    fig.text(0.065, 0.925, '2026 한빛시 시장 선거  |  개표 중계', fontsize=22, color='white', weight='bold')
    fig.text(0.065, 0.875, f'{upto}단계 / 10단계     개표율 {current["count_progress_pct"]:.2f}%     기준시각 {current["timestamp"][11:16]}', fontsize=17, color='#D9E5F8')
    for name in names:
        ys = series[name][:upto]
        ax.plot(xs[:upto], ys, color=colors[name], linewidth=4, marker='o', markersize=9, label=name)
        ax.annotate(f'{ys[-1]:.2f}%', (upto, ys[-1]), xytext=(12, 0), textcoords='offset points', color=colors[name], fontsize=15, va='center', weight='bold')
    ax.set_xlim(0.6, 11.6)
    ax.set_ylim(0, 75)
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(0, 76, 15))
    ax.set_xlabel('개표 단계', fontsize=15, color='#E2ECFA', labelpad=12)
    ax.set_ylabel('누적 유효표 중 득표율 (%)', fontsize=15, color='#E2ECFA', labelpad=12)
    ax.tick_params(axis='both', colors='#DAE3F2', labelsize=13, length=0)
    ax.grid(axis='y', color='#64748B', alpha=.32)
    for spine in ax.spines.values():
        spine.set_visible(False)
    legend = ax.legend(loc='upper right', facecolor='#192743', edgecolor='#34465C', fontsize=15, ncol=3)
    for txt in legend.get_texts():
        txt.set_color('white')
    if upto == 10:
        fig.text(0.69, 0.865, '최종 개표 완료 · 심청이 1위', fontsize=18, weight='bold', color='#FFE0E4')
    fig.text(0.065, 0.07, '가상 선거·교육용 시뮬레이션  |  실제 선거 결과 아님', fontsize=16, color='#FFFFFF', weight='bold')
    fig.text(0.065, 0.035, f'자료: {payload["source_id"]}  |  누적 개표 데이터', fontsize=11, color='#A9B9D1')
    dest = output / f'vote_share_step_{upto:02d}.png'
    fig.savefig(dest, facecolor=fig.get_facecolor(), dpi=120)
    plt.close(fig)
    print(f'생성 완료: {dest.relative_to(ROOT)}')
print('완료: PNG 10장 (각 1920×1080)')
