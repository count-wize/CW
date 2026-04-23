(function () {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  function init() {
    document.querySelectorAll('.will-animate').forEach(function (el) {
      observer.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

(function () {
  function triggerGradientFlash(targetElement, callback) {
    var leftover = document.querySelector('.gradient-flash-circle');
    if (leftover) leftover.remove();
    var rect = targetElement.getBoundingClientRect();
    var circle = document.createElement('div');
    circle.classList.add('gradient-flash-circle');
    circle.style.cssText = 'position:fixed;border-radius:50%;pointer-events:none;z-index:10000;opacity:0;will-change:transform,opacity;' +
      'background:linear-gradient(90deg,#a3dcad 0%,#d2ffda 50%,#a3dcad 100%);' +
      'transition:transform 0.9s ease-in-out,opacity 0.4s ease;' +
      'width:100px;height:100px;' +
      'left:' + (rect.left + rect.width / 2) + 'px;' +
      'top:' + (rect.top + rect.height / 2) + 'px;' +
      'transform:translate(-50%,-50%) scale(0);';
    document.body.appendChild(circle);
    void circle.offsetWidth;
    requestAnimationFrame(function () {
      circle.style.transform = 'translate(-50%,-50%) scale(60)';
      circle.style.opacity = '1';
    });
    setTimeout(callback, 1100);
  }

  function init() {
    document.querySelectorAll('a[href="recovery-questionnaire.html"]').forEach(function (btn) {
      if (btn.id === 'start-recovery-button' || btn.id === 'start-recovery-finish') return;
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        triggerGradientFlash(btn, function () {
          window.location.href = 'recovery-questionnaire.html';
        });
      });
    });
  }

  window.addEventListener('pageshow', function () {
    var leftover = document.querySelector('.gradient-flash-circle');
    if (leftover) leftover.remove();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
