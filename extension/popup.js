const API_BASE_URL = "http://localhost:5000";
let isProtectionActive = true;

async function loadStatsFromServer() {
  try {
    console.log("Загружаю статистику с сервера...");

    const response = await fetch(`${API_BASE_URL}/api/stats?user_id=1`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Получена статистика:", data);

    if (data.success) {
      document.getElementById("blockedCount").textContent =
        data.stats.total_blocks || 0;
      document.getElementById("filterCount").textContent =
        data.stats.unique_keywords_blocked || 0;

      const lastBlocked = data.stats.last_blocked;
      if (lastBlocked) {
        const date = new Date(lastBlocked);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);

        let timeText;
        if (diffMins < 1) {
          timeText = "только что";
        } else if (diffMins < 60) {
          timeText = `${diffMins} мин назад`;
        } else if (diffHours < 24) {
          timeText = `${diffHours} ч назад`;
        } else {
          timeText = date.toLocaleDateString("ru-RU");
        }

        document.getElementById("lastBlocked").textContent = timeText;
      } else {
        document.getElementById("lastBlocked").textContent = "никогда";
      }

      console.log("Статистика обновлена");
    } else {
      console.error("Ошибка в данных статистики:", data.error);
      setDefaultStats();
    }
  } catch (error) {
    console.error("Ошибка загрузки статистики:", error);
    setDefaultStats();
  }
}

function setDefaultStats() {
  document.getElementById("blockedCount").textContent = "0";
  document.getElementById("filterCount").textContent = "0";
  document.getElementById("lastBlocked").textContent = "никогда";
}

function updateStats() {
  if (isProtectionActive) {
    loadStatsFromServer().catch((error) => {
      console.error("Ошибка при обновлении статистики:", error);
    });
  }
}

document.addEventListener("DOMContentLoaded", async function () {
  console.log("Popup загружен, обновляю статистику...");

  await updateStats();

  let statsInterval = setInterval(updateStats, 3000);

  document.getElementById("settingsBtn").addEventListener("click", function () {
    window.open("http://localhost:5000", "_blank");
  });

  document.getElementById("pauseBtn").addEventListener("click", function () {
    const button = document.getElementById("pauseBtn");
    if (isProtectionActive) {
      button.textContent = "▶️ Возобновить защиту";
      button.style.background = "rgba(76, 175, 80, 0.3)";
      isProtectionActive = false;
      clearInterval(statsInterval);
    } else {
      button.textContent = "⏸️ Приостановить защиту";
      button.style.background = "rgba(255,255,255,0.2)";
      isProtectionActive = true;
      statsInterval = setInterval(updateStats, 3000);
      updateStats();
    }
  });

  document.getElementById("refreshBtn").addEventListener("click", function () {
    updateStats();
    const button = document.getElementById("refreshBtn");
    button.textContent = "⏳ Обновление...";
    setTimeout(() => {
      button.textContent = "🔄 Обновить статистику";
    }, 1000);
  });

  window.addEventListener("focus", updateStats);
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "updateStats") {
    updateStats();
  }
  return true;
});
