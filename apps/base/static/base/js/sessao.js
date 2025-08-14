// apps/base/static/base/js/sessao.js
(function(){
  if (window.__sessaoInit) return; window.__sessaoInit = true;

  const $ = (id)=>document.getElementById(id);
  const now = ()=>Date.now();
  const log = (...a)=>console.log("[sessao]", ...a);
  const warn = (...a)=>console.warn("[sessao]", ...a);

  function parseNum(v, fb){ const n = parseFloat(v); return Number.isFinite(n)?n:fb; }
  function bootstrapOK(){ return !!(window.bootstrap && typeof window.bootstrap.Modal === "function"); }

  function mkFallbackModal(){
    const el = document.createElement("div");
    el.id="sessao-fallback-overlay";
    el.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;align-items:center;justify-content:center;z-index:1055;font-family:system-ui,Arial";
    el.innerHTML=`
      <div style="background:#fff;width:min(520px,92%);border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.25);overflow:hidden">
        <div style="padding:12px 16px;color:#fff;background:linear-gradient(135deg,#2563eb,#14b8a6);font-weight:600">Sessão prestes a expirar</div>
        <div style="padding:16px;font-size:16px">Você ficou inativo(a). Sua sessão será encerrada em <strong><span id="contador-sessao-fb">120</span>s</strong>.</div>
        <div style="padding:12px 16px;display:flex;justify-content:flex-end;gap:8px">
          <button id="btn-voltei-fb" style="border:0;background:#16a34a;color:#fff;padding:8px 14px;border-radius:8px;font-weight:600;cursor:pointer">Voltei</button>
        </div>
      </div>`;
    document.body.appendChild(el);
    return {
      show(sec){ const s=$("contador-sessao-fb"); if(s) s.textContent=String(sec); el.style.display="flex"; },
      hide(){ el.style.display="none"; },
      onBack(cb){ el.addEventListener("click",e=>{ if(e.target && e.target.id==="btn-voltei-fb") cb(); }); }
    };
  }

  function init(){
    const cfg = $("sessao-config");
    if (!cfg){
      log("sem #sessao-config (provável usuário anônimo); nada a fazer.");
      return;
    }

    // Lê configs
    const keepaliveUrl = cfg.dataset.keepaliveUrl || "";
    const logoutBeaconUrl = cfg.dataset.logoutBeaconUrl || "";
    const logoutUrl = cfg.dataset.logoutUrl || "";
    const homeUrl   = cfg.dataset.homeUrl   || "/";
    const minInatMin = parseNum(cfg.dataset.popupMinInatividade, 1);
    const contMin    = parseNum(cfg.dataset.contagemRegressiva, 2);
    const hardCapMin = parseNum(cfg.dataset.tempoMaxSessao, 3);
    const debug = cfg.dataset.debug === "1";

    const minInatMs = minInatMin*60*1000;
    const hardCapMs = hardCapMin*60*1000;
    let countdown = Math.max(1, Math.round(contMin*60)); // seg

    // Estado
    let lastActivity = now();
    let popupOpen=false, countdownId=null, hardCapId=null, fbModal=null, bsModal=null;

    if (debug){
      log("init", {minInatMin, contMin, hardCapMin, bootstrap: bootstrapOK(), keepaliveUrl, logoutUrl, homeUrl});
      const badge = document.createElement("div");
      badge.style.cssText="position:fixed;bottom:10px;right:10px;background:#111;color:#fff;padding:6px 10px;border-radius:999px;font:12px/1.2 monospace;z-index:2000;opacity:.85";
      setInterval(()=>{ badge.textContent=`idle=${Math.floor((now()-lastActivity)/1000)}s | popup=${popupOpen?1:0}`; }, 1000);
      document.body.appendChild(badge);
    }

    function keepalive(){ if(keepaliveUrl) fetch(keepaliveUrl,{credentials:"same-origin"}).catch(()=>{}); }
    function forceLogout(){
      // Navega direto para logout com next=home; replace evita voltar ao estado anterior.
      const target = logoutUrl ? `${logoutUrl}?next=${encodeURIComponent(homeUrl)}&_=${Date.now()}`
                               : (logoutBeaconUrl || homeUrl);
      window.location.replace(target);
    }
    function ensureHardCap(){ clearTimeout(hardCapId); hardCapId=setTimeout(forceLogout, hardCapMs); }

    function startCountdown(update, done){
      clearInterval(countdownId);
      let sec = countdown; update(sec);
      countdownId=setInterval(()=>{ sec--; update(sec); if(sec<=0){ clearInterval(countdownId); countdownId=null; done(); } }, 1000);
    }

    function openPopup(){
      if(popupOpen) return; popupOpen=true;

      if (bootstrapOK()){
        const modalEl = $("sessaoModal");
        if(!modalEl){ warn("Bootstrap OK, mas #sessaoModal não encontrado; usando fallback."); return openFallback(); }
        const span = $("contador-sessao");
        if(!bsModal) bsModal = new bootstrap.Modal(modalEl,{backdrop:"static",keyboard:false});
        bsModal.show();
        startCountdown((s)=>{ if(span) span.textContent=String(s); }, ()=>{ closePopup(); forceLogout(); });
      } else {
        openFallback();
      }
    }
    function openFallback(){
      if(!fbModal) fbModal = mkFallbackModal();
      fbModal.show(countdown);
      fbModal.onBack(handleImBack);
      startCountdown((s)=>{ const span=$("contador-sessao-fb"); if(span) span.textContent=String(s); }, ()=>{ closePopup(); forceLogout(); });
    }
    function closePopup(){
      if(!popupOpen) return; popupOpen=false;
      clearInterval(countdownId); countdownId=null;
      try{ if(bsModal) bsModal.hide(); }catch(_){}
      try{ if(fbModal) fbModal.hide(); }catch(_){}
    }
    function handleImBack(){
      keepalive(); closePopup(); lastActivity=now(); ensureHardCap();
    }

    // Atividade (ignora se popup aberto)
    ["mousemove","keypress","click","scroll","touchstart"].forEach(evt=>{
      window.addEventListener(evt, ()=>{ if(!popupOpen) lastActivity=now(); }, {passive:true});
    });
    document.addEventListener("click", (e)=>{ if(e.target && e.target.id==="btn-voltei") handleImBack(); });

    // Heartbeat
    setInterval(()=>{ if(!popupOpen && (now()-lastActivity)>=minInatMs) openPopup(); }, 1000);
    ensureHardCap();

    // Utilidades de teste
    window.__forceSessionPopup = openPopup;
    window.__simulateIdle = (s)=>{ lastActivity = now() - (Math.max(1, s)*1000); };
  }

  if (document.readyState === "loading"){ document.addEventListener("DOMContentLoaded", init); }
  else { init(); }
})();
