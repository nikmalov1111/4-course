import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function sendLeadEmail(lead: { name: string; phone: string }) {
  const html = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f5f0e8; padding: 20px; border-radius: 10px;">
      <h2 style="color: #2c4a3b; margin-top: 0;">Новая заявка с сайта Vilet</h2>
      <div style="background-color: #ffffff; padding: 20px; border-radius: 8px;">
        <p style="font-size: 16px;"><strong>Имя:</strong> ${lead.name}</p>
        <p style="font-size: 16px;">
          <strong>Телефон:</strong> 
          <a href="tel:${lead.phone}" style="color: #c9a96e; text-decoration: none;">${lead.phone}</a>
        </p>
      </div>
      <p style="color: #888; font-size: 12px; text-align: center; margin-top: 20px;">
        Пожалуйста, перезвоните клиенту как можно скорее.
      </p>
    </div>
  `;

  // Отправляем
  await transporter.sendMail({
    from: `"Сайт Vilet" <${process.env.SMTP_USER}>`,
    to: process.env.MAIL_TO,
    subject: `Новая заявка: ${lead.name}`,
    html: html,
  });
}