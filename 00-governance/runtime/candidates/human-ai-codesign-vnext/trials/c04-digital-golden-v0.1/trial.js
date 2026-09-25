(() => {
  const body = document.body;
  const variant = body.dataset.variant;
  const params = new URLSearchParams(location.search);
  const forcedState = params.get('state');
  const sheet = document.querySelector('.sheet');

  const openRecovery = () => {
    if (variant === 'C') {
      body.classList.add('returning');
      document.querySelector('.mode-toggle')?.setAttribute('data-active', 'true');
      document.querySelector('.mode-toggle')?.setAttribute('aria-pressed', 'true');
      return;
    }
    if (sheet) sheet.hidden = false;
  };

  const closeRecovery = () => {
    if (variant === 'C') {
      body.classList.remove('returning');
      document.querySelector('.mode-toggle')?.setAttribute('data-active', 'false');
      document.querySelector('.mode-toggle')?.setAttribute('aria-pressed', 'false');
      return;
    }
    if (sheet) sheet.hidden = true;
  };

  document.querySelectorAll('[data-open-recovery]').forEach((button) => {
    button.addEventListener('click', openRecovery);
  });
  document.querySelectorAll('[data-close-recovery]').forEach((button) => {
    button.addEventListener('click', closeRecovery);
  });

  document.querySelector('.mode-toggle')?.addEventListener('click', () => {
    body.classList.contains('returning') ? closeRecovery() : openRecovery();
  });

  if (forcedState === 'return') openRecovery();

  window.__OLEANDER_C04_CODESIGN_TRIAL__ = {
    variant,
    openRecovery,
    closeRecovery,
    snapshot: () => ({
      variant,
      returning: body.classList.contains('returning'),
      recoverySurfaceVisible: variant === 'C'
        ? body.classList.contains('returning')
        : Boolean(sheet && !sheet.hidden),
      unknownFailClosed: Boolean(document.querySelector('[data-status="UNKNOWN"]')),
      noLiveClaim: Boolean(document.querySelector('[data-no-live-claim]')),
      digitalOffFallback: Boolean(document.querySelector('[data-digital-off-fallback]'))
    })
  };
})();
