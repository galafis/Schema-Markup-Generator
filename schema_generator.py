#!/usr/bin/env python3
"""
Schema Markup Generator
Generate structured data markup for SEO optimization.
"""

from flask import Flask, render_template_string, jsonify, request
import json

app = Flask(__name__)

class SchemaGenerator:
    def __init__(self):
        self.schema_types = {
            'Organization': self.generate_organization,
            'Person': self.generate_person,
            'Product': self.generate_product,
            'Article': self.generate_article,
            'LocalBusiness': self.generate_local_business,
            'Event': self.generate_event
        }
    
    def generate_organization(self, data):
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": data.get('name', ''),
            "url": data.get('url', ''),
            "logo": data.get('logo', ''),
            "description": data.get('description', ''),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": data.get('street', ''),
                "addressLocality": data.get('city', ''),
                "addressRegion": data.get('state', ''),
                "postalCode": data.get('zip', ''),
                "addressCountry": data.get('country', '')
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": data.get('phone', ''),
                "contactType": "customer service"
            }
        }
    
    def generate_product(self, data):
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": data.get('name', ''),
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "brand": {
                "@type": "Brand",
                "name": data.get('brand', '')
            },
            "offers": {
                "@type": "Offer",
                "price": data.get('price', ''),
                "priceCurrency": data.get('currency', 'USD'),
                "availability": "https://schema.org/InStock"
            }
        }
    
    def generate_article(self, data):
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": data.get('title', ''),
            "description": data.get('description', ''),
            "author": {
                "@type": "Person",
                "name": data.get('author', '')
            },
            "datePublished": data.get('date', ''),
            "image": data.get('image', ''),
            "publisher": {
                "@type": "Organization",
                "name": data.get('publisher', '')
            }
        }

generator = SchemaGenerator()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Schema Markup Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
        .card { background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; }
        .output { background: #f8f9fa; padding: 20px; border-radius: 5px; font-family: monospace; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏷️ Schema Markup Generator</h1>
            <p>Generate structured data markup for SEO optimization</p>
        </div>
        
        <div class="card">
            <h3>Schema Type</h3>
            <select id="schemaType" onchange="updateForm()">
                <option value="Organization">Organization</option>
                <option value="Product">Product</option>
                <option value="Article">Article</option>
            </select>
        </div>
        
        <div class="card">
            <h3>Schema Data</h3>
            <div id="formFields"></div>
            <button onclick="generateSchema()" class="btn">Generate Schema</button>
        </div>
        
        <div class="card">
            <h3>Generated Schema Markup</h3>
            <div id="output" class="output">Select a schema type and fill the form to generate markup</div>
        </div>
    </div>
    
    <script>
        function updateForm() {
            const type = document.getElementById('schemaType').value;
            const fields = document.getElementById('formFields');
            
            let html = '';
            if (type === 'Organization') {
                html = `
                    <div class="form-group"><label>Name:</label><input type="text" id="name" value="Example Company"></div>
                    <div class="form-group"><label>URL:</label><input type="text" id="url" value="https://example.com"></div>
                    <div class="form-group"><label>Description:</label><textarea id="description">A leading company in technology solutions</textarea></div>
                    <div class="form-group"><label>Phone:</label><input type="text" id="phone" value="+1-555-123-4567"></div>
                `;
            } else if (type === 'Product') {
                html = `
                    <div class="form-group"><label>Name:</label><input type="text" id="name" value="Amazing Product"></div>
                    <div class="form-group"><label>Description:</label><textarea id="description">High-quality product with excellent features</textarea></div>
                    <div class="form-group"><label>Brand:</label><input type="text" id="brand" value="Example Brand"></div>
                    <div class="form-group"><label>Price:</label><input type="text" id="price" value="99.99"></div>
                `;
            } else if (type === 'Article') {
                html = `
                    <div class="form-group"><label>Title:</label><input type="text" id="title" value="How to Improve SEO"></div>
                    <div class="form-group"><label>Description:</label><textarea id="description">Complete guide to search engine optimization</textarea></div>
                    <div class="form-group"><label>Author:</label><input type="text" id="author" value="John Doe"></div>
                    <div class="form-group"><label>Date:</label><input type="date" id="date" value="2024-01-15"></div>
                `;
            }
            fields.innerHTML = html;
        }
        
        async function generateSchema() {
            const type = document.getElementById('schemaType').value;
            const formData = {};
            
            document.querySelectorAll('#formFields input, #formFields textarea').forEach(input => {
                formData[input.id] = input.value;
            });
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: type, data: formData })
                });
                
                const schema = await response.json();
                document.getElementById('output').textContent = JSON.stringify(schema, null, 2);
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        // Initialize form
        updateForm();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def generate_schema():
    data = request.get_json()
    schema_type = data.get('type')
    form_data = data.get('data', {})
    
    if schema_type in generator.schema_types:
        schema = generator.schema_types[schema_type](form_data)
        return jsonify(schema)
    
    return jsonify({'error': 'Invalid schema type'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

