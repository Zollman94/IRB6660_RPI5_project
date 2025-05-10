from flask import Flask, send_from_directory, render_template_string, abort
import os

app = Flask(__name__)

BASE_DIR = '/opt/robot/IRB6660_RPI5_project'  # Změňte na požadovaný adresář
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapshot Preview</title>
    <meta http-equiv="refresh" content="1">  <!-- Automatické obnovení stránky každé 2 sekundy -->
</head>
<body>
    <h1>Live Snapshot Preview</h1>
    <a href="/">Home</a>
    <img src="latest.jpg" width="640" height="480" />
</body>
</html>
'''

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    files = os.listdir(abs_path)
    file_links = []
    for filename in files:
        file_path = os.path.join(req_path, filename)
        if os.path.isdir(os.path.join(BASE_DIR, file_path)):
            file_links.append(f'<li><a href="/{file_path}/">{filename}/</a></li>')
        else:
            file_links.append(f'<li><a href="/{file_path}">{filename}</a></li>')

    return render_template_string('''
        <a href="/stream">Stream</a>
        <br>
        <a href="/">Home</a>
        <h1>Index of /{{ req_path }}</h1>
        <ul>
            {% for file_link in file_links %}
                {{ file_link|safe }}
            {% endfor %}
        </ul>
    ''', req_path=req_path, file_links=file_links)

@app.route('/stream')
def stream():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
