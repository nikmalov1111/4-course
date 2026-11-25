import { revalidatePath } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get('secret');
  const path = request.nextUrl.searchParams.get('path');
  const type = request.nextUrl.searchParams.get('type') as 'page' | 'layout' | null;

  if (secret !== process.env.PAYLOAD_SECRET) {
    return NextResponse.json({ message: 'Invalid token' }, { status: 401 });
  }

  if (!path) {
    return NextResponse.json({ message: 'Missing path param' }, { status: 400 });
  }

  try {
    if (type === 'layout') {
      revalidatePath(path, 'layout');
    } else {
      revalidatePath(path);
    }
    return NextResponse.json({ revalidated: true, now: Date.now() });
  } catch (err) {
    return NextResponse.json({ message: 'Error revalidating' }, { status: 500 });
  }
}