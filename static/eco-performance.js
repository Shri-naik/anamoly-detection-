/**
 * EcoSense Performance Optimization Module
 * Handles lazy loading, image optimization, and performance enhancements
 */

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    // Lazy load images with data-src attribute
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
    
    // Defer non-critical CSS
    const deferredStyles = document.querySelectorAll('link[rel="stylesheet"][data-defer]');
    deferredStyles.forEach(styleSheet => {
        styleSheet.setAttribute('rel', 'stylesheet');
        styleSheet.removeAttribute('data-defer');
    });
});

// Optimize animations for performance
const optimizeAnimations = () => {
    // Check if device is low-end based on memory and CPU cores
    const isLowEndDevice = () => {
        // Check for memory (if available)
        if (navigator.deviceMemory && navigator.deviceMemory < 4) {
            return true;
        }
        
        // Check for hardware concurrency (CPU cores)
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            return true;
        }
        
        return false;
    };
    
    // Reduce animations on low-end devices
    if (isLowEndDevice()) {
        document.documentElement.classList.add('reduced-motion');
        
        // Simplify animations
        const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .slide-in-right');
        animatedElements.forEach(el => {
            el.style.transitionDuration = '0.2s';
            el.style.animationDuration = '0.2s';
        });
    }
};

// Optimize image display
const optimizeImages = () => {
    const images = document.querySelectorAll('img:not([data-src])');
    
    images.forEach(img => {
        // Add loading="lazy" attribute for native lazy loading
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }
        
        // Add decoding="async" to allow asynchronous image decoding
        if (!img.hasAttribute('decoding')) {
            img.setAttribute('decoding', 'async');
        }
    });
};

// Optimize resource hints
const addResourceHints = () => {
    // Add preconnect for Google Fonts
    if (!document.querySelector('link[rel="preconnect"][href="https://fonts.googleapis.com"]')) {
        const preconnectGoogle = document.createElement('link');
        preconnectGoogle.rel = 'preconnect';
        preconnectGoogle.href = 'https://fonts.googleapis.com';
        document.head.appendChild(preconnectGoogle);
        
        const preconnectGstatic = document.createElement('link');
        preconnectGstatic.rel = 'preconnect';
        preconnectGstatic.href = 'https://fonts.gstatic.com';
        preconnectGstatic.setAttribute('crossorigin', '');
        document.head.appendChild(preconnectGstatic);
    }
};

// Initialize performance optimizations
window.addEventListener('load', () => {
    optimizeAnimations();
    optimizeImages();
    addResourceHints();
    
    // Mark when the page is fully loaded and interactive
    performance.mark('fully-loaded');
});

// Optimize event listeners to prevent performance issues
const optimizeEventListeners = () => {
    // Use passive event listeners for touch and wheel events
    const passiveEvents = ['touchstart', 'touchmove', 'wheel'];
    
    passiveEvents.forEach(eventName => {
        window.addEventListener(eventName, (e) => {}, { passive: true });
    });
};

// Initialize optimizations
document.addEventListener('DOMContentLoaded', () => {
    optimizeEventListeners();
});