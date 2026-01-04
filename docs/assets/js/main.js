// ===========================
// Theme Toggle
// ===========================
function initTheme() {
  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);
  updateThemeButton(theme);
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeButton(newTheme);
}

function updateThemeButton(theme) {
  const button = document.getElementById('theme-toggle');
  if (button) {
    button.textContent = theme === 'light' ? '🌙' : '☀️';
    button.setAttribute('aria-label', `Switch to ${theme === 'light' ? 'dark' : 'light'} mode`);
  }
}

// ===========================
// Mobile Menu Toggle
// ===========================
function toggleMobileMenu() {
  const nav = document.querySelector('.nav');
  if (nav) {
    nav.classList.toggle('active');
  }
}

// ===========================
// Active Navigation Link
// ===========================
function updateActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav a, .sidebar-nav a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });
}

// ===========================
// Table of Contents Generator
// ===========================
function generateTableOfContents() {
  const tocContainer = document.getElementById('toc');
  if (!tocContainer) return;

  const headings = document.querySelectorAll('.main-content h2, .main-content h3');
  if (headings.length === 0) return;

  const tocList = document.createElement('ul');
  
  headings.forEach((heading, index) => {
    // Add ID to heading if it doesn't have one
    if (!heading.id) {
      heading.id = `heading-${index}`;
    }

    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = `#${heading.id}`;
    a.textContent = heading.textContent;
    
    if (heading.tagName === 'H3') {
      li.style.marginLeft = '1rem';
    }
    
    li.appendChild(a);
    tocList.appendChild(li);
  });

  tocContainer.appendChild(tocList);
}

// ===========================
// Smooth Scroll for Anchor Links
// ===========================
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// ===========================
// Copy Code Blocks
// ===========================
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre code');
  
  codeBlocks.forEach((codeBlock) => {
    const pre = codeBlock.parentElement;
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.style.cssText = `
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;
      padding: 0.25rem 0.75rem;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 0.25rem;
      color: white;
      cursor: pointer;
      font-size: 0.875rem;
    `;
    
    pre.style.position = 'relative';
    
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(codeBlock.textContent);
        button.textContent = 'Copied!';
        setTimeout(() => {
          button.textContent = 'Copy';
        }, 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
      }
    });
    
    pre.appendChild(button);
  });
}

// ===========================
// Search Functionality
// ===========================
function initSearch() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  if (!searchInput || !searchResults) return;

  let searchIndex = [];
  
  // Build simple search index
  const contentElements = document.querySelectorAll('.main-content h1, .main-content h2, .main-content h3, .main-content p');
  contentElements.forEach((element) => {
    searchIndex.push({
      text: element.textContent,
      element: element,
      type: element.tagName.toLowerCase()
    });
  });

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    
    if (query.length < 2) {
      searchResults.innerHTML = '';
      searchResults.style.display = 'none';
      return;
    }

    const results = searchIndex.filter(item => 
      item.text.toLowerCase().includes(query)
    ).slice(0, 10);

    if (results.length > 0) {
      searchResults.innerHTML = results.map(result => `
        <div class="search-result-item" onclick="scrollToElement('${result.element.id || result.element.textContent}')">
          <strong>${result.type}</strong>: ${highlightText(result.text, query)}
        </div>
      `).join('');
      searchResults.style.display = 'block';
    } else {
      searchResults.innerHTML = '<div class="search-result-item">No results found</div>';
      searchResults.style.display = 'block';
    }
  });

  // Close search results when clicking outside
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.style.display = 'none';
    }
  });
}

function highlightText(text, query) {
  const regex = new RegExp(`(${query})`, 'gi');
  return text.substring(0, 150).replace(regex, '<mark>$1</mark>') + '...';
}

function scrollToElement(id) {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}

// ===========================
// Initialize on DOM Load
// ===========================
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  updateActiveNavLink();
  generateTableOfContents();
  initSmoothScroll();
  addCopyButtons();
  initSearch();

  // Add event listener for theme toggle button
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }

  // Add event listener for mobile menu toggle
  const menuToggle = document.getElementById('menu-toggle');
  if (menuToggle) {
    menuToggle.addEventListener('click', toggleMobileMenu);
  }
});

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    toggleTheme,
    toggleMobileMenu,
    generateTableOfContents
  };
}
