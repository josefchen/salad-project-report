/* ── nav.js ── */
/* Navigation active-state logic + smooth scroll */

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-bar a');
    const sections = document.querySelectorAll('.section');

    // Smooth scroll for nav links
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            var hash = href.indexOf('#') !== -1 ? href.substring(href.indexOf('#') + 1) : null;
            if (hash) {
                var target = document.getElementById(hash);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                    history.replaceState(null, null, '#' + hash);
                }
            }
        });
    });

    // Active state on scroll
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var id = entry.target.id;
                navLinks.forEach(function(link) {
                    var href = link.getAttribute('href');
                    if (href.indexOf('#' + id) !== -1) {
                        link.style.color = 'var(--primary)';
                        link.style.borderColor = 'var(--primary)';
                    } else {
                        link.style.color = '';
                        link.style.borderColor = 'transparent';
                    }
                });
            }
        });
    }, { rootMargin: '-20% 0px -80% 0px' });

    sections.forEach(function(s) { observer.observe(s); });
});
