// Enhanced gaming website functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Scroll indicator functionality
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            window.scrollTo({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        });

        // Hide scroll indicator when near bottom
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY + window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            
            if (scrollPosition >= documentHeight - 100) {
                scrollIndicator.style.opacity = '0';
            } else {
                scrollIndicator.style.opacity = '1';
            }
        });
    }

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--neon-red)';
                    input.style.boxShadow = '0 0 10px rgba(255, 0, 85, 0.3)';
                } else {
                    input.style.borderColor = 'var(--neon-green)';
                    input.style.boxShadow = '0 0 10px rgba(0, 255, 136, 0.3)';
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Show error message
                showNotification('Please fill in all required fields!', 'error');
            }
        });
    });

    // Password confirmation validation
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const passwordInput = document.querySelector('input[name="password"]');
    
    if (confirmPasswordInput && passwordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            if (this.value !== passwordInput.value) {
                this.style.borderColor = 'var(--neon-red)';
                this.style.boxShadow = '0 0 10px rgba(255, 0, 85, 0.3)';
            } else {
                this.style.borderColor = 'var(--neon-green)';
                this.style.boxShadow = '0 0 10px rgba(0, 255, 136, 0.3)';
            }
        });
    }

    // Dynamic typing effect for welcome message
    const welcomeTitle = document.querySelector('.welcome-title');
    if (welcomeTitle) {
        const text = welcomeTitle.textContent;
        welcomeTitle.textContent = '';
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                welcomeTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        setTimeout(typeWriter, 500);
    }

    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        }
    });

    // Simple button feedback
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 200);
        });
    });

    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `flash-message flash-${type}`;
        notification.innerHTML = `
            <i class="fas fa-info-circle"></i>
            ${message}
            <button class="flash-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        const container = document.querySelector('.flash-messages') || createNotificationContainer();
        container.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    function createNotificationContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }

    // Dark mode toggle (future enhancement)
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('light-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('light-mode') ? 'false' : 'true');
        });
    }

    // Initialize dark mode from localStorage
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'false') {
        document.body.classList.add('light-mode');
    }

    // Simple hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('button, .social-btn, .nav-link, .cta-btn');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.opacity = '0.8';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.opacity = '1';
        });
    });

    // Profile dropdown functionality
    const profileDropdownBtn = document.getElementById('profileDropdownBtn');
    const profileDropdownMenu = document.getElementById('profileDropdownMenu');
    
    if (profileDropdownBtn && profileDropdownMenu) {
        profileDropdownBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            profileDropdownMenu.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileDropdownBtn.contains(e.target) && !profileDropdownMenu.contains(e.target)) {
                profileDropdownMenu.classList.remove('show');
            }
        });
        
        // Close dropdown on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                profileDropdownMenu.classList.remove('show');
            }
        });
    }

    // Console welcome message
    console.log(`
    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗███╗   ███╗ █████╗ ███╗   ██╗
    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝████╗ ████║██╔══██╗████╗  ██║
    ███████║██║   ██║██╔██╗ ██║   ██║   ███████╗██╔████╔██║███████║██╔██╗ ██║
    ██╔══██║██║   ██║██║╚██╗██║   ██║   ╚════██║██║╚██╔╝██║██╔══██║██║╚██╗██║
    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████║██║ ╚═╝ ██║██║  ██║██║ ╚████║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
    
    Welcome to Huntsman Space! 🎮
    `);
});

// Simple styles for better UX
const style = document.createElement('style');
style.textContent = `
    * {
        cursor: default;
    }
    
    a, button, input, textarea {
        cursor: pointer;
    }
`;
document.head.appendChild(style);