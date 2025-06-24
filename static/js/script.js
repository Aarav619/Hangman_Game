const stages = [
`  _______
 |       |
 |       O
 |      /|\\
 |      / \\
 |
_|_

=============`,
`  _______
 |       |
 |       O
 |      /|\\
 |      / 
 |
_|_

=============`,
`  _______
 |       |
 |       O
 |      /|\\
 |       
 |
_|_

=============`,
`  _______
 |       |
 |       O
 |      /|
 |      
 |
_|_

=============`,
`  _______
 |       |
 |       O
 |      / 
 |       
 |
_|_

=============`,
`  _______
 |       |
 |       O
 |      
 |       
 |
_|_

=============`,
`  _______
 |       |
 |       
 |      
 |      
 |
_|_

=============`];

let word = "";
let display = [];
let lives = 6;
let guessedLetters = [];

fetch('/start')
  .then(res => res.json())
  .then(data => {
    word = data.word.toLowerCase();
    display = Array(word.length).fill('_');
    document.getElementById('word').innerText = display.join(' ');
    document.getElementById('hangman').innerText = stages[0];
  });

function guess() {
  document.getElementById('click-sound').play();

  const letterInput = document.getElementById('letter');
  const letter = letterInput.value.toLowerCase();
  letterInput.value = '';
  letterInput.focus();

  if (!letter || letter.length !== 1 || !/[a-z]/.test(letter)) return;
  if (guessedLetters.includes(letter)) return;

  guessedLetters.push(letter);
  document.getElementById('guessed').innerText = guessedLetters.join(', ');

  let correct = false;
  for (let i = 0; i < word.length; i++) {
    if (word[i] === letter) {
      display[i] = letter;
      correct = true;
    }
  }

  if (!correct) {
    lives--;
    document.getElementById('hangman').innerText = stages[6 - lives];
  }

  document.getElementById('word').innerText = display.join(' ');

  if (!display.includes('_')) {
    document.getElementById('result').innerText = "🎉 You Win!";
    document.getElementById('win-sound').play();
    document.getElementById('letter').disabled = true;
  }

  if (lives === 0) {
    document.getElementById('result').innerText = `☠️ You Lost! Word was "${word}"`;
    document.getElementById('lose-sound').play();
    document.getElementById('died-sound').play();
    document.getElementById('letter').disabled = true;
  }
}

function restart() {
  window.location.reload();
}
