"""
문서 폴더 전체 파일 인덱스 생성기
- CSV: 전체 파일 목록 (경로, 이름, 확장자, 크기, 수정일, 해시)
- JSON: 폴더 트리 구조 + 통계
- TXT: 사람이 읽을 수 있는 요약 보고서
"""

import os
import csv
import json
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

BASE = r"/mnt/c/Users/seung/OneDrive - Daejoo Accounting Corporation/문서"
OUTPUT_DIR = r"/mnt/c/PycharmProjects/Founderskorea/file_index"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. CSV: 전체 파일 인벤토리 ---
csv_path = os.path.join(OUTPUT_DIR, f"file_inventory_{TIMESTAMP}.csv")
json_path = os.path.join(OUTPUT_DIR, f"folder_tree_{TIMESTAMP}.json")
report_path = os.path.join(OUTPUT_DIR, f"summary_report_{TIMESTAMP}.txt")

print(f"[1/3] CSV 인벤토리 생성 중: {csv_path}")

file_count = 0
total_size = 0
ext_stats = defaultdict(lambda: {"count": 0, "size": 0})
folder_stats = defaultdict(lambda: {"file_count": 0, "total_size": 0})
errors = []

def get_md5_prefix(filepath, chunk_size=8192):
    """파일의 MD5 해시 앞 16자리 (중복 탐지용)"""
    try:
        h = hashlib.md5()
        with open(filepath, "rb") as f:
            chunk = f.read(chunk_size)
            if chunk:
                h.update(chunk)
        return h.hexdigest()[:16]
    except Exception:
        return ""

with open(csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "relative_path",       # BASE 기준 상대경로
        "folder",              # 파일이 속한 폴더
        "filename",            # 파일명
        "extension",           # 확장자
        "size_bytes",          # 바이트 크기
        "size_readable",       # 읽기 쉬운 크기
        "modified_date",       # 수정일
        "created_date",        # 생성일 (OS 지원 시)
        "md5_prefix",          # MD5 앞 16자 (첫 8KB 기반)
        "top_level_folder",    # 최상위 폴더
        "depth",               # 폴더 깊이
    ])

    for root, dirs, files in os.walk(BASE):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                stat = os.stat(fpath)
                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                ctime = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                errors.append(f"STAT ERROR: {fpath} -> {e}")
                continue

            rel_path = os.path.relpath(fpath, BASE)
            folder = os.path.relpath(root, BASE)
            ext = Path(fname).suffix.lower()
            parts = rel_path.split(os.sep)
            top_folder = parts[0] if len(parts) > 1 else "(root)"
            depth = len(parts) - 1

            # 읽기 쉬운 크기
            if size < 1024:
                size_hr = f"{size} B"
            elif size < 1024**2:
                size_hr = f"{size/1024:.1f} KB"
            elif size < 1024**3:
                size_hr = f"{size/1024**2:.1f} MB"
            else:
                size_hr = f"{size/1024**3:.2f} GB"

            # MD5 (첫 8KB만 — 속도 우선)
            md5p = get_md5_prefix(fpath)

            writer.writerow([
                rel_path, folder, fname, ext,
                size, size_hr, mtime, ctime,
                md5p, top_folder, depth
            ])

            file_count += 1
            total_size += size
            ext_stats[ext]["count"] += 1
            ext_stats[ext]["size"] += size
            folder_stats[top_folder]["file_count"] += 1
            folder_stats[top_folder]["total_size"] += size

            if file_count % 5000 == 0:
                print(f"  ... {file_count}개 처리됨")

print(f"  완료: {file_count}개 파일 인덱싱")

# --- 2. JSON: 폴더 트리 + 통계 ---
print(f"[2/3] JSON 트리 생성 중: {json_path}")

