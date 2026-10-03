#!/usr/bin/env python3

import importlib.util
import pathlib
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location("sb", WURZEL / "scripts" / "seiten-bauen.py")
sb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sb)

def block(titel, *absaetze):
    zeilen = []
    for i, text in enumerate(absaetze):
        stil = ' style="margin-top:var(--sp-4)"' if i else ""
        zeilen.append(f"            <p{stil}>{text}</p>")
    return (
        "          <div>\n"
        f'            <h2 style="font-size:var(--fs-h3);margin-bottom:var(--sp-3)">{titel}</h2>\n'
        + "\n".join(zeilen)
        + "\n          </div>"
    )

def seite(slug, titel, spaltentitel, lead, bloecke):
    inhalt = f"""
    <section class="hero breite">
      <p class="etikett einblenden">Pflichtangaben</p>
      <h1 style="font-size:var(--fs-h2)">{titel}</h1>
      <p class="hero__lead einblenden">{lead}</p>
    </section>

    <section class="abschnitt breite">
      <div class="gespann">
        <div class="gespann__fest">
          <p class="etikett">{spaltentitel}</p>
        </div>
        <div style="display:grid;gap:var(--sp-8)">
{bloecke}
        </div>
      </div>
    </section>
"""
    ziel = WURZEL / slug / "index.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(
        sb.kopf("", titel, spaltentitel) + inhalt + sb.FUSS, encoding="utf-8"
    )
    print(f"geschrieben: {slug}/index.html")

NACHWEISBLOCK = """          <div>
            <h2 style="font-size:var(--fs-h3);margin-bottom:var(--sp-3)">Nachweise und Lizenzen</h2>
            <dl>
              <dt><strong>Schrift &bdquo;Syne&ldquo;</strong></dt>
              <dd style="margin:0 0 var(--sp-4)">
                SIL Open Font License 1.1. Lokal eingebunden, kein CDN.
                Lizenztext: <a href="../assets/fonts/OFL-Syne.txt">OFL-Syne.txt</a>
              </dd>
              <dt><strong>Schrift &bdquo;Outfit&ldquo;</strong></dt>
              <dd style="margin:0 0 var(--sp-4)">
                SIL Open Font License 1.1. Lokal eingebunden, kein CDN.
                Lizenztext: <a href="../assets/fonts/OFL-Outfit.txt">OFL-Outfit.txt</a>
              </dd>
            <!-- NACHWEISE:ANFANG -->
            <!-- NACHWEISE:ENDE -->
            </dl>
          </div>"""

