// Client-side form validation
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.form-crm').forEach(function(form) {
            form.addEventListener('submit', function(e) {
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
            form.querySelectorAll('input, select, textarea').forEach(function(input) {
                input.addEventListener('input', function() {
                    this.classList.remove('is-invalid');
                });
            });
        });
    });
})();

document.addEventListener('DOMContentLoaded', function() {

  const container = document.getElementById("magic-mouse-container");
  if (!container) return;

  const originPosition = { x: 0, y: 0 };

  const last = {
    starTimestamp: new Date().getTime(),
    starPosition: originPosition,
    mousePosition: originPosition
  };

  const config = {
    starAnimationDuration: 1500,
    minimumTimeBetweenStars: 300,
    minimumDistanceBetweenStars: 100,
    glowDuration: 75,
    maximumGlowPointSpacing: 10,
    colors: ["99 102 241", "129 140 248", "167 139 250", "14 165 233"],
    sizes: ["1.2rem", "0.9rem", "0.6rem"],
    animations: ["star-fall-1", "star-fall-2", "star-fall-3"]
  };

  let count = 0;

  const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
  const selectRandom = items => items[rand(0, items.length - 1)];
  const withUnit = (value, unit) => `${value}${unit}`;
  const px = value => withUnit(value, "px");
  const ms = value => withUnit(value, "ms");

  const calcDistance = (a, b) => {
    const diffX = b.x - a.x, diffY = b.y - a.y;
    return Math.sqrt(Math.pow(diffX, 2) + Math.pow(diffY, 2));
  };

  const calcElapsedTime = (start, end) => end - start;

  const appendElement = element => container.appendChild(element);
  const removeElement = (element, delay) => setTimeout(() => container.removeChild(element), delay);

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

  const createGlowPoint = position => {
    const glow = document.createElement("div");
    glow.className = "glow-point";
    glow.style.left = px(position.x);
    glow.style.top = px(position.y);
    appendElement(glow);
    removeElement(glow, config.glowDuration);
  };

  const determinePointQuantity = distance => Math.max(
    Math.floor(distance / config.maximumGlowPointSpacing), 1
  );

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

  // Landing nav scroll effect
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

  // Landing nav hamburger toggle
  const navToggle = document.querySelector('.landing-nav-toggle');
  const navLinks = document.querySelector('.landing-nav .nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function() {
      navLinks.classList.toggle('show');
    });
    document.addEventListener('click', function(e) {
      if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('show');
      }
    });
  }

});
