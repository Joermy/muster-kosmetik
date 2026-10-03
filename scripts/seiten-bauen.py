#!/usr/bin/env python3

import json
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parent.parent

BETRIEB = "Studio Leyla"

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
    "object-src 'none'; base-uri 'none'; form-action 'none'; "
    "upgrade-insecure-requests"
)

NAVIGATION = [
    ("behandlungen", "Behandlungen"),
    ("studio", "Studio"),
    ("preise", "Preise"),
    ("kontakt", "Kontakt"),
]

_nachweise = WURZEL / "bilder" / "nachweise.json"
BILDER = {}
if _nachweise.exists():
    BILDER = json.loads(_nachweise.read_text(encoding="utf-8"))["bilder"]

def bild(name: str, sizes: str, *, eifrig: bool = False, alt: str = None) -> str:
    b = BILDER.get(name)
    if not b:
        return f"<!-- Bild fehlt: {name} — scripts/bilder-holen.py laufen lassen -->"
    srcset = ", ".join(f"../bilder/{name}-{w}.webp {w}w" for w in b["breiten"])
    gross = b["breiten"][-1]
    laden = (
        'fetchpriority="high" decoding="async"'
        if eifrig
        else 'loading="lazy" decoding="async"'
    )
    return (
        f'<img src="../bilder/{name}-{gross}.webp" srcset="{srcset}" '
        f'sizes="{sizes}" width="{b["breite"]}" height="{b["hoehe"]}" '
        f'alt="{alt or b["alt"]}" {laden}>'
    )

def rahmen(name: str, klasse: str, sizes: str, **kw) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--bg-2)"
    return (
        f'<div class="bild {klasse}" style="--platzhalter:{farbe}">'
        + bild(name, sizes, **kw)
        + "</div>"
    )

def kopfbild(name: str, alt: str = None) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--bg-2)"
    return (
        '\n    <div class="breite maske">\n'
        '      <div class="maske__bild">\n'
        f'        <div class="kopfbild" style="--platzhalter:{farbe}">\n'
        "          " + bild(name, "(max-width: 1320px) 92vw, 1180px",
                            eifrig=True, alt=alt) + "\n"
        "        </div>\n"
        "      </div>\n"
        "    </div>\n"
    )

def kopf(slug: str, titel: str, beschreibung: str) -> str:
    nav = "\n".join(
        f'          <li><a href="../{ziel}/index.html"'
        f'{" aria-current=\"page\"" if ziel == slug else ""}>{text}</a></li>'
        for ziel, text in NAVIGATION
    )

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{titel} — {BETRIEB}</title>
  <meta name="description" content="{beschreibung}">
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/basis.css">
  <link rel="stylesheet" href="../assets/css/raster.css">
  <link rel="stylesheet" href="../assets/css/komponenten.css">
  <link rel="stylesheet" href="../assets/css/bilder.css">
  <link rel="stylesheet" href="../assets/css/bewegung.css">
</head>
<body data-wurzel="../">
  <a class="sprunglink" href="#inhalt">Zum Inhalt</a>

  <div class="flaechen" aria-hidden="true">
    <span></span><span></span><span></span><span></span>
  </div>
  <div class="lichtkegel" aria-hidden="true"></div>

  <header class="kopfzeile">
    <div class="breite kopfzeile__inhalt">
      <a class="marke" href="../index.html"><i></i>{BETRIEB}</a>
      <nav class="hauptnav" aria-label="Hauptnavigation">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="inhalt">
