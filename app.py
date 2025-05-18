from flask import Flask, jsonify, request, render_template, session
import random
import hangman_stages
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load words from file
with open('words_alpha.txt') as f:
    words = f.read().splitlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    chosen_word = random.choice(words)
    session['chosen_word'] = chosen_word
    session['display'] = ['_' for _ in chosen_word]
    session['lives'] = 6
    session['guessed'] = []
    print(f"Chosen word is: {chosen_word}")  # Debugging purpose
    return jsonify({
        'display': session['display'],
        'lives': session['lives'],
        'guessed': session['guessed'],
        'stage': hangman_stages.stages[6]
    })

@app.route('/guess', methods=['POST'])
def guess():
    if 'chosen_word' not in session:
        return jsonify({
            'message': 'Game not started. Please start a new game.',
            'game_over': True
        })

    data = request.get_json()
    guessed_letter = data['letter'].lower()

    # Validate session data integrity
    if not isinstance(session.get('display'), list) or not isinstance(session.get('guessed'), list):
        return jsonify({
            'message': 'Game session corrupted. Please restart the game.',
            'game_over': True
        })

    if guessed_letter in session['guessed']:
        return jsonify({
            'message': 'Already guessed!',
            'display': session['display'],
            'lives': session['lives'],
            'guessed': session['guessed'],
            'stage': hangman_stages.stages[session['lives']],
            'game_over': False
        })

    session['guessed'].append(guessed_letter)

    correct_guess = False
    for i, letter in enumerate(session['chosen_word']):
        if letter == guessed_letter:
            session['display'][i] = guessed_letter
            correct_guess = True

    if correct_guess:
        message = 'Correct!'
    else:
        session['lives'] -= 1
        message = 'Wrong!'

    game_over = False
    if '_' not in session['display']:
        message = f'You Win !! The word was: {session["chosen_word"]}'
        game_over = True
    elif session['lives'] == 0:
        message = f'You Lose !! Word was: {session["chosen_word"]}'
        game_over = True

    # Debug log for backend state
    print(f"DEBUG -- Display: {session['display']} | Word: {session['chosen_word']} | Game Over: {game_over} | Message: {message}")

    return jsonify({
        'display': session['display'],
        'lives': session['lives'],
        'message': message,
        'guessed': session['guessed'],
        'game_over': game_over,
        'word': session['chosen_word'] if game_over else None,
        'stage': hangman_stages.stages[session['lives']]
    })

if __name__ == '__main__':
    app.run(debug=True)
