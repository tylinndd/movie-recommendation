const API_BASE = (window.API_BASE || '').replace(/\/$/, '');

function apiUrl(path) {
    const normalized = path.startsWith('/') ? path : `/${path}`;
    return `${API_BASE}${normalized}`;
}

// Authentication State
let currentUser = null;
let currentView = 'browse'; // browse, watchlist, watched

// DOM Elements
const authView = document.getElementById('auth-view');
const appView = document.getElementById('app-view');
const loginCard = document.getElementById('login-card');
const signupCard = document.getElementById('signup-card');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginError = document.getElementById('login-error');
const signupError = document.getElementById('signup-error');
const userMenu = document.getElementById('user-menu');
const userMenuBtn = document.getElementById('user-menu-btn');
const userDropdown = document.getElementById('user-dropdown');
const usernameDisplay = document.getElementById('username-display');

// Views
const browseSection = document.getElementById('browse-section');
const watchlistSection = document.getElementById('watchlist-section');
const watchedSection = document.getElementById('watched-section');

// Movie elements
const form = document.getElementById('movie-form');
const movieInput = document.getElementById('movie-title');
const recommendationList = document.getElementById('recommendation-list');
const recommendationsSection = document.getElementById('recommendations');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const errorText = document.getElementById('error-text');
const emptyState = document.getElementById('empty-state');
const searchTerm = document.getElementById('search-term');
const modal = document.getElementById('movie-modal');
const closeModalBtn = document.getElementById('close-modal');
const searchedMovieSection = document.getElementById('searched-movie-section');
const searchedMovieCard = document.getElementById('searched-movie-card');

// Initialize app
async function initApp() {
    await checkAuthStatus();
    setupEventListeners();
}

// Check if user is authenticated
async function checkAuthStatus() {
    try {
        const response = await fetch(apiUrl('/api/current_user'), {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            showAppView();
        } else {
            showAuthView();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        showAuthView();
    }
}

// Show authentication view
function showAuthView() {
    authView.classList.remove('hidden');
    appView.classList.add('hidden');
    userMenu.classList.add('hidden');
}

// Show main app view
function showAppView() {
    authView.classList.add('hidden');
    appView.classList.remove('hidden');
    userMenu.classList.remove('hidden');
    usernameDisplay.textContent = currentUser.username;
    showBrowseView();
}

// Setup event listeners
function setupEventListeners() {
    // Auth switches
    document.getElementById('show-signup').addEventListener('click', () => {
        loginCard.classList.add('hidden');
        signupCard.classList.remove('hidden');
        loginError.classList.add('hidden');
        signupError.classList.add('hidden');
    });

    document.getElementById('show-login').addEventListener('click', () => {
        signupCard.classList.add('hidden');
        loginCard.classList.remove('hidden');
        loginError.classList.add('hidden');
        signupError.classList.add('hidden');
    });

    // Auth forms
    loginForm.addEventListener('submit', handleLogin);
    signupForm.addEventListener('submit', handleSignup);

    // User menu
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        userDropdown.classList.remove('show');
    });

    document.getElementById('my-watchlist-btn').addEventListener('click', showWatchlistView);
    document.getElementById('my-watched-btn').addEventListener('click', showWatchedView);
    document.getElementById('browse-movies-btn').addEventListener('click', showBrowseView);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);

    // Movie search
    form.addEventListener('submit', handleMovieSearch);

    // Modal
    closeModalBtn.addEventListener('click', closeModal);
    modal.querySelector('.modal-overlay').addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });

    // Input animations
    movieInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });

    movieInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    loginError.classList.add('hidden');

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(apiUrl('/api/login'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            showAppView();
        } else {
            loginError.textContent = data.error || 'Login failed';
            loginError.classList.remove('hidden');
        }
    } catch (error) {
        loginError.textContent = 'Network error. Please try again.';
        loginError.classList.remove('hidden');
    }
}

