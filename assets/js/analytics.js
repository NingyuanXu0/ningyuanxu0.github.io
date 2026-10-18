(() => {
  'use strict';

  const measurementId = document.querySelector('meta[name="ga4-measurement-id"]')?.content;
  const canonical = document.querySelector('link[rel="canonical"]')?.href;
  if (!/^G-[A-Z0-9]+$/.test(measurementId || '') || !canonical) return;

  const website = new URL(canonical);
  if (location.protocol !== 'https:' || location.hostname !== website.hostname) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
  });

  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
  document.head.append(script);
})();
