document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('searchForm');
    const input = document.getElementById('queryInput');
    const resultsContainer = document.getElementById('resultsContainer');
    const searchButton = document.getElementById('searchButton');
    const btnText = searchButton.querySelector('span');
    const btnLoader = searchButton.querySelector('.loader-spinner');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const query = input.value.trim();
        if (!query) return;

        // Set Loading State
        setLoading(true);
        resultsContainer.innerHTML = '';

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query, top_k: 5 })
            });

            if (!response.ok) {
                throw new Error(`API error! status: ${response.status}`);
            }

            const data = await response.json();
            renderResults(data.results);

        } catch (error) {
            console.error('Error fetching results:', error);
            resultsContainer.innerHTML = `
                <div class="error-message">
                    Failed to fetch results. Please make sure the backend is running and try again.
                </div>
            `;
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        input.disabled = isLoading;
        searchButton.disabled = isLoading;
        
        if (isLoading) {
            btnText.style.display = 'none';
            btnLoader.style.display = 'block';
        } else {
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
            // focus input again
            input.focus();
        }
    }

    function renderResults(results) {
        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    No matching reviews found for your query. Try rephrasing it.
                </div>
            `;
            return;
        }

        const html = results.map((result, index) => {
            const delay = index * 0.1; // Staggered animation
            return `
                <div class="card" style="animation-delay: ${delay}s">
                    <div class="card-header">
                        <div class="product-info">
                            <h3>Product ID: ${escapeHtml(result.product_id)}</h3>
                            <div class="meta">Review ID: ${escapeHtml(result.review_id)}</div>
                        </div>
                        <div class="score-and-rating" style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem;">
                            <div class="score-badge">${(result.similarity_score * 100).toFixed(1)}% Match</div>
                            <div class="stars" title="Rating: ${result.rating}/5">
                                ${generateStars(parseInt(result.rating) || 0)}
                            </div>
                        </div>
                    </div>
                    <div class="review-text">
                        "${escapeHtml(result.review_text)}"
                    </div>
                </div>
            `;
        }).join('');

        resultsContainer.innerHTML = html;
    }

    function generateStars(rating) {
        let starsHtml = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                starsHtml += '<span class="star filled">★</span>';
            } else {
                starsHtml += '<span class="star">★</span>';
            }
        }
        return starsHtml;
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return String(unsafe)
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
