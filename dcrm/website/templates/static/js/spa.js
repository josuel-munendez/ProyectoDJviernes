/*
 * spa.js — Módulo de navegación SPA (Single Page Application).
 *
 * Intercepta clics en enlaces y envíos de formularios para cargar
 * contenido de forma asíncrona sin recargar la página completa.
 * Actualiza el historial del navegador, los mensajes y el título
 * de la página, y mantiene sincronizados los enlaces activos de la
 * barra lateral.
 */
(function () {
  'use strict';

  /** @namespace SPA */
  var SPA = {
    contentEl: null,    // Elemento contenedor del contenido principal
    messagesEl: null,   // Elemento contenedor de mensajes flash
    isNavigating: false // Bandera para evitar navegaciones simultáneas
  };

  // Rutas de autenticación que NO deben ser interceptadas por el SPA
  var authPaths = ['/login', '/logout', '/registrar', '/register'];

  /**
   * Verifica si una ruta pertenece a las rutas de autenticación.
   * @param {string} pathname - Ruta a verificar
   * @returns {boolean}
   */
  function isAuthUrl(pathname) {
    return authPaths.some(function (p) {
      return pathname === p || pathname.indexOf(p + '/') === 0;
    });
  }

  /** @returns {string} Origen de la URL actual */
  function getUrl() {
    return window.location.origin;
  }

  /**
   * Extrae el pathname de una URL, o devuelve la cadena sin modificar si no es válida.
   * @param {string} url
   * @returns {string}
   */
  function getPath(url) {
    try { return new URL(url, getUrl()).pathname; }
    catch (e) { return url; }
  }

  /** @returns {string} Pathname actual del navegador */
  function currentPath() {
    return window.location.pathname;
  }

  /** @returns {string} Query string actual del navegador */
  function currentSearch() {
    return window.location.search;
  }

  /**
   * Inicializa el módulo SPA: registra los event listeners para
   * navegación mediante clics y envío de formularios, y el evento popstate.
   */
  SPA.init = function () {
    SPA.contentEl = document.getElementById('spa-content');
    SPA.messagesEl = document.getElementById('messages-container');
    if (!SPA.contentEl) return;

    // Intercepta clics en enlaces para navegación SPA
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      // Ignora clics que no sean primarios, con teclas modificadoras,
      // o enlaces externos, de descarga, target _blank, etc.
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

    // Intercepta envíos de formularios para envío asíncrono
    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (form.hasAttribute('data-spa-ignore')) return;

      var actionUrl = form.action || window.location.href;
      var actionPath = getPath(actionUrl);
      if (isAuthUrl(actionPath)) return;

      e.preventDefault();
      SPA.submitForm(form);
    });

    // Navegación con los botones atrás/adelante del navegador
    window.addEventListener('popstate', function (e) {
      if (e.state && e.state.url) {
        SPA.loadContent(e.state.url, false);
      }
    });
  };

  /**
   * Navega a una URL usando el SPA.
   * @param {string} url - URL de destino
   * @param {boolean} [pushState=true] - Si debe agregarse al historial
   */
  SPA.navigate = function (url, pushState) {
    if (pushState === undefined) pushState = true;
    if (SPA.isNavigating) return;
    SPA.loadContent(url, pushState);
  };

  /**
   * Carga contenido asíncronamente desde una URL via fetch.
   * @param {string} url
   * @param {boolean} pushState
   */
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

  /**
   * Envía un formulario vía fetch (GET o POST) y renderiza la respuesta.
   * @param {HTMLFormElement} form
   */
  SPA.submitForm = function (form) {
    var url = form.action || window.location.href;
    var method = (form.method || 'POST').toUpperCase();
    var formData = new FormData(form);

    // Los formularios GET se convierten en navegación con query string
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

  /**
   * Reemplaza el contenido del SPA con el HTML recibido.
   * Actualiza mensajes, título de página, historial y enlaces activos.
   * @param {string} html - HTML recibido del servidor
   * @param {string} finalUrl - URL final tras redirecciones
   * @param {boolean} pushState - Si se agrega al historial
   */
  SPA.renderContent = function (html, finalUrl, pushState) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(html, 'text/html');

    // Actualiza los mensajes flash si existen en la respuesta
    if (SPA.messagesEl) {
      var newMessages = doc.getElementById('messages-container');
      if (newMessages && newMessages.innerHTML.trim()) {
        SPA.messagesEl.innerHTML = newMessages.innerHTML;
        SPA.initAutoDismiss();
      } else {
        SPA.messagesEl.innerHTML = '';
      }
    }

    // Reemplaza el contenido principal
    if (SPA.contentEl) {
      var newContent = doc.getElementById('spa-content');
      if (newContent) {
        SPA.contentEl.innerHTML = newContent.innerHTML;
        SPA.executeScripts(SPA.contentEl);
        // Dispara la animación de entrada reiniciando el estado
        SPA.contentEl.classList.remove('animate-fade-in');
        void SPA.contentEl.offsetWidth;
        SPA.contentEl.classList.add('animate-fade-in');
      }
    }

    document.title = doc.title;

    // Actualiza el historial del navegador si corresponde
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

  /**
   * Re-ejecuta los scripts dentro del contenedor recién insertado.
   * Necesario porque el innerHTML no ejecuta etiquetas <script> automáticamente.
   * @param {HTMLElement} container
   */
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

  /**
   * Marca el enlace activo en la barra lateral según la ruta actual.
   */
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

  /**
   * Cierra el offcanvas de la barra lateral si está abierto.
   */
  SPA.closeOffcanvas = function () {
    if (typeof bootstrap !== 'undefined') {
      var el = document.getElementById('sidebarOffcanvas');
      if (el && el.classList.contains('show')) {
        var inst = bootstrap.Offcanvas.getInstance(el);
        if (inst) inst.hide();
      }
    }
  };

  /** Reduce la opacidad del contenido para indicar carga */
  SPA.showLoading = function () {
    if (SPA.contentEl) {
      SPA.contentEl.style.opacity = '0.4';
      SPA.contentEl.style.transition = 'opacity 0.15s ease';
    }
  };

  /** Restaura la opacidad del contenido al finalizar la carga */
  SPA.hideLoading = function () {
    if (SPA.contentEl) {
      SPA.contentEl.style.opacity = '1';
      SPA.contentEl.style.transition = 'opacity 0.3s ease';
    }
  };

  /** Muestra un mensaje de error genérico con opción de recargar */
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

  /**
   * Cierra automáticamente las alertas tipo .alert-crm después de 5 segundos.
   */
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

  // Inicialización automática al cargar el DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', SPA.init);
  } else {
    SPA.init();
  }
})();
