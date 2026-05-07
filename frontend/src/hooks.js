import { useEffect, useState } from "react";

import { apiFetch } from "./api";

export function useAsyncData(loader, deps = []) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError("");

    loader()
      .then((payload) => {
        if (alive) {
          setData(payload);
        }
      })
      .catch((err) => {
        if (alive) {
          setError(err.message);
        }
      })
      .finally(() => {
        if (alive) {
          setLoading(false);
        }
      });

    return () => {
      alive = false;
    };
  }, deps);

  return { data, error, loading, setData };
}

export function useUsers() {
  return useAsyncData(() => apiFetch("/users"), []);
}

export function rememberUser(userId) {
  window.localStorage.setItem("friend_persona_user_id", String(userId));
}

export function getRememberedUser() {
  return window.localStorage.getItem("friend_persona_user_id");
}
