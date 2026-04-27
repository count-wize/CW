(function() {
  var pixelInitialised = false;
  function initPixel() {
    if (pixelInitialised) return;
    pixelInitialised = true;
    if (typeof fbq === 'undefined') {
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
      document,'script','https://connect.facebook.net/en_US/fbevents.js');
    }
    fbq('init', '2353753348435760');
    fbq('track', 'PageView');
  }

  // For returning visitors: fires when Cookiebot loads and consent is already known
  window.addEventListener('CookiebotOnLoad', function() {
    if (window.Cookiebot && window.Cookiebot.consent && window.Cookiebot.consent.marketing) {
      initPixel();
    }
  });

  // For new visitors: fires when user accepts consent on banner
  window.addEventListener('CookiebotOnAccept', function() {
    if (window.Cookiebot && window.Cookiebot.consent && window.Cookiebot.consent.marketing) {
      initPixel();
    }
  });

  // On decline: delete the consent cookie so banner re-appears next session
  window.addEventListener('CookiebotOnDecline', function() {
    var host = window.location.hostname;
    var domain = host.indexOf('www.') === 0 ? host.slice(4) : host;
    document.cookie = 'CookieConsent=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'CookieConsent=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain + ';';
    document.cookie = 'CookieConsent=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + domain + ';';
  });
})();
