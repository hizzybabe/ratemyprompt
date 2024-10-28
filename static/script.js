async function ratePrompt() {
    const promptInput = document.getElementById('promptInput').value;
    const loading = document.getElementById('loading');
    const scoreDiv = document.getElementById('score');
    const adviceDiv = document.getElementById('advice');

    if (!promptInput.trim()) {
        alert('Please enter a prompt first!');
        return;
    }

    // Show loading state
    loading.style.display = 'block';
    scoreDiv.innerHTML = '';
    adviceDiv.innerHTML = '';

    try {
        const response = await fetch('/rate-prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: promptInput })
        });

        const data = await response.json();

        // Hide loading state
        loading.style.display = 'none';

        // Display results
        scoreDiv.innerHTML = `<h2>Score: <span class="score">${data.score}/100</span></h2>`;
        adviceDiv.innerHTML = `<h2>Improvement Advice:</h2><p>${data.advice}</p>`;
    } catch (error) {
        loading.style.display = 'none';
        alert('Error analyzing prompt. Please try again.');
    }
}
