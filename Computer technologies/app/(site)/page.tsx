import { getPayloadClient } from "@/lib/payload";
import HomeCta from "@/components/HomeCta";

export const dynamic = 'force-dynamic';

export default async function Home() {
  const payload = await getPayloadClient();
  const home = await payload.findGlobal({ slug: 'home-page' });

  return (
    <div>
      <section className="bg-white py-24 px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-vilet-green mb-6">
          {home.heroTitle || "Искусство быть собой"}
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8 whitespace-pre-line">
          {home.heroSubtitle || "Премиальный уход, опытные мастера и атмосфера, в которую хочется возвращаться."}
        </p>
        <HomeCta label={home.ctaLabel || "Записаться онлайн"} />
      </section>

      <section className="py-16 px-4 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          {home.features?.map((feat, idx) => (
            <div key={idx}>
              <h3 className="text-xl font-bold text-vilet-green mb-2">{feat.title}</h3>
              <p className="text-gray-600">{feat.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}