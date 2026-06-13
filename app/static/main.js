const fetchBtn = document.getElementById("fetch-btn");
const checkBtn = document.getElementById("check-btn");
const questionArea = document.getElementById("question-area");
const questionMeta = document.getElementById("question-meta");
const questionText = document.getElementById("question-text");
const previewsEl = document.getElementById("previews");
const sqlInput = document.getElementById("sql-input");
const resultArea = document.getElementById("result-area");
const resultTitle = document.getElementById("result-title");
const resultMeta = document.getElementById("result-meta");
const resultTable = document.getElementById("result-table");
const feedbackEl = document.getElementById("feedback");
const noKeyNotice = document.getElementById("no-key-notice");

let currentQuestionId = null;

if (!localStorage.getItem("gemini_api_key")) {
  noKeyNotice.classList.remove("hidden");
}

function renderTable(container, columns, rows, caption) {
  if (!rows.length) {
    container.innerHTML += `<p class="meta">${caption ? caption + ": " : ""}結果は0件です。</p>`;
    return;
  }
  let html = "<div class='table-scroll'><table>";
  if (caption) {
    html += `<caption class="meta" style="text-align:left;">${caption}</caption>`;
  }
  html += "<thead><tr>";
  for (const col of columns) {
    html += `<th>${col}</th>`;
  }
  html += "</tr></thead><tbody>";
  for (const row of rows) {
    html += "<tr>";
    for (const value of row) {
      html += `<td>${value === null ? "NULL" : value}</td>`;
    }
    html += "</tr>";
  }
  html += "</tbody></table></div>";
  container.innerHTML += html;
}

async function fetchQuestion() {
  const difficulty = document.querySelector('input[name="difficulty"]:checked').value;
  const res = await fetch(`/api/question?difficulty=${difficulty}`);
  const data = await res.json();
  if (!res.ok) {
    alert(data.error || "問題の取得に失敗しました。");
    return;
  }

  currentQuestionId = data.id;
  questionMeta.textContent = `カテゴリ: ${data.category} / 難易度: ${data.difficulty}`;
  questionText.textContent = data.question;

  previewsEl.innerHTML = "";
  for (const table of data.tables) {
    const preview = data.previews[table];
    const heading = document.createElement("h2");
    heading.textContent = `テーブル: ${table}（先頭${preview.rows.length}件 / 全${preview.total_rows}件）`;
    previewsEl.appendChild(heading);
    renderTable(previewsEl, preview.columns, preview.rows);
  }

  sqlInput.value = "";
  resultArea.classList.add("hidden");
  questionArea.classList.remove("hidden");
}

async function checkAnswer() {
  const sql = sqlInput.value.trim();
  if (!sql) {
    alert("回答SQLを入力してください。");
    return;
  }

  checkBtn.disabled = true;
  checkBtn.textContent = "判定中...";

  try {
    const res = await fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: currentQuestionId,
        sql: sql,
        gemini_api_key: localStorage.getItem("gemini_api_key") || "",
      }),
    });
    const data = await res.json();

    if (!res.ok) {
      alert(data.error || "判定に失敗しました。");
      return;
    }

    resultArea.classList.remove("hidden");
    if (data.correct) {
      resultTitle.textContent = "✅ 正解";
      resultTitle.className = "result-correct";
    } else if (data.sql_error) {
      resultTitle.textContent = "❌ 不正解（SQLエラー）";
      resultTitle.className = "result-incorrect";
    } else {
      resultTitle.textContent = "❌ 不正解";
      resultTitle.className = "result-incorrect";
    }

    resultTable.innerHTML = "";
    if (data.sql_error) {
      resultMeta.textContent = "";
      resultTable.innerHTML = `<p class="meta">SQLエラー: ${data.sql_error}</p>`;
    } else {
      resultMeta.textContent = `あなたの実行結果: ${data.your_row_count}件 / 正解の実行結果: ${data.expected_row_count}件`;
      renderTable(resultTable, data.your_columns, data.your_result, "あなたの実行結果");
    }

    if (data.feedback) {
      feedbackEl.textContent = data.feedback;
      feedbackEl.classList.remove("hidden");
    } else {
      feedbackEl.classList.add("hidden");
    }
  } finally {
    checkBtn.disabled = false;
    checkBtn.textContent = "回答する";
  }
}

fetchBtn.addEventListener("click", fetchQuestion);
checkBtn.addEventListener("click", checkAnswer);
