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
