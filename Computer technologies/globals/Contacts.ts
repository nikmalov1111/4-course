import type { GlobalConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const Contacts: GlobalConfig = {
  slug: 'contacts',
  label: 'Контакты',
  access: { read: () => true },
    hooks: {
    afterChange: [
      async () => {
        await revalidatePaths(['/'], 'layout');
      },
    ],
  },
  fields: [
    { name: 'phone', type: 'text', required: true, label: 'Телефон' },
    { name: 'address', type: 'text', required: true, label: 'Адрес' },
    {
      name: 'schedule',
      type: 'text',
      required: true,
      label: 'График работы',
      admin: { description: 'Например: Пн-Сб 09:00–19:00, Вс 09:00–18:00' },
    },
    {
      name: 'mapCoordinates',
      type: 'text',
      label: 'Координаты для карты',
      admin: { description: 'Формат: широта,долгота. Например: 59.187097,39.911661' },
    },
  ],
}