/**
 * Diana Nails — Appointment Scheduling Helpers
 */
document.addEventListener('DOMContentLoaded', function () {

  const serviceSelect = document.getElementById('id_service');
  const startInput = document.getElementById('id_start_time');
  const endInput = document.getElementById('id_end_time');

  if (!serviceSelect || !startInput || !endInput) return;

  function autoCalculateEnd() {
    const opt = serviceSelect.options[serviceSelect.selectedIndex];
    if (!opt) return;
    const dur = parseInt(opt.getAttribute('data-duration'), 10);
    if (!dur || !startInput.value) return;

    const [h, m] = startInput.value.split(':').map(Number);
    const total = h * 60 + m + dur;
    endInput.value =
      String(Math.floor(total / 60)).padStart(2, '0') + ':' +
      String(total % 60).padStart(2, '0');
  }

  serviceSelect.addEventListener('change', autoCalculateEnd);
  startInput.addEventListener('change', autoCalculateEnd);

});
