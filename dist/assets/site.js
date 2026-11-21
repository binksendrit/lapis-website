'use strict';
document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  navigation.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.querySelector('.menu-label').textContent = 'Menü';
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
  menuButton.querySelector('.menu-label').textContent = open ? 'Schliessen' : 'Menü';
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu(); menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);

const form = document.querySelector('#contact-form');
if (form) {
  const config = JSON.parse(document.querySelector('#site-contact').textContent);
  const result = document.querySelector('#request-result');
  const preview = document.querySelector('#request-preview');
  const status = document.querySelector('#result-status');
  const emailLink = document.querySelector('#email-request');
  const fields = [['name', 'Name'], ['email', 'E-Mail'], ['phone', 'Telefon'], ['place', 'Ort der Liegenschaft'], ['units', 'Anzahl Mietobjekte'], ['topic', 'Anliegen']];
  if (config.email) {
    const box = document.querySelector('#contact-details');
    box.replaceChildren();
    const title = document.createElement('h3'); title.textContent = 'Ihr direkter Kontakt';
    const email = document.createElement('a'); email.href = 'mailto:' + config.email; email.textContent = config.email;
    box.append(title, email);
    if (config.phone) { const phone = document.createElement('p'); phone.textContent = config.phone; box.append(phone); }
    document.querySelector('#form-notice').textContent = 'Bereiten Sie Ihre Anfrage vor. Anschliessend können Sie den Text mit Ihrer E-Mail-App versenden. Dieses Formular sendet selbst keine Nachricht.';
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const lines = fields.map(([key,label]) => [label,String(data.get(key) || '').trim()]).filter(([,value]) => value).map(([label,value]) => `${label}: ${value}`);
    preview.value = 'Anfrage an LAPIS Immobilienverwaltung\n\n' + lines.join('\n') + '\n\nNachricht:\n' + String(data.get('message')).trim();
    status.textContent = 'Ihre Anfrage ist vorbereitet. Es wurde noch keine Nachricht versendet.';
    result.hidden = false;
    if (config.email) {
      emailLink.href = 'mailto:' + encodeURIComponent(config.email) + '?subject=' + encodeURIComponent('Anfrage zur Immobilienverwaltung') + '&body=' + encodeURIComponent(preview.value);
      emailLink.hidden = false;
    }
    result.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',block:'start'});
    preview.focus({preventScroll:true});
  });
  form.addEventListener('input', () => {
    if (!result.hidden) { result.hidden = true; emailLink.hidden = true; }
  });
  document.querySelector('#copy-request').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(preview.value); status.textContent = 'Anfragetext kopiert. Es wurde noch keine Nachricht versendet.'; }
    catch { preview.focus(); preview.select(); status.textContent = 'Bitte kopieren Sie den markierten Text manuell. Es wurde noch keine Nachricht versendet.'; }
  });
  document.querySelector('#download-request').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([preview.value], {type:'text/plain;charset=utf-8'}));
    const link = document.createElement('a'); link.href = url; link.download = 'LAPIS_Anfrageentwurf.txt';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Der Download Ihres Anfrageentwurfs wurde gestartet. Es wurde noch keine Nachricht versendet.';
  });
}
