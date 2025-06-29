// Copy code functionality
function copyCode() {
    const codeElement = document.getElementById('install-code');
    const textArea = document.createElement('textarea');
    textArea.value = codeElement.textContent;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    
    // Show feedback
    const copyBtn = document.querySelector('.copy-btn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = 'Copied!';
    copyBtn.style.background = '#95e1d3';
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = '#4ecdc4';
    }, 2000);
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    const links = document.querySelectorAll('a[href^="#"]');
    
    for (const link of links) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    }
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all feature cards and sections
    const animatedElements = document.querySelectorAll('.feature-card, .download-card, .control-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Tetris piece animation
    animateTetrisPieces();
});

// Animate the Tetris pieces in the preview
function animateTetrisPieces() {
    const pieces = document.querySelectorAll('.tetris-piece');
    
    pieces.forEach((piece, index) => {
        // Add a subtle glow animation
        piece.style.animation = `glow 2s ease-in-out infinite alternate`;
        piece.style.animationDelay = `${index * 0.5}s`;
    });
    
    // Add CSS for glow animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes glow {
            from {
                box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2);
            }
            to {
                box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.4);
            }
        }
    `;
    document.head.appendChild(style);
}

// Add keyboard navigation for accessibility
document.addEventListener('keydown', function(e) {
    // Allow keyboard navigation of buttons
    if (e.key === 'Enter' || e.key === ' ') {
        const focusedElement = document.activeElement;
        if (focusedElement.classList.contains('btn')) {
            e.preventDefault();
            focusedElement.click();
        }
    }
});

// Add loading animation for external links
document.addEventListener('DOMContentLoaded', function() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    
    externalLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Opening...';
            this.style.opacity = '0.7';
            
            // Reset after a short delay
            setTimeout(() => {
                this.textContent = originalText;
                this.style.opacity = '1';
            }, 1000);
        });
    });
});

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        // Easter egg activated!
        showEasterEgg();
        konamiCode = [];
    }
});

function showEasterEgg() {
    // Create a fun animation
    const title = document.querySelector('.title');
    const originalText = title.textContent;
    
    title.textContent = '🎮 TETRIS MASTER! 🎮';
    title.style.animation = 'none';
    title.style.background = 'linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3)';
    title.style.backgroundSize = '400% 400%';
    title.style.animation = 'gradient 0.5s ease infinite, bounce 0.5s ease infinite';
    
    // Add bounce animation
    const bounceStyle = document.createElement('style');
    bounceStyle.textContent = `
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-20px); }
            60% { transform: translateY(-10px); }
        }
    `;
    document.head.appendChild(bounceStyle);
    
    // Reset after 3 seconds
    setTimeout(() => {
        title.textContent = originalText;
        title.style.animation = 'gradient 3s ease infinite';
        document.head.removeChild(bounceStyle);
    }, 3000);
}
