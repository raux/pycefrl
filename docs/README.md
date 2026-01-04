# pycefrl Documentation

This directory contains the GitHub Pages website for pycefrl.

## Structure

- `index.md` - Homepage
- `installation.md` - Installation guide
- `quickstart.md` - Quick start tutorial
- `guide.md` - Comprehensive user guide
- `api.md` - API reference
- `examples.md` - Usage examples
- `contributing.md` - Contributing guidelines
- `dashboard.md` - Interactive results dashboard
- `_config.yml` - Jekyll configuration
- `_layouts/` - Page layout templates
- `_includes/` - Reusable HTML components
- `assets/` - CSS, JavaScript, and images

## Local Development

### Using Jekyll

If you have Ruby and Jekyll installed:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000/pycefrl in your browser.

### Without Jekyll

Simply open the HTML files in a web browser. Note that some features (like includes and layouts) won't work without Jekyll.

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch. The site is available at:

https://raux.github.io/pycefrl

## Updating Documentation

1. Edit the relevant `.md` files
2. Test locally if possible
3. Commit and push changes
4. GitHub Pages will automatically rebuild the site

## Styling

The site uses custom CSS in `assets/css/style.css` with:
- CSS variables for theming
- Dark/light mode support
- Responsive design
- Modern, clean layout

## JavaScript Features

Interactive features in `assets/js/`:
- `main.js` - Theme toggle, navigation, TOC generation
- `dashboard.js` - Data visualization and analysis display

## Contributing

See [contributing.md](./contributing.md) for guidelines on contributing to the documentation.
