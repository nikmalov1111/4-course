import type { CollectionConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const Masters: CollectionConfig = {
  slug: 'masters',
  labels: { singular: 'Мастер', plural: 'Мастера' },
  admin: {
    useAsTitle: 'name',
    defaultColumns: ['name', 'role', 'experience'],
    group: 'Контент',
  },
  orderable: true,
   hooks: {
    afterChange: [
      async ({ doc }) => {
        const paths = ['/', '/masters'];
        if (doc.slug) paths.push(`/masters/${doc.slug}`);
        await revalidatePaths(paths);
      },
    ],
  },
  fields: [
    { name: 'name', type: 'text', required: true, label: 'Имя' },
    { name: 'slug', type: 'text', required: true, unique: true, label: 'Slug (URL)' },
    { name: 'role', type: 'text', required: true, label: 'Специализация' },
    { name: 'experience', type: 'text', label: 'Опыт (например, «7 лет»)' },
    { name: 'description', type: 'textarea', label: 'Описание' },
    {
      name: 'image',
      type: 'upload',
      relationTo: 'media',
      required: true,
      label: 'Фото',
    },
  ],
}