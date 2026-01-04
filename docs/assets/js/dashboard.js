// ===========================
// Dashboard Data Management
// ===========================
let analysisData = null;
let summaryData = null;
let totalData = null;

// ===========================
// Load Analysis Data
// ===========================
async function loadSampleData() {
  try {
    // Try to load data from different sources
    const responses = await Promise.all([
      fetch('../data.json').catch(() => null),
      fetch('../DATA_JSON/summary_data.json').catch(() => null),
      fetch('../DATA_JSON/total_data.json').catch(() => null)
    ]);

    if (responses[0] && responses[0].ok) {
      analysisData = await responses[0].json();
    }
    if (responses[1] && responses[1].ok) {
      summaryData = await responses[1].json();
    }
    if (responses[2] && responses[2].ok) {
      totalData = await responses[2].json();
    }

    if (!summaryData && !analysisData) {
      // Load demo data if no real data is available
      loadDemoData();
    } else {
      displayDashboard();
    }
  } catch (error) {
    console.error('Error loading data:', error);
    loadDemoData();
  }
}

function loadDemoData() {
  summaryData = {
    "Levels": {
      "A1": 450,
      "A2": 380,
      "B1": 120,
      "B2": 45,
      "C1": 28,
      "C2": 12
    },
    "Class": {
      "Simple List": 81,
      "Simple Assignment": 150,
      "Simple If statements": 95,
      "Function": 42,
      "Simple Class": 15
    }
  };
  displayDashboard();
}

// ===========================
// File Upload Handler
// ===========================
function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      
      // Determine data type and load accordingly
      if (data.Levels) {
        summaryData = data;
      } else if (Array.isArray(data)) {
        analysisData = data;
      } else {
        totalData = data;
      }
      
      displayDashboard();
      showNotification('Data loaded successfully!', 'success');
    } catch (error) {
      console.error('Error parsing JSON:', error);
      showNotification('Error loading file. Please ensure it\'s valid JSON.', 'error');
    }
  };
  
  reader.readAsText(file);
}

// ===========================
// Display Dashboard
// ===========================
function displayDashboard() {
  if (summaryData && summaryData.Levels) {
    displayLevelStats(summaryData.Levels);
    createLevelChart(summaryData.Levels);
  }
  
  if (summaryData && summaryData.Class) {
    createClassChart(summaryData.Class);
  }
  
  if (totalData) {
    displayDetailedAnalysis(totalData);
  }
}

// ===========================
// Level Statistics
// ===========================
function displayLevelStats(levels) {
  const statsGrid = document.getElementById('stats-grid');
  if (!statsGrid) return;

  const total = Object.values(levels).reduce((sum, count) => sum + count, 0);
  
  statsGrid.innerHTML = Object.entries(levels)
    .filter(([level]) => ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].includes(level))
    .map(([level, count]) => {
      const percentage = ((count / total) * 100).toFixed(1);
      return `
        <div class="stat-card">
          <div class="stat-value level-${level.toLowerCase()}">${count}</div>
          <div class="stat-label">Level ${level} (${percentage}%)</div>
        </div>
      `;
    }).join('');
}

// ===========================
// Level Distribution Chart
// ===========================
function createLevelChart(levels) {
  const canvas = document.getElementById('level-chart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const standardLevels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
  const data = standardLevels.map(level => levels[level] || 0);
  const colors = [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'
  ];

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Chart dimensions
  const padding = 40;
  const chartWidth = canvas.width - 2 * padding;
  const chartHeight = canvas.height - 2 * padding;
  const maxValue = Math.max(...data);
  const barWidth = chartWidth / data.length;

  // Draw bars
  data.forEach((value, index) => {
    const barHeight = (value / maxValue) * chartHeight;
    const x = padding + index * barWidth;
    const y = canvas.height - padding - barHeight;

    // Draw bar
    ctx.fillStyle = colors[index];
    ctx.fillRect(x + 5, y, barWidth - 10, barHeight);

    // Draw value on top
    ctx.fillStyle = '#666';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(value, x + barWidth / 2, y - 5);

    // Draw label
    ctx.fillText(standardLevels[index], x + barWidth / 2, canvas.height - padding + 20);
  });

  // Draw axes
  ctx.strokeStyle = '#ddd';
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, canvas.height - padding);
  ctx.lineTo(canvas.width - padding, canvas.height - padding);
  ctx.stroke();
}

