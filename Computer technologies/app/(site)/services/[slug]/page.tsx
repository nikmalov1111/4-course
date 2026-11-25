import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense, cache } from "react";
import { Metadata } from "next";
import { getPayloadClient } from "@/lib/payload";
import ServiceBookingButton from "@/components/ServiceBookingButton";

const getService = cache(async (slug: string) => {
  const payload = await getPayloadClient();
  const { docs } = await payload.find({
    collection: 'services',
    where: { slug: { equals: slug } },
    limit: 1,
  });
  return docs[0];
});

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const service = await getService(slug);

  if (!service) {
    return { title: 'Услуга не найдена | Vilet' };
  }

  const description = service.description 
    ? service.description.slice(0, 160) + '...' 
    : `Услуга ${service.title} в парикмахерской Vilet. Цена: ${service.price} ₽.`;

  return {
    title: `${service.title} — ${service.price} ₽ | Парикмахерская Vilet`,
    description: description,
  };
}

export default function ServiceDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  return (
    <div className="max-w-4xl mx-auto py-16 px-4">
      <div className="text-sm text-gray-500 mb-8">
        <Link href="/" className="hover:text-vilet-green">Главная</Link> / 
        <Link href="/services" className="hover:text-vilet-green mx-1">Услуги</Link> / 
      </div>

      <Suspense fallback={<div className="text-center py-20 text-gray-500">Загрузка...</div>}>
        <ServiceContent params={params} />
      </Suspense>
    </div>
  );
}

async function ServiceContent({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  const service = await getService(resolvedParams.slug);

  if (!service) {
    notFound();
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 md:p-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 border-b border-gray-100 pb-8">
        <div>
          <span className="text-vilet-gold font-medium tracking-wider uppercase text-sm mb-2 block">
            {service.hall}
          </span>
          <h1 className="text-3xl md:text-4xl font-bold text-vilet-green">
            {service.title}
          </h1>
        </div>
        <div className="text-left md:text-right">
          <div className="text-3xl font-bold text-gray-800">{service.price} ₽</div>
          <div className="text-gray-500">Время: {service.duration}</div>
        </div>
      </div>

      <div className="prose max-w-none text-gray-600 mb-10">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Описание услуги</h3>
        <p className="mb-4 whitespace-pre-line">{service.description}</p>
        <p>
          Наши мастера используют только премиальные материалы и индивидуальный подход к каждому гостю. 
          Вы можете быть уверены в безупречном результате и приятной атмосфере.
        </p>
      </div>

      <div className="flex gap-4">
        <Link 
          href="/services"
          className="px-6 py-3 border border-gray-300 rounded-full text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Назад к услугам
        </Link>
        <ServiceBookingButton />
      </div>
    </div>
  );
}