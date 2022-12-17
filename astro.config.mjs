import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import svelte from '@astrojs/svelte';
import partytown from '@astrojs/partytown';

// https://astro.build/config
export default defineConfig({
  trailingSlash: 'never',
  integrations: [
    tailwind({
      config: {
        applyBaseStyles: false
      }
    }),
    svelte(),
    partytown({
      config: {
        forward: ['dataLayer.push'],
        debug: false
      }
    })
  ]
});
