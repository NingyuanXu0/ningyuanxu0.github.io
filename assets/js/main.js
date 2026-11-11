/* Progressive enhancements: the complete academic content is in HTML. */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js-ready');

  /* Toast / live region ---------------------------------------------------- */
  const message = document.querySelector('.live-message');
  let messageTimer;
  const announce = (text) => {
    if (!message) return;
    message.textContent = text;
    window.clearTimeout(messageTimer);
    messageTimer = window.setTimeout(() => { message.textContent = ''; }, 4500);
  };

  /* Theme: the inline boot script in <head> sets the first value before paint. */
  const themeButton = document.querySelector('.theme-toggle');
  const themeColour = document.querySelector('meta[name="theme-color"]');
  const systemTheme = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('nx-theme'); } catch (_) { /* Storage is optional. */ }
  if (savedTheme !== 'light' && savedTheme !== 'dark') savedTheme = null;
  const applyTheme = (theme) => {
    const dark = theme === 'dark';
    root.dataset.theme = theme;
    if (themeColour?.dataset[theme]) themeColour.content = themeColour.dataset[theme];
    if (themeButton) {
      themeButton.setAttribute('aria-pressed', String(dark));
      themeButton.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
      themeButton.title = dark ? 'Light theme' : 'Dark theme';
    }
  };
  applyTheme(savedTheme || (systemTheme?.matches ? 'dark' : 'light'));
  themeButton?.addEventListener('click', () => {
    savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(savedTheme);
    try { localStorage.setItem('nx-theme', savedTheme); } catch (_) { /* Keep the current session usable. */ }
  });
  systemTheme?.addEventListener?.('change', (event) => {
    if (!savedTheme) applyTheme(event.matches ? 'dark' : 'light');
  });

  /* Collapsible navigation on narrow screens -------------------------------- */
  const menu = document.querySelector('#site-nav');
  const menuButton = document.querySelector('.menu-toggle');
  const setMenu = (open) => {
    menu?.classList.toggle('is-open', open);
    menuButton?.setAttribute('aria-expanded', String(open));
  };
  const menuOpen = () => Boolean(menu?.classList.contains('is-open'));
  menuButton?.addEventListener('click', () => setMenu(!menuOpen()));
  menu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuOpen()) {
      setMenu(false);
      menuButton?.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (menuOpen() && !event.target.closest('.site-header')) setMenu(false);
  });

  /* Copy buttons ------------------------------------------------------------ */
  document.querySelectorAll('[data-copy-target], [data-copy-text]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = button.dataset.copyTarget && document.getElementById(button.dataset.copyTarget);
      const value = button.dataset.copyText || target?.textContent;
      if (!value) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(value.trim());
        announce(button.dataset.copyText ? 'Email address copied.' : 'BibTeX copied.');
      } catch (_) {
        if (target && window.getSelection) {
          const range = document.createRange();
          range.selectNodeContents(target);
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
        }
        announce('Please select and copy the text, or use the email / BibTeX link.');
      }
    });
  });

  if ('IntersectionObserver' in window) {
    /* Highlight the section currently being read. */
    const navLinks = Array.from(document.querySelectorAll('#site-nav a[href^="#"]'));
    if (navLinks.length) {
      const spy = new IntersectionObserver((entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (!visible.length) return;
        const href = `#${visible[0].target.id}`;
        navLinks.forEach((link) => {
          if (link.getAttribute('href') === href) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }, { rootMargin: '-90px 0px -40% 0px', threshold: [0, 0.1, 0.4] });
      document.querySelectorAll('main section[id]').forEach((section) => spy.observe(section));
    }

    /* Gentle entrance for blocks below the fold; skipped when motion is unwelcome. */
    const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    const blocks = document.querySelectorAll(['.section-top', '.section-intro', '.research-card', '.publications-list', '.patent-list', '.background-grid > div', '.supervisors', '.hobby-list', '.contact-panel', '.guestbook']
      .map((selector) => `.section ${selector}`).join(', '));
    if (!reducedMotion && blocks.length) {
      const reveal = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          reveal.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px' });
      blocks.forEach((block) => {
        if (block.getBoundingClientRect().top < window.innerHeight) return;
        block.classList.add('reveal');
        reveal.observe(block);
      });
      /* Printing must never hide content that has not been scrolled to. */
      window.addEventListener('beforeprint', () => blocks.forEach((block) => block.classList.add('is-visible')));
    }
  }

  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
})();
