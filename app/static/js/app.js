document.addEventListener('DOMContentLoaded', () => {
    const statusBadge = document.getElementById('status-badge');
    const groqStatus = document.getElementById('groq-status');
    const tgStatus = document.getElementById('tg-status');
    const schedulerStatus = document.getElementById('scheduler-status');
    const refreshBtn = document.getElementById('refresh-btn');

    async function checkHealth() {
        try {
            const res = await fetch('/health');
            const data = await res.json();

            groqStatus.textContent = data.groq ? 'Online' : 'Offline';
            groqStatus.style.color = data.groq ? '#22c55e' : '#ef4444';

            tgStatus.textContent = data.telegram ? 'Online' : 'Offline';
            tgStatus.style.color = data.telegram ? '#22c55e' : '#ef4444';

            schedulerStatus.textContent = data.scheduler ? 'Running' : 'Stopped';
            schedulerStatus.style.color = data.scheduler ? '#22c55e' : '#ef4444';

            if (data.status === 'ok') {
                statusBadge.textContent = 'Operational';
                statusBadge.className = 'badge ok';
            } else {
                statusBadge.textContent = 'Degraded';
                statusBadge.className = 'badge degraded';
            }
        } catch (err) {
            statusBadge.textContent = 'Error';
            statusBadge.className = 'badge degraded';
        }
    }

    refreshBtn.addEventListener('click', checkHealth);
    checkHealth();
});
