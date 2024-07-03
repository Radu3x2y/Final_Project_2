document.addEventListener('DOMContentLoaded', function () {
    const collapseLinks = document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');
    const collapsedLinks = document.querySelectorAll('.collapsed-link');

    // Restore collapse state from localStorage
    const isCollapseOpen = localStorage.getItem('isCollapseOpen') === 'true';
    const activeLinkHref = localStorage.getItem('activeLinkHref');

    collapseLinks.forEach(link => {
        const collapseTarget = document.querySelector(link.getAttribute('href'));
        if (isCollapseOpen && collapseTarget && collapseTarget.classList.contains('collapse')) {
            collapseTarget.classList.add('show');
            link.classList.add('focus-highlight');
            link.setAttribute('aria-expanded', 'true');
        }
    });

    collapsedLinks.forEach(link => {
        if (activeLinkHref && link.getAttribute('href') === activeLinkHref) {
            link.classList.add('active');
        }
    });

    collapseLinks.forEach(link => {
        link.addEventListener('click', function () {
            const collapseTarget = document.querySelector(this.getAttribute('href'));
            const isExpanded = collapseTarget.classList.contains('show');

            localStorage.setItem('isCollapseOpen', isExpanded ? 'false' : 'true');
            this.classList.toggle('focus-highlight', !isExpanded);
        });
    });

    collapsedLinks.forEach(link => {
        link.addEventListener('click', function () {
            collapsedLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
            localStorage.setItem('activeLinkHref', this.getAttribute('href'));
        });
    });
});
