import { getPayload } from 'payload'
import config from '@payload-config'

let cached = global as unknown as { payload: Awaited<ReturnType<typeof getPayload>> }

export const getPayloadClient = async () => {
  if (cached.payload) return cached.payload

  const payload = await getPayload({ config })
  if (process.env.NODE_ENV !== 'production') cached.payload = payload

  return payload
}