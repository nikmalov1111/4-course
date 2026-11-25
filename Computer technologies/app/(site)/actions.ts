"use server";

import { leadSchema } from "@/lib/schemas";
import { sendLeadEmail } from "@/lib/mailer";
import { getPayloadClient } from "@/lib/payload";

async function validateTurnstile(token: string): Promise<boolean> {
  if (!token) return false;

  try {
    const verifyEndpoint = "https://challenges.cloudflare.com/turnstile/v0/siteverify";
    const res = await fetch(verifyEndpoint, {
      method: "POST",
      body: new URLSearchParams({
        secret: process.env.TURNSTILE_SECRET_KEY!,
        response: token,
      }),
    });

    const data = await res.json();
    return data.success === true;
  } catch (error) {
    console.error("Ошибка проверки Turnstile:", error);
    return false;
  }
}

export async function submitLead(data: any) {
  const parsed = leadSchema.safeParse(data);

  if (!parsed.success) {
    return { success: false, errors: parsed.error.flatten().fieldErrors };
  }

  const isHuman = await validateTurnstile(data.turnstileToken);
  if (!isHuman) {
    return { success: false, message: "Подтвердите, что вы не робот." };
  }

  try {
    const payload = await getPayloadClient();

    await payload.create({
      collection: 'leads',
      data: {
        name: parsed.data.name,
        phone: parsed.data.phone,
        status: 'new',
        source: 'Сайт',
      },
    });

    await sendLeadEmail(parsed.data);
    
    return { success: true };
  } catch (error) {
    console.error("Ошибка при сохранении или отправке:", error);
    return { success: false, message: "Ошибка отправки. Пожалуйста, позвоните нам." };
  }
}