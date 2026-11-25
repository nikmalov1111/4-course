import type { GlobalConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const HomePage: GlobalConfig = {
  slug: 'home-page',
  label: 'Главная страница',
  access: { read: () => true },
    hooks: {
    afterChange: [
      async () => {
        await revalidatePaths(['/']);
      },
    ],
  },
  fields: [
    { name: 'heroTitle', type: 'text', required: true, label: 'Заголовок баннера' },
    { name: 'heroSubtitle', type: 'textarea', required: true, label: 'Подзаголовок' },
    { name: 'ctaLabel', type: 'text', required: true, label: 'Текст кнопки' },
    {
      name: 'features',
      type: 'array',
      label: 'Блоки преимуществ',
      minRows: 1,
      maxRows: 6,
      fields: [
        { name: 'title', type: 'text', required: true, label: 'Заголовок' },
        { name: 'description', type: 'textarea', required: true, label: 'Описание' },
      ],
    },
  ],
}