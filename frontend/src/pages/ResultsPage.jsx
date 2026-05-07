import { Copy, Crown } from "lucide-react";
import { useState } from "react";

import { apiFetch } from "../api";
import { useAsyncData } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";

export default function ResultsPage() {
  const { data, error, loading } = useAsyncData(() => apiFetch("/results/today"), []);
  const [copied, setCopied] = useState(false);

  async function shareResults() {
    await navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <section className="stack-page results-page">
      <div className="page-title-row">
        <div>
          <span className="eyebrow">今日结果</span>
          <h1>群友今日人格播报</h1>
        </div>
        <button className="icon-text-button" onClick={shareResults}>
          <Copy size={18} />
          {copied ? "已复制" : "分享"}
        </button>
      </div>

      {loading && <LoadingState text="正在统计今日整活指数..." />}
      {error && <Message tone="error">{error}</Message>}

      <div className="result-stack">
        {data?.results.map((item, index) => (
          <article key={item.question.id} className="result-card">
            <div className="question-topline">
              <span>题目 {index + 1}</span>
              <span>{item.question.category}</span>
            </div>
            <h2>{item.question.text}</h2>

            {item.champions.length > 0 ? (
              <div className="champion-row">
                <Crown size={22} />
                <div>
                  <strong>{item.champions.map((user) => user.nickname).join("、")}</strong>
                  <span>{item.top_count} 票登顶</span>
                </div>
              </div>
            ) : (
              <div className="champion-row empty">
                <Crown size={22} />
                <div>
                  <strong>暂无冠军</strong>
                  <span>第一票还在路上</span>
                </div>
              </div>
            )}

            <p className="commentary">{item.commentary}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
