"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { leadSchema } from "@/lib/schemas";
import { submitLead } from "@/app/(site)/actions";
import { useState, useRef } from "react";
import { Turnstile } from "@marsidev/react-turnstile";
import type { TurnstileInstance } from "@marsidev/react-turnstile";

export default function LeadForm() {
  const [serverMessage, setServerMessage] = useState("");
  const [turnstileToken, setTurnstileToken] = useState("");
  const turnstileRef = useRef<TurnstileInstance | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    resolver: zodResolver(leadSchema),
  });

  async function onSubmit(data: any) {
    const result = await submitLead({ ...data, turnstileToken });

    if (result.success) {
      setServerMessage("Спасибо! Заявка отправлена, мы скоро свяжемся с вами.");
      reset();
    } else {
      setServerMessage(result.message || "Что-то пошло не так. Попробуйте снова.");
    }

    turnstileRef.current?.reset();
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block mb-1 font-medium text-sm text-gray-700">Ваше имя</label>
        <input id="name" {...register("name")} className="w-full border p-2 rounded-lg text-black focus:ring-2 focus:ring-vilet-gold outline-none" />
        {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message as string}</p>}
      </div>

      <div>
        <label htmlFor="phone" className="block mb-1 font-medium text-sm text-gray-700">Телефон</label>
        <input id="phone" {...register("phone")} type="tel" placeholder="+7 (___) ___-__-__" className="w-full border p-2 rounded-lg text-black focus:ring-2 focus:ring-vilet-gold outline-none" />
        {errors.phone && <p className="text-red-500 text-xs mt-1">{errors.phone.message as string}</p>}
      </div>

      <div className="flex items-start gap-2">
        <input id="consent" type="checkbox" {...register("consent")} className="mt-1" />
        <label htmlFor="consent" className="text-xs text-gray-600">
          Я даю согласие на обработку персональных данных
        </label>
      </div>
      {errors.consent && <p className="text-red-500 text-xs">{errors.consent.message as string}</p>}

      {/* Виджет Cloudflare Turnstile */}
      <div className="pt-2">
        <Turnstile
          ref={turnstileRef}
          siteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY!}
          onSuccess={(token) => setTurnstileToken(token)}
          onExpire={() => setTurnstileToken("")}
          options={{ theme: "light" }}
        />
      </div>

      <button
        disabled={isSubmitting}
        type="submit"
        className="w-full bg-vilet-green text-white py-3 rounded-xl font-medium hover:bg-opacity-90 transition-colors disabled:opacity-50 mt-4"
      >
        {isSubmitting ? "Отправка..." : "Отправить заявку"}
      </button>

      {serverMessage && (
        <p className={`text-center text-sm mt-4 p-2 rounded ${serverMessage.includes("Спасибо") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
          {serverMessage}
        </p>
      )}
    </form>
  );
}