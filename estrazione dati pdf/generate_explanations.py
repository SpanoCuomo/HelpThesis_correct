#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
import argparse
from typing import List, Dict, Any

# ------------------------ Prompt template ------------------------

SYSTEM_PROMPT = """Sei un giurista didattico. Per ogni domanda fornita, aggiungi una spiegazione HTML molto dettagliata nel campo "explanation".
Lo stile DEVE seguire questa struttura a paragrafi (in italiano):
1) <p>✅ <strong>Risposta corretta: ...</strong></p>
2) <p>Paragrafo introduttivo che spiega il contesto e i concetti chiave.</p>
3) <p>Riferimento normativo preciso (articolo di legge/c.p.c./c.c., ecc.) e cosa dispone.</p>
4) <p>👉 Ratio/funzione della regola: perché esiste, cosa tutela, come si applica.</p>
5) <p>💡 <strong>Esempio pratico:</strong> esempio concreto e realistico.</p>

Importante:
- Mantieni intatti "id", "q", "options", "correct" (non modificarli).
- Compila SOLO il nuovo campo "explanation" come stringa HTML (nessun markdown).
- La spiegazione deve essere originale, non ripetitiva, e coerente con la risposta corretta.
- Non inventare norme se non necessarie: cita articoli reali dove possibile (es.: art. 147 c.p.c.).
- Restituisci SOLO un JSON array di oggetti con chiavi: id, explanation.
"""

# ⚠️ RADDOPPIA LE GRAFFE per evitare KeyError con .format(...)
USER_PROMPT_TEMPLATE = """Completa con "explanation" i seguenti quesiti.
Restituisci SOLO un JSON array, in cui ogni elemento è {{\"id\": <id>, \"explanation\": \"<html>\"}}
DOMANDE:
{payload}
"""

# ------------------------ LLM adapter ------------------------

def call_llm(messages: List[Dict[str, str]], provider: str, model: str, temperature: float = 0.2) -> str:
    """
    Provider supportati:
      - openai (SDK v1): pip install --upgrade openai
    """
    provider = (provider or "openai").lower().strip()

    if provider == "openai":
        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError("Libreria 'openai' non installata. Esegui: pip install --upgrade openai") from e

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("Variabile d'ambiente OPENAI_API_KEY mancante.")

        client = OpenAI()
        resp = client.chat.completions.create(
            model=model,                 # es.: "gpt-5" o un modello a cui hai accesso
            temperature=temperature,
            messages=messages
        )
        return resp.choices[0].message.content

    else:
        raise NotImplementedError(f"Provider non supportato: {provider}. Usa --provider openai.")

# ------------------------ Utility ------------------------

def chunk_list(seq, n):
    return [seq[i:i+n] for i in range(0, len(seq), n)]

def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": int(item["id"]),
        "q": item["q"],
        "options": {
            "A": item.get("A") or item.get("options", {}).get("A", ""),
            "B": item.get("B") or item.get("options", {}).get("B", ""),
            "C": item.get("C") or item.get("options", {}).get("C", ""),
        },
        "correct": item.get("correct", ""),
    }

def php_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

def to_php_array(questions: List[Dict[str, Any]]) -> str:
    rows = []
    for q in questions:
        row = []
        row.append('  [')
        row.append(f'    "id" => {q["id"]},')
        row.append(f'    "q"  => "{php_escape(q["q"])}",')
        row.append(f'    "options" => ["A" => "{php_escape(q["options"]["A"])}", "B" => "{php_escape(q["options"]["B"])}", "C" => "{php_escape(q["options"]["C"])}"],')
        row.append(f'    "correct" => "{php_escape(q["correct"])}",')
        if q.get("explanation"):
            row.append(f'    "explanation" => "{php_escape(q["explanation"])}"')
        else:
            row[-1] = row[-1].rstrip(",")
        row.append('  ]')
        rows.append("\n".join(row))
    return "<?php\n$questions = [\n" + ",\n".join(rows) + "\n];\n?>\n"

def save_php(out_path: str, questions_by_id: Dict[int, Dict[str, Any]]):
    ordered = [questions_by_id[i] for i in sorted(questions_by_id)]
    php_text = to_php_array(ordered)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(php_text)

