import type { GlobalConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const AboutPage: GlobalConfig = {
  slug: 'about-page',
  label: 'Страница «О нас»',
  access: { read: () => true },
    hooks: {
    afterChange: [
      async () => {
        await revalidatePaths(['/about']);
      },
    ],
  },
  fields: [
    { name: 'title', type: 'text', required: true, label: 'Заголовок' },
    { name: 'intro', type: 'textarea', required: true, label: 'Вступление' },
    {
      name: 'image',
      type: 'upload',
      relationTo: 'media',
      required: true,
      label: 'Картинка интерьера',
    },
    {
      name: 'advantages',
      type: 'array',
      label: 'Преимущества',
      minRows: 1,
      maxRows: 6,
      fields: [
        { name: 'title', type: 'text', required: true, label: 'Заголовок' },
        { name: 'description', type: 'textarea', required: true, label: 'Описание' },
      ],
    },
  ],
}