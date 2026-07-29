// main.js – global interactions

// VanillaTilt on all .tilt-card elements
document.addEventListener('DOMContentLoaded', () => {
  if (typeof VanillaTilt !== 'undefined') {
    VanillaTilt.init(document.querySelectorAll('[data-tilt]'), {
      max: 10, speed: 400, glare: true, 'max-glare': 0.15,
      perspective: 800, scale: 1.03,
    });
  }

  // Animate stat bars on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.bar-fill, .rating-fill').forEach(bar => {
          const w = bar.style.width;
          bar.style.width = '0';
          requestAnimationFrame(() => { bar.style.width = w; });
        });
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.stat-section, .player-card').forEach(el => observer.observe(el));

  // Fade-in cards on load
  document.querySelectorAll('.match-card, .scorer-card, .group-card, .player-card, .viz-card')
    .forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity .4s ease ${i * 0.05}s, transform .4s ease ${i * 0.05}s`;
      setTimeout(() => { el.style.opacity = '1'; el.style.transform = 'translateY(0)'; }, 80 + i * 50);
    });
});
