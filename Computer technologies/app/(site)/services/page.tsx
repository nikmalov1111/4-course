import { getPayloadClient } from '@/lib/payload'
import ServicesList from "./ServicesList";
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: "Наши услуги | Парикмахерская Vilet",
  description: "Полный список услуг парикмахерской Vilet: женские и мужские стрижки, окрашивание, уход за волосами и бородой.",
};

export default async function ServicesPage() {
  const payload = await getPayloadClient()
  
  const { docs: services } = await payload.find({
    collection: 'services',
    limit: 200,
  })
  
  return <ServicesList services={services} />;
}