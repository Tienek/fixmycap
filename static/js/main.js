/**
 * FixMyCar AI — Frontend JavaScript
 * Handles navigation, mobile menu, alerts, and interactive repair sessions.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }

  // Dismissible Alert Messages
  const alertCloseBtns = document.querySelectorAll('.alert-close');
  alertCloseBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const alert = e.target.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 200);
      }
    });
  });

  // Screen Wake Lock API (Progressive Enhancement for Workshop use)
  let wakeLock = null;
  const requestWakeLock = async () => {
    if ('wakeLock' in navigator && document.querySelector('.session-container')) {
      try {
        wakeLock = await navigator.wakeLock.request('screen');
      } catch (err) {
        // WakeLock request can fail silently if battery saver is on
      }
    }
  };

  if (document.querySelector('.session-container')) {
    requestWakeLock();
    document.addEventListener('visibilitychange', () => {
      if (wakeLock !== null && document.visibilityState === 'visible') {
        requestWakeLock();
      }
    });
  }

  // Keyboard Navigation for Repair Session (Left/Right arrow keys)
  const prevBtn = document.getElementById('prev-step-btn');
  const nextBtn = document.getElementById('next-step-btn');

  if (prevBtn || nextBtn) {
    document.addEventListener('keydown', (e) => {
      // Ignore if user is currently typing inside textarea or input
      if (['input', 'textarea', 'select'].includes(document.activeElement.tagName.toLowerCase())) {
        return;
      }

      if (e.key === 'ArrowLeft' && prevBtn && !prevBtn.disabled) {
        prevBtn.click();
      } else if (e.key === 'ArrowRight' && nextBtn && !nextBtn.disabled) {
        nextBtn.click();
      }
    });
  }
});
