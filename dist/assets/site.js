'use strict';

document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');

if (menuButton && navigation) {
  const closeMenu = () => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.querySelector('.menu-label').textContent = 'Menü';
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.querySelector('.menu-label').textContent = open ? 'Schliessen' : 'Menü';
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
}

const form = document.querySelector('#contact-form');
if (form) {
  const config = JSON.parse(document.querySelector('#site-contact').textContent);
  const result = document.querySelector('#request-result');
  const preview = document.querySelector('#request-preview');
  const status = document.querySelector('#result-status');
  const emailLink = document.querySelector('#email-request');
  const fields = [['name', 'Name'], ['email', 'E-Mail'], ['place', 'Ort der Liegenschaft']];

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const lines = fields.map(([key, label]) => [label, String(data.get(key) || '').trim()])
      .filter(([, value]) => value)
      .map(([label, value]) => `${label}: ${value}`);
    preview.value = 'Anfrage an LAPIS Immobilienverwaltung\n\n' + lines.join('\n') +
      '\n\nAnliegen:\n' + String(data.get('message') || '').trim();
    result.hidden = false;
    status.textContent = 'Ihre Anfrage ist vorbereitet. Es wurde noch keine Nachricht versendet.';
    if (config.email) {
      emailLink.href = 'mailto:' + encodeURIComponent(config.email) +
        '?subject=' + encodeURIComponent('Anfrage zur Immobilienverwaltung') +
        '&body=' + encodeURIComponent(preview.value);
      emailLink.hidden = false;
    }
    result.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start'});
    preview.focus({preventScroll: true});
  });

  form.addEventListener('input', () => {
    result.hidden = true;
    emailLink.hidden = true;
  });

  document.querySelector('#copy-request').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(preview.value);
      status.textContent = 'Text kopiert. Es wurde noch keine Nachricht versendet.';
    } catch {
      preview.focus();
      preview.select();
      status.textContent = 'Bitte kopieren Sie den markierten Text manuell.';
    }
  });

  document.querySelector('#download-request').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([preview.value], {type: 'text/plain;charset=utf-8'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'LAPIS_Anfrageentwurf.txt';
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Der Download wurde gestartet. Es wurde noch keine Nachricht versendet.';
  });
}