// Handle signup
async function handleSignup(e) {
    e.preventDefault();
    signupError.classList.add('hidden');

    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    try {
        const response = await fetch(apiUrl('/api/signup'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            showAppView();
        } else {
            signupError.textContent = data.error || 'Signup failed';
            signupError.classList.remove('hidden');
        }
    } catch (error) {
        signupError.textContent = 'Network error. Please try again.';
        signupError.classList.remove('hidden');
    }
}

// Handle logout
async function handleLogout() {
    try {
        await fetch(apiUrl('/api/logout'), { 
            method: 'POST',
            credentials: 'include'
        });
        currentUser = null;
        showAuthView();
        // Reset forms
        loginForm.reset();
        signupForm.reset();
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// View management
function showBrowseView() {
    currentView = 'browse';
    browseSection.classList.remove('hidden');
    watchlistSection.classList.add('hidden');
    watchedSection.classList.add('hidden');
    userDropdown.classList.remove('show');
}

function showWatchlistView() {
    currentView = 'watchlist';
    browseSection.classList.add('hidden');
    watchlistSection.classList.remove('hidden');
    watchedSection.classList.add('hidden');
    userDropdown.classList.remove('show');
    loadWatchlist();
}

function showWatchedView() {
    currentView = 'watched';
    browseSection.classList.add('hidden');
    watchlistSection.classList.add('hidden');
    watchedSection.classList.remove('hidden');
    userDropdown.classList.remove('show');
    loadWatchedList();
}

// Load watchlist
async function loadWatchlist() {
    try {
        const response = await fetch(apiUrl('/api/watchlist'), {
            credentials: 'include'
        });
        const data = await response.json();

        const watchlistContent = document.getElementById('watchlist-content');
        const watchlistEmpty = document.getElementById('watchlist-empty');
        const watchlistCount = document.getElementById('watchlist-count');

        watchlistCount.textContent = data.length;

        if (data.length === 0) {
            watchlistContent.innerHTML = '';
            watchlistEmpty.classList.remove('hidden');
        } else {
            watchlistEmpty.classList.add('hidden');
            watchlistContent.innerHTML = '';
            
            data.forEach((item, index) => {
                const movie = item.movie_data;
                const card = createMovieCard(movie, index, 'watchlist', item.id);
                watchlistContent.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Failed to load watchlist:', error);
    }
}

// Load watched list
async function loadWatchedList() {
    try {
        const response = await fetch(apiUrl('/api/watched'), {
            credentials: 'include'
        });
        const data = await response.json();

        const watchedContent = document.getElementById('watched-content');
        const watchedEmpty = document.getElementById('watched-empty');
        const watchedCount = document.getElementById('watched-count');

        watchedCount.textContent = data.length;

        if (data.length === 0) {
            watchedContent.innerHTML = '';
            watchedEmpty.classList.remove('hidden');
        } else {
            watchedEmpty.classList.add('hidden');
            watchedContent.innerHTML = '';
            
            data.forEach((item, index) => {
                const movie = item.movie_data;
                const card = createMovieCard(movie, index, 'watched', item.id);
                watchedContent.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Failed to load watched list:', error);
    }
}

// Handle movie search
async function handleMovieSearch(e) {
    e.preventDefault();
    const movieTitle = movieInput.value.trim();

    recommendationsSection.classList.add('hidden');
    searchedMovieSection.classList.add('hidden');
    errorElement.classList.add('hidden');
    emptyState.classList.add('hidden');
    loadingElement.classList.remove('hidden');

    try {
        const response = await fetch(apiUrl('/recommend?title=' + encodeURIComponent(movieTitle)));
        const data = await response.json();

        loadingElement.classList.add('hidden');

        if (data.error || !data.recommendations || data.recommendations.length === 0) {
            errorElement.classList.remove('hidden');
            errorText.textContent = `Sorry, we couldn't find "${movieTitle}". Please try another movie title.`;
            return;
        }

        // Display searched movie
        const searchedMovie = data.searched_movie;
        searchTerm.textContent = searchedMovie.title;
        
        searchedMovieCard.innerHTML = `
            <div class="searched-movie-info-full">
                <h3 class="searched-movie-title">${searchedMovie.title}</h3>
                ${searchedMovie.tagline ? `<p class="searched-movie-tagline">"${searchedMovie.tagline}"</p>` : ''}
                <div class="searched-movie-meta">
                    <span class="meta-badge">
                        <i class="fas fa-star"></i> ${searchedMovie.vote_average}/10
                    </span>
                    <span class="meta-badge">
                        <i class="fas fa-calendar"></i> ${searchedMovie.release_date}
                    </span>
                    ${searchedMovie.runtime ? `<span class="meta-badge"><i class="fas fa-clock"></i> ${searchedMovie.runtime} min</span>` : ''}
                </div>
                <p class="searched-movie-overview">${searchedMovie.overview}</p>
                <div class="searched-movie-genres">
                    ${searchedMovie.genres ? (() => {
                        try {
                            const genresArray = JSON.parse(searchedMovie.genres.replace(/'/g, '"'));
                            return genresArray.map(g => `<span class="genre-badge">${g.name}</span>`).join('');
                        } catch(e) {
                            return '';
                        }
                    })() : ''}
                </div>
                <div class="movie-actions">
                    ${createActionButtons(searchedMovie)}
                </div>
            </div>
        `;
        
        searchedMovieSection.classList.remove('hidden');
        
        // Add event listeners to searched movie action buttons
        setupActionButtons(searchedMovieCard, searchedMovie);
        
        // Display recommendations
        recommendationList.innerHTML = '';
        data.recommendations.forEach((movie, index) => {
            const card = createMovieCard(movie, index, 'browse');
            recommendationList.appendChild(card);
        });

        recommendationsSection.classList.remove('hidden');
        
        setTimeout(() => {
            searchedMovieSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        loadingElement.classList.add('hidden');
        errorElement.classList.remove('hidden');
        errorText.textContent = 'Oops! Something went wrong. Please try again.';
        console.error(error);
    }
}

// Create movie card
function createMovieCard(movie, index, listType, itemId = null) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    card.innerHTML = `
        <div class="movie-card-content-full">
            <h3 class="movie-title">${movie.title}</h3>
            <div class="movie-rating">
                <i class="fas fa-star"></i>
                <span>${movie.vote_average}/10</span>
            </div>
            <p class="movie-year">${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}</p>
            ${listType !== 'browse' ? `
                <div class="movie-actions">
                    ${listType === 'watchlist' ? `
                        <button class="action-btn watched-btn" data-action="watched">
                            <i class="fas fa-check"></i> Mark as Watched
                        </button>
                        <button class="action-btn remove-btn" data-action="remove-watchlist">
                            <i class="fas fa-times"></i> Remove
                        </button>
                    ` : `
                        <button class="action-btn remove-btn" data-action="remove-watched">
                            <i class="fas fa-times"></i> Remove
                        </button>
                    `}
                </div>
            ` : ''}
        </div>
    `;
    
    // Click to open modal (only on the title/rating area, not on buttons)
    const contentArea = card.querySelector('.movie-card-content-full');
    const titleArea = card.querySelector('.movie-title');
    const ratingArea = card.querySelector('.movie-rating');
    const yearArea = card.querySelector('.movie-year');
    
    [titleArea, ratingArea, yearArea].forEach(area => {
        area.addEventListener('click', (e) => {
            e.stopPropagation();
            openModal(movie);
        });
        area.style.cursor = 'pointer';
    });
    
    // Setup action buttons
    if (listType !== 'browse') {
        setupListActionButtons(card, movie, itemId, listType);
    } else {
        // Add action buttons for browse view
        const cardContent = card.querySelector('.movie-card-content-full');
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'movie-actions';
        actionsDiv.innerHTML = createActionButtons(movie);
        cardContent.appendChild(actionsDiv);
        setupActionButtons(card, movie);
    }
    
    return card;
}

// Create action buttons HTML
function createActionButtons(movie) {
    return `
        <button class="action-btn watchlist-btn" data-action="watchlist">
            <i class="fas fa-bookmark"></i> Watchlist
        </button>
        <button class="action-btn watched-btn" data-action="watched">
            <i class="fas fa-check"></i> Watched
        </button>
    `;
}

// Setup action buttons for browse/search results
function setupActionButtons(container, movie) {
    const watchlistBtn = container.querySelector('[data-action="watchlist"]');
    const watchedBtn = container.querySelector('[data-action="watched"]');

    if (watchlistBtn) {
        watchlistBtn.addEventListener('click', async (e) => {
            e.stopPropagation();
            await addToWatchlist(movie, watchlistBtn);
        });
    }

    if (watchedBtn) {
        watchedBtn.addEventListener('click', async (e) => {
            e.stopPropagation();
            await addToWatched(movie, watchedBtn);
        });
    }
}

// Setup action buttons for list views
function setupListActionButtons(card, movie, itemId, listType) {
    const buttons = card.querySelectorAll('.action-btn');
    
    buttons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const action = btn.dataset.action;
            
            if (action === 'watched') {
                await addToWatched(movie);
                loadWatchlist();
            } else if (action === 'remove-watchlist') {
                await removeFromWatchlist(itemId);
                loadWatchlist();
            } else if (action === 'remove-watched') {
                await removeFromWatched(itemId);
                loadWatchedList();
            }
        });
    });
}

// Add to watchlist
async function addToWatchlist(movie, button = null) {
    try {
        const response = await fetch(apiUrl('/api/watchlist'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                movie_title: movie.title,
                movie_data: movie
            })
        });

        const data = await response.json();

        if (response.ok) {
            if (button) {
                button.innerHTML = '<i class="fas fa-check"></i> Added!';
                button.classList.add('added');
                button.disabled = true;
            }
            showNotification('Added to watchlist!', 'success');
        } else {
            showNotification(data.error || 'Failed to add to watchlist', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// Add to watched list
async function addToWatched(movie, button = null) {
    try {
        const response = await fetch(apiUrl('/api/watched'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                movie_title: movie.title,
                movie_data: movie
            })
        });

        const data = await response.json();

        if (response.ok) {
            if (button) {
                button.innerHTML = '<i class="fas fa-check"></i> Watched!';
                button.classList.add('added');
                button.disabled = true;
            }
            showNotification('Added to watched list!', 'success');
        } else {
            showNotification(data.error || 'Failed to add to watched list', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// Remove from watchlist
async function removeFromWatchlist(itemId) {
    try {
        const response = await fetch(apiUrl(`/api/watchlist/${itemId}`), {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            showNotification('Removed from watchlist', 'success');
        }
    } catch (error) {
        showNotification('Failed to remove', 'error');
    }
}

// Remove from watched list
async function removeFromWatched(itemId) {
    try {
        const response = await fetch(apiUrl(`/api/watched/${itemId}`), {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            showNotification('Removed from watched list', 'success');
        }
    } catch (error) {
        showNotification('Failed to remove', 'error');
    }
}

// Show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#e74c3c'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Modal functions
function openModal(movie) {
    document.getElementById('modal-title').textContent = movie.title;
    document.getElementById('modal-tagline').textContent = movie.tagline || '';
    document.getElementById('modal-release-date').textContent = movie.release_date;
    document.getElementById('modal-runtime').textContent = movie.runtime ? `${movie.runtime} min` : 'N/A';
    document.getElementById('modal-rating').textContent = movie.vote_average ? `${movie.vote_average}/10` : 'N/A';
    document.getElementById('modal-description').textContent = movie.overview;
    
    // Parse and display genres
    const genresContainer = document.getElementById('modal-genres');
    genresContainer.innerHTML = '';
    if (movie.genres) {
        try {
            const genresArray = JSON.parse(movie.genres.replace(/'/g, '"'));
            genresArray.forEach(genre => {
                const genreTag = document.createElement('span');
                genreTag.className = 'genre-tag';
                genreTag.textContent = genre.name;
                genresContainer.appendChild(genreTag);
            });
        } catch (e) {
            genresContainer.innerHTML = `<span class="genre-tag">${movie.genres}</span>`;
        }
    }
    
    // Add action buttons to modal
    const modalActions = document.getElementById('modal-actions');
    modalActions.innerHTML = createActionButtons(movie);
    setupActionButtons(modalActions, movie);
    
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize app on load
initApp();

