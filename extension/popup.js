const API_BASE_URL = "http://localhost:5000";

async function loadStatsFromServer() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/stats?user_id=1`);

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.json();

    if (data.success) {
      document.getElementById("blockedCount").textContent =
        data.stats.total_blocks || 0;
      document.getElementById("filterCount").textContent =
        data.stats.unique_keywords_blocked || 0;

      const lastBlocked = data.stats.last_blocked;
      if (lastBlocked) {
        const date = new Date(lastBlocked).toLocaleDateString();
        document.getElementById("lastBlocked").textContent = date;
      }
    }
  } catch (error) {
    console.error("Ошибка загрузки статистики:", error);
    document.getElementById("blockedCount").textContent = "0";
    document.getElementById("filterCount").textContent = "0";
    document.getElementById("lastBlocked").textContent = "никогда";
  }
}

document.addEventListener("DOMContentLoaded", async function () {
  await loadStatsFromServer();

  document.getElementById("settingsBtn").addEventListener("click", function () {
    window.open("http://localhost:5000", "_blank");
  });

  document.getElementById("pauseBtn").addEventListener("click", function () {
    const button = document.getElementById("pauseBtn");
    if (button.textContent.includes("Приостановить")) {
      button.textContent = "▶️ Возобновить";
    } else {
      button.textContent = "⏸️ Приостановить";
    }
  });
});
