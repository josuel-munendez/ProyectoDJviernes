(function () {
  'use strict';

  var SPA = {
    contentEl: null,
    messagesEl: null,
    isNavigating: false
  };

  var authPaths = ['/login', '/logout', '/registrar', '/register'];

  function isAuthUrl(pathname) {
    return authPaths.some(function (p) {
      return pathname === p || pathname.indexOf(p + '/') === 0;
    });
  }

  function getUrl() {
    return window.location.origin;
  }

  function getPath(url) {
    try { return new URL(url, getUrl()).pathname; }
    catch (e) { return url; }
  }

  function currentPath() {
    return window.location.pathname;
  }

  function currentSearch() {
    return window.location.search;
  }

  SPA.init = function () {
    SPA.contentEl = document.getElementById('spa-content');
    SPA.messagesEl = document.getElementById('messages-container');
    if (!SPA.contentEl) return;

    document.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (!link || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
      if (link.hasAttribute('data-spa-ignore')) return;
      if (link.getAttribute('target') === '_blank') return;
      if (link.hasAttribute('download')) return;
      if (link.protocol && !link.protocol.startsWith('http')) return;
      if (link.origin !== window.location.origin) return;

      var linkPath = getPath(link.href);
      if (linkPath === currentPath() && link.search === currentSearch()) return;
      if (isAuthUrl(linkPath)) return;

      e.preventDefault();
      SPA.navigate(link.href);
    });

    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (form.hasAttribute('data-spa-ignore')) return;

      var actionUrl = form.action || window.location.href;
      var actionPath = getPath(actionUrl);
      if (isAuthUrl(actionPath)) return;

      e.preventDefault();
      SPA.submitForm(form);
    });

    window.addEventListener('popstate', function (e) {
      if (e.state && e.state.url) {
        SPA.loadContent(e.state.url, false);
      }
    });
  };

  SPA.navigate = function (url, pushState) {
    if (pushState === undefined) pushState = true;
    if (SPA.isNavigating) return;
    SPA.loadContent(url, pushState);
  };

  SPA.loadContent = function (url, pushState) {
    SPA.isNavigating = true;
    SPA.showLoading();

    var finalUrl = url;

    fetch(url, { redirect: 'follow' })
      .then(function (resp) {
        if (!resp.ok) throw new Error('Error ' + resp.status);
        finalUrl = resp.url;
        return resp.text();
      })
      .then(function (html) {
        SPA.renderContent(html, finalUrl, pushState);
      })
      .catch(function (err) {
        console.error('SPA error:', err);
        SPA.showError();
      })
      .then(function () {
        SPA.isNavigating = false;
        SPA.hideLoading();
      });
  };

  SPA.submitForm = function (form) {
    var url = form.action || window.location.href;
    var method = (form.method || 'POST').toUpperCase();
    var formData = new FormData(form);

    if (method === 'GET') {
      var u = new URL(url, getUrl());
      u.search = new URLSearchParams(formData).toString();
      SPA.navigate(u.toString());
      return;
    }

    SPA.isNavigating = true;
    SPA.showLoading();

    var finalUrl = url;

    fetch(url, {
      method: method,
      body: formData,
      redirect: 'follow'
    })
      .then(function (resp) {
        if (!resp.ok) throw new Error('Error ' + resp.status);
        finalUrl = resp.url;
        return resp.text();
      })
      .then(function (html) {
        SPA.renderContent(html, finalUrl, true);
      })
      .catch(function (err) {
        console.error('SPA form error:', err);
        SPA.showError();
      })
      .then(function () {
        SPA.isNavigating = false;
        SPA.hideLoading();
      });
  };

  SPA.renderContent = function (html, finalUrl, pushState) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(html, 'text/html');

    if (SPA.messagesEl) {
      var newMessages = doc.getElementById('messages-container');
      if (newMessages && newMessages.innerHTML.trim()) {
        SPA.messagesEl.innerHTML = newMessages.innerHTML;
        SPA.initAutoDismiss();
      } else {
        SPA.messagesEl.innerHTML = '';
      }
    }

    if (SPA.contentEl) {
      var newContent = doc.getElementById('spa-content');
      if (newContent) {
        SPA.contentEl.innerHTML = newContent.innerHTML;
        SPA.executeScripts(SPA.contentEl);
        SPA.contentEl.classList.remove('animate-fade-in');
        void SPA.contentEl.offsetWidth;
        SPA.contentEl.classList.add('animate-fade-in');
      }
    }

    document.title = doc.title;

    if (pushState) {
      var stateUrl = finalUrl || window.location.href;
      if (stateUrl !== window.location.href) {
        window.history.pushState({ url: stateUrl }, '', stateUrl);
      }
    }

    SPA.updateActiveLink();
    SPA.closeOffcanvas();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  SPA.executeScripts = function (container) {
    container.querySelectorAll('script').forEach(function (old) {
      var script = document.createElement('script');
      Array.from(old.attributes).forEach(function (attr) {
        script.setAttribute(attr.name, attr.value);
      });
      script.textContent = old.textContent;
      old.parentNode.replaceChild(script, old);
    });
  };

  SPA.updateActiveLink = function () {
    var current = currentPath();

    document.querySelectorAll('.sidebar-crm .nav-link, .offcanvas-sidebar .nav-link').forEach(function (link) {
      link.classList.remove('active');
      var href = link.getAttribute('href');
      if (!href) return;
      try {
        var linkPath = new URL(href, getUrl()).pathname;
        if (linkPath === '/') {
          if (current === '/') link.classList.add('active');
        } else if (current === linkPath || current.indexOf(linkPath) === 0) {
          link.classList.add('active');
        }
      } catch (e) {}
    });
  };

  SPA.closeOffcanvas = function () {
    if (typeof bootstrap !== 'undefined') {
      var el = document.getElementById('sidebarOffcanvas');
      if (el && el.classList.contains('show')) {
        var inst = bootstrap.Offcanvas.getInstance(el);
        if (inst) inst.hide();
      }
    }
  };

  SPA.showLoading = function () {
    if (SPA.contentEl) {
      SPA.contentEl.style.opacity = '0.4';
      SPA.contentEl.style.transition = 'opacity 0.15s ease';
    }
  };

  SPA.hideLoading = function () {
    if (SPA.contentEl) {
      SPA.contentEl.style.opacity = '1';
      SPA.contentEl.style.transition = 'opacity 0.3s ease';
    }
  };

  SPA.showError = function () {
    if (SPA.contentEl) {
      SPA.contentEl.innerHTML =
        '<div class="animate-fade-in"><div class="empty-state">' +
        '<div class="empty-icon"><i class="bi bi-exclamation-triangle"></i></div>' +
        '<h5>Error al cargar la pagina</h5>' +
        '<p class="text-muted">Intenta de nuevo o recarga la pagina.</p>' +
        '<a href="' + currentPath() + '" class="btn btn-crm btn-crm-primary" onclick="location.reload()">' +
        '<i class="bi bi-arrow-clockwise me-1"></i>Recargar</a></div></div>';
    }
  };

  SPA.initAutoDismiss = function () {
    if (typeof bootstrap !== 'undefined') {
      document.querySelectorAll('#messages-container .alert-crm').forEach(function (alert) {
        setTimeout(function () {
          try {
            var bs = bootstrap.Alert.getOrCreateInstance(alert);
            bs.close();
          } catch (e) {}
        }, 5000);
      });
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', SPA.init);
  } else {
    SPA.init();
  }
})();
