/* Progressive enhancements: the complete academic content is in HTML. */
(() => {
  'use strict';
  document.documentElement.classList.add('js-ready');
  const message = document.querySelector('[role="status"]');
  let messageTimer;
  const announce = (text) => {
    if (!message) return;
    message.textContent = text;
    window.clearTimeout(messageTimer);
    messageTimer = window.setTimeout(() => { message.textContent = ''; }, 4500);
  };
  const themeButton = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('nx-theme'); } catch (_) { /* Storage is optional. */ }
  const applyTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    if (themeButton) {
      themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
      themeButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      themeButton.title = theme === 'dark' ? 'Light theme' : 'Dark theme';
    }
  };
  applyTheme(savedTheme === 'light' || savedTheme === 'dark' ? savedTheme : (systemTheme?.matches ? 'dark' : 'light'));
  themeButton?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    savedTheme = next;
    applyTheme(next);
    try { localStorage.setItem('nx-theme', next); } catch (_) { /* Keep the current session usable. */ }
  });
  systemTheme?.addEventListener?.('change', (event) => {
    if (!savedTheme) applyTheme(event.matches ? 'dark' : 'light');
  });

  const menu = document.querySelector('#site-nav');
  const menuButton = document.querySelector('.menu-toggle');
  const closeMenu = () => {
    menu?.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
  };
  menuButton?.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  menu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.classList.contains('is-open')) {
      closeMenu();
      menuButton?.focus();
    }
  });

  document.querySelectorAll('[data-copy-target], [data-copy-text]').forEach((button) => {
    button.addEventListener('click', async () => {
      const value = button.dataset.copyText || document.getElementById(button.dataset.copyTarget)?.textContent;
      if (!value) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(value.trim());
        announce(button.dataset.copyText ? 'Email address copied.' : 'BibTeX copied.');
      } catch (_) {
        const target = button.dataset.copyTarget && document.getElementById(button.dataset.copyTarget);
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

  const navLinks = Array.from(document.querySelectorAll('#site-nav a[href^="#"]'));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (!visible.length) return;
      const id = visible[0].target.id;
      navLinks.forEach((link) => {
        if (link.getAttribute('href') === `#${id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-100px 0px -40% 0px', threshold: [0, 0.1, 0.4] });
    document.querySelectorAll('main section[id]').forEach((section) => observer.observe(section));
  }
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
})();
