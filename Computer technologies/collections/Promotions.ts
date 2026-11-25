import type { CollectionConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const Promotions: CollectionConfig = {
  slug: 'promotions',
  labels: { singular: 'Акция', plural: 'Акции' },
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'badge'],
    group: 'Контент',
  },
  orderable: true,
    hooks: {
    afterChange: [
      async () => {
        await revalidatePaths(['/', '/promotions']);
      },
    ],
  },
  fields: [
    { name: 'title', type: 'text', required: true, label: 'Заголовок' },
    { name: 'description', type: 'textarea', required: true, label: 'Описание' },
    { name: 'badge', type: 'text', label: 'Бейдж (например, «-20%»)' },
    {
      name: 'image',
      type: 'upload',
      relationTo: 'media',
      required: false,
      label: 'Картинка акции',
    },
  ],
}