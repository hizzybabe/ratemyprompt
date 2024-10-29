function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
});

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
