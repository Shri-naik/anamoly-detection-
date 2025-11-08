/**
 * EcoSence - Animation and Interactive Elements
 * Modern JavaScript for enhancing user experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and interactive elements
    initScrollAnimations();
    initParallaxEffects();
    initHoverEffects();
    
    // If there are charts on the page, initialize them
    if (document.querySelector('.eco-chart')) {
        initCharts();
    }
});

/**
 * Scroll-triggered animations for elements
 */
function initScrollAnimations() {
    // Get all elements that should animate on scroll
    const animatedElements = document.querySelectorAll('.slide-up, .scale-in');
    
    // Create an observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe each element
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Parallax scrolling effects
 */
function initParallaxEffects() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrollY * speed);
            element.style.backgroundPosition = `center ${yPos}px`;
        });
    });
}

/**
 * Enhanced hover effects for interactive elements
 */
function initHoverEffects() {
    // Cards with hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = 'var(--shadow-xl)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--shadow-md)';
        });
    });
    
    // Buttons with hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Scroll-triggered charts and data visualization
 * Uses Chart.js if available
 */
function initCharts() {
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js is not loaded. Data visualization will not work.');
        return;
    }
    
    // Initialize charts when they come into view
    const chartElements = document.querySelectorAll('.eco-chart');
    
    const chartObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chartElement = entry.target;
                const chartType = chartElement.dataset.chartType || 'bar';
                const chartData = JSON.parse(chartElement.dataset.chartData || '{}');
                
                new Chart(chartElement, {
                    type: chartType,
                    data: chartData,
                    options: {
                        responsive: true,
                        animation: {
                            duration: 2000,
                            easing: 'easeOutQuart'
                        }
                    }
                });
                
                // Unobserve after initializing to prevent re-initialization
                chartObserver.unobserve(chartElement);
            }
        });
    }, {
        threshold: 0.1
    });
    
    chartElements.forEach(chart => {
        chartObserver.observe(chart);
    });
}

/**
 * Smooth scrolling for navigation links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 100,
                behavior: 'smooth'
            });
        }
    });
});

/**
 * Mobile navigation toggle
 */
const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
if (mobileNavToggle) {
    mobileNavToggle.addEventListener('click', function() {
        const navMenu = document.querySelector('.nav-menu');
        navMenu.classList.toggle('active');
        this.classList.toggle('active');
    });
}