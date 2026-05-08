#!/usr/bin/env python3
"""Search the AI security resources index bundled with this skill."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
INDEX_PATH = SKILL_DIR / 'references' / 'resource-index.json'
WEIGHT = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}


def load_rows() -> list[dict[str, Any]]:
    data = json.loads(INDEX_PATH.read_text())
    rows: list[dict[str, Any]] = []
    for mod in data['modules']:
        title = mod['title'].replace(mod['id'], '', 1).strip()
        for item in mod['items']:
            row = dict(item)
            row['module_id'] = mod['id']
            row['module_title'] = title
            row['module_subtitle'] = mod.get('subtitle', '')
            rows.append(row)
    return rows


def norm(value: Any) -> str:
    return '' if value is None else str(value).lower()


def num(value: Any) -> int:
    try:
        return int(str(value or '0').replace(',', ''))
    except ValueError:
        return 0


def matches(row: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.module and row['module_id'].lower() != args.module.lower():
        return False
    if args.importance and row.get('importance', '').upper() != args.importance.upper():
        return False
    if args.type and args.type.lower() not in norm(row.get('type')):
        return False
    if args.category and args.category.lower() not in norm(row.get('category')):
        return False
    if args.query:
        haystack = ' '.join(norm(row.get(k)) for k in ['name', 'type', 'importance', 'category', 'desc', 'url', 'module_id', 'module_title'])
        for token in args.query.lower().split():
            if token not in haystack:
                return False
    return True


def sort_rows(rows: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    if mode == 'stars':
        return sorted(rows, key=lambda r: (num(r.get('stars')), WEIGHT.get(r.get('importance'), 0), -num(r.get('seq'))), reverse=True)
    if mode == 'seq':
        return sorted(rows, key=lambda r: num(r.get('seq')))
    if mode == 'name':
        return sorted(rows, key=lambda r: norm(r.get('name')))
    return sorted(rows, key=lambda r: (WEIGHT.get(r.get('importance'), 0), num(r.get('stars')), -num(r.get('seq'))), reverse=True)


def markdown(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return '未找到匹配资源。'
    lines = ['| # | 模块 | 资源 | 等级 | Stars | 分类 | URL |', '|---:|---|---|---|---:|---|---|']
    for r in rows:
        stars = r.get('stars') or '0'
        url = r.get('url') or ''
        name = r.get('name') or ''
        link = f'[{name}]({url})' if url else name
        lines.append(f"| {r.get('seq','')} | {r['module_id']} | {link} | {r.get('importance','')} | {stars} | {r.get('category','')} | {url} |")
        desc = (r.get('desc') or '').strip()
        if desc:
            lines.append(f"|  |  | <sub>{desc[:220]}{'…' if len(desc) > 220 else ''}</sub> |  |  |  |  |")
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Search AI安全资源军火库 resources.')
    parser.add_argument('--query', '-q', default='', help='Keyword query; all tokens must match')
    parser.add_argument('--module', choices=['M1', 'M2', 'M3', 'M4', 'M5', 'M6'], help='Filter by module')
    parser.add_argument('--category', help='Filter by category substring')
    parser.add_argument('--importance', choices=['S', 'A', 'B', 'C', 'D'], help='Filter by importance')
    parser.add_argument('--type', help='Filter by resource type substring, e.g. GitHub仓库, Blog')
    parser.add_argument('--sort', choices=['priority', 'stars', 'seq', 'name'], default='priority')
    parser.add_argument('--limit', type=int, default=10, help='Max rows to output; use 0 for all')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of Markdown')
    parser.add_argument('--list-modules', action='store_true', help='List module summary')
    parser.add_argument('--list-categories', action='store_true', help='List categories and counts')
    args = parser.parse_args()

    rows = load_rows()
    if args.list_modules:
        modules: dict[str, dict[str, Any]] = {}
        for r in rows:
            modules.setdefault(r['module_id'], {'module': r['module_id'], 'title': r['module_title'], 'count': 0})['count'] += 1
        print(json.dumps(list(modules.values()), ensure_ascii=False, indent=2) if args.json else '\n'.join(f"{m['module']} {m['title']}: {m['count']}" for m in modules.values()))
        return 0
    if args.list_categories:
        counts: dict[str, int] = {}
        for r in rows:
            if (not args.module or r['module_id'].lower() == args.module.lower()):
                counts[r.get('category') or ''] = counts.get(r.get('category') or '', 0) + 1
        items = [{'category': k, 'count': v} for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
        print(json.dumps(items, ensure_ascii=False, indent=2) if args.json else '\n'.join(f"{x['category']}: {x['count']}" for x in items))
        return 0

    filtered = sort_rows([r for r in rows if matches(r, args)], args.sort)
    if args.limit > 0:
        filtered = filtered[: args.limit]
    print(json.dumps(filtered, ensure_ascii=False, indent=2) if args.json else markdown(filtered))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
