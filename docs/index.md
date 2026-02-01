---
layout: default
title: pycefrl - Python Code Level Analyzer
description: Identifying Python3 Code Level Using the CEFR Framework as Inspiration
---

<section class="hero">
  <h1>🐍 pycefrl</h1>
  <p>Identify Python3 Code Level Using the CEFR Framework as Inspiration</p>
  <p>Analyze code complexity and skill levels in Python projects, repositories, and snippets</p>
  <div class="cta-buttons">
    <a href="./installation" class="btn btn-primary">Get Started</a>
    <a href="./dashboard" class="btn btn-secondary">View Dashboard</a>
    <a href="https://github.com/raux/pycefrl" class="btn btn-secondary" target="_blank" rel="noopener">GitHub</a>
  </div>
</section>

<div class="container">
  <section>
    <h2 class="text-center">What is pycefrl?</h2>
    <p class="text-center">
      pycefrl is a powerful tool that evaluates Python code using a framework inspired by the 
      <a href="https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages" target="_blank" rel="noopener">Common European Framework of Reference for Languages (CEFR)</a>.
      It assigns complexity levels (A1 to C2) to code elements, helping developers understand and improve code quality.
    </p>
  </section>

  <section class="features">
    <div class="card">
      <div class="card-icon">📊</div>
      <h3>Multi-Source Analysis</h3>
      <p>Analyze local directories, GitHub repositories, individual users, or code snippets with ease.</p>
    </div>
    
    <div class="card">
      <div class="card-icon">🎯</div>
      <h3>CEFR-Inspired Levels</h3>
      <p>Code elements are categorized from A1 (basic) to C2 (advanced), providing clear complexity insights.</p>
    </div>
    
    <div class="card">
      <div class="card-icon">📈</div>
      <h3>Rich Visualizations</h3>
      <p>Interactive dashboards with charts, heatmaps, and detailed reports in JSON and CSV formats.</p>
    </div>
    
    <div class="card">
      <div class="card-icon">⚡</div>
      <h3>Easy to Use</h3>
      <p>Simple command-line interface and Streamlit web app for real-time analysis and visualization.</p>
    </div>
    
    <div class="card">
      <div class="card-icon">🔍</div>
      <h3>Detailed Breakdown</h3>
      <p>Get file-by-file, class-by-class analysis with line numbers and displacement information.</p>
    </div>
    
    <div class="card">
      <div class="card-icon">🚀</div>
      <h3>Open Source</h3>
      <p>Free and open source under MIT license. Contribute and customize to your needs.</p>
    </div>
  </section>

  <section class="mt-4">
    <h2>Quick Start</h2>
    <p>Get started with pycefrl in just a few steps:</p>
    
    <div class="card">
      <h3>1. Install Dependencies</h3>
      <pre><code>pip3 install -r requirements.txt</code></pre>
    </div>
    
    <div class="card">
      <h3>2. Generate Level Dictionary</h3>
      <pre><code>python3 dict.py</code></pre>
    </div>
    
    <div class="card">
      <h3>3. Run Analysis</h3>
      <pre><code># Analyze a directory
python3 pycerfl.py directory /path/to/code

# Analyze a GitHub repository
python3 pycerfl.py repo https://github.com/user/repo

# Analyze a GitHub user
python3 pycerfl.py user username</code></pre>
    </div>
    
    <div class="card">
      <h3>4. View Results</h3>
      <p>Results are saved as <code>data.json</code> and <code>data.csv</code>. Use our interactive dashboard to visualize them!</p>
      <a href="./dashboard" class="btn btn-primary">Open Dashboard</a>
    </div>
  </section>

  <section class="mt-4">
    <h2>Code Level Examples</h2>
    <div class="features">
      <div class="card">
        <div class="level-badge level-a1">A1</div>
        <h4>Basic Elements</h4>
        <p>Simple lists, tuples, assignments, print statements</p>
      </div>
      
      <div class="card">
        <div class="level-badge level-a2">A2</div>
        <h4>Elementary</h4>
        <p>File operations, simple loops, function calls, imports</p>
      </div>
      
      <div class="card">
        <div class="level-badge level-b1">B1</div>
        <h4>Intermediate</h4>
        <p>Functions with arguments, classes, exception handling</p>
      </div>
      
      <div class="card">
        <div class="level-badge level-b2">B2</div>
        <h4>Upper Intermediate</h4>
        <p>Advanced functions, decorators, class inheritance</p>
      </div>
      
      <div class="card">
        <div class="level-badge level-c1">C1</div>
        <h4>Advanced</h4>
        <p>Comprehensions, generators, metaclasses, descriptors</p>
      </div>
      
      <div class="card">
        <div class="level-badge level-c2">C2</div>
        <h4>Proficient</h4>
        <p>Complex comprehensions, advanced OOP patterns</p>
      </div>
    </div>
  </section>

  <section class="mt-4">
    <h2>Streamlit Web Interface</h2>
    <p>Launch the interactive Streamlit application for real-time analysis with beautiful visualizations:</p>
    <pre><code>python3 -m streamlit run app.py</code></pre>
    <p><strong>Features:</strong></p>
    <ul>
      <li>Real-time execution logs and system statistics</li>
      <li>Interactive visualizations: Bubble Charts, Heatmaps, Treemaps</li>
      <li>Download reports in JSON and CSV formats</li>
      <li>Select analysis mode: Directory, GitHub Repository, or GitHub User</li>
    </ul>
  </section>

  <section class="mt-4 text-center">
    <h2>Ready to Get Started?</h2>
    <p>Explore the documentation to learn more about pycefrl's capabilities</p>
    <div class="cta-buttons">
      <a href="./installation" class="btn btn-primary">Installation Guide</a>
      <a href="./examples" class="btn btn-secondary">View Examples</a>
      <a href="./api" class="btn btn-secondary">API Reference</a>
    </div>
  </section>
</div>

