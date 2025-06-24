from flask import Flask, render_template, jsonify, send_from_directory
import random
import os
import words_file

app = Flask(__name__)

# Home route to render the game
@app.route('/')
def home():
    return render_template('index.html')

# API to get a random word
@app.route('/start', methods=['GET'])
def start_game():
    word = random.choice(words_file.words)
    return jsonify({"word": word})

# Optional favicon handler (suppresses 404 errors for favicon)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local
    app.run(host='0.0.0.0', port=port)

