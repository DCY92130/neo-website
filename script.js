// Neowebsite — interactions légères
(function () {
  "use strict";

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    if (!toggle || !nav) return;
    toggle.classList.remove("is-active");
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.classList.toggle("is-active", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
  }

  // Formulaire de contact → ouvre un mail pré-rempli vers contact@neo-website.fr
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var nom = form.elements.nom.value.trim();
      var email = form.elements.email.value.trim();
      var activite = form.elements.activite.value;
      var message = form.elements.message.value.trim();

      var subject = "Demande de site — " + (nom || "Nouveau contact");
      var body = "Nom : " + nom + "\nEmail : " + email + "\nActivité : " + activite + "\n\n" + message;

      window.location.href =
        "mailto:contact@neo-website.fr" +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    });
  }

  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }
})();
