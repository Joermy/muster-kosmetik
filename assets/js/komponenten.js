(() => {
  "use strict";

  const WURZEL = document.body.dataset.wurzel || "";

  const sicher = (wert) => {
    const div = document.createElement("div");
    div.textContent = wert == null ? "" : String(wert);
    return div.innerHTML;
  };

  function bild(name, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    const o = optionen || {};
    const srcset = b.breiten
      .map((w) => `${WURZEL}bilder/${name}-${w}.webp ${w}w`)
      .join(", ");
    const gross = b.breiten[b.breiten.length - 1];
    return (
      `<img src="${WURZEL}bilder/${name}-${gross}.webp"` +
      ` srcset="${srcset}"` +
      ` sizes="${o.sizes || "100vw"}"` +
      ` width="${b.breite}" height="${b.hoehe}"` +
      ` alt="${sicher(o.alt != null ? o.alt : b.alt)}"` +
      (o.eifrig
        ? ' fetchpriority="high" decoding="async"'
        : ' loading="lazy" decoding="async"') +
      ">"
    );
  }

  function rahmen(name, klasse, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    return (
      `<div class="bild ${klasse}" style="--platzhalter:${b.farbe}">` +
      bild(name, optionen) +
      "</div>"
    );
  }

  window.BILDBAU = { bild, rahmen };

  document.querySelectorAll(".klapp__knopf").forEach((knopf) => {
    const inhalt = document.getElementById(knopf.getAttribute("aria-controls"));
    if (!inhalt) return;

    knopf.addEventListener("click", () => {
      const offen = knopf.getAttribute("aria-expanded") === "true";

      if (offen) {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        requestAnimationFrame(() => {
          inhalt.style.height = "0px";
        });
        knopf.setAttribute("aria-expanded", "false");
      } else {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        knopf.setAttribute("aria-expanded", "true");
        inhalt.addEventListener(
          "transitionend",
          () => {
            if (knopf.getAttribute("aria-expanded") === "true") {
              inhalt.style.height = "auto";
            }
          },
          { once: true }
        );
      }
    });
  });

  let etwasGebaut = false;

  function behandlungskarte(b) {
    const marken = (b.marken || [])
      .map((m) => `<span class="marke-chip">${sicher(m)}</span>`)
      .join("");
    return (
      '<article class="glas glas--greifbar behandlung einblenden"' +
      ` data-bereich="${sicher(b.bereich)}"` +
      ` data-zeit="${sicher(b.zeit)}"` +
      ` data-anlass="${sicher(b.anlass)}">` +
      rahmen(b.bild, "bild--1-1 bild--klein", {
        sizes: "(max-width: 620px) 84vw, (max-width: 900px) 42vw, 300px",
      }) +
      '<div class="behandlung__kopf">' +
      `<h3>${sicher(b.name)}</h3>` +
      `<span class="behandlung__dauer">${sicher(b.dauer)} Min.</span>` +
      "</div>" +
      `<p>${sicher(b.text)}</p>` +
      `<div class="behandlung__marken">${marken}</div>` +
      "</article>"
    );
  }

  const raster = document.getElementById("behandlungen-raster");
  if (raster && Array.isArray(window.BEHANDLUNGEN)) {
    raster.innerHTML = window.BEHANDLUNGEN.map(behandlungskarte).join("");
    etwasGebaut = true;
  }

  const finder = document.getElementById("finder");
  if (finder && raster && Array.isArray(window.FINDER)) {
    const gewaehlt = {};

    finder.innerHTML = window.FINDER.map((f, i) => {
      const knoepfe = f.optionen
        .map(
          (o, j) =>
            `<button class="finder__wahl" type="button"` +
            ` data-feld="${sicher(f.feld)}" data-wert="${sicher(o.wert)}"` +
            ` aria-pressed="${j === 0 ? "true" : "false"}">${sicher(o.text)}</button>`
        )
        .join("");
      return (
        '<div class="finder__frage">' +
        `<p id="finder-frage-${i}">${sicher(f.frage)}</p>` +
        `<div class="finder__gruppe" role="group" aria-labelledby="finder-frage-${i}">` +
        knoepfe +
        "</div></div>"
      );
    }).join("") +
      '<p class="finder__ergebnis" id="finder-ergebnis" role="status"></p>';

    const ergebnis = document.getElementById("finder-ergebnis");

    function filtern() {
      let sichtbar = 0;
      raster.querySelectorAll(".behandlung").forEach((karte) => {
        const passt = Object.keys(gewaehlt).every(
          (feld) => !gewaehlt[feld] || karte.dataset[feld] === gewaehlt[feld]
        );
        karte.hidden = !passt;
        if (passt) sichtbar += 1;
      });

      const gesamt = raster.querySelectorAll(".behandlung").length;
      if (sichtbar === gesamt) {
        ergebnis.textContent = `Alle ${gesamt} Behandlungen werden angezeigt.`;
      } else if (sichtbar === 0) {
        ergebnis.textContent =
          "Dazu passt nichts aus der Liste. Rufen Sie an — dann finden wir etwas.";
      } else if (sichtbar === 1) {
        ergebnis.textContent = "Eine Behandlung passt.";
      } else {
        ergebnis.textContent = `${sichtbar} Behandlungen passen.`;
      }
    }

    finder.addEventListener("click", (e) => {
      const knopf = e.target.closest(".finder__wahl");
      if (!knopf) return;
      const feld = knopf.dataset.feld;
      gewaehlt[feld] = knopf.dataset.wert;

      finder
        .querySelectorAll(`.finder__wahl[data-feld="${feld}"]`)
        .forEach((k) => k.setAttribute("aria-pressed", String(k === knopf)));

      filtern();
    });

    filtern();
  }

  const ablauf = document.getElementById("ablauf");
  if (ablauf && Array.isArray(window.ABLAUF)) {
    ablauf.innerHTML = window.ABLAUF.map(
      (s) =>
        '<div class="ablauf__schritt einblenden">' +
        `<h3>${sicher(s.titel)}</h3>` +
        `<p>${sicher(s.text)}</p>` +
        "</div>"
    ).join("");
    etwasGebaut = true;
  }

  if (etwasGebaut) {
    document.dispatchEvent(new CustomEvent("raster:bereit"));
  }
})();