"""

FUSS = f"""  </main>

  <footer class="fusszeile">
    <div class="breite">
      <div class="fusszeile__raster">
        <div>
          <p class="fusszeile__marke">Studio<br>Leyla</p>
        </div>
        <div>
          <h2>Studio</h2>
          <p style="color:var(--muted)">
            Lister Meile 48<br>
            30161 Hannover
          </p>
        </div>
        <div>
          <h2>Kontakt</h2>
          <ul>
            <li><a href="tel:+4951139240">0511 39 24 0</a></li>
            <li><a href="mailto:termin@studio-leyla.de">termin@studio-leyla.de</a></li>
          </ul>
        </div>
        <div>
          <h2>Seiten</h2>
          <ul>
            <li><a href="../behandlungen/index.html">Behandlungen</a></li>
            <li><a href="../studio/index.html">Studio</a></li>
            <li><a href="../preise/index.html">Preise</a></li>
            <li><a href="../kontakt/index.html">Kontakt</a></li>
          </ul>
        </div>
      </div>

      <p class="fusszeile__hinweis">
        <strong>Musterprojekt.</strong> Betrieb, Anschrift und Inhalte sind frei
        erfunden. Kein Kundenauftrag. Diese Seite dient als Arbeitsprobe.
        Die Fotos stammen von Unsplash und zeigen weder dieses Studio noch
        Behandlungsergebnisse — Urheber und Lizenz stehen im
        <a href="../impressum/index.html">Impressum</a>.
      </p>

      <div class="fusszeile__unten">
        <p>{BETRIEB} — © 2026</p>
        <ul>
          <li><a href="../impressum/index.html">Impressum</a></li>
          <li><a href="../datenschutz/index.html">Datenschutz</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="../daten/inhalte.js" defer></script>
  <script src="../daten/bilder.js" defer></script>
  <script src="../assets/js/bewegung.js" defer></script>
  <script src="../assets/js/komponenten.js" defer></script>
</body>
</html>
"""

def seitenkopf(etikett: str, titel: str, lead: str = "") -> str:
    lead_html = (
        f'\n      <p class="hero__lead einblenden">{lead}</p>' if lead else ""
    )
    return f"""
    <section class="hero breite">
      <p class="etikett einblenden">{etikett}</p>
      <h1 data-woerter style="font-size:var(--fs-h2)">{titel}</h1>{lead_html}
    </section>
"""

SEITEN = {
    "behandlungen": {
        "titel": "Behandlungen",
        "beschreibung": "Gesichtsbehandlungen, Maniküre, Wimpern und Brauen im Studio Leyla in Hannover.",
        "inhalt": seitenkopf(
            "Angebot",
            "Sechs Behandlungen, <em>ausreichend Zeit.</em>",
            "Mehr sind es absichtlich nicht. Was hier steht, wird regelmäßig "
            "gemacht — und deshalb auch gut gemacht.",
        )
        + kopfbild("detail-wimpern", "Nahaufnahme eines Auges mit langen Wimpern")
        + """
    <section class="abschnitt breite">
      <div class="glas finder einblenden" id="finder"></div>
      <div class="spalten spalten--3" id="behandlungen-raster" style="margin-top:var(--sp-7)"></div>

      <noscript>
        <ul style="margin-top:var(--sp-6)">
          <li>Klassische Gesichtsbehandlung — 60 Minuten</li>
          <li>Intensivbehandlung — 90 Minuten</li>
          <li>Kurze Auffrischung — 30 Minuten</li>
          <li>Pflege für empfindliche Haut — 60 Minuten</li>
          <li>Maniküre — 45 Minuten</li>
          <li>Wimpern und Brauen — 45 Minuten</li>
        </ul>
      </noscript>
    </section>

    <section class="abschnitt breite">
      <div class="einblenden">
        __STRECKE_BEHANDLUNGEN__
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="fragen-titel">
      <div class="kopf">
        <p class="etikett einblenden">Häufig gefragt</p>
        <h2 id="fragen-titel" data-woerter>Bevor Sie <em>kommen.</em></h2>
      </div>

      <div class="einblenden" style="max-width:760px;margin-inline:auto">
        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="f-1">
            <span>Wie lange dauert ein Termin?</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="f-1">
            <div><p>Zwischen 30 und 90 Minuten, je nach Behandlung. Beim
            ersten Termin kommt ein kurzes Gespräch dazu, rechnen Sie also
            zehn Minuten mehr ein.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="f-2">
            <span>Muss ich etwas mitbringen?</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="f-2">
            <div><p>Nein. Wenn Sie Produkte benutzen, bei denen Sie unsicher
            sind, bringen Sie sie gern mit — dann sehen wir sie uns an.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="f-3">
            <span>Ich habe eine Hauterkrankung. Geht das?</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="f-3">
            <div><p>Sprechen Sie uns vorher an. Kosmetik ersetzt keine
            ärztliche Behandlung, und manche Hautzustände gehören zuerst zur
            Hautärztin oder zum Hautarzt. Wir sagen es Ihnen ehrlich, wenn wir
            der falsche Ort sind.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="f-4">
            <span>Werden mir am Ende Produkte verkauft?</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="f-4">
            <div><p>Nur wenn Sie danach fragen. Kein Verkaufsgespräch am
            Ende der Behandlung.</p></div>
          </div>
        </div>

        <div class="klapp">
          <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="f-5">
            <span>Wie sage ich einen Termin ab?</span><span class="klapp__zeichen" aria-hidden="true"></span>
          </button>
          <div class="klapp__inhalt" id="f-5">
            <div><p>Ein Anruf reicht. Bis 24 Stunden vor dem Termin kostet die Absage nichts; danach berechnen wir die Hälfte des Behandlungspreises.</p></div>
          </div>
        </div>
      </div>
    </section>
