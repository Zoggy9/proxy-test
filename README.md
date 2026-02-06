# Web Proxy Server

A simple educational web proxy built with Python Flask. Browse websites through this proxy with a clean, modern interface.

## Features

- 🎨 Clean, gradient UI with responsive design
- 🔗 Automatic link rewriting (browse from site to site)
- 🚀 Easy to run - just one command
- 📱 Mobile-friendly interface
- ⚡ Fast and lightweight

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.7+ installed. Check with:
```bash
python --version
```

### 2. Install Dependencies
Open your terminal/command prompt in this folder and run:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask requests
```

### 3. Run the Proxy
```bash
python proxy_server.py
```

### 4. Open Your Browser
Go to: **http://localhost:5000**

## How to Use

1. Enter any URL in the input box (e.g., `example.com` or `https://example.com`)
2. Click "Browse"
3. The website will load through the proxy
4. Click on links within the page to navigate - they'll also go through the proxy

## How It Works

### The Python Backend (proxy_server.py)
- Uses Flask to create a web server
- Fetches websites using the `requests` library
- Rewrites all links in the HTML to route through the proxy
- Handles both absolute and relative URLs

### The Frontend (HTML/CSS)
- Modern gradient background (purple theme)
- Responsive form for URL input
- Clean card-based layout
- Error handling display

### URL Rewriting
The proxy uses regular expressions to find and rewrite:
- `href` attributes in links
- `src` attributes in images/scripts
- Absolute URLs (`https://...`)
- Protocol-relative URLs (`//...`)
- Relative URLs (`/path/to/page`)

## Limitations

⚠️ **This is for educational purposes only!**

- JavaScript-heavy sites may not work perfectly
- Some sites block proxy access
- HTTPS sites with strict security may have issues
- Images/CSS might not always load correctly
- Not suitable for production use

## Troubleshooting

**"Module not found" error?**
- Run `pip install -r requirements.txt` again

**Port 5000 already in use?**
- Change the port in `proxy_server.py`: `app.run(port=8080)`

**Site won't load?**
- Some sites block proxies
- Try a simpler website first (like example.com)
- Check your internet connection

## Next Steps to Learn More

1. **Add caching** - Store fetched pages to speed up repeat visits
2. **Add filtering** - Block certain domains or content
3. **Improve link rewriting** - Handle more edge cases
4. **Add HTTPS support** - Make the proxy itself use HTTPS
5. **Add request logging** - See what's being proxied

## Code Explanation

### Main Components:

```python
@app.route('/', methods=['GET', 'POST'])
def proxy():
    # Main function that handles both the form and proxy requests
```

- Handles POST requests from the URL form
- Handles GET requests when clicking links
- Fetches the target URL using `requests`
- Rewrites links before sending to browser

```python
def rewrite_links(content, base_url, proxy_url):
    # Finds and rewrites all URLs to route through proxy
```

- Uses regex to find URLs in HTML
- Replaces them with proxy URLs
- Preserves relative and absolute paths

## Educational Value

This project teaches:
- HTTP requests and responses
- URL parsing and manipulation
- Regular expressions
- Flask web framework basics
- HTML/CSS integration with Python
- Client-server architecture

## License

Free to use for educational purposes!
