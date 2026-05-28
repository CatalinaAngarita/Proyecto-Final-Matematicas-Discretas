document.addEventListener('DOMContentLoaded', function () {

  /* ── Sidebar toggle (mobile) ── */
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (sidebarToggle && sidebar && overlay) {
    function toggleSidebar() {
      sidebar.classList.toggle('show');
      overlay.classList.toggle('show');
    }
    sidebarToggle.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
  }

  /* ── Sidebar accordion: todo cerrado por defecto ── */
  const toggleButtons = document.querySelectorAll('.sidebar-toggle-btn[data-collapse]');

  function closeSection(btn, target) {
    target.classList.remove('open');
    target.style.maxHeight = '0px';
    btn.setAttribute('aria-expanded', 'false');
  }

  function openSection(btn, target) {
    target.classList.add('open');
    target.style.maxHeight = target.scrollHeight + 'px';
    btn.setAttribute('aria-expanded', 'true');
  }

  function closeAllExcept(exceptId) {
    toggleButtons.forEach(function (btn) {
      const collapseId = btn.getAttribute('data-collapse');
      if (collapseId === exceptId) return;
      const target = document.getElementById('collapse-' + collapseId);
      if (target && target.classList.contains('open')) {
        closeSection(btn, target);
      }
    });
  }

  toggleButtons.forEach(function (btn) {
    const collapseId = btn.getAttribute('data-collapse');
    const target = document.getElementById('collapse-' + collapseId);
    if (!target) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (target.classList.contains('open')) {
        closeSection(btn, target);
      } else {
        closeAllExcept(collapseId);
        openSection(btn, target);
      }
    });
  });

  /* ── Highlight active nav + abrir seccion correspondiente ── */
  function setActiveNav() {
    const currentPath = window.location.pathname;
    const currentUrl = window.location.pathname + window.location.search;

    document.querySelectorAll('.sidebar-link, .sidebar-toggle-btn, .sidebar-sub-link').forEach(function (el) {
      el.classList.remove('active');
    });

    document.querySelectorAll('[data-nav]').forEach(function (link) {
      const href = link.getAttribute('href');
      if (!href) return;
      if (currentPath === href || currentUrl === href) {
        link.classList.add('active');
        return;
      }
      if (href !== '/' && currentPath.startsWith(href)) {
        link.classList.add('active');
      }
    });

    toggleButtons.forEach(function (btn) {
      const collapseId = btn.getAttribute('data-collapse');
      const target = document.getElementById('collapse-' + collapseId);
      if (!target) return;
      const hasActive = target.querySelector('.sidebar-sub-link.active');
      if (hasActive) {
        btn.classList.add('active');
        openSection(btn, target);
      }
    });
  }

  setActiveNav();

  /* ── Auto-dismiss alerts ── */
  document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch {}
    }, 5000);
  });

  /* ── Tooltips globales ── */
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    try {
      new bootstrap.Tooltip(el);
    } catch {}
  });

  /* ── Confirm delete modal handler ── */
  document.querySelectorAll('[data-confirm-delete]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = btn.getAttribute('data-confirm-delete');
      const message = btn.getAttribute('data-message') || '¿Estás seguro de eliminar este elemento?';
      const modal = document.getElementById('confirmDeleteModal');
      if (modal) {
        modal.querySelector('#confirmDeleteMessage').textContent = message;
        modal.querySelector('#confirmDeleteForm').action = url;
        try {
          const bsModal = new bootstrap.Modal(modal);
          bsModal.show();
        } catch {}
      }
    });
  });

});