""",
    },
    "studio": {
        "titel": "Studio",
        "beschreibung": "Zwei Behandlungsplätze, ein Termin nach dem anderen: das Studio Leyla in Hannover.",
        "inhalt": seitenkopf(
            "Der Ort",
            "Klein geblieben, <em>mit Absicht.</em>",
            "Seit 2019 an der Lister Meile, geführt von Leyla Demir. Aus "
            "einem Behandlungsplatz sind zwei geworden — mehr sollen es "
            "nicht werden.",
        )
        + kopfbild("studio-raum", "Heller Behandlungsraum mit zwei Stühlen und einem Waschtisch")
        + """
    <section class="abschnitt breite">
      <div class="gespann">
        <div class="gespann__fest">
          <p class="etikett einblenden">Arbeitsweise</p>
          <h2 data-woerter style="margin-top:var(--sp-4)">
            Wer behandelt, hat <em>vorher zugehört.</em>
          </h2>
        </div>
        <div>
          <p class="einblenden" style="color:var(--muted)">
            In einer Kette bucht man eine Behandlung und bekommt sie. Hier wird vorher gefragt, was die Haut gerade braucht — und manchmal ist die Antwort, dass weniger besser wäre als das, was gebucht wurde. Das Gespräch führt die, die danach auch behandelt.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Leyla Demir ist gelernte Kosmetikerin, Abschluss 2014 an der Fachschule Hannover, seit 2019 selbstständig. Mira Kalb ist seit 2022 im Studio. Beide gehen einmal im Jahr auf eine Fachfortbildung; das Studio schließt dafür zwei Tage.
          </p>

          <div class="scharfstellen" style="margin-top:var(--sp-8)">
            __BILD_PORTRAET__
          </div>
          <p class="bildzeile"><b>Leyla Demir</b><span>Inhaberin, Kosmetikerin seit 2014</span></p>
        </div>
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="raum-titel">
      <div class="kopf">
        <p class="etikett einblenden">Räume</p>
        <h2 id="raum-titel" data-woerter>Hell, ruhig, <em>aufgeräumt.</em></h2>
      </div>

      <div class="galerie">
        <div class="scharfstellen">__BILD_SPIEGEL__</div>
        <div class="scharfstellen">__BILD_KERZEN__</div>
        <div class="scharfstellen">__BILD_HAENDE__</div>
      </div>
    </section>

    <section class="abschnitt--eng breite">
      <dl class="kennzahlen einblenden">
        <div class="kennzahl">
          <dt>Behandlungsplätze</dt>
          <dd><span data-zaehlziel="2">2</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Minuten je Termin</dt>
          <dd><span data-zaehlziel="60">60</span><span>ab</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Jahre im Beruf</dt>
          <dd><span data-zaehlziel="12">12</span></dd>
        </div>
      </dl>
    </section>