def impressum():
    return "\n".join([
        block(
            "Angaben gem&auml;&szlig; &sect; 5 DDG",
            "Studio Leyla &mdash; Inhaberin Leyla Demir<br>"
            "Lister Meile 48<br>"
            "30161 Hannover",
            "Vertreten durch: Leyla Demir",
        ),
        block(
            "Kontakt",
            "Telefon: 0511 39 24 0<br>"
            "E-Mail: termin@studio-leyla.de",
        ),
        block(
            "Berufsrechtliche Angaben",
            "Kosmetik ist ein zulassungsfreies Handwerk (Anlage B1 der "
            "Handwerksordnung). Erforderlich ist die Eintragung in das "
            "Verzeichnis der zulassungsfreien Handwerke bei der zust&auml;ndigen "
            "Handwerkskammer.",
            "Zust&auml;ndige Handwerkskammer: Handwerkskammer Hannover, Berliner Allee 17, 30175 Hannover<br>"
            "Verzeichnisnummer: 41 2087",
            "Angeboten werden ausschlie&szlig;lich kosmetische Behandlungen. "
            "Medizinische Fu&szlig;pflege und andere heilkundliche Leistungen "
            "geh&ouml;ren nicht dazu.",
        ),
        block(
            "Umsatzsteuer",
            "Als Kleinunternehmerin nach &sect; 19 Umsatzsteuergesetz wird keine "
            "Umsatzsteuer berechnet und keine Umsatzsteuer-Identifikationsnummer "
            "gef&uuml;hrt.",
        ),
        block(
            "Verantwortlich f&uuml;r den Inhalt nach &sect; 18 Abs. 2 MStV",
            "Leyla Demir<br>Lister Meile 48, 30161 Hannover",
        ),
        block(
            "Werbung mit kosmetischen Aussagen",
            "F&uuml;r Aussagen &uuml;ber kosmetische Mittel gelten die "
            "EU-Kosmetikverordnung (EG) Nr. 1223/2009 und die Verordnung (EU) "
            "Nr. 655/2013 &uuml;ber Werbeaussagen. Aussagen m&uuml;ssen wahr, "
            "belegbar und redlich sein; Wirkungen d&uuml;rfen nicht versprochen "
            "werden, die nicht belegt sind.",
            "Diese Seite beschreibt deshalb, <em>was gemacht wird</em>, und nicht, "
            "was es bewirken soll. Vorher-Nachher-Bilder gibt es aus demselben "
            "Grund nicht.",
            "Wer eine Hauterkrankung hat, geh&ouml;rt zur Haut&auml;rztin oder "
            "zum Hautarzt. Wir sagen das offen, wenn wir der falsche Ort sind.",
        ),
        block(
            "Streitschlichtung",
            "Wir sind nicht verpflichtet und nicht bereit, an "
            "Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle "
            "teilzunehmen (&sect; 36 Verbraucherstreitbeilegungsgesetz).",
            '<span style="color:var(--muted);font-size:var(--fs-meta)">Die '
            "Online-Streitbeilegungs-Plattform der Europ&auml;ischen Kommission "
            "wurde zum 20. Juli 2025 eingestellt. Ein Verweis darauf "
            "entf&auml;llt deshalb.</span>",
        ),
        block(
            "Haftung f&uuml;r Inhalte und Links",
            "Trotz sorgf&auml;ltiger inhaltlicher Kontrolle &uuml;bernehmen wir "
            "keine Haftung f&uuml;r die Inhalte externer Links. F&uuml;r den Inhalt "
            "der verlinkten Seiten sind ausschlie&szlig;lich deren Betreiber "
            "verantwortlich.",
        ),
        NACHWEISBLOCK,
    ])

