import { Medal } from "lucide-react";
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { apiFetch } from "../api";
import { useAsyncData } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";

export default function LeaderboardPage() {
  const { data, error, loading } = useAsyncData(() => apiFetch("/leaderboard"), []);
  const [selectedKey, setSelectedKey] = useState("");

  const boards = data?.leaderboards || [];
  const activeBoard = useMemo(() => {
    if (boards.length === 0) {
      return null;
    }
    return boards.find((board) => board.trait_key === selectedKey) || boards[0];
  }, [boards, selectedKey]);

  return (
    <section className="stack-page">
      <div className="page-title-row">
        <div>
          <span className="eyebrow">排行榜</span>
          <h1>历史人格江湖座次</h1>
        </div>
      </div>

      {loading && <LoadingState text="正在排座次..." />}
      {error && <Message tone="error">{error}</Message>}

      {boards.length > 0 && (
        <>
          <div className="board-tabs" role="tablist">
            {boards.map((board) => (
              <button
                key={board.trait_key}
                className={activeBoard?.trait_key === board.trait_key ? "active" : ""}
                onClick={() => setSelectedKey(board.trait_key)}
              >
                {board.board_name}
              </button>
            ))}
          </div>

          <article className="leaderboard-panel">
            <div className="leaderboard-title">
              <Medal size={22} />
              <div>
                <h2>{activeBoard.board_name}</h2>
                <span>{activeBoard.trait_name}历史累计投票排序</span>
              </div>
            </div>

            <div className="rank-list">
              {activeBoard.entries.map((entry) => (
                <Link key={entry.user.id} className="rank-row" to={`/profile/${entry.user.id}`}>
                  <span className={`rank-number rank-${entry.rank}`}>{entry.rank}</span>
                  <span className="avatar small">{entry.user.avatar}</span>
                  <strong>{entry.user.nickname}</strong>
                  <span>{entry.score}</span>
                </Link>
              ))}
            </div>
          </article>
        </>
      )}
    </section>
  );
}