""",
    },
    "preise": {
        "titel": "Preise",
        "beschreibung": "Preisliste und Öffnungszeiten des Studio Leyla in Hannover.",
        "inhalt": seitenkopf(
            "Preisliste",
            "Alles steht <em>vorher</em> fest.",
            "Keine Pakete, keine Zuschläge, die erst am Ende auftauchen. "
            "Was dazukommt, wird vorher besprochen.",
        )
        + kopfbild("detail-haende", "Hand mit hellem Naturnagellack")
        + """
    <section class="abschnitt breite">
      <div class="gespann">
        <div class="gespann__fest">
          <p class="etikett einblenden">Behandlungen</p>
          <h2 data-woerter style="margin-top:var(--sp-4)">Preise</h2>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Alle Preise sind Endpreise und enthalten die gesetzliche
            Umsatzsteuer.
          </p>
        </div>
        <div>
          <dl class="preise einblenden">
            <div>
              <dt>Klassische Gesichtsbehandlung<small>60 Minuten</small></dt>
              <dd>72 €</dd>
            </div>
            <div>
              <dt>Intensivbehandlung<small>90 Minuten</small></dt>
              <dd>105 €</dd>
            </div>
            <div>
              <dt>Kurze Auffrischung<small>30 Minuten</small></dt>
              <dd>39 €</dd>
            </div>
            <div>
              <dt>Pflege für empfindliche Haut<small>60 Minuten</small></dt>
              <dd>76 €</dd>
            </div>
            <div>
              <dt>Maniküre<small>45 Minuten</small></dt>
              <dd>45 €</dd>
            </div>
            <div>
              <dt>Wimpern und Brauen<small>45 Minuten</small></dt>
              <dd>52 €</dd>
            </div>
          </dl>

          <p class="einblenden" style="margin-top:var(--sp-6);font-size:var(--fs-meta);color:var(--muted)">
            Behandlungen finden nur nach Vereinbarung statt. Termine, die
            weniger als 24 Stunden vorher abgesagt werden, berechnen wir mit
            der Hälfte des Behandlungspreises.
          </p>

          <div class="einblenden" style="margin-top:var(--sp-9)">
            __STRECKE_PREISE__
          </div>

          <h2 style="margin-top:var(--sp-9);font-size:var(--fs-h3)">Öffnungszeiten</h2>
          <dl class="zeiten einblenden" style="margin-top:var(--sp-4)">
            <div><dt>Montag</dt><dd>geschlossen</dd></div>
            <div><dt>Dienstag bis Freitag</dt><dd>9 – 18 Uhr</dd></div>
            <div><dt>Samstag</dt><dd>9 – 14 Uhr</dd></div>
            <div><dt>Sonntag</dt><dd>geschlossen</dd></div>
          </dl>

          <p class="einblenden" style="margin-top:var(--sp-6);color:var(--muted)">
            Behandlungen nur nach Vereinbarung. Zahlen können Sie bar oder mit Karte.
          </p>
        </div>
      </div>
    </section>
""",
    },
    "kontakt": {
        "titel": "Kontakt",
        "beschreibung": "Telefon, E-Mail und Anfahrt zum Studio Leyla in Hannover.",
        "inhalt": seitenkopf(
            "Termin",
            "Rufen Sie an — <em>das geht am schnellsten.</em>",
            "Für einen Termin brauchen wir zwei Minuten am Telefon: worum es "
            "gehen soll und wann es Ihnen passt.",
        )
        + kopfbild("ruhe-kerzen", "Kerzen auf einer Ablage")
        + """
    <section class="abschnitt breite">
      <div class="gespann">
        <div class="gespann__fest">
          <p class="etikett einblenden">Direkt</p>
          <h2 data-woerter style="margin-top:var(--sp-4)">So erreichen Sie uns.</h2>
        </div>
        <div>
          <dl class="kontaktliste einblenden">
            <dt>Telefon</dt>
            <dd><a href="tel:+4951139240">0511 39 24 0</a></dd>
            <dt>E-Mail</dt>
            <dd><a href="mailto:termin@studio-leyla.de">termin@studio-leyla.de</a></dd>
            <dt>Studio</dt>
            <dd>Lister Meile 48<br>30161 Hannover</dd>
          </dl>

          <p class="einblenden" style="margin-top:var(--sp-5);font-size:var(--fs-meta);color:var(--muted)">
            Diese Seite hat kein Buchungssystem und kein Kontaktformular.
            Beides würde personenbezogene Daten verarbeiten und einen
            Auftragsverarbeitungsvertrag, eine Einwilligung und einen Eintrag
            in der Datenschutzerklärung nötig machen. Telefon und E-Mail
            leisten dasselbe, ohne das alles.
          </p>
        </div>
      </div>
    </section>

    <section class="abschnitt breite">
      <div class="einblenden">
        __STRECKE_KONTAKT__
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="anfahrt-titel">
      <div class="gespann">
        <div class="gespann__fest">
          <p class="etikett einblenden">Anfahrt</p>
          <h2 id="anfahrt-titel" data-woerter style="margin-top:var(--sp-4)">So finden Sie her.</h2>
        </div>
        <div>
          <p class="einblenden" style="color:var(--muted)">
            Stadtbahn 3, 7 oder 9 bis Lister Meile, von dort zwei Minuten stadtauswärts auf der rechten Seite. Parken lässt sich am besten im Parkhaus Celler Straße, drei Gehminuten entfernt.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);font-size:var(--fs-meta);color:var(--muted)">
            Eine eingebettete Karte fehlt hier bewusst: sie würde beim Aufruf
            Daten an einen fremden Anbieter senden, bevor jemand eingewilligt
            hat. Der Link darunter wird erst auf Klick geöffnet.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-6)">
            <a class="knopf knopf--glas" href="https://www.openstreetmap.org/search?query=Lister%20Meile%2048%2C%2030161%20Hannover" rel="noopener">
              In der Karte öffnen
            </a>
          </p>
        </div>
      </div>
    </section>
