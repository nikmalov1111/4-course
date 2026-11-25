import { getPayloadClient } from "@/lib/payload";
import PromotionsList from "./PromotionsList";
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: "Акции и спецпредложения | Парикмахерская Vilet",
  description: "Актуальные акции и скидки на услуги парикмахерской Vilet. Приятные бонусы и специальные предложения для наших гостей.",
};


export default async function PromotionsPage() {
  const payload = await getPayloadClient();
  const { docs: promotions } = await payload.find({
    collection: 'promotions',
    limit: 100,
  });
  
  return <PromotionsList promotions={promotions} />;
}