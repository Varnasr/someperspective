// Additional Chart Functions for Methodology and International Comparisons
// Add this JavaScript to your index.html file in the script section

// Chart for methodology - data coverage
function createDataCoverageChart() {
    const ctx = document.getElementById('dataCoverageChart');
    if (!ctx) return;
    
    const isDark = document.body.classList.contains('dark-mode');
    const textColor = isDark ? '#cbd5e1' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['GDP', 'Employment', 'Inequality', 'Fiscal', 'Democratic'],
            datasets: [{
                label: 'Government Sources',
                data: [100, 85, 60, 95, 30],
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderColor: 'rgb(59, 130, 246)',
                borderWidth: 1
            }, {
                label: 'Independent Sources',
                data: [80, 70, 95, 60, 100],
                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                borderColor: 'rgb(16, 185, 129)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Data Coverage by Source Type (%)',
                    color: textColor,
                    font: { size: 16 }
                },
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                x: {
                    stacked: false,
                    grid: { color: gridColor },
                    ticks: { color: textColor }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: gridColor },
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Chart for methodology - index construction weights
function createIndexMethodChart() {
    const ctx = document.getElementById('indexMethodChart');
    if (!ctx) return;
    
    const isDark = document.body.classList.contains('dark-mode');
    const textColor = isDark ? '#cbd5e1' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Data Suppression', 'Release Delays', 'Institutional Capture', 'Methodology Changes', 'Access Restrictions'],
            datasets: [{
                label: 'SSI Components',
                data: [100, 80, 90, 60, 70],
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderColor: 'rgb(239, 68, 68)',
                pointBackgroundColor: 'rgb(239, 68, 68)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(239, 68, 68)'
            }, {
                label: 'Weight in Index',
                data: [30, 20, 25, 15, 10],
                backgroundColor: 'rgba(124, 58, 237, 0.2)',
                borderColor: 'rgb(124, 58, 237)',
                pointBackgroundColor: 'rgb(124, 58, 237)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(124, 58, 237)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Index Construction Methodology - SSI Example',
                    color: textColor,
                    font: { size: 16 }
                },
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: gridColor },
                    pointLabels: {
                        color: textColor,
                        font: { size: 10 }
                    },
                    ticks: {
                        color: textColor,
                        backdropColor: 'transparent'
                    }
                }
            }
        }
    });
}

// Chart for international comparisons
function createInternationalComparisonChart() {
    const ctx = document.getElementById('internationalComparisonChart');
    if (!ctx) return;
    
    const isDark = document.body.classList.contains('dark-mode');
    const textColor = isDark ? '#cbd5e1' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Press Freedom', 'Electoral Integrity', 'Civil Liberties', 'Rule of Law', 'Fiscal Autonomy'],
            datasets: [{
                label: 'India',
                data: [159, 65, 55, 60, 30],
                backgroundColor: 'rgba(249, 115, 22, 0.6)',
                borderColor: 'rgb(249, 115, 22)',
                borderWidth: 1
            }, {
                label: 'Turkey',
                data: [165, 58, 52, 55, 45],
                backgroundColor: 'rgba(239, 68, 68, 0.6)',
                borderColor: 'rgb(239, 68, 68)',
                borderWidth: 1
            }, {
                label: 'Hungary',
                data: [92, 70, 65, 65, 35],
                backgroundColor: 'rgba(124, 58, 237, 0.6)',
                borderColor: 'rgb(124, 58, 237)',
                borderWidth: 1
            }, {
                label: 'Brazil',
                data: [92, 75, 70, 70, 55],
                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                borderColor: 'rgb(16, 185, 129)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Democratic Indicators: International Comparison (2024)',
                    color: textColor,
                    font: { size: 16 }
                },
                legend: {
                    labels: { color: textColor }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== null) {
                                if (context.dataIndex === 0) {
                                    label += context.parsed.y + '/180 (worse is higher)';
                                } else {
                                    label += context.parsed.y + '/100';
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: gridColor },
                    ticks: { 
                        color: textColor,
                        font: { size: 10 },
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 180,
                    grid: { color: gridColor },
                    ticks: { color: textColor }
                }
            }
        }
    });
}

// Chart for democratic decline comparison
function createDemocraticDeclineChart() {
    const ctx = document.getElementById('democraticDeclineChart');
    if (!ctx) return;
    
    const isDark = document.body.classList.contains('dark-mode');
    const textColor = isDark ? '#cbd5e1' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [2014, 2016, 2018, 2020, 2022, 2024],
            datasets: [{
                label: 'India',
                data: [0.72, 0.68, 0.62, 0.55, 0.48, 0.42],
                borderColor: 'rgb(249, 115, 22)',
                backgroundColor: 'rgba(249, 115, 22, 0.1)',
                tension: 0.4,
                borderWidth: 2
            }, {
                label: 'Turkey',
                data: [0.65, 0.58, 0.50, 0.45, 0.43, 0.40],
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.4,
                borderWidth: 2
            }, {
                label: 'Hungary',
                data: [0.70, 0.65, 0.58, 0.52, 0.48, 0.45],
                borderColor: 'rgb(124, 58, 237)',
                backgroundColor: 'rgba(124, 58, 237, 0.1)',
                tension: 0.4,
                borderWidth: 2
            }, {
                label: 'Brazil',
                data: [0.68, 0.65, 0.60, 0.58, 0.62, 0.65],
                borderColor: 'rgb(16, 185, 129)',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                borderWidth: 2,
                borderDash: [5, 5]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Democratic Quality Index Decline (2014-2024)',
                    color: textColor,
                    font: { size: 16 }
                },
                legend: {
                    labels: { color: textColor }
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 0.5,
                            yMax: 0.5,
                            borderColor: 'rgba(255, 99, 132, 0.5)',
                            borderWidth: 2,
                            borderDash: [10, 5],
                            label: {
                                enabled: true,
                                content: 'Hybrid Regime Threshold',
                                position: 'start'
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: gridColor },
                    ticks: { color: textColor }
                },
                y: {
                    beginAtZero: false,
                    min: 0.3,
                    max: 0.8,
                    grid: { color: gridColor },
                    ticks: { 
                        color: textColor,
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    },
                    title: {
                        display: true,
                        text: 'Democratic Quality Index',
                        color: textColor
                    }
                }
            }
        }
    });
}

// Call these functions when the respective tabs are shown
// Add this to your showTab function:
/*
case 'methods':
    setTimeout(() => {
        createDataCoverageChart();
        createIndexMethodChart();
    }, 100);
    break;
    
case 'implications':
    setTimeout(() => {
        createInternationalComparisonChart();
        createDemocraticDeclineChart();
    }, 100);
    break;
*/
