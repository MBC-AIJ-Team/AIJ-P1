"""AIJ-P1: 가상 후보 이름 '심청이' -> '심청' 변경.

먼저 검사: python step8_rename_candidate.py
적용:       python step8_rename_candidate.py --apply

텍스트 원본 백업 후 수정. 승인 및 감사 이력은 수정하지 않고 재승인용 기사를 따로 작성.
MP3, PNG, MP4와 DOCX/PDF는 직접 수정하지 않음.
"""
from __future__ import annotations
import argparse
import json
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
OLD, NEW = '심청이', '심청'
TEXT_EXT = {'.py', '.csv', '.json', '.md', '.txt', '.srt', '.vtt', '.html', '.css', '.js', '.ts', '.tsx', '.jsx', '.yaml', '.yml'}
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', 'name_change_backup'}
SKIP_NAMES = {'approved_ai_article_step_10.json', 'step8_rename_candidate.py'}

def historical(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(p in SKIP_DIRS or p.startswith('name_change_backup_') for p in rel.parts[:-1]):
        return True
    name = path.name.lower()
    return name in SKIP_NAMES or 'approval_log' in name or 'audit_log' in name or name == 'article_log.json' or name.endswith('.jsonl')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='백업 후 텍스트 파일 변경')
    args = ap.parse_args()
    matches = []
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXT or historical(p):
            continue
        try:
            raw = p.read_bytes()
            text = raw.decode('utf-8-sig')
        except (UnicodeDecodeError, OSError):
            continue
        if OLD in text:
            matches.append((p, raw, text))
    print(f'이름 변경 대상: {len(matches)}개 텍스트 파일')
    for p, _, t in matches:
        print(f'  {p.relative_to(ROOT)} ({t.count(OLD)}건)')
    approved = ROOT / 'rag' / 'approved' / 'approved_ai_article_step_10.json'
    if not approved.exists():
        approved = ROOT / 'approved_ai_article_step_10.json'
    if approved.exists():
        print(f'승인 기사 발견(원본 보존): {approved.relative_to(ROOT)}')
    if not args.apply:
        print('검사만 수행했습니다. 실제 변경하려면 --apply 옵션을 지정하세요.')
        return
    backup = ROOT / ('name_change_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.mkdir(parents=True)
    for p, raw, t in matches:
        rel = p.relative_to(ROOT)
        dest = backup / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
        p.write_bytes(bom + t.replace(OLD, NEW).encode('utf-8'))
    if approved.exists():
        dest = backup / approved.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(approved, dest)
        article = json.loads(approved.read_text(encoding='utf-8-sig'))
        article['article'] = article['article'].replace(OLD, NEW)
        article['status'] = '검토 필요'
        for field in ('approved_by', 'approved_at', 'approval_reason', 'source_article_hash'):
            article.pop(field, None)
        article['revision_note'] = '후보명 심청이→심청 변경. 변경된 데이터 및 기사 재검증·재승인 필요.'
        pending = ROOT / 'rag' / 'articles' / 'ai_article_step_10_name_corrected_pending.json'
        pending.parent.mkdir(parents=True, exist_ok=True)
        pending.write_text(json.dumps(article, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'재승인 대상 기사 생성: {pending.relative_to(ROOT)}')
    print(f'완료. 수정 전 텍스트 파일은 {backup.name}에 백업했습니다.')
    print('주의: 기존 MP3·PNG·MP4는 이름이 자동 교체되지 않습니다. TTS·그래프를 재생성하세요.')
    print('주의: DOCX·PDF·이미지 내 텍스트는 별도로 교체하세요.')

if __name__ == '__main__':
    main()
