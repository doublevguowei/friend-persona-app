import { CheckCircle2, SendHorizonal } from "lucide-react";
import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

import { apiFetch } from "../api";
import { rememberUser, useAsyncData, useUsers } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";

export default function VotePage() {
  const [searchParams] = useSearchParams();
  const userId = Number(searchParams.get("user_id"));
  const [selectedTargets, setSelectedTargets] = useState({});
  const [feedback, setFeedback] = useState("");
  const [submittingId, setSubmittingId] = useState(null);

  const { data: users, error: usersError, loading: usersLoading } = useUsers();
  const {
    data: daily,
    error: dailyError,
    loading: dailyLoading,
    setData: setDaily
  } = useAsyncData(
    () => apiFetch(`/daily-questions${userId ? `?user_id=${userId}` : ""}`),
    [userId]
  );

  const currentUser = useMemo(() => users?.find((user) => user.id === userId), [users, userId]);
  const candidates = useMemo(() => users?.filter((user) => user.id !== userId) || [], [users, userId]);

  if (!userId) {
    return (
      <section className="stack-page">
        <Message tone="error">先选个身份再投票，不然系统不知道是谁在整活。</Message>
        <Link className="primary-link" to="/">
          返回首页选择身份
        </Link>
      </section>
    );
  }

  if (userId && currentUser) {
    rememberUser(userId);
  }

  async function submitVote(question) {
    const targetId = Number(selectedTargets[question.id]);
    if (!targetId) {
      setFeedback("这题还没选人，先抓一个今日代表。");
      return;
    }

    setSubmittingId(question.id);
    setFeedback("");
    try {
      const payload = await apiFetch("/vote", {
        method: "POST",
        body: JSON.stringify({
          voter_id: userId,
          question_id: question.id,
          target_id: targetId
        })
      });
      setFeedback(payload.message);
      setDaily((prev) => ({
        ...prev,
        questions: prev.questions.map((item) =>
          item.id === question.id ? { ...item, has_voted: true, voted_target_id: targetId } : item
        )
      }));
    } catch (err) {
      setFeedback(err.message);
    } finally {
      setSubmittingId(null);
    }
  }

  const loading = usersLoading || dailyLoading;
  const error = usersError || dailyError;

  return (
    <section className="stack-page">
      <div className="page-title-row">
        <div>
          <span className="eyebrow">今日投票</span>
          <h1>{currentUser ? `${currentUser.nickname}，开投` : "今日投票"}</h1>
        </div>
        <Link className="ghost-button" to="/">
          换身份
        </Link>
      </div>

      {loading && <LoadingState text="正在生成今日 4 题..." />}
      {error && <Message tone="error">{error}</Message>}
      {feedback && <Message>{feedback}</Message>}

      <div className="question-list">
        {daily?.questions.map((question, index) => {
          const votedTarget = users?.find((user) => user.id === question.voted_target_id);
          return (
            <article key={question.id} className="question-card">
              <div className="question-topline">
                <span>第 {index + 1} 题</span>
                <span>{question.category}</span>
              </div>
              <h2>{question.text}</h2>
              <p>{question.trait_name} +1</p>

              {question.has_voted ? (
                <div className="voted-state">
                  <CheckCircle2 size={20} />
                  <span>已投给 {votedTarget?.nickname || "某位群友"}，今日无法反悔。</span>
                </div>
              ) : (
                <>
                  <div className="candidate-grid">
                    {candidates.map((user) => (
                      <button
                        key={user.id}
                        className={`candidate-button ${
                          Number(selectedTargets[question.id]) === user.id ? "selected" : ""
                        }`}
                        onClick={() =>
                          setSelectedTargets((prev) => ({
                            ...prev,
                            [question.id]: user.id
                          }))
                        }
                      >
                        <span>{user.avatar}</span>
                        {user.nickname}
                      </button>
                    ))}
                  </div>
                  <button
                    className="primary-button"
                    disabled={submittingId === question.id}
                    onClick={() => submitVote(question)}
                  >
                    <SendHorizonal size={18} />
                    {submittingId === question.id ? "提交中..." : "就投这个"}
                  </button>
                </>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
