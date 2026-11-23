/* ==========================================================================
   LS'Eau — interface scripts (vanilla JS, no dependencies)
   1. Mobile navigation toggle
   2. Header transformation (compact + solid after scroll)
   3. Progressive section reveals (IntersectionObserver)
   4. Restrained hero parallax
   5. Gallery category filters
   6. Gallery lightbox (native <dialog>)
   All features are progressive enhancements: the site remains fully usable
   without JavaScript (nav links, gallery images and captions are plain HTML,
   and reveal targets are only hidden once JS is confirmed running).
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* 1. Mobile navigation -------------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");

  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    };

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (
        nav.classList.contains("is-open") &&
        !nav.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        setOpen(false);
      }
    });

    // Close the menu after following an in-page anchor link.
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
  }

  /* 2. Header transformation ---------------------------------------------- */
  var header = document.querySelector(".site-header");
  var heroMedia = document.querySelector(".hero__media img");
  var hero = document.querySelector(".hero");
  var ticking = false;

  var onScroll = function () {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 24);
    document.body.classList.toggle("is-scrolled", y > 24);

    /* 4. Hero parallax: small, clamped, transform-only (no layout shift). */
    if (heroMedia && hero && !reduceMotion.matches) {
      var limit = hero.offsetHeight;
      if (y <= limit) {
        heroMedia.style.transform = "translate3d(0," + Math.min(y * 0.16, 120) + "px,0)";
      }
    }
    ticking = false;
  };

  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );
  onScroll();

  /* 3. Progressive reveals ------------------------------------------------ */
  var revealTargets = Array.prototype.slice.call(
    document.querySelectorAll("[data-reveal]")
  );

  if (
    revealTargets.length &&
    "IntersectionObserver" in window &&
    !reduceMotion.matches
  ) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    revealTargets.forEach(function (el) {
      el.classList.add("reveal-init");
      observer.observe(el);
    });
  }

  /* 5. Gallery filters ------------------------------------------------------ */
  var filterBar = document.querySelector(".gallery-filters");
  var galleryItems = Array.prototype.slice.call(
    document.querySelectorAll(".gallery-grid > li")
  );

  if (filterBar && galleryItems.length) {
    var emptyMsg = document.querySelector(".gallery-empty");

    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter-btn");
      if (!btn) return;

      filterBar.querySelectorAll(".filter-btn").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });

      var cat = btn.getAttribute("data-filter");
      var visible = 0;
      galleryItems.forEach(function (li) {
        var show = cat === "all" || li.getAttribute("data-category") === cat;
        li.hidden = !show;
        if (show) visible += 1;
      });
      if (emptyMsg) emptyMsg.hidden = visible !== 0;
    });
  }

  /* 6. Gallery lightbox ----------------------------------------------------- */
  var dialog = document.getElementById("lightbox");
  var links = Array.prototype.slice.call(
    document.querySelectorAll(".gallery-grid a[data-lightbox]")
  );

  if (dialog && links.length && typeof dialog.showModal === "function") {
    var img = dialog.querySelector("img");
    var caption = dialog.querySelector(".lightbox__caption");
    var counter = dialog.querySelector(".lightbox__count");
    var current = 0;
    var lastFocused = null;

    var visibleLinks = function () {
      return links.filter(function (a) {
        return !a.closest("li").hidden;
      });
    };

    var render = function () {
      var list = visibleLinks();
      var a = list[current];
      if (!a) return;
      img.src = a.getAttribute("href");
      img.alt = a.querySelector("img").alt;
      caption.textContent = a.getAttribute("data-caption") || "";
      counter.textContent = current + 1 + " / " + list.length;
    };

    var open = function (a) {
      var list = visibleLinks();
      current = Math.max(0, list.indexOf(a));
      lastFocused = document.activeElement;
      render();
      dialog.showModal();
      dialog.querySelector(".lightbox__close").focus();
    };

    var step = function (delta) {
      var list = visibleLinks();
      current = (current + delta + list.length) % list.length;
      render();
    };

    links.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        open(a);
      });
    });

    dialog.querySelector(".lightbox__close").addEventListener("click", function () {
      dialog.close();
    });
    dialog.querySelector(".lightbox__nav--prev").addEventListener("click", function () {
      step(-1);
    });
    dialog.querySelector(".lightbox__nav--next").addEventListener("click", function () {
      step(1);
    });

    dialog.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });

    // Click on the backdrop (the dialog element itself) closes the lightbox.
    dialog.addEventListener("click", function (e) {
      if (e.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", function () {
      img.src =
        "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==";
      img.alt = "";
      if (lastFocused) lastFocused.focus();
    });
  }
})();