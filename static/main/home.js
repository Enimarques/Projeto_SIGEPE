function atualizarGraficos(cpu, mem, resp, uptime, alertas24h, faces) {
  if (cpuChart) cpuChart.destroy();
  if (memChart) memChart.destroy();
  if (respChart) respChart.destroy();

  document.getElementById('cpuValue').innerText = cpu + '%';
  document.getElementById('memValue').innerText = mem + '%';
  document.getElementById('respValue').innerText = resp + 'ms';
  document.getElementById('uptimeValue').innerText = uptime;
  document.getElementById('alertas24hValue').innerText = alertas24h;
  document.getElementById('facesValue').innerText = faces;

  cpuChart = createDonutChart(document.getElementById('cpuChart').getContext('2d'), cpu, '#28a745');
  memChart = createDonutChart(document.getElementById('memChart').getContext('2d'), mem, '#ffc107');
  let respPercent = Math.min(100, Math.round((resp / 500) * 100));
  respChart = createDonutChart(document.getElementById('respChart').getContext('2d'), respPercent, '#17a2b8');
}

async function buscarMetricas() {
  try {
    const resp = await fetch('/main/api/metricas/');
    const data = await resp.json();
    atualizarGraficos(data.cpu, data.mem, data.resp, data.uptime, data.alertas24h, data.faces);
  } catch (e) {
    atualizarGraficos(0, 0, 0, '--', '--', '--');
  }
} 