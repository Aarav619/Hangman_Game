from flask import Flask, render_template, jsonify, send_from_directory
import random
import os
import words_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_game():
    word = random.choice(words_file.words)
    return jsonify({"word": word})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render gives the port
    app.run(host='0.0.0.0', port=port)
