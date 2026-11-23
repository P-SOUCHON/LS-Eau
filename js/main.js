/* ==========================================================================
   LS'Eau — interface scripts (vanilla JS, no dependencies)
   1. Mobile navigation toggle
   2. Sticky header shadow
   3. Gallery category filters
   4. Gallery lightbox (native <dialog>)
   All features are progressive enhancements: the site remains fully usable
   without JavaScript (nav links, gallery images and captions are plain HTML).
   ========================================================================== */
(function () {
  "use strict";

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

  /* 2. Sticky header shadow ------------------------------------------------ */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 4);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* 3. Gallery filters ------------------------------------------------------ */
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

  /* 4. Gallery lightbox ----------------------------------------------------- */
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