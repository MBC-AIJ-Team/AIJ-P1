import csv
import json
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
ARTICLE_DIR = ROOT / 'rag' / 'articles'
ARTICLE_PATH = ARTICLE_DIR / 'ai_article_step_10.json'
DATA_DIR = ROOT / 'data' / 'STEP2_Data'
CANDIDATES = ['심청', '이몽룡', '홍길동']
VALIDATION_ERRORS = []
EXPECTED = {'DOC-002': ('C01', '이몽룡', '광역교통망 확충'),
            'DOC-003': ('C02', '심청', '청년 주거 지원'),
            'DOC-004': ('C03', '홍길동', '소상공인 지원')}
NUM = r'[\d,]+'
PCT = r'\d+(?:\.\d+)?'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def report(label, errors):
    print('\n===== ' + label + ' =====')
    VALIDATION_ERRORS.extend(errors)
    for error in errors:
        print('[FAIL]', error)
    if not errors:
        print('[PASS]', label)
    return not errors


def validate_article():
    VALIDATION_ERRORS.clear()
    errors = []
    try:
        d = read_json(ARTICLE_PATH)
        a = d['article']
        step = d['step']
        if not isinstance(a, str) or not a.strip():
            raise ValueError('기사 본문 없음')
        if type(step) is not int or not 1 <= step <= 10:
            errors.append('개표 단계 범위 오류')
        m = re.fullmatch(r'ai_article_step_(\d{2})(?:_.*)?\.json', ARTICLE_PATH.name)
        if not m or int(m[1]) != step:
            errors.append('파일명과 개표 단계 불일치')
        if d.get('is_synthetic') is not True or '교육용 시뮬레이션' not in a or '[가상 선거]' not in a:
            errors.append('가상 선거 표시 누락')
        if '심청이 후보' in a:
            errors.append('후보명 불일치')
        if datetime.fromisoformat(d['timestamp']).utcoffset() is None:
            errors.append('기준시각 시간대 누락')
        if not d.get('model') or not d.get('generation_method'):
            errors.append('AI 작성 정보 누락')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        errors.append(f'기사 기본 검사 오류: {e}')
    return report('기사 기본 검증', errors)


