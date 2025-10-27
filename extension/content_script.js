console.log("SpoilerBlocker активирован! Загружаю ключевые слова...");

let SPOILER_KEYWORDS = [];
let USER_ID = 1;
let API_BASE_URL = "http://localhost:5000";

async function loadKeywordsFromServer() {
  try {
    console.log("Загружаю ключевые слова с API сервера...");

    const response = await fetch(`${API_BASE_URL}/api/keywords`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      SPOILER_KEYWORDS = data.keywords.map((kw) => kw.text);
      console.log(`Загружено ${SPOILER_KEYWORDS.length} ключевых слов`);
    } else {
      console.error("Ошибка загрузки ключевых слов:", data.error);
      SPOILER_KEYWORDS = ["спойлер", "финал", "смерть персонажа", "развязка"];
    }
  } catch (error) {
    console.error("Ошибка подключения к API серверу:", error);
    SPOILER_KEYWORDS = ["спойлер", "финал", "смерть персонажа", "развязка"];
  }
}

async function sendBlockLogToServer(keywordText, blockedContent) {
  try {
    console.log(`Отправляю лог блокировки: "${keywordText}"`);

    const logData = {
      user_id: USER_ID,
      keyword_text: keywordText,
      url: window.location.href,
      content: blockedContent.substring(0, 100),
    };

    const response = await fetch(`${API_BASE_URL}/api/block`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logData),
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const result = await response.json();
    if (result.success) {
      console.log("Лог блокировки успешно отправлен на сервер");
    }
  } catch (error) {
    console.error("Ошибка отправки лога на сервер:", error);
  }
}

function blockSpoilers() {
  if (SPOILER_KEYWORDS.length === 0) {
    console.log("Ключевые слова еще не загружены с сервера...");
    return;
  }

  let blockedCount = 0;

  SPOILER_KEYWORDS.forEach((spoiler) => {
    const regex = new RegExp(spoiler, "gi");
    const elements = document.body.getElementsByTagName("*");

    for (let element of elements) {
      for (let node of element.childNodes) {
        if (node.nodeType === Node.TEXT_NODE) {
          const originalText = node.textContent;

          if (regex.test(originalText)) {
            const blockedText = originalText.replace(
              regex,
              "[СПОЙЛЕР ЗАБЛОКИРОВАН]"
            );
            node.textContent = blockedText;
            blockedCount++;

            sendBlockLogToServer(spoiler, originalText);
          }
        }
      }
    }
  });

  if (blockedCount > 0) {
    console.log(`SpoilerBlocker заблокировал ${blockedCount} спойлеров`);
  }
}

async function initializeExtension() {
  console.log("Инициализация SpoilerBlocker...");

  await loadKeywordsFromServer();
  blockSpoilers();

  setInterval(blockSpoilers, 3000);

  console.log("SpoilerBlocker успешно инициализирован и работает!");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeExtension);
} else {
  initializeExtension();
}

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length) {
      setTimeout(blockSpoilers, 100);
    }
  });
});

observer.observe(document.body, { childList: true, subtree: true });
