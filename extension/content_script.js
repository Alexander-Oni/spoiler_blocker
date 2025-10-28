console.log("SpoilerBlocker активирован! Загружаю ключевые слова...");

let SPOILER_KEYWORDS = [];
let USER_ID = 1;
let API_BASE_URL = "http://localhost:5000";

function decodeUnicode(str) {
  try {
    return str.replace(/\\u[\dA-F]{4}/gi, (match) =>
      String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16))
    );
  } catch (e) {
    console.log("Ошибка декодирования:", e);
    return str; // Если ошибка - возвращаем как есть
  }
}

function normalizeKeywords(keywords) {
  return keywords.map((keyword) => {
    // Убираем лишние пробелы и приводим к нижнему регистру для поиска
    return keyword.trim().toLowerCase();
  });
}

async function loadKeywordsFromServer() {
  try {
    console.log("Загружаю ключевые слова с API сервера...");

    const response = await fetch(`${API_BASE_URL}/api/keywords`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Получены данные:", data);

    if (data.success) {
      SPOILER_KEYWORDS = data.keywords.map((kw) => {
        const decodedText = decodeUnicode(kw.text);
        console.log(`Декодировано: "${kw.text}" → "${decodedText}"`);
        return decodedText;
      });

      SPOILER_KEYWORDS = normalizeKeywords(SPOILER_KEYWORDS);

      console.log(`Загружено ${SPOILER_KEYWORDS.length} ключевых слов`);
      console.log("Слова для блокировки:", SPOILER_KEYWORDS);
    } else {
      console.error("Ошибка загрузки ключевых слов:", data.error);
      useDefaultKeywords();
    }
  } catch (error) {
    console.error("Ошибка подключения к API серверу:", error);
    useDefaultKeywords();
  }
}

function useDefaultKeywords() {
  // ИСПОЛЬЗУЕМ ПРАВИЛЬНУЮ КИРИЛЛИЦУ
  SPOILER_KEYWORDS = [
    "Игра престолов финал",
    "Смерть Тони Старка",
    "Сюжет Дюны",
    "спойлер",
    "финал",
    "смерть персонажа",
    "развязка",
  ];
  console.log("Использую тестовые слова:", SPOILER_KEYWORDS);
  setTimeout(blockSpoilers, 100);
}

async function sendBlockLogToServer(keywordText, blockedContent) {
  try {
    console.log(`Отправляю лог блокировки: "${keywordText}"`);

    const logData = {
      user_id: USER_ID,
      keyword_text: keywordText,
      url: window.location.href,
      content: blockedContent.substring(0, 200),
    };

    console.log("Данные для отправки:", logData);

    const response = await fetch(`${API_BASE_URL}/api/block`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(logData),
    });

    console.log(`Статус ответа: ${response.status}`);

    if (!response.ok) {
      const errorText = await response.text();

      // Если ключевое слово не найдено, добавляем его автоматически
      if (response.status === 404 && errorText.includes("Keyword not found")) {
        console.log(
          `Ключевое слово "${keywordText}" не найдено в базе. Можно добавить автоматически.`
        );
        // Здесь можно добавить логику для автоматического добавления ключевого слова
      }

      throw new Error(
        `HTTP error! status: ${response.status}, response: ${errorText}`
      );
    }

    const result = await response.json();
    console.log("Ответ сервера:", result);

    if (result.success) {
      console.log("✅ Лог блокировки успешно записан в базу данных");

      // Обновляем статистику в popup
      chrome.runtime.sendMessage({ action: "blockedContent" });
    } else {
      console.error("❌ Ошибка на сервере:", result.error);
    }
  } catch (error) {
    console.error("❌ Ошибка отправки лога на сервер:", error);

    if (error.message.includes("Failed to fetch")) {
      console.error("🔧 Проблема с сетью или CORS. Проверьте:");
      console.error("   - Запущен ли API сервер на localhost:5000");
    } else if (error.message.includes("404")) {
      console.error("🔍 Ключевое слово не найдено в базе данных");
      console.error(
        "   - Запустите скрипт add_test_keywords.py для добавления тестовых данных"
      );
    } else if (error.message.includes("500")) {
      console.error("💾 Ошибка сервера. Проверьте логи API");
    }
  }
}

