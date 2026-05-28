/**
 * script.js - Student Feedback System (Polished)
 * Clean vanilla JS for UI interactions, animations, and form validation
 */

document.addEventListener('DOMContentLoaded', function () {

    // 1. Page Load Animation Class
    document.body.classList.add('page-loaded');



    // 3. Smooth scroll for anchor links (handling /#features and #features path configurations)
    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;
            const targetId = href.substring(hashIndex);
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Only intercept and smooth scroll if the target element actually exists on the current page
                e.preventDefault();

                if (targetId === '#features') {
                    // Center the features section vertically in the viewport natively
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    // Standard top-aligned scroll with navbar offset
                    const navbarEl = document.getElementById('main-navbar');
                    const offset = navbarEl ? navbarEl.offsetHeight : 0;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const targetScrollPosition = elementPosition + window.pageYOffset - offset;

                    window.scrollTo({
                        top: targetScrollPosition,
                        behavior: 'smooth'
                    });
                }

                // Update URL hash without jumping
                history.pushState(null, null, targetId);
            }
        });
    });

    // Center #features on page load if hash matches
    if (window.location.hash === '#features') {
        const targetElement = document.getElementById('features');
        if (targetElement) {
            setTimeout(() => {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        }
    }

    // 4. Scroll Reveal Animations (Intersection Observer)
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.05
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply observer to reveal elements
    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });

    // 4. Auto-dismiss Flash Messages with smooth SaaS collapsing transition
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('alert-dismissing');
            alert.classList.remove('show');
            setTimeout(() => {
                alert.remove();
            }, 400); // Wait for the 0.4s CSS transition to complete
        }, 4000); // Dismiss after 4 seconds
    });



    // 6. Form Submit Button Loading State
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            // Handle custom confirm dialogs safely
            if (form.classList.contains('db-confirm-form')) {
                const msg = form.getAttribute('data-confirm');
                if (msg && !confirm(msg)) {
                    e.preventDefault();
                    return; // Stop processing immediately
                }
            }

            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Prevent multiple submissions
                if (submitBtn.classList.contains('btn-loading')) {
                    return false;
                }

                const originalText = submitBtn.innerHTML;

                if (form.id !== 'login-form' && form.id !== 'feedbackForm' && form.id !== 'admin-password-change-form') {
                    submitBtn.classList.add('btn-loading');
                    if (submitBtn.classList.contains('db-btn-delete') || submitBtn.classList.contains('db-btn-icon-only')) {
                        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="width: 1.1rem; height: 1.1rem; border-width: 0.15em;"></span>`;
                    } else {
                        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing..`;
                    }
                }

                // Optional: restore button if form is invalid (handled by browser natively usually, but good practice)
                setTimeout(() => {
                    if (!form.checkValidity()) {
                        submitBtn.classList.remove('btn-loading');
                        submitBtn.innerHTML = originalText;
                    }
                }, 100);
            }
        });
    });

    // 7. Character Counter for Textareas (Feedback Form)
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const wrapper = document.createElement('div');
        wrapper.className = 'text-end mt-1';

        const counter = document.createElement('small');
        counter.className = 'text-muted fw-medium';
        counter.textContent = `${textarea.value.length} / ${maxLength}`;

        wrapper.appendChild(counter);
        textarea.parentNode.insertBefore(wrapper, textarea.nextSibling);

        textarea.addEventListener('input', function () {
            const currentLength = this.value.length;
            counter.textContent = `${currentLength} / ${maxLength}`;

            if (currentLength >= maxLength * 0.9) {
                counter.classList.replace('text-muted', 'text-warning');
            } else {
                counter.classList.replace('text-warning', 'text-muted');
                counter.classList.replace('text-danger', 'text-muted');
            }
            if (currentLength == maxLength) {
                counter.classList.replace('text-warning', 'text-danger');
            }
        });
    });

    // 8. Shared Button Ripple Effect (Hero & CTA)
    const interactiveBtns = document.querySelectorAll('.hero-section .btn-ai-primary, .btn-about-cta');
    interactiveBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            // Respect prefers-reduced-motion
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

            // Create ripple element
            const ripple = document.createElement('span');
            ripple.className = 'btn-ripple';

            // Calculate size (ensure it covers the whole button)
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);

            // Calculate exact click coordinates relative to button
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            // Apply styles
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            // Auto-remove ripple element after animation ends
            ripple.addEventListener('animationend', () => {
                ripple.remove();
            });
        });
    });

    // 9. Back-button / bfcache Restore Cleanup
    window.addEventListener('pageshow', function (event) {
        // If the page was loaded from the back/forward cache
        if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
            // Remove any leftover ripple elements
            document.querySelectorAll('.btn-ripple').forEach(ripple => {
                ripple.remove();
            });

            // Ensure interactive buttons are in their base state
            const buttons = document.querySelectorAll('.hero-section .btn-ai-primary, .btn-about-cta');
            buttons.forEach(btn => {
                // Reset any potential inline styles added by JS
                btn.style.transform = '';
                // The CSS :active state will handle itself once the click is done
            });
        }
    });

    // 10. Login Modal Logic (Premium Popup)
    const loginModal = document.getElementById('login-modal-overlay');
    const openLoginBtn = document.getElementById('open-login-modal');
    const closeLoginBtn = document.getElementById('close-login-modal');
    const loginForm = document.getElementById('login-form');
    const passwordInput = document.getElementById('login-password');
    const togglePasswordBtn = document.getElementById('toggle-password');
    const errorMsg = document.getElementById('login-error-message');
    const submitBtn = document.getElementById('login-submit-btn');

    if (loginModal && openLoginBtn) {
        // State flag
        let isLoginSubmitting = false;

        // Helper to reset button state
        const resetLoginBtn = () => {
            isLoginSubmitting = false;
            submitBtn.disabled = false;
            submitBtn.removeAttribute('disabled');
            submitBtn.classList.remove('disabled');
        };

        // Open Modal
        openLoginBtn.addEventListener('click', () => {
            loginModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scroll
            resetLoginBtn(); // Ensure button is reset when opened
        });

        // Close Modal Functions
        const closeModal = () => {
            loginModal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scroll
            errorMsg.style.display = 'none'; // Hide errors on close
            loginForm.reset(); // Clear form
            resetLoginBtn(); // Reset button
        };

        closeLoginBtn.addEventListener('click', closeModal);

        loginModal.addEventListener('click', (e) => {
            if (e.target === loginModal) closeModal();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && loginModal.classList.contains('active')) closeModal();
        });

        // Password Toggle
        if (togglePasswordBtn) {
            togglePasswordBtn.addEventListener('click', () => {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                const wrapper = togglePasswordBtn.querySelector('.password-toggle-icon-wrapper');
                const isPassword = type === 'password';
                if (wrapper) {
                    wrapper.innerHTML = `<i class="fa-regular ${isPassword ? 'fa-eye' : 'fa-eye-slash'} icon-sm"></i>`;
                }
            });
        }

        // Clear error on typing
        const loginInputs = loginForm.querySelectorAll('input');
        loginInputs.forEach(input => {
            input.addEventListener('input', () => {
                errorMsg.style.display = 'none';
                resetLoginBtn();
            });
        });

        // Login Form Submission Handling (Connected to Backend)
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault(); // Prevent page reload

                if (isLoginSubmitting) return;

                // Reset UI state
                isLoginSubmitting = true;
                errorMsg.style.display = 'none';

                submitBtn.disabled = true;

                const formData = new FormData(loginForm);
                const payload = {
                    user_id: formData.get('user_id'),
                    password: formData.get('password')
                };

                try {
                    const response = await fetch('/admin/login', {
                        method: 'POST',
                        body: JSON.stringify(payload),
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest',
                            'Accept': 'application/json'
                        }
                    });

                    const data = await response.json();

                    if (data.success) {
                        // Success: Redirect to dashboard
                        window.location.href = data.redirect;
                    } else {
                        // Error: Show message inside modal
                        errorMsg.querySelector('span').textContent = data.message || 'Invalid User ID or password.';
                        errorMsg.style.display = 'flex';
                        resetLoginBtn();
                    }
                } catch (error) {
                    console.error('Login Error:', error);
                    errorMsg.querySelector('span').textContent = 'A system error occurred. Please try again.';
                    errorMsg.style.display = 'flex';
                    resetLoginBtn();
                }
            });
        }
    }

    // 11. Navbar Scroll Effect (Premium SaaS Style)
    const navbarEl = document.getElementById('main-navbar');
    if (navbarEl) {
        const toggleNavbarScroll = () => {
            if (window.scrollY > 10) {
                navbarEl.classList.add('scrolled');
            } else {
                navbarEl.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', toggleNavbarScroll);
        toggleNavbarScroll(); // Initial check on load
    }

    // 11.5 Auto-close mobile navbar on link click
    const navbarCollapse = document.getElementById('navbarNav');
    if (navbarCollapse) {
        const toggler = document.querySelector('.navbar-toggler');
        const menuLinks = navbarCollapse.querySelectorAll('.nav-link, .btn-pill-login, a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show') && toggler) {
                    toggler.click();
                }
            });
        });
    }

    // 12. Automatic Uppercase & Character Validation for User ID and Subject Code Inputs
    const uppercaseSelectors = [
        'input[name="user_id"]',
        'input[name="username"]',
        'input[name="teacher_employee_id"]',
        'input[name="subject_code"]',
        '#login-username',
        '#admin_username'
    ];

    document.addEventListener('input', function (e) {
        if (e.target && e.target.matches) {
            const isMatch = uppercaseSelectors.some(selector => e.target.matches(selector));
            if (isMatch) {
                const start = e.target.selectionStart;
                const originalValue = e.target.value;

                if (e.target.matches('input[name="subject_code"]')) {
                    // Subject Code Format: 2 Letters, single space, 3-4 digits
                    const formatVal = function (val) {
                        if (!val) return '';
                        let result = '';
                        for (let i = 0; i < val.length; i++) {
                            const char = val[i].toUpperCase();
                            if (result.length < 2) {
                                if (/[A-Z]/.test(char)) {
                                    result += char;
                                }
                            } else if (result.length === 2) {
                                if (char === ' ' || char === '-') {
                                    result += ' ';
                                } else if (/[0-9]/.test(char)) {
                                    result += ' ' + char;
                                }
                            } else {
                                if (result.length < 7 && /[0-9]/.test(char)) {
                                    result += char;
                                }
                            }
                        }
                        return result;
                    };

                    const finalValue = formatVal(originalValue);
                    const prefixBeforeCursor = originalValue.slice(0, start);
                    const formattedPrefix = formatVal(prefixBeforeCursor);

                    e.target.value = finalValue;
                    const newCursorPos = formattedPrefix.length;
                    e.target.setSelectionRange(newCursorPos, newCursorPos);
                } else {
                    // Username/User ID Format: AAA123 (Exactly 3 uppercase letters, next 3 digits, max length 6)
                    const formatUser = function (val) {
                        if (!val) return '';
                        let result = '';
                        for (let i = 0; i < val.length; i++) {
                            const char = val[i].toUpperCase();
                            if (result.length < 6) {
                                if (result.length < 3) {
                                    if (/[A-Z]/.test(char)) {
                                        result += char;
                                    }
                                } else {
                                    if (/[0-9]/.test(char)) {
                                        result += char;
                                    }
                                }
                            }
                        }
                        return result;
                    };

                    const finalValue = formatUser(originalValue);
                    const prefixBeforeCursor = originalValue.slice(0, start);
                    const formattedPrefix = formatUser(prefixBeforeCursor);

                    e.target.value = finalValue;
                    const newCursorPos = formattedPrefix.length;
                    e.target.setSelectionRange(newCursorPos, newCursorPos);
                }
            }
        }
    });


});

