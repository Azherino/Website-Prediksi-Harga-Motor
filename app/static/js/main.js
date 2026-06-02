/* ── Flash Toasts ──────────────────────────────────────────────────────── */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  const icons = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' };
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOut .3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/* ── Auto-dismiss flash messages ───────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
});

/* ── Active nav link ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (path === href || (href !== '/' && path.startsWith(href)))) {
      link.classList.add('active');
    }
  });
});

/* ── Confirm Modal ─────────────────────────────────────────────────────── */
function openModal(id) {
  document.getElementById(id).classList.add('active');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
  }
});

/* ── Upload Zone Drag & Drop ───────────────────────────────────────────── */
function initUploadZone(zoneId, inputId) {
  const zone  = document.getElementById(zoneId);
  const input = document.getElementById(inputId);
  if (!zone || !input) return;

  zone.addEventListener('click', () => input.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      input.files = e.dataTransfer.files;
      updateZoneLabel(zone, e.dataTransfer.files[0].name);
    }
  });
  input.addEventListener('change', () => {
    if (input.files.length) updateZoneLabel(zone, input.files[0].name);
  });
}

function updateZoneLabel(zone, name) {
  zone.querySelector('h4').textContent = name;
  zone.querySelector('p').textContent  = 'File siap diupload. Klik tombol Upload untuk melanjutkan.';
  zone.style.borderColor = 'var(--success)';
  zone.style.background  = 'rgba(39,174,96,.05)';
}

/* ── Range Slider Value Display ────────────────────────────────────────── */
function initSlider(sliderId, displayId) {
  const slider  = document.getElementById(sliderId);
  const display = document.getElementById(displayId);
  if (!slider || !display) return;
  const update = () => {
    display.textContent = slider.value + '%';
  };
  slider.addEventListener('input', update);
  update();
}

/* ── Format Rupiah ─────────────────────────────────────────────────────── */
function formatRupiah(angka) {
  return 'Rp ' + parseInt(angka).toLocaleString('id-ID');
}

/* ── Password Toggle ───────────────────────────────────────────────────── */
function togglePassword(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon  = document.getElementById(iconId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    if (icon) icon.className = 'ri-eye-off-line';
  } else {
    input.type = 'password';
    if (icon) icon.className = 'ri-eye-line';
  }
}
