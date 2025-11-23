document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. NAVBAR SCROLL EFFECT ---
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('nav-black');
        } else {
            navbar.classList.remove('nav-black');
        }
    });

    // --- 2. SCROLL ARROWS LOGIC ---
    const rows = document.querySelectorAll('.row-container');
    rows.forEach(row => {
        const slider = row.querySelector('.movie-row');
        const leftBtn = row.querySelector('.left-btn');
        const rightBtn = row.querySelector('.right-btn');

        // Only add listeners if buttons exist (search results might not have them)
        if (leftBtn && rightBtn) {
            rightBtn.addEventListener('click', () => {
                slider.scrollBy({ left: 500, behavior: 'smooth' });
            });
            leftBtn.addEventListener('click', () => {
                slider.scrollBy({ left: -500, behavior: 'smooth' });
            });
        }
    });

    // --- 3. CLICK-TO-PLAY SYSTEM (Dynamic) ---
    document.body.addEventListener('click', function(e) {
        
        // Find the closest parent with class 'video-card'
        const card = e.target.closest('.video-card');
        
        // If a card was clicked AND it is not already playing
        if (card && !card.classList.contains('playing')) {
            const videoId = card.getAttribute('data-id');
            
            if (videoId) {
                // Mark as playing
                card.classList.add('playing');

                // Create the Iframe
                const iframe = document.createElement('iframe');
                
                // Parameters to make it look cleaner:
                // autoplay=1: Play immediately
                // modestbranding=1: Hide YouTube Logo
                // rel=0: Show related videos only from same channel
                // controls=1: Allow user to pause/volume
                // iv_load_policy=3: Hide annotations
                iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&modestbranding=1&rel=0&iv_load_policy=3&fs=1`;
                iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
                iframe.allowFullscreen = true;

                // Wipe the image and icon
                card.innerHTML = '';
                
                // Inject the video
                card.appendChild(iframe);
            }
        }
    });

});