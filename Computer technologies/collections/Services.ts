import type { CollectionConfig } from 'payload'
import { revalidatePaths } from '../lib/revalidate'

export const Services: CollectionConfig = {
  slug: 'services',
  labels: { singular: 'Услуга', plural: 'Услуги' },
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'hall', 'price', 'duration'],
    group: 'Контент',
  },
  orderable: true,
  hooks: {
    afterChange: [
      async ({ doc }) => {
        const paths = ['/', '/services', '/prices'];
        if (doc.slug) paths.push(`/services/${doc.slug}`);
        await revalidatePaths(paths);
      },
    ],
  },
  fields: [
    { name: 'title', type: 'text', required: true, label: 'Название' },
    {
      name: 'slug',
      type: 'text',
      required: true,
      unique: true,
      label: 'Slug (URL)',
      admin: { description: 'Например: zhenskaya-strizhka' },
    },
    { name: 'price', type: 'number', required: true, label: 'Цена, ₽' },
    { name: 'duration', type: 'text', required: true, label: 'Длительность' },
    { name: 'description', type: 'textarea', label: 'Описание' },
    { name: 'hall', type: 'text', required: true, label: 'Зал' },
  ],
}