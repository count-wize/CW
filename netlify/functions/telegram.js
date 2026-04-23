exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!token || !chatId) {
    return { statusCode: 500, body: "Missing Telegram credentials" };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: "Invalid JSON" };
  }

  const { message, files } = body;

  // Send text message
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text: message,
      parse_mode: "HTML",
    }),
  });

  // Send files if any
  if (Array.isArray(files) && files.length > 0) {
    for (const file of files) {
      const buffer = Buffer.from(file.data, "base64");
      const formData = new FormData();
      formData.append("chat_id", chatId);
      formData.append(
        "document",
        new Blob([buffer], { type: file.type }),
        file.name
      );
      await fetch(`https://api.telegram.org/bot${token}/sendDocument`, {
        method: "POST",
        body: formData,
      });
    }
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ok: true }),
  };
};
