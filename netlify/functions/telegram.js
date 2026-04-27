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

  const { message, files, email, name } = body;

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

  // Send confirmation email to submitter via Resend
  if (email && process.env.RESEND_API_KEY) {
    const firstName = name ? name.split(" ")[0] : "there";
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: "CountWize <noreply@countwize.co>",
        to: [email],
        subject: "We've received your enquiry — CountWize",
        html: `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;max-width:600px;width:100%;">
        <!-- Header -->
        <tr><td style="background:#090910;padding:32px 40px;text-align:center;">
          <span style="color:#07B96A;font-size:24px;font-weight:700;letter-spacing:-0.5px;">CountWize</span>
        </td></tr>
        <!-- Body -->
        <tr><td style="padding:40px;">
          <p style="margin:0 0 16px;font-size:16px;color:#090910;">Hi ${firstName},</p>
          <p style="margin:0 0 16px;font-size:16px;color:#3d3d4e;line-height:1.6;">Thank you for reaching out to CountWize. We've received your enquiry and a senior analyst will review your case within <strong>one business day</strong>.</p>
          <p style="margin:0 0 24px;font-size:16px;color:#3d3d4e;line-height:1.6;">We'll be in touch via this email address or the phone number you provided.</p>

          <!-- Security warning box -->
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;border-left:4px solid #07B96A;border-radius:4px;margin-bottom:24px;">
            <tr><td style="padding:16px 20px;">
              <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#090910;">Important — protect yourself from impersonators</p>
              <p style="margin:0;font-size:13px;color:#3d3d4e;line-height:1.6;">CountWize will <strong>never</strong> ask for your seed phrase, private keys, exchange password, two-factor codes, remote access to your device, or any cryptocurrency payment to begin work. Any message claiming to be from CountWize and requesting these is a scam — report it to us and to <a href="https://www.actionfraud.police.uk" style="color:#07B96A;">actionfraud.police.uk</a>.</p>
            </td></tr>
          </table>

          <p style="margin:0;font-size:14px;color:#3d3d4e;">Best regards,<br><strong>The CountWize Team</strong></p>
        </td></tr>
        <!-- Footer -->
        <tr><td style="background:#f4f4f5;padding:24px 40px;text-align:center;border-top:1px solid #e5e5e8;">
          <p style="margin:0 0 8px;font-size:12px;color:#8888a0;">CountWize | <a href="https://countwize.co" style="color:#07B96A;text-decoration:none;">countwize.co</a></p>
          <p style="margin:0;font-size:11px;color:#8888a0;line-height:1.5;">CountWize is not authorised or regulated by the Financial Conduct Authority. We provide on-chain tracing and blockchain analytics. We do not provide investment advice or regulated financial services.</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`,
      }),
    }).catch(() => {});
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ok: true }),
  };
};
