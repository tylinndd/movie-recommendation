form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevents the default form submission behavior
    const movieTitle = document.getElementById('movie-title').value;

    // Fetch recommendations from the backend
    const response = await fetch(`/recommend?title=${encodeURIComponent(movieTitle)}`);
    const recommendations = await response.json();

    // Display recommendations
    recommendationList.innerHTML = '';
    recommendations.forEach(movie => {
        const li = document.createElement('li');
        li.textContent = movie;
        recommendationList.appendChild(li);
    });
});