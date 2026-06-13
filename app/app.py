"""study-sql: SQL練習問題アプリ (Flask)

起動方法:
    python app/app.py

起動後、ブラウザで http://127.0.0.1:8000 を開く。
"""

import json
import random
import re
import sqlite3
from collections import Counter
from pathlib import Path

from flask import Flask, jsonify, render_template, request

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "db" / "sample.db"
QUESTIONS_PATH = APP_DIR / "data" / "questions.json"

with open(QUESTIONS_PATH, encoding="utf-8") as f:
    QUESTIONS = json.load(f)

QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS}

QUESTIONS_BY_DIFFICULTY: dict[str, list[dict]] = {}
for q in QUESTIONS:
    QUESTIONS_BY_DIFFICULTY.setdefault(q["difficulty"], []).append(q)

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"

FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter", "create",
    "replace", "attach", "detach", "pragma", "vacuum", "reindex", "grant",
}

app = Flask(__name__)


def validate_select_only(sql: str) -> str:
    cleaned = sql.strip()
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()
    if not cleaned:
        raise ValueError("SQLが空です。")
    if ";" in cleaned:
        raise ValueError("複数のSQL文は実行できません。")

    first_word_match = re.match(r"[a-zA-Z]+", cleaned)
    first_word = first_word_match.group(0).lower() if first_word_match else ""
    if first_word not in ("select", "with"):
        raise ValueError("SELECT文（またはWITH句）のみ実行できます。")

    tokens = set(re.findall(r"[a-zA-Z]+", cleaned.lower()))
    bad_tokens = tokens & FORBIDDEN_KEYWORDS
    if bad_tokens:
        raise ValueError(f"使用できないキーワードが含まれています: {', '.join(sorted(bad_tokens))}")

    return cleaned


def run_query(sql: str) -> tuple[list[tuple], list[str]]:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description] if cur.description else []
        return rows, columns
    finally:
        conn.close()


def table_preview(table_name: str, limit: int = 10) -> dict:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description]
        total_rows = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        return {
            "columns": columns,
            "rows": [list(r) for r in rows],
            "total_rows": total_rows,
        }
    finally:
        conn.close()


def normalize_rows(rows: list[tuple]) -> Counter:
    normalized = []
    for row in rows:
        normalized.append(tuple(round(v, 4) if isinstance(v, float) else v for v in row))
    return Counter(normalized)


def get_feedback(question: str, user_sql: str, user_result: list[tuple],
                expected_result: list[tuple], api_key: str | None, model: str,
                sql_error: str | None = None) -> str:
    if not api_key:
        return "(Gemini APIキーが設定されていないため、AIによる解説はスキップされました。「はじめての人はこちら」からAPIキーを設定してください)"

    from google import genai

    if sql_error:
        result_section = f"""# SQLの実行エラー
{sql_error}
"""
    else:
        result_section = f"""# 受講者の実行結果（先頭5件、列数={len(user_result[0]) if user_result else 0}）
{user_result[:5]}

# 正解の実行結果の件数
{len(expected_result)}件（先頭5件: {expected_result[:5]}）
"""

    prompt = f"""あなたはSQLの先生です。受講者がSQLの練習問題に回答しましたが、結果が正解と一致しませんでした
（SQLの実行エラーになっている場合もあります）。
正解のSQLそのものは教えず、何が間違っている可能性が高いかを2〜3文程度の日本語で簡潔に指摘し、改善のヒントを与えてください。

# 問題文
{question}

# 受講者が実行したSQL
{user_sql}

{result_section}"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text or "(AIからの応答が空でした)"
    except Exception as e:
        return f"(AI評価中にエラーが発生しました: {e})"


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/setup")
def setup():
    return render_template("setup.html", default_model=DEFAULT_GEMINI_MODEL)


@app.get("/practice")
def practice():
    return render_template("practice.html")


@app.get("/api/question")
def api_question():
    difficulty = request.args.get("difficulty", "easy")
    candidates = QUESTIONS_BY_DIFFICULTY.get(difficulty)
    if not candidates:
        valid = "/".join(QUESTIONS_BY_DIFFICULTY.keys())
        return jsonify({"error": f"difficultyは{valid}のいずれかを指定してください。"}), 400

    q = random.choice(candidates)
    previews = {table: table_preview(table) for table in q["tables"]}

    return jsonify({
        "id": q["id"],
        "category": q["category"],
        "difficulty": q["difficulty"],
        "question": q["question"],
        "tables": q["tables"],
        "previews": previews,
    })


@app.post("/api/check")
def api_check():
    data = request.get_json(force=True) or {}
    question_id = data.get("question_id")
    sql = data.get("sql", "")
    api_key = (data.get("gemini_api_key") or "").strip() or None
    model = (data.get("gemini_model") or "").strip() or DEFAULT_GEMINI_MODEL

    q = QUESTIONS_BY_ID.get(question_id)
    if q is None:
        return jsonify({"error": "指定されたquestion_idの問題が見つかりません。"}), 404

    try:
        cleaned_sql = validate_select_only(sql)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    sql_error = None
    try:
        user_rows, user_columns = run_query(cleaned_sql)
    except sqlite3.Error as e:
        user_rows, user_columns = [], []
        sql_error = str(e)

    expected_rows, _ = run_query(q["answer_sql"])
    is_correct = sql_error is None and normalize_rows(user_rows) == normalize_rows(expected_rows)

    feedback = None
    if not is_correct:
        feedback = get_feedback(q["question"], sql, user_rows, expected_rows, api_key, model, sql_error)

    return jsonify({
        "correct": is_correct,
        "your_columns": user_columns,
        "your_result": [list(r) for r in user_rows[:20]],
        "your_row_count": len(user_rows),
        "expected_row_count": len(expected_rows),
        "sql_error": sql_error,
        "feedback": feedback,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)
