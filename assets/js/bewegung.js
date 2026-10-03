(() => {
  "use strict";

  const reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const kopfzeile = document.querySelector(".kopfzeile");
  if (kopfzeile) {
    const pruefen = () => {
      kopfzeile.classList.toggle("ist-gescrollt", window.scrollY > 8);
    };
    pruefen();
    window.addEventListener("scroll", pruefen, { passive: true });
  }

  if (reduziert) return;

  document.documentElement.classList.add("js-bewegung");

  document.querySelectorAll("[data-woerter]").forEach((el) => {
    let nummer = 0;
    const zerlegen = (knoten) => {
      Array.from(knoten.childNodes).forEach((kind) => {
        if (kind.nodeType === 3) {
          const teile = kind.textContent.split(/(\s+)/);
          const bruch = document.createDocumentFragment();
          teile.forEach((teil) => {
            if (!teil.trim()) {
              bruch.appendChild(document.createTextNode(teil));
              return;
            }
            const span = document.createElement("span");
            span.className = "wort";
            span.style.setProperty("--verzug", `${nummer * 55}ms`);
            span.textContent = teil;
            nummer += 1;
            bruch.appendChild(span);
          });
          kind.replaceWith(bruch);
        } else if (kind.nodeType === 1) {
          zerlegen(kind);
        }
      });
    };
    zerlegen(el);
  });

  const AUFDECKEN = ".einblenden, .scharfstellen, [data-woerter]";

  function beobachten(elemente) {
    if (!("IntersectionObserver" in window)) {
      elemente.forEach((el) => el.classList.add("ist-sichtbar"));
      return;
    }

    const beobachter = new IntersectionObserver(
      (eintraege, obs) => {
        eintraege.forEach((eintrag) => {
          if (!eintrag.isIntersecting) return;
          eintrag.target.classList.add("ist-sichtbar");
          obs.unobserve(eintrag.target);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -5% 0px" }
    );

    elemente.forEach((el, i) => {
      if (!el.hasAttribute("data-woerter")) {
        el.style.transitionDelay = `${(i % 4) * 90}ms`;
      }
      beobachter.observe(el);
    });
  }

  beobachten(Array.from(document.querySelectorAll(AUFDECKEN)));

  document.addEventListener("raster:bereit", () => {
    beobachten(
      Array.from(
        document.querySelectorAll(
          ".einblenden:not(.ist-sichtbar), .scharfstellen:not(.ist-sichtbar)"
        )
      )
    );
  });

  function nachzuegler() {
    const hoehe = window.innerHeight || document.documentElement.clientHeight || 0;
    document
      .querySelectorAll(
        ".einblenden:not(.ist-sichtbar), .scharfstellen:not(.ist-sichtbar), [data-woerter]:not(.ist-sichtbar)"
      )
      .forEach((el) => {
        const kasten = el.getBoundingClientRect();
        if (kasten.top < hoehe && kasten.bottom > 0) el.classList.add("ist-sichtbar");
      });
  }

  setTimeout(nachzuegler, 1200);
  window.addEventListener("load", () => setTimeout(nachzuegler, 400));

  function endzustandFestschreiben() {
    document
      .querySelectorAll(".ist-sichtbar:not(.ist-fertig)")
      .forEach((el) => el.classList.add("ist-fertig"));
  }

  setTimeout(endzustandFestschreiben, 3000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      setTimeout(nachzuegler, 80);
      setTimeout(endzustandFestschreiben, 160);
    }
  });
  window.addEventListener("focus", () => setTimeout(endzustandFestschreiben, 160));

  function hochzaehlen(el) {
    const ziel = Number(el.dataset.zaehlziel);
    if (!Number.isFinite(ziel)) return;

    const dauer = 1200;
    const start = performance.now();
    let fertig = false;

    function schritt(jetzt) {
      const anteil = Math.min((jetzt - start) / dauer, 1);
      const weich = 1 - Math.pow(1 - anteil, 3);
      el.textContent = String(Math.round(ziel * weich));
      if (anteil < 1) {
        requestAnimationFrame(schritt);
      } else {
        fertig = true;
      }
    }

    el.textContent = "0";
    requestAnimationFrame(schritt);

    setTimeout(() => {
      if (!fertig) el.textContent = String(ziel);
    }, dauer + 700);
  }

  const zahlen = Array.from(document.querySelectorAll("[data-zaehlziel]"));
  if (zahlen.length) {
    if ("IntersectionObserver" in window) {
      const zaehlBeobachter = new IntersectionObserver(
        (eintraege, obs) => {
          eintraege.forEach((eintrag) => {
            if (!eintrag.isIntersecting) return;
            obs.unobserve(eintrag.target);
            hochzaehlen(eintrag.target);
          });
        },
        { threshold: 0.6 }
      );
      zahlen.forEach((el) => zaehlBeobachter.observe(el));
    } else {
      zahlen.forEach(hochzaehlen);
    }
  }

  const kegel = document.querySelector(".lichtkegel");
  if (kegel && window.matchMedia("(hover: hover)").matches) {
    window.addEventListener(
      "pointermove",
      (e) => {
        if (e.pointerType === "touch") return;
        kegel.style.setProperty("--maus-x", `${e.clientX}px`);
        kegel.style.setProperty("--maus-y", `${e.clientY}px`);
        kegel.classList.add("ist-an");
      },
      { passive: true }
    );

    document.addEventListener("pointerleave", () => kegel.classList.remove("ist-an"));
  }

  function sichtHoehe() {
    return window.innerHeight || document.documentElement.clientHeight || 1;
  }

  const masken = Array.from(document.querySelectorAll(".maske"));
  if (masken.length) {
    function maskenAktualisieren() {
      const hoehe = sichtHoehe();
      masken.forEach((maske) => {
        const kasten = maske.getBoundingClientRect();
        if (kasten.bottom < -200 || kasten.top > hoehe + 200) return;
        const start = hoehe;
        const ende = hoehe * 0.45;
        const gesamt = Math.max(start - ende, 1);
        const anteil = Math.min(Math.max((start - kasten.top) / gesamt, 0), 1);
        maske.style.setProperty("--oeffnung", anteil.toFixed(4));
      });
    }

    window.addEventListener("scroll", maskenAktualisieren, { passive: true });
    window.addEventListener("resize", maskenAktualisieren, { passive: true });
    window.addEventListener("load", maskenAktualisieren);
    maskenAktualisieren();
  }

  const kopfbild = document.querySelector(".kopfbild");
  if (kopfbild) {
    function versatzSetzen() {
      const kasten = kopfbild.getBoundingClientRect();
      const hoehe = sichtHoehe();
      if (kasten.bottom < 0 || kasten.top > hoehe) return;

      const mitte = kasten.top + kasten.height / 2;
      const lage = (mitte - hoehe / 2) / (hoehe / 2 + kasten.height / 2);
      const weg = Math.max(-1, Math.min(1, lage)) * (kasten.height * 0.06);
      kopfbild.style.setProperty("--versatz", `${weg.toFixed(1)}px`);
    }

    window.addEventListener("scroll", versatzSetzen, { passive: true });
    window.addEventListener("resize", versatzSetzen, { passive: true });
    window.addEventListener("load", versatzSetzen);
    versatzSetzen();
  }
})();
