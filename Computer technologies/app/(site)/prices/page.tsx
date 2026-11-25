import { getPayloadClient } from '@/lib/payload'
import PricesTable from "./PricesTable";
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: "Цены на услуги | Парикмахерская Vilet",
  description: "Прозрачные и актуальные цены на все услуги парикмахерской Vilet. Удобная таблица с поиском по названию или залу.",
};


export default async function PricesPage() {
  const payload = await getPayloadClient()
  
  const { docs: services } = await payload.find({
    collection: 'services',
    limit: 200,
  })
  
  return <PricesTable services={services} />;
}