import type { CollectionConfig } from 'payload'

export const Media: CollectionConfig = {
  slug: 'media',
  labels: { singular: 'Медиа', plural: 'Медиафайлы' },
  access: { read: () => true },
  upload: {
    staticDir: process.env.MEDIA_DIR || 'media',
    mimeTypes: ['image/*'],
    imageSizes: [
      { name: 'thumbnail', width: 400, height: 300, position: 'centre' },
      { name: 'card', width: 768, height: 1024 },
    ],
    adminThumbnail: 'thumbnail',
    focalPoint: true,
    crop: true,
  },
  fields: [
    { name: 'alt', type: 'text', required: true, label: 'Alt-текст' },
  ],
}