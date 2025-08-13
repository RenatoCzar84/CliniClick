// apps/base/static/base/js/sessao.js
(function () {
  // Lê config do HTML (sem depender de Django templatetags além de data-attrs)
  const cfgEl = document.getElementById('sessao-config');
  if (!cfgEl) return;

  const isAuth = cfgEl.dataset.auth === '1';
  if (!isAuth) return; // só roda para usuário autenticado

  // Endpoints: hardcoded para evitar {% url %} no template
  const LOGOUT_URL    = cfgEl.dataset.logoutUrl    || '/usuarios/logout-beacon/';
  const KEEPALIVE_URL = cfgEl.dataset.keepaliveUrl || '/usuarios/keepalive/';
  const HOME_URL      = cfgEl.dataset.homeUrl      || '/';

  // Configurações
  const IDLE_MS = 60 * 1000;              // 1 min de inatividade para abrir popup
  const TOTAL_MS = 3 * 60 * 1000;         // 3 min até expirar sessão
  const COUNTDOWN_MS = TOTAL_MS - IDLE_MS; // 120s (2 min) de contagem

  // Elementos de UI
  const POPUP = document.getElementById('sessao-popup');
  const LABEL = document.getElementById('contador-sessao');
  const BTN   = document.getElementById('btn-voltei');

  if (!POPUP || !LABEL || !BTN) return;

  let idleTimer = null;
  let countdownTimer = null;
  let countdownLeft = COUNTDOWN_MS;

  function msToSeconds(ms) { return Math.max(0, Math.ceil(ms / 1000)); }

  function showPopup() {
    countdownLeft = COUNTDOWN_MS;
    LABEL.textContent = msToSeconds(countdownLeft);
    POPUP.style.display = 'flex';

    if (countdownTimer) clearInterval(countdownTimer);
    countdownTimer = setInterval(() => {
      countdownLeft -= 1000;
      LABEL.textContent = msToSeconds(countdownLeft);
      if (countdownLeft <= 0) {
        clearInterval(countdownTimer);
        expireSession();
      }
    }, 1000);
  }

  function hidePopup() {
    POPUP.style.display = 'none';
    if (countdownTimer) {
      clearInterval(countdownTimer);
      countdownTimer = null;
    }
  }

  function resetIdle() {
    hidePopup();
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(showPopup, IDLE_MS);
  }

  function expireSession() {
    if (navigator.sendBeacon) {
      try { navigator.sendBeacon(LOGOUT_URL); } catch (_) {}
      setTimeout(() => { window.location.href = HOME_URL + '?expirou=1'; }, 150);
    } else {
      window.location.href = HOME_URL + '?expirou=1';
    }
  }

  function keepAliveThenReset() {
    fetch(KEEPALIVE_URL, { method: 'GET', credentials: 'same-origin' })
      .catch(() => {}) // ignora falhas de rede
      .finally(resetIdle);
  }

  // Botão "Voltei"
  BTN.addEventListener('click', function () {
    hidePopup();
    keepAliveThenReset();
  });

  // Eventos que contam como atividade
  ['mousemove','keydown','click','scroll','touchstart'].forEach(evt => {
    window.addEventListener(evt, resetIdle, { passive: true });
  });

  // Inicia contagem
  resetIdle();
})();
