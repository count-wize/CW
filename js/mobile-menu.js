/**
 * Mobile Menu Scroll Lock
 * Prevents body scroll when mobile menu is open.
 * Works with all nav button selector variants across the site.
 */
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    // Support all button selector variants used across the site
    var menuButton = document.querySelector('.w-nav-button');
    if (!menuButton) return;

    var disableScroll = function() {
      document.body.style.overflow = 'hidden';
      document.documentElement.style.overflow = 'hidden';
    };

    var enableScroll = function() {
      document.body.style.overflow = '';
      document.documentElement.style.overflow = '';
    };

    var toggleScroll = function() {
      var isOpen = menuButton.classList.contains('w--open');
      if (isOpen) {
        disableScroll();
      } else {
        enableScroll();
      }
      // Update aria-expanded state for accessibility
      menuButton.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    };

    menuButton.addEventListener('click', function() {
      // Small delay to allow Webflow to add/remove the w--open class
      setTimeout(toggleScroll, 50);
    });

    // Also handle escape key to close menu
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && menuButton.classList.contains('w--open')) {
        menuButton.click();
      }
    });
  });
})();
