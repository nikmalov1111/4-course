import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense, cache } from "react";
import { Metadata } from "next";
import { getPayloadClient } from "@/lib/payload";
import ServiceBookingButton from "@/components/ServiceBookingButton";

const getMaster = cache(async (slug: string) => {
  const payload = await getPayloadClient();
  const { docs } = await payload.find({
    collection: 'masters',
    where: { slug: { equals: slug } },
    limit: 1,
  });
  return docs[0];
});

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const master = await getMaster(slug);

  if (!master) {
    return { title: 'Мастер не найден | Vilet' };
  }

  const description = master.description 
    ? master.description.slice(0, 160) + '...' 
    : `Запишитесь к мастеру ${master.name} (${master.role}) в парикмахерскую Vilet.`;

  return {
    title: `${master.name} — ${master.role} | Парикмахерская Vilet`,
    description: description,
  };
}

export default function MasterDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  return (
    <div className="max-w-5xl mx-auto py-16 px-4">
      <div className="text-sm text-gray-500 mb-8">
        <Link href="/" className="hover:text-vilet-green">Главная</Link> / 
        <Link href="/masters" className="hover:text-vilet-green mx-1">Мастера</Link> / 
      </div>

      <Suspense fallback={<div className="text-center py-20 text-gray-500">Загрузка профиля мастера...</div>}>
        <MasterContent params={params} />
      </Suspense>
    </div>
  );
}

async function MasterContent({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;

  const master = await getMaster(resolvedParams.slug);

  if (!master) {
    notFound();
  }

  const imageUrl = typeof master.image === 'object' && master.image?.url 
    ? master.image.url 
    : '/placeholder.jpg';

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col md:flex-row">
      <div className="md:w-1/2 relative min-h-[400px] md:min-h-full bg-gray-200">
        <img
          src={imageUrl}
          alt={master.name}
          className="absolute inset-0 w-full h-full object-cover"
        />
      </div>

      <div className="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
        <span className="text-vilet-gold font-medium tracking-wider uppercase text-sm mb-2 block">
          {master.role}
        </span>
        <h1 className="text-4xl font-bold text-vilet-green mb-4">
          {master.name}
        </h1>
        <div className="bg-vilet-beige inline-block px-4 py-2 rounded-lg text-sm font-medium text-vilet-green mb-6">
          Стаж: {master.experience}
        </div>

        <h3 className="text-xl font-bold text-gray-800 mb-2">О специалисте</h3>
        <p className="text-gray-600 mb-8 leading-relaxed whitespace-pre-line">
          {master.description}
        </p>

        <div className="flex gap-4">
          <Link 
            href="/masters"
            className="px-6 py-3 border border-gray-300 rounded-full text-gray-700 hover:bg-gray-50 transition-colors text-center"
          >
            Все мастера
          </Link>
          <ServiceBookingButton />
        </div>
      </div>
    </div>
  );
}