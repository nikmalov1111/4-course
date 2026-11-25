import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    agentFeedback: true,
  },
  cacheComponents: false,
  partialPrefetching: false,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '3000',
        pathname: '/api/media/**',
      },
      {
        protocol: 'https',
        hostname: 'vilet35.ru',
        pathname: '/api/media/**',
      },
    ],
  },

  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://challenges.cloudflare.com https://api-maps.yandex.ru https://yastatic.net https://suggest-maps.yandex.ru https://*.yandex.ru https://*.yandex.net",
              "style-src 'self' 'unsafe-inline' https://yastatic.net https://*.yandex.ru",
              "img-src 'self' data: blob: https://*.maps.yandex.net https://*.api-maps.yandex.ru https://yandex.ru https://vilet35.ru",
              "connect-src 'self' data: blob: https://verify.yandex.ru https://*.maps.yandex.net https://api.routing.yandex.net https://challenges.cloudflare.com https://vilet35.ru https://*.yandex.ru wss://vilet35.ru",
              "frame-src 'self' https://yandex.ru https://*.yandex.ru https://challenges.cloudflare.com",
              "font-src 'self' data:",
              "media-src 'self' blob: data: https://vilet35.ru",
            ].join("; "),
          },
        ],
      },
    ];
  },
};

export default nextConfig;