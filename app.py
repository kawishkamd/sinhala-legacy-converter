from flask import Flask, request, jsonify, send_from_directory
import json

app = Flask(__name__)

# Load the mapping data
with open('data_list.json', 'r', encoding='utf-8') as f:
    mapping_data = json.load(f)

# Create conversion dictionaries
unicode_to_fm = {}
unicode_to_isi = {}

for item in mapping_data:
    if item['uni'] and item['fm']:
        unicode_to_fm[item['uni']] = item['fm']
    if item['uni'] and item['isi']:
        unicode_to_isi[item['uni']] = item['isi']

def convert_text(text, style):
    converted_text = []
    if style == 'fm':
        mapping = unicode_to_fm
    elif style == 'isi':
        mapping = unicode_to_isi
    else:
        return text
    
    i = 0
    n = len(text)
    
    while i < n:
        # Check for longest possible match (up to 4 characters)
        matched = False
        for l in range(4, 0, -1):
            if i + l <= n:
                substr = text[i:i+l]
                if substr in mapping:
                    converted_text.append(mapping[substr])
                    i += l
                    matched = True
                    break
        if not matched:
            converted_text.append(text[i])
            i += 1
    
    return ''.join(converted_text)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/data_list.json')
def data_list():
    return send_from_directory('.', 'data_list.json')

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json()
    text = data.get('text', '')
    style = data.get('style', 'fm')
    converted = convert_text(text, style)
    return jsonify({'converted_text': converted})

if __name__ == '__main__':
    app.run(debug=True)