// ===========================
// Class Distribution Chart
// ===========================
function createClassChart(classes) {
  const container = document.getElementById('class-chart');
  if (!container) return;

  // Get top 10 classes
  const sortedClasses = Object.entries(classes)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const maxCount = sortedClasses[0][1];

  container.innerHTML = `
    <h3>Top 10 Code Elements</h3>
    <div class="horizontal-bar-chart">
      ${sortedClasses.map(([name, count]) => {
        const percentage = (count / maxCount) * 100;
        return `
          <div class="bar-item">
            <div class="bar-label">${name}</div>
            <div class="bar-container">
              <div class="bar-fill" style="width: ${percentage}%"></div>
              <div class="bar-count">${count}</div>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// ===========================
// Detailed File Analysis
// ===========================
function displayDetailedAnalysis(totalData) {
  const container = document.getElementById('detailed-analysis');
  if (!container) return;

  const rows = [];
  for (const [repoName, files] of Object.entries(totalData)) {
    for (const [fileName, stats] of Object.entries(files)) {
      if (stats.Levels) {
        rows.push({
          repository: repoName,
          file: fileName,
          ...stats.Levels
        });
      }
    }
  }

  if (rows.length === 0) return;

  // Create table
  const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
  const table = `
    <h3>File-Level Analysis</h3>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Repository</th>
            <th>File</th>
            ${levels.map(level => `<th>Level ${level}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${rows.map(row => `
            <tr>
              <td>${row.repository}</td>
              <td>${row.file}</td>
              ${levels.map(level => `<td>${row[level] || 0}</td>`).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;

  container.innerHTML = table;
}

// ===========================
// Filter and Search
// ===========================
function filterResults() {
  const searchTerm = document.getElementById('filter-input')?.value.toLowerCase();
  const levelFilter = document.getElementById('level-filter')?.value;
  
  if (!searchTerm && !levelFilter) {
    displayDashboard();
    return;
  }

  // Implement filtering logic here
  console.log('Filtering by:', searchTerm, levelFilter);
}

// ===========================
// Export Data
// ===========================
function exportToCSV() {
  if (!summaryData) {
    showNotification('No data to export', 'error');
    return;
  }

  let csv = 'Type,Name,Count\n';
  
  if (summaryData.Levels) {
    for (const [level, count] of Object.entries(summaryData.Levels)) {
      csv += `Level,${level},${count}\n`;
    }
  }
  
  if (summaryData.Class) {
    for (const [className, count] of Object.entries(summaryData.Class)) {
      csv += `Class,${className},${count}\n`;
    }
  }

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'pycefrl-analysis.csv';
  a.click();
  window.URL.revokeObjectURL(url);
  
  showNotification('Data exported successfully!', 'success');
}

// ===========================
// Notifications
// ===========================
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 80px;
    right: 20px;
    padding: 1rem 2rem;
    background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    color: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    animation: slideIn 0.3s ease;
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// ===========================
// Initialize Dashboard
// ===========================
document.addEventListener('DOMContentLoaded', () => {
  // Add event listeners
  const fileInput = document.getElementById('file-upload');
  if (fileInput) {
    fileInput.addEventListener('change', handleFileUpload);
  }

  const filterInput = document.getElementById('filter-input');
  if (filterInput) {
    filterInput.addEventListener('input', filterResults);
  }

  const levelFilter = document.getElementById('level-filter');
  if (levelFilter) {
    levelFilter.addEventListener('change', filterResults);
  }

  const exportBtn = document.getElementById('export-csv');
  if (exportBtn) {
    exportBtn.addEventListener('click', exportToCSV);
  }

  // Load data
  loadSampleData();
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
  .horizontal-bar-chart { margin-top: 1rem; }
  .bar-item { margin-bottom: 1rem; }
  .bar-label { font-size: 0.875rem; margin-bottom: 0.25rem; color: var(--text-secondary); }
  .bar-container { display: flex; align-items: center; gap: 0.5rem; }
  .bar-fill { 
    height: 30px; 
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    border-radius: 0.25rem;
    transition: width 0.3s ease;
  }
  .bar-count { 
    font-weight: 600; 
    min-width: 40px;
    color: var(--text-primary);
  }
  .table-container {
    overflow-x: auto;
    margin-top: 1rem;
  }
`;
document.head.appendChild(style);
