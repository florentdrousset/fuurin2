<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { afterNavigate } from '$app/navigation';

  function updateActiveNav() {
    try {
      const path = location.pathname;
      const items = document.querySelectorAll('.nav-items .nav-item');
      items.forEach((a) => {
        const href = a.getAttribute('href') || '';
        if (!href) return;
        if (href === '/' && path === '/') {
          a.classList.add('active');
          if (!a.querySelector('.active-indicator')) {
            const dot = document.createElement('div');
            dot.className = 'active-indicator';
            a.appendChild(dot);
          }
        } else if (href !== '/' && path.startsWith(href)) {
          a.classList.add('active');
        } else {
          a.classList.remove('active');
          const dot = a.querySelector('.active-indicator');
          if (dot) dot.remove();
        }
      });
    } catch (e) {}
  }

  onMount(() => {
    updateActiveNav();
  });

  afterNavigate(() => {
    updateActiveNav();
  });
</script>

<svelte:head>
  <script src="/assets/js/fuurin-charts.js" defer></script>
</svelte:head>

<slot />