def validate_against_source():
    errors = []
    try:
        d = read_json(ARTICLE_PATH)
        a = d['article']
        step = d['step']
        src = read_json(DATA_DIR / 'election_summary.json')
        s = next(x for x in src['steps'] if x['step'] == step)
        if d['source_id'] != src['source_id'] or d['timestamp'] != s['timestamp']:
            errors.append('출처 또는 기준시각 불일치')
        with (DATA_DIR / 'election_results.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = [r for r in csv.DictReader(f) if int(r['step']) == step]
        ids = d.get('data_row_ids', [])
        expected_ids = {r['row_id'] for r in rows}
        if len(rows) != 15 or len(expected_ids) != 15 or not isinstance(ids, list) or len(ids) != 15 or set(ids) != expected_ids:
            errors.append('데이터 행 ID 누락 또는 불일치')
        if any(r['source_id'] != d['source_id'] or r['timestamp'] != d['timestamp'] for r in rows):
            errors.append('CSV 출처 또는 기준시각 불일치')
        if len({(r['region_id'], r['candidate_id']) for r in rows}) != 15:
            errors.append('지역·후보 조합 중복 또는 누락')
        candidates = {c['name']: c for c in s['candidate_results']}
        for c in candidates.values():
            if sum(int(r['votes']) for r in rows if r['candidate_id'] == c['candidate_id']) != c['votes']:
                errors.append(f"{c['name']} CSV 합계 불일치")
        if sum(c['votes'] for c in candidates.values()) != s['valid_votes']:
            errors.append('유효투표수 합계 불일치')
        if s['valid_votes'] + s['invalid_votes'] != s['counted_ballots']:
            errors.append('개표수 합계 불일치')
        if abs(s['counted_ballots'] / src['total_ballots'] * 100 - s['count_progress_pct']) > 0.0001:
            errors.append('원본 개표율 계산 불일치')
        ranked = sorted(candidates.values(), key=lambda c: c['votes'], reverse=True)
        if ranked[0]['votes'] - ranked[1]['votes'] != s['margin_votes']:
            errors.append('원본 득표 차이 불일치')
        for i, c in enumerate(ranked, 1):
            if c['rank'] != i or abs(c['votes'] / s['valid_votes'] * 100 - c['vote_share_pct']) > 0.0001:
                errors.append(f"{c['name']} 원본 순위 또는 득표율 오류")
        def check(pattern, expected, label, required=False, tolerance=0):
            matches = re.findall(pattern, a)
            if required and not matches:
                errors.append(label + ' 누락')
            for v in matches:
                if abs(float(v.replace(',', '')) - expected) > tolerance:
                    errors.append(label + ' 불일치: ' + v)
            return len(matches)
        check(rf'개표율(?:은|이)?\s*(?:약\s*)?({PCT})%', s['count_progress_pct'], '개표율', True, 0.0051)
        check(r'(?<!율)득표(?:수)?\s*차이는\s*([\d,]+)표', s['margin_votes'], '득표 차이', step == 10)
        check(rf'(?:격차(?:는|가)?\s*|)({PCT})%p', s['margin_percentage_points'], '득표율 격차', False, 0.0051)
        for label, key in [('유효투표수', 'valid_votes'), ('무효표', 'invalid_votes'), ('개표된 투표수', 'counted_ballots')]:
            check(rf'{label}(?:는|은)?\s*({NUM})표', s[key], label)
        rate_count = 0
        for name, c in candidates.items():
            prefix = rf'{re.escape(name)}\s*(?:후보)?(?:의\s*누적\s*득표율은|는|가)?\s*'
            rate_count += check(prefix + rf'(?:{NUM}표\s*\()?({PCT})%(?!p)', c['vote_share_pct'], name + ' 득표율', step == 10, 0.0051)
            check(prefix + rf'({NUM})표', c['votes'], name + ' 득표수', step == 10)
            check(prefix + rf'(?:{NUM}표\s*\()?{PCT}%\)?(?:로|를 얻어)?\s*(\d)위', c['rank'], name + ' 순위')
        if rate_count == 0:
            errors.append('검증 가능한 후보 득표율 없음')
        for v in re.findall(r'(\d{1,2})단계\s*개표', a):
            if int(v) != step:
                errors.append('본문 개표 단계 불일치')
        for hour, minute in re.findall(r'오후\s*(\d{1,2})시(?:\s*(\d{1,2})분)?', a):
            dt = datetime.fromisoformat(s['timestamp'])
            if int(hour) % 12 + 12 != dt.hour or int(minute or 0) != dt.minute:
                errors.append('본문 기준시각 불일치')
        if '다섯 개 구 모두 이몽룡 후보의 누적 득표가 가장 많습니다' in a:
            regions = {r['region_id'] for r in rows}
            for region in regions:
                group = [r for r in rows if r['region_id'] == region]
                mine = [int(r['votes']) for r in group if r['candidate_id'] == 'C01']
                other = [int(r['votes']) for r in group if r['candidate_id'] != 'C01']
                if not mine or not other or mine[0] <= max(other):
                    errors.append(region + ' 지역 선두 불일치')
            if len(regions) != 5:
                errors.append('지역 수 불일치')
        # 현재 기사 형식에서 확인되는 선두 표현을 검증한다.
        for name in candidates:
            if re.search(rf'{name}\s*(?:후보)?(?:는|가)?\s*(?:{PCT}%로\s*)?선두', a) and name != s['leader_name']:
                errors.append(name + ' 선두 불일치')
    except (OSError, ValueError, KeyError, TypeError, StopIteration, AttributeError, ZeroDivisionError) as e:
        errors.append(f'원본 교차검증 오류: {e}')
    return report('원본 데이터 교차검증', errors)


def validate_rag_evidence():
    errors = []
    try:
        d = read_json(ARTICLE_PATH)
        a = d['article']
        ids = d.get('evidence_ids', [])
        docs = {x['document_id']: x for x in read_json(DATA_DIR / 'policy_documents.json')}
        cited = set(re.findall(r'\((DOC-\d+)\)', a))
        if not isinstance(ids, list) or set(ids) != cited or len(ids) != len(set(ids)) or not set(EXPECTED).issubset(ids):
            errors.append('근거 ID 누락 또는 목록 불일치')
        for eid in ids:
            doc = docs.get(eid)
            if not doc or doc.get('source_id') != d['source_id']:
                errors.append(f'{eid}: 근거 문서 또는 출처 불일치')
                continue
            if eid in EXPECTED:
                cid, name, policy = EXPECTED[eid]
                if doc.get('candidate_id') != cid or name not in doc.get('text', '') or policy not in doc.get('text', ''):
                    errors.append(f'{eid}: 근거 원문 불일치')
                if not re.search(rf'{name} 후보[^.!?\n]*?{re.escape(policy)}\s*(?:을 제시했습니다|이며|입니다)?\s*\({eid}\)', a):
                    errors.append(f'{eid}: 기사 내 후보·공약 연결 불일치')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        errors.append(f'RAG 검증 오류: {e}')
    return report('RAG 근거 검증', errors)


def run_one(path):
    global ARTICLE_PATH
    ARTICLE_PATH = path
    print('\n###', path.name)
    results = [validate_article(), validate_against_source(), validate_rag_evidence()]
    ok = all(results)
    print('최종 결과:', 'PASS / 사람 검토 필요' if ok else 'FAIL / 승인 차단')
    return ok


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit('사용법: article_validator.py [--all | 기사 파일 경로]')
    if len(sys.argv) == 2 and sys.argv[1] == '--all':
        results = [run_one(ARTICLE_DIR / f'ai_article_step_{i:02d}.json') for i in range(1, 11)]
        print(f'\n전체 결과: {sum(results)}/10 PASS')
        sys.exit(0 if all(results) else 1)
    sys.exit(0 if run_one(Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else ARTICLE_PATH) else 1)
