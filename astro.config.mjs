import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // 실제 배포 도메인이 정해지면 아래 주소를 변경하세요.
  site: 'https://https://blog-insite.pages.dev/',
  integrations: [sitemap()],
});
