
document.addEventListener('DOMContentLoaded', function () {

    // =====================================
    // DOM ELEMENTS
    // =====================================

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

    // API endpoint
    // Works locally and after deployment on the same domain
    const API_URL = '/summarize';

    // Summary length labels
    const labels = ['Tiny', 'Short', 'Medium', 'Long', 'Full'];


    // =====================================
    // WORD COUNT
    // =====================================

    function updateWordCount() {

        const text = inputText.value.trim();

        const words = text
            ? text.split(/\s+/).filter(Boolean).length
            : 0;

        wordCount.textContent = `${words} words`;
    }

    inputText.addEventListener('input', updateWordCount);

    // Initialize word count
    updateWordCount();


    // =====================================
    // SUMMARY LENGTH SLIDER
    // =====================================

    summaryLength.addEventListener('input', function (e) {

        const value = parseInt(e.target.value, 10);

        sliderValue.textContent = labels[value - 1];

    });


    // =====================================
    // DARK MODE TOGGLE
    // =====================================

    themeToggle.addEventListener('click', function () {

        const isDark =
            document.body.getAttribute('data-theme') === 'dark';

        document.body.setAttribute(
            'data-theme',
            isDark ? 'light' : 'dark'
        );

        themeToggle.textContent = isDark ? '🌙' : '☀️';

    });


    // =====================================
    // SUMMARIZE BUTTON
    // =====================================

    summarizeBtn.addEventListener('click', summarize);


    // =====================================
    // SUMMARIZE FUNCTION
    // =====================================

    async function summarize() {

        const text = inputText.value.trim();

        const length = parseInt(summaryLength.value, 10);


        // Validate input
        if (!text) {

            alert('Please enter some text first!');

            inputText.focus();

            return;
        }

        if (text.length < 30) {

            alert('Please enter a longer text for summarization.');

            return;
        }


        // =====================================
        // LOADING UI
        // =====================================

        summarizeBtn.disabled = true;

        summarizeBtn.textContent = 'Summarizing...';

        progressContainer.style.display = 'block';

        outputSection.classList.add('loading');

        summary.textContent = 'Generating your summary...';

        summary.classList.remove('empty-state');


        // Simulated progress
        let progress = 0;

        const progressInterval = setInterval(() => {

            progress += Math.random() * 10;

            if (progress > 90) {
                progress = 90;
            }

            progressFill.style.width = progress + '%';

        }, 300);


        // =====================================
        // API REQUEST
        // =====================================

        try {

            const response = await fetch(API_URL, {

                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({

                    text: text,

                    length: length

                })

            });


            // STEP 1: Read API response
            const data = await response.json();


            // STEP 2: Check API errors
            if (!response.ok) {

                const errorMessage =
                    typeof data.detail === 'string'
                        ? data.detail
                        : data.detail
                            ? JSON.stringify(data.detail)
                            : data.error || `API Error: ${response.status}`;

                throw new Error(errorMessage);
            }


            // STEP 3: Validate summary
            if (!data.summary) {

                throw new Error('No summary was returned by the server.');

            }


            // STEP 4: Display generated summary
            setTimeout(() => {

                summary.textContent = data.summary;

                summary.classList.remove('empty-state');

            }, 500);


        } catch (error) {


            // =====================================
            // ERROR HANDLING
            // =====================================

            console.error('Summarization error:', error);

            summary.textContent =
                `Error: ${error.message}\nPlease check your API and try again.`;

            summary.classList.remove('empty-state');


        } finally {


            // =====================================
            // RESET LOADING UI
            // =====================================

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
