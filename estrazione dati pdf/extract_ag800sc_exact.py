#!/usr/bin/env python3
# -- coding: utf-8 --

import argparse
import json
import os
import re
from typing import List, Tuple, Dict, Any

# Regex
NUM_ONLY_RE = re.compile(r'^\d{1,4}$')
PAIR_LINE_RE = re.compile(r'^\s*(\d{1,4})\s+([ABC])\s*$', re.M)


def read_lines(path: str) -> Tuple[List[str], str]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    return raw.replace("\r\n", "\n").replace("\r", "\n").split("\n"), raw


def is_number_only(s: str) -> bool:
    return bool(NUM_ONLY_RE.fullmatch(s.strip()))


def next_nonempty_idx(lines: List[str], i: int) -> int | None:
    j = i + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    return j if j < len(lines) else None


def split_question_blocks(lines: List[str]) -> List[Tuple[int, List[str]]]:
    """
    Splitta in blocchi (id, righe_blocco) usando un lookahead:
    una riga numerica è INIZIO DOMANDA solo se la prossima riga non vuota NON è numerica.
    """
    entries: List[Tuple[int, List[str]]] = []
    current_id: int | None = None
    buf: List[str] = []

    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if is_number_only(ln):
            j = next_nonempty_idx(lines, i)
            nxt = lines[j] if j is not None else ""
            if current_id is None:
                if not is_number_only(nxt):
                    current_id = int(ln)
                    buf = []
            else:
                if not is_number_only(nxt):
                    # chiudo il blocco precedente
                    entries.append((current_id, buf[:]))
                    current_id = int(ln)
                    buf = []
                else:
                    buf.append(ln)
        else:
            if current_id is not None and ln != "":
                buf.append(ln)
        i += 1

    if current_id is not None:
        entries.append((current_id, buf[:]))

    return entries


def normalize_space(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_block_to_record(qid: int, block: List[str]) -> Dict[str, Any]:
    data = [ln.strip() for ln in block if ln.strip() != ""]
    if len(data) >= 4:
        q_lines = data[:-3]
        opts = data[-3:]
    else:
        # fallback grezzo se il blocco non è nel formato atteso
        q_lines = data[:-3] if len(data) > 3 else data
        opts = data[-3:] if len(data) >= 3 else ["", "", ""]

    q = " ".join(q_lines).strip()
    q = normalize_space(q)

    # Opzioni A, B, C
    A, B, C = (opts + ["", "", ""])[:3]
    A = normalize_space(A)
    B = normalize_space(B)
    C = normalize_space(C)

    return {"id": qid, "q": q, "A": A, "B": B, "C": C}


def read_answer_key(raw_text: str) -> Dict[int, str]:
    pairs = PAIR_LINE_RE.findall(raw_text)
    return {int(i): l for i, l in pairs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Percorso al file TXT.")
    ap.add_argument("-o", "--output", help="Percorso JSON di output (default input.json).")
    args = ap.parse_args()

    lines, raw = read_lines(args.input)
    blocks = split_question_blocks(lines)

    # Ordina per id
    blocks.sort(key=lambda t: t[0])

    records = [parse_block_to_record(qid, blk) for qid, blk in blocks]

    # Mappa risposte corrette
    ans_map = read_answer_key(raw)
    for r in records:
        r["correct"] = ans_map.get(r["id"], None)

    # Statistiche
    missing_correct = [r["id"] for r in records if r["correct"] is None]
    missing_opts = [r["id"] for r in records if not (r["A"] and r["B"] and r["C"])]

    out_path = args.output or os.path.splitext(args.input)[0] + ".json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"[OK] Salvato {out_path}")
    print(f"[INFO] Domande totali {len(records)}")
    if missing_correct:
        print(f"[ATTENZIONE] Soluzione mancante per id {missing_correct}")
    if missing_opts:
        print(f"[ATTENZIONE] Opzioni incomplete per id {missing_opts}")


if __name__ == "__main__":
    main()
