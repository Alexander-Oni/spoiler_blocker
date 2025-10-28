console.log("Background script запущен");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "blockedContent") {
    console.log("Получено сообщение о блокировке, обновляю статистику...");

    chrome.runtime.sendMessage({ action: "updateStats" });
  }

  return true;
});

chrome.runtime.onInstalled.addListener(() => {
  console.log("SpoilerBlocker установлен!");
});
