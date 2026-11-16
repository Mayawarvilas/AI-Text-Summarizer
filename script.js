document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('inputText');
    const wordCount = document.getElementById('wordCount');
    const summaryLength = document.getElementById('summaryLength');
    const sliderValue = document.getElementById('sliderValue');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const themeToggle = document.getElementById('themeToggle');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const summary = document.getElementById('summary');
    const outputSection = document.getElementById('outputSection');

    // Word count
    inputText.addEventListener('input', () => {
        const words = inputText.value.trim().split(/\s+/).filter(w => w).length;
        wordCount.textContent = `${words} words`;
    });

    // Summary length slider
    summaryLength.addEventListener('input', (e) => {
        const value = e.target.value;
        const labels = ['Tiny', 'Short', 'Medium', 'Long', 'Full'];
        sliderValue.textContent = labels[value - 1];
    });

    // Theme toggle
    themeToggle.addEventListener('click', () => {
        const isDark = document.body.getAttribute('data-theme') === 'dark';
        document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
        themeToggle.textContent = isDark ? '☀️' : '🌙';
    });

    // Summarize function
    summarizeBtn.addEventListener('click', summarize);

    async function summarize() {
        const text = inputText.value.trim();
        if (!text) {
            alert('Please enter some text first!');
            return;
        }

        // UI states
        summarizeBtn.disabled = true;
        summarizeBtn.textContent = 'Summarizing...';
        progressContainer.style.display = 'block';
        outputSection.classList.add('loading');

        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 200);

        try {
            // Replace with your actual API endpoint
            const response = await fetch('http://127.0.0.1:8000/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    length: parseInt(summaryLength.value) // 1-5 scale
                })
            });

            if (!response.ok) throw new Error('API request failed');

            const data = await response.json();
            
            // Animate summary reveal
            setTimeout(() => {
                summary.textContent = data.summary || 'No summary generated';
                summary.classList.remove('empty-state');
            }, 500);

        } catch (error) {
            summary.innerHTML = `<strong>Error:</strong> ${error.message}<br><small>Check your API endpoint</small>`;
        } finally {
            clearInterval(progressInterval);
            progressFill.style.width = '100%';
            setTimeout(() => {
                progressContainer.style.display = 'none';
                progressFill.style.width = '0%';
                summarizeBtn.disabled = false;
                summarizeBtn.textContent = '✨ Summarize Text';
                outputSection.classList.remove('loading');
            }, 800);
        }
    }
});