""",
    },
}

def strecke(*eintraege):
    karten = []
    for name, titel, zeile in eintraege:
        karten.append(
            '<div class="scharfstellen">'
            + rahmen(name, "bild--3-2",
                     "(max-width: 620px) 88vw, (max-width: 900px) 44vw, 30vw")
            + f'<p class="bildzeile"><b>{titel}</b><span>{zeile}</span></p>'
            + "</div>"
        )
    return '<div class="spalten spalten--3">' + "".join(karten) + "</div>"


MARKEN = {
    "__STRECKE_BEHANDLUNGEN__": lambda: strecke(
        ("produkte-ablage", "Ablage", "nur das, was gebraucht wird"),
        ("detail-haende", "Maniküre", "Naturlack, kein Gel"),
        ("ruhe-kerzen", "Ruhe", "kein Radio, kein Bildschirm"),
    ),
    "__STRECKE_PREISE__": lambda: strecke(
        ("produkte-flaschen", "Pflege", "zwei Linien, mehr nicht"),
        ("behandlung-pflege", "Abschluss", "Creme statt Verkaufsgespräch"),
        ("ruhe-handtuecher", "Frisch bezogen", "nach jedem Termin"),
    ),
    "__STRECKE_KONTAKT__": lambda: strecke(
        ("studio-raum", "Der Raum", "zwei Plätze, Tageslicht"),
        ("portraet-zweit", "Mira Kalb", "seit 2022 im Studio"),
        ("produkte-pinsel", "Werkzeug", "nach jedem Termin gereinigt"),
    ),
    "__BILD_PORTRAET__": lambda: rahmen(
        "portraet-team", "bild--4-5", "(max-width: 900px) 88vw, 46vw"
    ),
    "__BILD_SPIEGEL__": lambda: rahmen(
        "studio-spiegel", "bild--4-5", "(max-width: 760px) 44vw, 30vw"
    ),
    "__BILD_KERZEN__": lambda: rahmen(
        "ruhe-kerzen", "bild--3-2", "(max-width: 760px) 44vw, 30vw"
    ),
    "__BILD_HAENDE__": lambda: rahmen(
        "detail-haende", "bild--3-2", "(max-width: 760px) 90vw, 30vw"
    ),
}

def bauen() -> None:
    if not BILDER:
        print("WARNUNG: bilder/nachweise.json fehlt.")
        print("         Erst scripts/bilder-holen.py laufen lassen.\n")

    for slug, seite in SEITEN.items():
        inhalt = seite["inhalt"]
        for marke, bauer in MARKEN.items():
            if marke in inhalt:
                inhalt = inhalt.replace(marke, bauer())

        ziel = WURZEL / slug / "index.html"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(
            kopf(slug, seite["titel"], seite["beschreibung"]) + inhalt + FUSS,
            encoding="utf-8",
        )
        print(f"geschrieben: {ziel.relative_to(WURZEL)}")

if __name__ == "__main__":
    bauen()
    print("\nImpressum und Datenschutz werden NICHT erzeugt — sie stehen von Hand,")
    print("damit kein Generator versehentlich eine Pflichtangabe umschreibt.")