def datenschutz():
    return "\n".join([
        block(
            "Verantwortliche Stelle",
            "Leyla Demir<br>Lister Meile 48, 30161 Hannover<br>"
            "E-Mail: termin@studio-leyla.de",
        ),
        block(
            "Keine Cookies, kein Tracking",
            "Diese Website setzt keine Cookies, keine Analyse- oder "
            "Tracking-Software und keine Social-Media-Plug-ins ein. Es gibt kein "
            "Einwilligungsbanner, weil es nichts gibt, wof&uuml;r eine Einwilligung "
            "n&ouml;tig w&auml;re.",
        ),
        block(
            "Kein Buchungssystem",
            "Termine werden telefonisch oder per E-Mail vereinbart. Ein "
            "Online-Buchungssystem w&uuml;rde personenbezogene Daten an einen "
            "Dienstleister &uuml;bermitteln und einen Vertrag zur "
            "Auftragsverarbeitung nach Art. 28 DSGVO n&ouml;tig machen. Beides gibt "
            "es hier nicht.",
        ),
        block(
            "Keine externen Ressourcen",
            "Alle Schriften, Skripte und Bilder werden von diesem Server "
            "ausgeliefert. Es werden keine Inhalte von fremden Domains nachgeladen "
            "&mdash; auch keine Schriften und keine Karten. Diese Aussage wird vor "
            "jeder Ver&ouml;ffentlichung maschinell gepr&uuml;ft.",
            "Das gilt ausdr&uuml;cklich auch f&uuml;r die Fotos: sie stammen zwar "
            "von einem Bilddienst, wurden aber heruntergeladen und liegen auf "
            "diesem Server. Urheber und Lizenz stehen im "
            '<a href="../impressum/index.html">Impressum</a>.',
        ),
        block(
            "Server-Logdateien",
            "Diese Seite wird &uuml;ber GitHub Pages, einen Dienst der GitHub, Inc., "
            "88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA, ausgeliefert. Beim Aufruf verarbeitet der Hoster automatisch "
            "technische Zugriffsdaten &mdash; unter anderem IP-Adresse, Datum und "
            "Uhrzeit des Zugriffs, aufgerufene Datei und User-Agent.",
            "Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Das berechtigte "
            "Interesse liegt im technisch fehlerfreien Betrieb und in der Sicherheit "
            "der Website.",
            "Dabei werden Daten in die USA &uuml;bermittelt. GitHub, Inc. ist nach dem "
            "EU-US Data Privacy Framework zertifiziert; die &Uuml;bermittlung st&uuml;tzt sich "
            "auf den Angemessenheitsbeschluss der Europ&auml;ischen Kommission nach Art. 45 DSGVO. "
            "Auf Art und Dauer der Speicherung der Logdateien bei GitHub haben wir keinen Einfluss.",
        ),
        block(
            "Daten aus dem Beratungsgespr&auml;ch",
            "Vor einer Behandlung werden Angaben zu Hautzustand, Allergien und "
            "Medikamenten erfragt. Das sind <strong>Gesundheitsdaten</strong> im "
            "Sinne des Art. 9 DSGVO und damit besonders gesch&uuml;tzt. Sie werden "
            "nur mit ausdr&uuml;cklicher Einwilligung nach Art. 9 Abs. 2 lit. a "
            "DSGVO erhoben, ausschlie&szlig;lich zur Durchf&uuml;hrung der "
            "Behandlung verwendet und nicht weitergegeben.",
            "Festgehalten wird nur, was f&uuml;r die n&auml;chste Behandlung "
            "gebraucht wird: eine Karteikarte aus Papier, im abgeschlossenen "
            "Schrank im Studio, zug&auml;nglich allein f&uuml;r Leyla Demir und "
            "Mira Kalb. Die Einwilligung wird auf derselben Karte unterschrieben. "
            "Nach drei Jahren ohne Termin wird die Karte vernichtet. Eine "
            "digitale Speicherung dieser Angaben findet nicht statt.",
        ),
        block(
            "Kontaktaufnahme",
            "Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir die "
            "dabei &uuml;bermittelten Angaben ausschlie&szlig;lich zur Bearbeitung "
            "Ihrer Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b beziehungsweise "
            "lit. f DSGVO. Diese Website enth&auml;lt kein Kontaktformular.",
        ),
        block(
            "Speicherdauer",
            "Anfragen bewahren wir so lange auf, wie es zur Bearbeitung n&ouml;tig "
            "ist, dar&uuml;ber hinaus nur, soweit gesetzliche Aufbewahrungsfristen es "
            "verlangen. Auf die Speicherdauer der Server-Logdateien beim "
            "Hosting-Anbieter haben wir keinen Einfluss.",
        ),
        block(
            "Ihre Rechte",
            "Sie haben das Recht auf Auskunft, Berichtigung, L&ouml;schung, "
            "Einschr&auml;nkung der Verarbeitung, Daten&uuml;bertragbarkeit und "
            "Widerspruch bez&uuml;glich Ihrer bei uns gespeicherten "
            "personenbezogenen Daten sowie das Recht auf Beschwerde bei einer "
            "Datenschutzaufsichtsbeh&ouml;rde (Art. 77 DSGVO). Eine erteilte "
            "Einwilligung k&ouml;nnen Sie jederzeit mit Wirkung f&uuml;r die Zukunft "
            "widerrufen.",
        ),
        block(
            "Keine automatisierte Entscheidungsfindung",
            "Es findet keine automatisierte Entscheidungsfindung einschlie&szlig;lich "
            "Profiling nach Art. 22 DSGVO statt. Die Auswahlhilfe auf dieser Seite "
            "l&auml;uft vollst&auml;ndig im Browser; es wird nichts gesendet und "
            "nichts gespeichert.",
        ),
    ])

def main():
    ueberschreiben = "--ueberschreiben" in sys.argv
    vorhanden = [
        s for s in ("impressum", "datenschutz")
        if (WURZEL / s / "index.html").exists()
    ]
    if vorhanden and not ueberschreiben:
        print("Diese Rechtsseiten gibt es schon:", ", ".join(vorhanden))
        print("Sie werden von Hand gepflegt. Zum Ueberschreiben:")
        print("  python scripts/rechtsseiten-bauen.py --ueberschreiben")
        return 1

    seite(
        "impressum",
        "Impressum",
        "Anbieter",
        "Angaben gem&auml;&szlig; &sect; 5 Digitale-Dienste-Gesetz (DDG).",
        impressum(),
    )
    seite(
        "datenschutz",
        "Datenschutz",
        "DSGVO",
        "Diese Seite l&auml;dt nichts von Dritten nach, setzt keine Cookies und "
        "betreibt kein Tracking.",
        datenschutz(),
    )
    print("\nAb jetzt von Hand pflegen. Dieses Skript nicht erneut laufen lassen.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