function blockSpoilers() {
  console.log(
    `Начинаю проверку страницы. Доступно слов: ${SPOILER_KEYWORDS.length}`
  );

  if (SPOILER_KEYWORDS.length === 0) {
    console.log("Нет ключевых слов для блокировки");
    return;
  }

  let blockedCount = 0;
  const elements = document.querySelectorAll(
    "p, span, div, li, td, h1, h2, h3, h4, h5, h6, a, strong, em"
  );

  elements.forEach((element) => {
    // Пропускаем элементы, которые уже были обработаны
    if (element.classList.contains("spoiler-blocker-processed")) {
      return;
    }

    // Помечаем элемент как обработанный
    element.classList.add("spoiler-blocker-processed");

    // Работаем с текстовыми узлами внутри элемента
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) {
      textNodes.push(node);
    }

    textNodes.forEach((textNode) => {
      const originalText = textNode.textContent;
      let modifiedText = originalText;

      SPOILER_KEYWORDS.forEach((spoiler) => {
        try {
          const regex = new RegExp(spoiler, "gi");
          if (regex.test(modifiedText)) {
            modifiedText = modifiedText.replace(
              regex,
              " [СПОЙЛЕР ЗАБЛОКИРОВАН] "
            );
            blockedCount++;
            console.log(`Заблокирован: "${spoiler}"`);
            sendBlockLogToServer(spoiler, originalText.substring(0, 200));
          }
        } catch (error) {
          console.error(`Ошибка при обработке слова "${spoiler}":`, error);
        }
      });

      // Заменяем текстовый узел только если были изменения
      if (modifiedText !== originalText) {
        const newSpan = document.createElement("span");
        newSpan.innerHTML = modifiedText.replace(
          /\[СПОЙЛЕР ЗАБЛОКИРОВАН\]/g,
          '<span style="background: #ffeb3b; color: #000; padding: 2px 4px; border-radius: 3px; font-weight: bold;">[СПОЙЛЕР ЗАБЛОКИРОВАН]</span>'
        );
        textNode.parentNode.replaceChild(newSpan, textNode);
      }
    });
  });

  if (blockedCount > 0) {
    console.log(`SpoilerBlocker заблокировал ${blockedCount} спойлеров`);
    showBlockNotification(blockedCount);
  }
}

function showBlockNotification(count) {
  const notification = document.createElement("div");
  notification.innerHTML = `
        <div style="background: #4CAF50; color: white; padding: 10px 15px; border-radius: 5px; 
                   font-family: Arial, sans-serif; font-size: 14px; margin-bottom: 5px;">
            🛡️ SpoilerBlocker заблокировал ${count} спойлеров
        </div>
    `;
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

async function initializeExtension() {
  console.log("Инициализация SpoilerBlocker...");
  console.log("Текущая страница:", window.location.href);

  try {
    await loadKeywordsFromServer();
  } catch (error) {
    console.error("Ошибка инициализации:", error);
    useDefaultKeywords();
  }

  // Периодическая проверка
  setInterval(() => {
    console.log("Периодическая проверка...");
    blockSpoilers();
  }, 5000);

  console.log("SpoilerBlocker успешно инициализирован и работает!");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeExtension);
} else {
  setTimeout(initializeExtension, 100);
}

const observer = new MutationObserver((mutations) => {
  let hasChanges = false;

  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length > 0) {
      hasChanges = true;
    }
  });

  if (hasChanges) {
    console.log("Обнаружены изменения DOM, проверяю...");
    setTimeout(blockSpoilers, 500);
  }
});

setTimeout(() => {
  try {
    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    console.log("Наблюдатель за изменениями активирован");
  } catch (error) {
    console.error("Ошибка запуска наблюдателя:", error);
  }
}, 1000);
