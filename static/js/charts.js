// static/js/charts.js
document.addEventListener("DOMContentLoaded", () => {
    fetch('/api/chart-data')
        .then(res => res.json())
        .then(data => {
            const commonOpts = {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#6b7280', font: { family: 'Poppins' } } }
                },
                scales: {
                    x: { ticks: { color: '#9ca3af' }, grid: { display: false } },
                    y: { ticks: { color: '#9ca3af' }, grid: { color: '#f3f4f6' } }
                }
            };

            // Goals per group
            const gCtx = document.getElementById('goalsChart');
            if (gCtx) {
                new Chart(gCtx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.goals_by_group),
                        datasets: [{
                            label: 'Goals',
                            data: Object.values(data.goals_by_group).map(v => v[0]),
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        }]
                    },
                    options: commonOpts
                });
            }

            // Top teams by wins
            const wCtx = document.getElementById('winsChart');
            if (wCtx) {
                new Chart(wCtx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: Object.keys(data.top_teams_wins),
                        datasets: [{
                            label: 'Wins',
                            data: Object.values(data.top_teams_wins),
                            borderColor: '#059669',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: commonOpts
                });
            }

            // Top scorers bar
            fetch('/api/players').then(r=>r.json()).then(players => {
                const sCtx = document.getElementById('scorersChart');
                if (sCtx) {
                    new Chart(sCtx.getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: players.slice(0, 5).map(p => p.name),
                            datasets: [{
                                label: 'Goals',
                                data: players.slice(0, 5).map(p => p.goals),
                                backgroundColor: '#f59e0b',
                                borderRadius: 6
                            }]
                        },
                        options: commonOpts
                    });
                }
            });
            
            // Mock Radar & Poss Chart just for visual structure
            const rCtx = document.getElementById('radarChart');
            if (rCtx) {
                new Chart(rCtx.getContext('2d'), {
                    type: 'radar',
                    data: {
                        labels: ['Attack', 'Defense', 'Possession', 'Speed', 'Stamina'],
                        datasets: [{
                            label: 'Argentina',
                            data: [90, 80, 85, 70, 85],
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.2)'
                        }, {
                            label: 'France',
                            data: [95, 75, 80, 90, 80],
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59, 130, 246, 0.2)'
                        }]
                    },
                    options: {
                        scales: { r: { grid: { color: '#e5e7eb' }, ticks: { display: false } } },
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
            }

            const pCtx = document.getElementById('possChart');
            if (pCtx) {
                new Chart(pCtx.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Argentina', 'France'],
                        datasets: [{
                            data: [55, 45],
                            backgroundColor: ['#10b981', '#f3f4f6'],
                            borderWidth: 0
                        }]
                    },
                    options: { cutout: '70%', plugins: { legend: { position: 'bottom' } } }
                });
            }
        });
});
