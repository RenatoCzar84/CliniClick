(function () {
  const cfg = document.getElementById('sessao-config');
  if (!cfg) return;

  // Só ativa se estiver logado
  const LOGGED = cfg.dataset.logged === '1';
  if (!LOGGED) return;

  // Tempos vindos do HTML (fallbacks)
  const IDLE_MS = parseInt(cfg.dataset.idleMs || '60000', 10);        // agora 10000
  const COUNTDOWN_MS = parseInt(cfg.dataset.countdownMs || '120000', 10); // agora 30000
  const KEEPALIVE_URL = cfg.dataset.keepaliveUrl;
  const LOGOUT_URL = cfg.dataset.logoutUrl;
  const INDEX_URL = cfg.dataset.indexUrl;
  const VARIANT = (cfg.dataset.alertVariant || 'warning'); // danger, warning, etc.

  // Elementos do popup (cria se não existir)
  let modal = document.getElementById('sessao-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'sessao-modal';
    modal.className = 'modal fade';
    modal.innerHTML = `
      <div class="modal-dialog modal-sm modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header py-2">
            <h5 class="modal-title">Sessão inativa</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
          </div>
          <div class="modal-body">
            <p class="mb-2">Por segurança, você será desconectado em <b><span id="sessao-count">30</span>s</b>.</p>
            <div class="progress mb-3" style="height:6px;">
              <div id="sessao-bar" class="progress-bar" role="progressbar" style="width: 100%;"></div>
            </div>
            <div class="d-flex justify-content-between">
              <button id="sessao-stay" class="btn btn-sm btn-outline-secondary">Voltei</button>
              <button id="sessao-exit" class="btn btn-sm btn-outline-danger">Sair agora</button>
            </div>
          </div>
        </div>
      </div>`;
    document.body.appendChild(modal);
  }

  // aplica a cor "atenção" (danger) no header e na barra
  const header = modal.querySelector('.modal-header');
  const bar = modal.querySelector('#sessao-bar');
  header.classList.remove('bg-warning','bg-danger','bg-primary','bg-info','text-dark','text-white');
  bar.classList.remove('bg-warning','bg-danger','bg-primary','bg-info');

  if (VARIANT === 'danger') {
    header.classList.add('bg-danger','text-white');
    bar.classList.add('bg-danger');
  } else if (VARIANT === 'warning') {
    header.classList.add('bg-warning','text-dark');
    bar.classList.add('bg-warning');
  } else {
    header.classList.add('bg-primary','text-white');
    bar.classList.add('bg-primary');
  }

  const bsModal = new bootstrap.Modal(modal, { backdrop: 'static', keyboard: false });
  const stayBtn = modal.querySelector('#sessao-stay');
  const exitBtn = modal.querySelector('#sessao-exit');
  const countEl = modal.querySelector('#sessao-count');

  let idleTimer = null;
  let countdownTimer = null;
  let countdownLeft = COUNTDOWN_MS;

  function resetIdleTimer() {
    if (idleTimer) clearTimeout(idleTimer);
    if (countdownTimer) { clearInterval(countdownTimer); countdownTimer = null; }
    // esconde se estava visível
    try { bsModal.hide(); } catch(e){}
    idleTimer = setTimeout(showWarning, IDLE_MS);
    // opcional: ping para manter sessão viva enquanto há atividade
    if (KEEPALIVE_URL) navigator.sendBeacon(KEEPALIVE_URL);
  }

  function showWarning() {
    countdownLeft = COUNTDOWN_MS;
    updateCountdownUI();
    bsModal.show();
    // barra regressiva
    const start = Date.now();
    countdownTimer = setInterval(() => {
      const elapsed = Date.now() - start;
      countdownLeft = Math.max(COUNTDOWN_MS - elapsed, 0);
      updateCountdownUI();
      if (countdownLeft <= 0) {
        clearInterval(countdownTimer);
        doLogout();
      }
    }, 200);
  }

  function updateCountdownUI() {
    const secs = Math.ceil(countdownLeft / 1000);
    countEl.textContent = secs;
    const pct = (countdownLeft / COUNTDOWN_MS) * 100;
    bar.style.width = pct + '%';
  }

  function doLogout() {
    // avisa o backend e redireciona para a home
    if (LOGOUT_URL) navigator.sendBeacon(LOGOUT_URL);
    window.location.href = LOGOUT_URL;
  }

  // Botões do modal
  stayBtn.addEventListener('click', () => {
    // usuário voltou → mantém sessão ativa e reinicia contagem de inatividade
    if (KEEPALIVE_URL) navigator.sendBeacon(KEEPALIVE_URL);
    resetIdleTimer();
  });
  exitBtn.addEventListener('click', () => doLogout());

  // Eventos de atividade do usuário
  ['mousemove','mousedown','keydown','scroll','touchstart','touchmove'].forEach(ev => {
    document.addEventListener(ev, resetIdleTimer, { passive: true });
  });

  // inicia
  resetIdleTimer();
})();
