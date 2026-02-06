from flask import Flask, request, render_template_string, Response
import requests
from urllib.parse import urljoin, urlparse
import re

app = Flask(__name__)

# HTML template for the proxy interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment Details - Math-7A Sequoia</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 30px 10px 10px 20px;
            width: 100%;
            padding: 10px;
        }
        
        h1 {
            color: #000000;
            margin-bottom: 20px;
            font-size: 2em;
        }
        
        .url-form {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .url-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .url-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #5568d3;
        }
        
        .info {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
        
        .content {
            flex: 1;
            background: white;
            margin: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .iframe-container {
            width: 100%;
            height: calc(100vh - 220px);
            border: none;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            margin: 20px;
            border-radius: 8px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🌐 Waizender Proxy V2.1</h1>
            <form method="POST" action="/" class="url-form">
                <input 
                    type="text" 
                    name="url" 
                    class="url-input" 
                    placeholder="https://example.com"
                    value="{{ current_url }}"
                    required
                >
                <button type="submit" class="btn">Browse</button>
            </form>
            <details class="info">
                ℹ️ Use the Waizender Proxy as a simple http/web proxy interface to access websites that may otherwise be blocked by a firewall.
            </details>
        </div>
    </div>
    
    {% if error %}
    <div class="warning">
        <strong>Error:</strong> {{ error }}
    </div>
    {% endif %}
    
    {% if content %}
    <div class="content">
        {{ content|safe }}
    </div>
    {% endif %}
</body>
</html>
'''

def rewrite_links(content, base_url, proxy_url):
    """Rewrite URLs in the content to go through the proxy"""
    
    # Rewrite absolute URLs
    content = re.sub(
        r'(href|src)=["\']https?://([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_url}?url=http://{m.group(2)}"',
        content
    )
    
    # Rewrite protocol-relative URLs
    content = re.sub(
        r'(href|src)=["\']//([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_url}?url=http://{m.group(2)}"',
        content
    )
    
    # Rewrite relative URLs
    parsed_base = urlparse(base_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    content = re.sub(
        r'(href|src)=["\'](?!http|//|#)([^"\']+)["\']',
        lambda m: f'{m.group(1)}="{proxy_url}?url={urljoin(base_domain, m.group(2))}"',
        content
    )
    
    return content

@app.route('/', methods=['GET', 'POST'])
def proxy():
    current_url = ''
    error = None
    content = None
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        current_url = url
        
        if url:
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            try:
                # Fetch the page
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                # Check if it's HTML content
                content_type = response.headers.get('Content-Type', '')
                
                if 'text/html' in content_type:
                    # Rewrite links to go through proxy
                    proxy_url = request.url_root.rstrip('/')
                    content = rewrite_links(response.text, url, proxy_url)
                else:
                    content = f'<pre>{response.text}</pre>'
                    
            except requests.RequestException as e:
                error = f"Failed to fetch URL: {str(e)}"
            except Exception as e:
                error = f"An error occurred: {str(e)}"
    
    elif request.args.get('url'):
        # Handle links clicked within proxied pages
        url = request.args.get('url')
        current_url = url
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            content_type = response.headers.get('Content-Type', '')
            
            if 'text/html' in content_type:
                proxy_url = request.url_root.rstrip('/')
                content = rewrite_links(response.text, url, proxy_url)
            else:
                # For non-HTML content, return it directly
                return Response(response.content, mimetype=response.headers.get('Content-Type'))
                
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    
    return render_template_string(HTML_TEMPLATE, current_url=current_url, error=error, content=content)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting Web Proxy Server...")
    print(f"📍 Server running on port {port}")
    print("⚠️  Note: This is for educational purposes only!")
    app.run(debug=False, host='0.0.0.0', port=port)
