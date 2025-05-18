async function startGame() {
    const response = await fetch('/start', { method: 'POST' });
    const data = await response.json();
    updateUI(data);

    const input = document.getElementById('guess-input');
    input.disabled = false;
    input.value = '';
    input.focus();
}

async function makeGuess() {
    const input = document.getElementById('guess-input');
    const letter = input.value.trim().toLowerCase();

    if (!letter.match(/^[a-z]$/)) {
        alert('Please enter a valid single letter (a-z).');
        input.value = '';
        input.focus();
        return;
    }

    const response = await fetch('/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letter })
    });

    const data = await response.json();
    console.log("DEBUG RESPONSE:", data);  // 👈 DEBUG LOG

    updateUI(data);

    if (data.game_over) {
        //input.disabled = true;
        // Wait 100ms to allow UI update before showing alert
        setTimeout(() => {
            alert(data.message);
        }, 100);
    }

    input.value = '';
    input.focus();
}

function updateUI(data) {
    document.getElementById('word-display').innerText = data.display.join(' ');
    document.getElementById('lives').innerText = data.lives;
    document.getElementById('guessed').innerText = data.guessed.join(', ');
    document.getElementById('message').innerText = data.message;
    document.getElementById('stage-display').innerText = data.stage;
}