def build_tree(base_path, max_depth=3, current_depth=0):
    tree = {"name": os.path.basename(base_path), "type": "directory", "children": []}
    try:
        entries = sorted(os.listdir(base_path))
    except PermissionError:
        return tree

    file_count_here = 0
    total_size_here = 0

    for entry in entries:
        full = os.path.join(base_path, entry)
        if os.path.isdir(full):
            if current_depth < max_depth:
                child = build_tree(full, max_depth, current_depth + 1)
                tree["children"].append(child)
            else:
                # 깊이 제한 — 파일 수만 세기
                try:
                    fc = sum(len(fs) for _, _, fs in os.walk(full))
                except:
                    fc = 0
                tree["children"].append({
                    "name": entry, "type": "directory",
                    "file_count": fc, "note": "depth_limit_reached"
                })
        else:
            file_count_here += 1
            try:
                total_size_here += os.path.getsize(full)
            except:
                pass

    tree["files_in_this_folder"] = file_count_here
    tree["size_in_this_folder"] = total_size_here
    return tree

tree = build_tree(BASE, max_depth=3)

index_meta = {
    "generated_at": datetime.now().isoformat(),
    "base_path": BASE,
    "total_files": file_count,
    "total_size_bytes": total_size,
    "total_size_readable": f"{total_size/1024**3:.2f} GB",
    "folder_stats": {k: v for k, v in sorted(folder_stats.items(), key=lambda x: -x[1]["file_count"])},
    "extension_stats": {k: v for k, v in sorted(ext_stats.items(), key=lambda x: -x[1]["count"])[:30]},
    "folder_tree": tree,
    "errors": errors[:100],
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(index_meta, f, ensure_ascii=False, indent=2)

print(f"  완료")

# --- 3. TXT: 사람이 읽는 요약 보고서 ---
print(f"[3/3] 요약 보고서 생성 중: {report_path}")

def fmt_size(b):
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.1f} MB"
    return f"{b/1024**3:.2f} GB"

with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("  문서 폴더 파일 인벤토리 보고서\n")
    f.write(f"  생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"  대상경로: {BASE}\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"  총 파일 수:  {file_count:,}개\n")
    f.write(f"  총 용량:     {fmt_size(total_size)}\n")
    f.write(f"  오류 건수:   {len(errors)}건\n\n")

    # 폴더별 통계
    f.write("-" * 70 + "\n")
    f.write("  [최상위 폴더별 통계]\n")
    f.write("-" * 70 + "\n")
    f.write(f"  {'폴더':<35} {'파일 수':>10} {'용량':>12}\n")
    f.write(f"  {'─'*35} {'─'*10} {'─'*12}\n")
    for folder, stats in sorted(folder_stats.items(), key=lambda x: -x[1]["file_count"]):
        f.write(f"  {folder:<35} {stats['file_count']:>10,} {fmt_size(stats['total_size']):>12}\n")

    f.write(f"\n")

    # 확장자별 통계
    f.write("-" * 70 + "\n")
    f.write("  [확장자별 통계 (상위 25개)]\n")
    f.write("-" * 70 + "\n")
    f.write(f"  {'확장자':<15} {'파일 수':>10} {'용량':>12}\n")
    f.write(f"  {'─'*15} {'─'*10} {'─'*12}\n")
    sorted_ext = sorted(ext_stats.items(), key=lambda x: -x[1]["count"])[:25]
    for ext, stats in sorted_ext:
        label = ext if ext else "(없음)"
        f.write(f"  {label:<15} {stats['count']:>10,} {fmt_size(stats['size']):>12}\n")

    f.write(f"\n")

    # 오류 목록
    if errors:
        f.write("-" * 70 + "\n")
        f.write(f"  [오류 목록 (최대 50건)]\n")
        f.write("-" * 70 + "\n")
        for err in errors[:50]:
            f.write(f"  {err}\n")

    f.write("\n" + "=" * 70 + "\n")
    f.write("  관련 파일:\n")
    f.write(f"  - CSV 인벤토리: {csv_path}\n")
    f.write(f"  - JSON 트리:    {json_path}\n")
    f.write(f"  - 이 보고서:    {report_path}\n")
    f.write("=" * 70 + "\n")

print(f"  완료\n")
print("=" * 50)
print(f"  생성된 파일:")
print(f"  1. {csv_path}")
print(f"  2. {json_path}")
print(f"  3. {report_path}")
print("=" * 50)
