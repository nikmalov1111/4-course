import { z } from "zod";

export const leadSchema = z.object({
  name: z.string().min(2, "Имя должно быть не короче 2 символов"),
  phone: z.string().regex(/^(\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}$/, "Введите номер в формате +7 (999) 123-45-67"),
  consent: z.literal(true, {
    error: "Без согласия на обработку данных мы не можем принять заявку",
  }),
});