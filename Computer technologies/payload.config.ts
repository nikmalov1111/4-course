import { buildConfig } from 'payload'
import { sqliteAdapter } from '@payloadcms/db-sqlite'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import path from 'path'
import { fileURLToPath } from 'url'
import sharp from 'sharp'
import { Users } from './collections/Users'
import { Media } from './collections/Media'
import { Services } from './collections/Services'
import { Masters } from './collections/Masters'
import { Promotions } from './collections/Promotions'
import { Leads } from './collections/Leads'

import { Contacts } from './globals/Contacts'
import { AboutPage } from './globals/AboutPage'
import { HomePage } from './globals/HomePage'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

const serverURL = process.env.NEXT_PUBLIC_SERVER_URL || 'http://localhost:3000'

export default buildConfig({
  admin: {
    user: 'users',
  },
  serverURL,
  cors: [serverURL],
  csrf: [serverURL],
  db: sqliteAdapter({
    client: {
      url: process.env.DATABASE_URL || 'file:./dev.db',
    },
  }),
  editor: lexicalEditor({}),
  sharp,
  collections: [Users, Media, Services, Masters, Promotions, Leads],
  globals: [Contacts, AboutPage, HomePage],
  secret: process.env.PAYLOAD_SECRET as string,
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
})