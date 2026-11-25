export async function revalidatePaths(paths: string[], type: 'page' | 'layout' = 'page') {
  const url = process.env.NEXT_PUBLIC_SERVER_URL || 'http://localhost:3000';
  const secret = process.env.PAYLOAD_SECRET;

  for (const path of paths) {
    try {
      await fetch(`${url}/api/revalidate?secret=${secret}&path=${path}&type=${type}`);
    } catch (error) {
      console.error(`Не удалось обновить кэш для пути: ${path}`, error);
    }
  }
}