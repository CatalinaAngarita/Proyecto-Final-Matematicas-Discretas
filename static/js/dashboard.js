/**
 * Diana Nails — Dashboard Stats & Charts (Versión morado)
 */
document.addEventListener('DOMContentLoaded', function () {

  const ctx = document.getElementById('weeklyChart');
  if (!ctx) return;

  const labels = JSON.parse(ctx.dataset.labels || '[]');
  const data = JSON.parse(ctx.dataset.values || '[]');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Citas completadas',
        data: data,
        borderColor: '#996998',        /* Morado */
        backgroundColor: 'rgba(153, 105, 152, 0.15)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#996998',
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#7A4F79',
        pointHoverBorderColor: '#fff',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(153, 105, 152, 0.9)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#996998',
          borderWidth: 2,
          cornerRadius: 12,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return context.parsed.y + ' citas';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(153, 105, 152, 0.1)',
            drawBorder: false,
          },
          ticks: {
            stepSize: 1,
            color: '#6B7280',
            font: {
              size: 12
            }
          },
          border: {
            display: false
          }
        },
        x: {
          grid: {
            display: false,
            drawBorder: false,
          },
          ticks: {
            color: '#6B7280',
            font: {
              size: 12
            }
          },
          border: {
            display: false
          }
        },
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
    },
  });

});
