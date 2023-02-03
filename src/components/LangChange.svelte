<script lang="ts">
  import { change_locale, locales } from 'tools/i18n';
  import { clsx } from 'tools/clsx';
  import Select from 'components/Select.svelte';
  import { writable } from 'svelte/store';
  import type { langKey } from 'langs';

  export let value: string;
  const val = writable(value);
  $: options = (() => {
    const opts: any = {};
    for (let x in locales)
      opts[x] = {
        text: locales[x as langKey],
        className: clsx('bg-black font-semibold', $val === x ? 'text-yellow-400' : 'text-white')
      };
    return opts;
  })();
</script>

<div class="my-10 flex justify-center">
  <Select
    value={val}
    className="px-1 font-bold bg-black text-white border-2 border-lime-500 outline-none rounded-lg"
    onChange={() => change_locale($val)}
    {options}
  />
</div>
