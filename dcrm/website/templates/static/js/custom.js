/*
 * custom.js — Efectos visuales y validación de formularios del lado del cliente.
 *
 * Este archivo contiene dos funcionalidades principales:
 *   1) Validación de formularios .form-crm mediante delegación de eventos
 *      (compatible con navegación SPA).
 *   2) Efecto visual de estrellas y brillo que sigue el cursor del ratón
 *      (inspirado en interfaces tipo Mario UI).
 */

/**
 * Valida formularios .form-crm al enviarlos.
 * Comprueba campos requeridos, formato de email y longitud de contraseña.
 * Agrega/remueve la clase .is-invalid en los campos según corresponda.
 */
(function() {
    document.addEventListener('submit', function(e) {
        var form = e.target.closest('.form-crm');
        if (!form) return;
        var valid = true;
        form.querySelectorAll('input[required], select[required], textarea[required]').forEach(function(input) {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        form.querySelectorAll('input[type="email"]').forEach(function(input) {
            if (input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
                input.classList.add('is-invalid');
                valid = false;
            }
        });
        form.querySelectorAll('input[type="password"]').forEach(function(input) {
            if (input.value && input.value.length < 8) {
                input.classList.add('is-invalid');
                valid = false;
            }
        });
        if (!valid) {
            e.preventDefault();
        }
    });

    // Limpia el estado de error al escribir sobre el campo
    document.addEventListener('input', function(e) {
        if (e.target.closest('.form-crm')) {
            e.target.classList.remove('is-invalid');
        }
    });
})();

/**
 * Efecto de estrellas y brillo al mover el cursor.
 * Crea partículas tipo estrella y puntos de resplandor que siguen al ratón.
 * También gestiona el menú de navegación de la landing page.
 */
document.addEventListener('DOMContentLoaded', function() {

  const container = document.getElementById("magic-mouse-container");
  if (!container) return;

  const originPosition = { x: 0, y: 0 };

  // Almacena el estado anterior del cursor y las estrellas
  const last = {
    starTimestamp: new Date().getTime(),
    starPosition: originPosition,
    mousePosition: originPosition
  };

  // Configuración de los efectos visuales
  const config = {
    starAnimationDuration: 1500,    // Duración de la animación de cada estrella
    minimumTimeBetweenStars: 300,   // Tiempo mínimo entre estrellas consecutivas
    minimumDistanceBetweenStars: 100, // Distancia mínima para crear una nueva estrella
    glowDuration: 75,               // Duración del brillo en ms
    maximumGlowPointSpacing: 10,    // Espaciado máximo entre puntos de brillo
    colors: ["99 102 241", "129 140 248", "167 139 250", "14 165 233"],
    sizes: ["1.2rem", "0.9rem", "0.6rem"],
    animations: ["star-fall-1", "star-fall-2", "star-fall-3"]
  };

  let count = 0;

  // Funciones auxiliares
  const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
  const selectRandom = items => items[rand(0, items.length - 1)];
  const withUnit = (value, unit) => `${value}${unit}`;
  const px = value => withUnit(value, "px");
  const ms = value => withUnit(value, "ms");

  /**
   * Calcula la distancia euclidiana entre dos puntos.
   */
  const calcDistance = (a, b) => {
    const diffX = b.x - a.x, diffY = b.y - a.y;
    return Math.sqrt(Math.pow(diffX, 2) + Math.pow(diffY, 2));
  };

  const calcElapsedTime = (start, end) => end - start;

  const appendElement = element => container.appendChild(element);
  const removeElement = (element, delay) => setTimeout(() => container.removeChild(element), delay);

  /**
   * Crea una partícula estrella en la posición indicada con color y tamaño aleatorios.
   */
  const createStar = position => {
    const star = document.createElement("span");
    const color = selectRandom(config.colors);

    star.className = "star-particle bi bi-star-fill";

    star.style.left = px(position.x);
    star.style.top = px(position.y);
    star.style.fontSize = selectRandom(config.sizes);
    star.style.color = `rgb(${color} / 0.4)`;
    star.style.textShadow = `0 0 1.5rem rgb(${color} / 0.3)`;
    star.style.animationName = config.animations[count++ % 3];
    star.style.animationDuration = ms(config.starAnimationDuration);

    appendElement(star);
    removeElement(star, config.starAnimationDuration);
  };

  /**
   * Crea un punto de brillo en la posición indicada.
   */
  const createGlowPoint = position => {
    const glow = document.createElement("div");
    glow.className = "glow-point";
    glow.style.left = px(position.x);
    glow.style.top = px(position.y);
    appendElement(glow);
    removeElement(glow, config.glowDuration);
  };

  /**
   * Determina cuántos puntos de brillo generar según la distancia recorrida.
   */
  const determinePointQuantity = distance => Math.max(
    Math.floor(distance / config.maximumGlowPointSpacing), 1
  );

  /**
   * Genera una estela de brillo interpolando puntos entre la última y la posición actual.
   */
  const createGlow = (lastPos, current) => {
    const distance = calcDistance(lastPos, current);
    const quantity = determinePointQuantity(distance);
    const dx = (current.x - lastPos.x) / quantity;
    const dy = (current.y - lastPos.y) / quantity;

    Array.from(Array(quantity)).forEach((_, index) => {
      createGlowPoint({ x: lastPos.x + dx * index, y: lastPos.y + dy * index });
    });
  };

  const updateLastStar = position => {
    last.starTimestamp = new Date().getTime();
    last.starPosition = position;
  };

  const updateLastMousePosition = position => last.mousePosition = position;
  const adjustLastMousePosition = position => {
    if (last.mousePosition.x === 0 && last.mousePosition.y === 0) {
      last.mousePosition = position;
    }
  };

  /**
   * Maneja el movimiento del ratón: crea estrellas (si cumple distancia/tiempo) y genera brillo continuo.
   */
  const handleOnMove = e => {
    const mousePosition = { x: e.clientX, y: e.clientY };
    adjustLastMousePosition(mousePosition);

    const now = new Date().getTime();
    const hasMovedFarEnough = calcDistance(last.starPosition, mousePosition) >= config.minimumDistanceBetweenStars;
    const hasBeenLongEnough = calcElapsedTime(last.starTimestamp, now) > config.minimumTimeBetweenStars;

    if (hasMovedFarEnough || hasBeenLongEnough) {
      createStar(mousePosition);
      updateLastStar(mousePosition);
    }

    createGlow(last.mousePosition, mousePosition);
    updateLastMousePosition(mousePosition);
  };

  window.onmousemove = e => handleOnMove(e);
  window.ontouchmove = e => handleOnMove(e.touches[0]);
  document.body.onmouseleave = () => updateLastMousePosition(originPosition);

  // Aplica efecto scrolled a la barra de navegación de la landing page al hacer scroll
  const landingNav = document.querySelector('.landing-nav');
  if (landingNav) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        landingNav.classList.add('scrolled');
      } else {
        landingNav.classList.remove('scrolled');
      }
    });
  }

  // Menú hamburguesa para la navegación responsiva de la landing page
  const navToggle = document.querySelector('.landing-nav-toggle');
  const navLinks = document.querySelector('.landing-nav .nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function() {
      navLinks.classList.toggle('show');
    });
    // Cierra el menú al hacer clic fuera de él
    document.addEventListener('click', function(e) {
      if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('show');
      }
    });
  }

});
