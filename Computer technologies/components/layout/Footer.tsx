import Link from "next/link";

export default function Footer({ contacts }: { contacts: any }) {
  return (
    <footer className="bg-vilet-green text-white py-8 mt-auto">
      <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
          <p className="text-xl font-bold tracking-widest">VILET</p>
          <p className="text-sm opacity-80 whitespace-pre-line">{contacts.schedule}</p>
          <p className="text-sm mt-2 opacity-80">{contacts.phone}</p>
        </div>
        
        <div className="text-sm text-center md:text-right flex flex-col gap-2 opacity-80">
          <Link href="/privacy" className="hover:underline">Политика обработки персональных данных</Link>
          <p>© 2026 Парикмахерская Vilet. Все права защищены.</p>
        </div>
      </div>
    </footer>
  );
}