def parse_json_array_or_raise(text: str) -> list:
    """Prova a fare json.loads direttamente; se fallisce, ripulisce code fences e spazi."""
    try:
        return json.loads(text)
    except Exception:
        # rimuovi eventuali code fence
        t = text.strip()
        if t.startswith("```"):
            t = t.strip("`")
            # dopo strip residuale, prova a trovare un array
        # prova a cercare il primo '[' e l'ultimo ']'
        start = t.find('[')
        end = t.rfind(']')
        if start != -1 and end != -1 and end > start:
            snippet = t[start:end+1]
            return json.loads(snippet)
        # se ancora errore, rilancia con preview utile
        preview = (text[:800] + "...") if len(text) > 800 else text
        raise RuntimeError(f"Parsing JSON fallito. Risposta del modello (inizio): {preview}")

# ------------------------ Core ------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="File JSON input (quiz_ag800sc.json)")
    ap.add_argument("--out", dest="out_path", required=True, help="File PHP output ($questions array)")
    ap.add_argument("--provider", default="openai", help="LLM provider (default: openai)")
    ap.add_argument("--model", default="gpt-5", help="Nome modello (es. gpt-5; usa un modello a cui hai accesso)")
    ap.add_argument("--chunk", type=int, default=20, help="Dimensione blocchi (default 20)")
    ap.add_argument("--temperature", type=float, default=0.2, help="Temperature LLM")
    ap.add_argument("--sleep", type=float, default=0.7, help="Pausa fra i batch per rate limiting")
    ap.add_argument("--save-every", action="store_true", help="Scrive/aggiorna il file PHP dopo ogni batch")
    ap.add_argument("--min-words", type=int, default=0, help="Se >0, chiede spiegazioni di almeno N parole")
    ap.add_argument("--start", type=int, default=None, help="ID iniziale (incluso) da processare")
    ap.add_argument("--end", type=int, default=None, help="ID finale (incluso) da processare")
    args = ap.parse_args()

    with open(args.in_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    questions = [normalize_item(it) for it in raw]
    questions_by_id = {q["id"]: q for q in questions}

    ids = sorted(questions_by_id)
    if args.start is not None or args.end is not None:
        lo = args.start if args.start is not None else ids[0]
        hi = args.end if args.end is not None else ids[-1]
        ids = [i for i in ids if lo <= i <= hi]

    batches = chunk_list(ids, args.chunk)

    sys_prompt = SYSTEM_PROMPT
    if args.min_words and args.min_words > 0:
        sys_prompt += f"\n- Ogni spiegazione deve contenere almeno {args.min_words} parole."

    for idx, batch_ids in enumerate(batches, 1):
        batch_items = [questions_by_id[i] for i in batch_ids]
        payload = json.dumps(batch_items, ensure_ascii=False, indent=2)
        user_prompt = USER_PROMPT_TEMPLATE.format(payload=payload)

        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]

        print(f"[Batch {idx}/{len(batches)}] Invio {len(batch_items)} domande al modello…")

        # retry semplice con backoff
        backoff = 1.0
        for attempt in range(5):
            try:
                text = call_llm(messages, provider=args.provider, model=args.model, temperature=args.temperature).strip()
                break
            except Exception as e:
                print(f"  Tentativo {attempt+1} fallito: {e}")
                time.sleep(backoff)
                backoff *= 1.6
        else:
            raise RuntimeError("Troppe failure consecutive verso l'API.")

        resp = parse_json_array_or_raise(text)
        if not isinstance(resp, list):
            raise RuntimeError("La risposta del modello non è un array JSON.")

        for obj in resp:
            qid = int(obj["id"])
            exp = (obj.get("explanation") or "").strip()
            if qid in questions_by_id and exp:
                questions_by_id[qid]["explanation"] = exp

        if args.save_every:
            save_php(args.out_path, questions_by_id)
            print(f"  ✓ Aggiornato: {args.out_path}")

        time.sleep(args.sleep)

    save_php(args.out_path, questions_by_id)
    print(f"✅ File PHP generato: {args.out_path}")

if __name__ == "__main__":
    main()
