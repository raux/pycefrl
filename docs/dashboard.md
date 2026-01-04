---
layout: default
title: Analysis Dashboard
description: Interactive dashboard for viewing pycefrl analysis results
dashboard: true
---

<div class="container">
  <h1>Analysis Dashboard</h1>
  <p>Upload your analysis results to visualize code complexity and explore detailed breakdowns.</p>

  <section class="dashboard-controls">
    <div>
      <label for="file-upload" class="btn btn-primary" style="cursor: pointer; margin: 0;">
        📁 Load JSON File
        <input type="file" id="file-upload" accept=".json" style="display: none;">
      </label>
    </div>
    
    <input type="text" id="filter-input" placeholder="Search files or elements..." />
    
    <select id="level-filter">
      <option value="">All Levels</option>
      <option value="A1">Level A1</option>
      <option value="A2">Level A2</option>
      <option value="B1">Level B1</option>
      <option value="B2">Level B2</option>
      <option value="C1">Level C1</option>
      <option value="C2">Level C2</option>
    </select>
    
    <button id="export-csv" class="btn btn-secondary">💾 Export to CSV</button>
  </section>

  <section>
    <h2>Level Distribution</h2>
    <div id="stats-grid" class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">Loading...</div>
        <div class="stat-label">Please upload data</div>
      </div>
    </div>
  </section>

  <section class="chart-container">
    <h2>CEFR Level Analysis</h2>
    <canvas id="level-chart" width="800" height="400"></canvas>
  </section>

  <section class="chart-container">
    <div id="class-chart"></div>
  </section>

  <section>
    <div id="detailed-analysis"></div>
  </section>

  <section class="mt-4">
    <h2>How to Use This Dashboard</h2>
    <div class="features">
      <div class="card">
        <h3>1. Upload Results</h3>
        <p>Click "Load JSON File" to upload your <code>data.json</code> or <code>summary_data.json</code> file from a pycefrl analysis.</p>
      </div>
      
      <div class="card">
        <h3>2. Explore Visualizations</h3>
        <p>View level distribution charts, element breakdowns, and file-by-file analysis.</p>
      </div>
      
      <div class="card">
        <h3>3. Filter & Search</h3>
        <p>Use the search box and level filter to focus on specific code elements or complexity levels.</p>
      </div>
      
      <div class="card">
        <h3>4. Export Data</h3>
        <p>Download filtered results as CSV for further analysis in Excel or other tools.</p>
      </div>
    </div>
  </section>

  <section class="mt-4">
    <h2>Understanding the Visualizations</h2>
    
    <h3>Level Distribution</h3>
    <p>Shows the count of code elements at each CEFR level (A1-C2). Higher levels indicate more complex code patterns.</p>
    
    <h3>CEFR Level Chart</h3>
    <p>Bar chart visualization of how many elements exist at each complexity level. Useful for getting a quick overview of overall code complexity.</p>
    
    <h3>Top Code Elements</h3>
    <p>Displays the most frequently used code constructs in your project, helping identify common patterns and potential areas for refactoring.</p>
    
    <h3>File-Level Analysis</h3>
    <p>Detailed breakdown showing which files contain elements at each level. Helps identify which files might benefit from simplification or refactoring.</p>
  </section>

  <section class="mt-4">
    <h2>Interpretation Guide</h2>
    
    <div class="card">
      <h3>What High C1/C2 Percentages Mean</h3>
      <p>A high percentage of advanced (C1/C2) elements might indicate:</p>
      <ul>
        <li>Complex, sophisticated code that uses advanced Python features</li>
        <li>Code that may be harder for junior developers to understand</li>
        <li>Good use of Pythonic idioms (comprehensions, generators, etc.)</li>
        <li>Potential areas where simpler alternatives might improve readability</li>
      </ul>
    </div>
    
    <div class="card">
      <h3>What High A1/A2 Percentages Mean</h3>
      <p>A high percentage of basic (A1/A2) elements might indicate:</p>
      <ul>
        <li>Code that is easy to read and understand</li>
        <li>Good for beginners and learning resources</li>
        <li>Potential opportunities to use more advanced Python features</li>
        <li>Scripts or simple utilities that don't require complexity</li>
      </ul>
    </div>
    
    <div class="card">
      <h3>Balanced Distribution</h3>
      <p>A balanced distribution across levels often indicates:</p>
      <ul>
        <li>Well-structured code with appropriate complexity for different tasks</li>
        <li>Good separation of concerns (simple utilities + complex business logic)</li>
        <li>Code that's accessible to developers of various skill levels</li>
      </ul>
    </div>
  </section>

  <section class="mt-4 text-center">
    <h2>Need Help?</h2>
    <p>For more information on running analyses and generating data files:</p>
    <div class="cta-buttons">
      <a href="./quickstart" class="btn btn-primary">Quick Start Guide</a>
      <a href="./examples" class="btn btn-secondary">View Examples</a>
      <a href="https://github.com/raux/pycefrl" class="btn btn-secondary" target="_blank" rel="noopener">GitHub</a>
    </div>
  </section>
</div>
