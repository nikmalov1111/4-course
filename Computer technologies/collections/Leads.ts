import type { CollectionConfig } from 'payload'

export const Leads: CollectionConfig = {
  slug: 'leads',
  labels: { singular: 'Заявка', plural: 'Заявки' },
  admin: {
    useAsTitle: 'name',
    defaultColumns: ['name', 'phone', 'status', 'createdAt'],
    group: 'Заявки',
  },

  access: {
    create: () => true,
    read: ({ req: { user } }) => Boolean(user),
    update: ({ req: { user } }) => Boolean(user),
    delete: ({ req: { user } }) => Boolean(user),
  },
  fields: [
    { name: 'name', type: 'text', required: true, label: 'Имя' },
    { name: 'phone', type: 'text', required: true, label: 'Телефон' },
    {
      name: 'status',
      type: 'select',
      defaultValue: 'new',
      options: [
        { label: 'Новая', value: 'new' },
        { label: 'В обработке', value: 'in_progress' },
        { label: 'Закрыта', value: 'done' },
      ],
      label: 'Статус',
    },
    {
      name: 'source',
      type: 'text',
      label: 'Источник',
      admin: { description: 'Например: «модалка на главной», «услуга: стрижка»' },
    },
  ],
  timestamps: true,
}