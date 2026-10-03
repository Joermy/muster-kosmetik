window.BEHANDLUNGEN = [
  {
    name: "Klassische Gesichtsbehandlung",
    bild: "behandlung-gesicht",
    dauer: 60,
    bereich: "gesicht",
    zeit: "mittel",
    anlass: "regelmaessig",
    text:
      "Reinigung, Peeling, Ausreinigung nach Bedarf, Maske und Abschluss­pflege. " +
      "Die Grundbehandlung, auf der alles andere aufbaut.",
    marken: ["Reinigung", "Peeling", "Maske"],
  },
  {
    name: "Intensivbehandlung",
    bild: "behandlung-maske",
    dauer: 90,
    bereich: "gesicht",
    zeit: "lang",
    anlass: "besonders",
    text:
      "Wie die klassische Behandlung, zusätzlich mit Massage von Gesicht, " +
      "Hals und Dekolleté sowie einer zweiten, länger einwirkenden Maske.",
    marken: ["Massage", "Zwei Masken", "Dekolleté"],
  },
  {
    name: "Kurze Auffrischung",
    bild: "behandlung-reinigung",
    dauer: 30,
    bereich: "gesicht",
    zeit: "kurz",
    anlass: "zwischendurch",
    text:
      "Reinigung, leichtes Peeling, Pflege. Gedacht für die Mittagspause " +
      "oder vor einem Termin am Abend.",
    marken: ["Reinigung", "Peeling"],
  },
  {
    name: "Pflege für empfindliche Haut",
    bild: "behandlung-pflege",
    dauer: 60,
    bereich: "gesicht",
    zeit: "mittel",
    anlass: "regelmaessig",
    text:
      "Ohne Ausreinigung, ohne Dampf, mit ruhigen Produkten. " +
      "Wir nehmen dafür die Linie ohne Duftstoffe.",
    marken: ["Ohne Dampf", "Ruhig"],
  },
  {
    name: "Maniküre",
    bild: "behandlung-naegel",
    dauer: 45,
    bereich: "haende",
    zeit: "mittel",
    anlass: "regelmaessig",
    text:
      "Nägel kürzen und in Form bringen, Nagelhaut zurückschieben, " +
      "Handbad, Pflege. Auf Wunsch mit Lack.",
    marken: ["Form", "Nagelhaut", "Lack optional"],
  },
  {
    name: "Wimpern und Brauen",
    bild: "behandlung-wimpern",
    dauer: 45,
    bereich: "augen",
    zeit: "mittel",
    anlass: "besonders",
    text:
      "Brauen in Form bringen, auf Wunsch färben, Wimpern färben. " +
      "Verlängerung nach Absprache und mit eigenem Termin.",
    marken: ["Form", "Färben", "Nach Absprache"],
  },
];

window.FINDER = [
  {
    feld: "bereich",
    frage: "Worum soll es gehen?",
    optionen: [
      { wert: "", text: "Egal" },
      { wert: "gesicht", text: "Gesicht" },
      { wert: "haende", text: "Hände" },
      { wert: "augen", text: "Augen und Brauen" },
    ],
  },
  {
    feld: "zeit",
    frage: "Wie viel Zeit haben Sie?",
    optionen: [
      { wert: "", text: "Egal" },
      { wert: "kurz", text: "Eine halbe Stunde" },
      { wert: "mittel", text: "Etwa eine Stunde" },
      { wert: "lang", text: "Anderthalb Stunden" },
    ],
  },
  {
    feld: "anlass",
    frage: "Was ist der Anlass?",
    optionen: [
      { wert: "", text: "Egal" },
      { wert: "zwischendurch", text: "Zwischendurch" },
      { wert: "regelmaessig", text: "Regelmäßige Pflege" },
      { wert: "besonders", text: "Ein besonderer Termin" },
    ],
  },
];

window.ABLAUF = [
  {
    titel: "Termin vereinbaren",
    text:
      "Telefonisch oder per E-Mail. Sagen Sie kurz, worum es gehen soll — " +
      "danach richtet sich, wie viel Zeit eingeplant wird.",
  },
  {
    titel: "Kurzes Gespräch",
    text:
      "Vor der ersten Behandlung sprechen wir über Hautzustand, Allergien, " +
      "Medikamente und darüber, was Sie bisher benutzen.",
  },
  {
    titel: "Behandlung",
    text:
      "Die vereinbarte Zeit gehört Ihnen. Es wird nichts dazugebucht, was " +
      "nicht vorher besprochen war.",
  },
  {
    titel: "Danach",
    text:
      "Sie bekommen gesagt, worauf Sie in den nächsten Tagen achten sollten. " +
      "Produkte verkaufen wir nur, wenn Sie danach fragen.",
  },
];
