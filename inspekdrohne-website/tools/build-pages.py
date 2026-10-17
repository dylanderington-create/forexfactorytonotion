#!/usr/bin/env python3
"""Erzeugt die Unterseiten (Impressum, Datenschutz, AGB, Danke, 404) mit gemeinsamem Kopf und Fuß.
Aufruf aus dem Projektordner:  python3 tools/build-pages.py
Texte ändern: unten in PAGES bearbeiten und Skript erneut ausführen."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.inspekdrohne.de"
STAND = "Oktober 2026"

ADDR = "Sezer Özgüden<br>Inspekdrohne – Luftbildaufnahmen<br>Am Sandbuckel 6<br>68809 Neulußheim"
CONTACT = ('Telefon: <a href="tel:+4962053646528">06205 3646528</a><br>'
           'Mobil: <a href="tel:+4917622678053">0176 22678053</a><br>'
           'E-Mail: <a href="mailto:info@swg-dachbau.de">info@swg-dachbau.de</a>')


def head(title, desc, path, index=True):
    robots = "index,follow" if index else "noindex,follow"
    canon = f'<link rel="canonical" href="{SITE}{path}">\n' if index else ""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{canon}<meta name="robots" content="{robots}">
<meta name="theme-color" content="#07090c">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Inspekdrohne">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/big-shoulders-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="nav solid" id="nav">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Inspekdrohne – zur Startseite"><img src="/assets/img/logo.svg" alt="Inspekdrohne" width="113" height="58"></a>
    <nav aria-label="Hauptnavigation"><ul id="menu">
      <li><a href="/#leistungen">Leistungen</a></li>
      <li><a href="/#waermebild">Wärmebild</a></li>
      <li><a href="/#ablauf">Ablauf</a></li>
      <li><a href="/#gebiet">Einsatzgebiet</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="/#kontakt">Kontakt</a></li>
    </ul></nav>
    <a class="btn cta-top" href="/#kontakt">Flug anfragen <span class="arr">→</span></a>
    <button class="burger" id="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>
"""


FOOT = """
<footer>
  <div class="wrap">
    <div class="cols">
      <a class="flogo" href="/" aria-label="Inspekdrohne – zur Startseite"><img src="/assets/img/logo.svg" alt="Inspekdrohne" width="125" height="64" loading="lazy"></a>
      <address>Inspekdrohne · Sezer Özgüden<br>Am Sandbuckel 6, 68809 Neulußheim<br><a href="tel:+4962053646528">06205 3646528</a> · <a href="mailto:info@swg-dachbau.de">info@swg-dachbau.de</a></address>
    </div>
    <div class="legal">
      <small>© 2026 Inspekdrohne · Drohnenservice im Rhein-Neckar-Kreis</small>
      <nav aria-label="Rechtliches"><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a><a href="/agb">AGB</a><button type="button" class="consent-link">Cookie-Einstellungen</button></nav>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def legal(eyebrow, h1, inner):
    return f"""<main id="main" class="page">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <div class="prose">
{inner}
    </div>
  </div>
</main>"""


IMPRESSUM = f"""
<h2>Angaben gemäß § 5 DDG</h2>
<address><p>{ADDR}</p></address>

<h2>Kontakt</h2>
<p>{CONTACT}</p>

<h2>Verantwortlich für den Inhalt</h2>
<p>Verantwortlich nach § 18 Abs. 2 MStV:<br>Sezer Özgüden, Am Sandbuckel 6, 68809 Neulußheim</p>

<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>

<h2>Haftung für Inhalte</h2>
<p>Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.</p>
<p>Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden entsprechender Rechtsverletzungen entfernen wir diese Inhalte umgehend.</p>

<h2>Haftung für Links</h2>
<p>Unser Angebot enthält gegebenenfalls Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für diese fremden Inhalte übernehmen wir keine Gewähr. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entfernen wir derartige Links umgehend.</p>

<h2>Urheberrecht</h2>
<p>Die durch den Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des Autors bzw. Erstellers. Die Wärmebild- und Dachdarstellungen auf der Startseite sind eigene, schematische Grafiken.</p>
"""

DATENSCHUTZ = f"""
<p class="meta">Stand: {STAND}</p>

<h2>1. Verantwortlicher</h2>
<p>Verantwortlich für die Datenverarbeitung auf dieser Website im Sinne der Datenschutz-Grundverordnung (DSGVO) ist:</p>
<address><p>{ADDR}<br>{CONTACT}</p></address>

<h2>2. Das Wichtigste in Kürze</h2>
<ul>
  <li>Diese Website setzt <strong>keine Cookies</strong> und verwendet derzeit <strong>keine Analyse- oder Tracking-Dienste</strong>. Optionale Dienste würden erst nach Ihrer Zustimmung im Cookie-Banner geladen.</li>
  <li>Schriften, Grafiken und Skripte liegen auf unserem eigenen Server. Beim Aufruf werden <strong>keine Daten an Google oder andere Drittanbieter</strong> übertragen.</li>
  <li>Personenbezogene Daten verarbeiten wir nur, wenn Sie uns kontaktieren oder einen Auftrag erteilen.</li>
</ul>

<h2>3. Hosting und Server-Logfiles</h2>
<p>Diese Website wird bei Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA gehostet. Beim Aufruf der Website verarbeitet der Hoster automatisch Informationen, die Ihr Browser übermittelt (Server-Logfiles):</p>
<ul>
  <li>IP-Adresse des anfragenden Geräts</li>
  <li>Datum und Uhrzeit des Zugriffs</li>
  <li>aufgerufene Seite bzw. Datei und übertragene Datenmenge</li>
  <li>Referrer-URL (die zuvor besuchte Seite)</li>
  <li>verwendeter Browser und Betriebssystem</li>
</ul>
<p>Die Verarbeitung ist erforderlich, um die Website auszuliefern, ihre Stabilität und Sicherheit zu gewährleisten und Angriffe abzuwehren. Rechtsgrundlage ist unser berechtigtes Interesse nach Art. 6 Abs. 1 lit. f DSGVO. Die Logfiles werden vom Hoster nur kurzfristig gespeichert und anschließend gelöscht.</p>
<p>Mit Vercel besteht ein Vertrag zur Auftragsverarbeitung (Art. 28 DSGVO). Vercel ist nach dem EU-US Data Privacy Framework zertifiziert; damit liegt für Übermittlungen in die USA ein Angemessenheitsbeschluss der EU-Kommission vor (Art. 45 DSGVO). Ergänzend gelten die EU-Standardvertragsklauseln. Weitere Informationen: <a href="https://vercel.com/legal/privacy-policy" rel="noopener">vercel.com/legal/privacy-policy</a>.</p>

<h2>4. Kontaktaufnahme</h2>
<p>Wenn Sie uns per E-Mail, Telefon oder über das Anfrageformular kontaktieren, verarbeiten wir die von Ihnen mitgeteilten Daten (z. B. Name, E-Mail-Adresse oder Telefonnummer, Angaben zum Objekt und Ihre Nachricht), um Ihre Anfrage zu bearbeiten und Ihnen ein Angebot zu erstellen.</p>
<p><strong>Anfrageformular:</strong> Das Formular verschickt derzeit keine Daten über unseren Server. Nach dem Absenden öffnet sich Ihr eigenes E-Mail-Programm mit einer vorausgefüllten Nachricht an uns. Erst wenn Sie diese E-Mail selbst absenden, erhalten wir Ihre Angaben. Der Versand erfolgt dann über Ihren E-Mail-Anbieter.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, soweit Ihre Anfrage auf einen Vertrag abzielt, und im Übrigen unser berechtigtes Interesse an der Beantwortung von Anfragen (Art. 6 Abs. 1 lit. f DSGVO). Wir löschen Ihre Daten, sobald die Anfrage abschließend bearbeitet ist, es sei denn, gesetzliche Aufbewahrungspflichten (z. B. sechs bzw. zehn Jahre für Geschäftsbriefe und Rechnungen nach HGB und AO) stehen dem entgegen.</p>

<h2>5. Durchführung von Drohnenflügen</h2>
<p>Bei Aufträgen erstellen wir Foto-, Video-, Wärmebild- und Vermessungsaufnahmen des vereinbarten Objekts. Dabei achten wir darauf, keine unbeteiligten Personen, Nachbargrundstücke oder Kfz-Kennzeichen erkennbar aufzunehmen. Lässt sich dies im Einzelfall nicht vermeiden, werden solche Inhalte vor der Weitergabe unkenntlich gemacht oder gelöscht. Rechtsgrundlage ist die Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO) sowie unser berechtigtes Interesse an einer ordnungsgemäßen Auftragsdurchführung (Art. 6 Abs. 1 lit. f DSGVO). Rohdaten bewahren wir in der Regel drei Monate nach Abschluss des Auftrags auf und löschen sie anschließend, sofern nichts anderes vereinbart ist.</p>

<h2>6. Cookie-Banner und Speicherung im Browser</h2>
<p>Diese Website setzt keine Cookies. Um Ihre Auswahl im Cookie-Banner zu speichern, legen wir im lokalen Speicher Ihres Browsers (Local Storage) den Eintrag „inspek-consent“ ab. Er enthält nur Ihre Entscheidung und das Datum, wird nicht an uns oder Dritte übertragen und bleibt gespeichert, bis Sie ihn in Ihrem Browser löschen. Diese Speicherung ist technisch erforderlich, damit der Banner Ihre Wahl respektiert (§ 25 Abs. 2 Nr. 2 TDDDG); Rechtsgrundlage ist Art. 6 Abs. 1 lit. c DSGVO in Verbindung mit Art. 7 Abs. 1 DSGVO.</p>
<p>Optionale Dienste wie Statistik werden ausschließlich nach Ihrer Einwilligung geladen (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 lit. a DSGVO). Derzeit setzen wir keine solchen Dienste ein. Sie können Ihre Auswahl jederzeit über den Link „Cookie-Einstellungen“ im Seitenfuß ändern oder widerrufen.</p>

<h2>7. SSL/TLS-Verschlüsselung</h2>
<p>Diese Website nutzt aus Sicherheitsgründen eine SSL/TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie an „https://“ in der Adresszeile Ihres Browsers.</p>

<h2>8. Ihre Rechte</h2>
<p>Sie haben jederzeit das Recht auf:</p>
<ul>
  <li>Auskunft über Ihre bei uns gespeicherten Daten (Art. 15 DSGVO)</li>
  <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
  <li>Löschung (Art. 17 DSGVO)</li>
  <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
  <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
  <li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO)</li>
</ul>
<p><strong>Widerspruchsrecht (Art. 21 DSGVO):</strong> Soweit wir Daten auf Grundlage berechtigter Interessen verarbeiten, können Sie dieser Verarbeitung aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit widersprechen.</p>
<p>Für alle Anliegen genügt eine formlose Nachricht an <a href="mailto:info@swg-dachbau.de">info@swg-dachbau.de</a>.</p>

<h2>9. Beschwerderecht</h2>
<p>Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Für uns zuständig ist: Der Landesbeauftragte für den Datenschutz und die Informationsfreiheit Baden-Württemberg, Lautenschlagerstraße 20, 70173 Stuttgart, <a href="https://www.baden-wuerttemberg.datenschutz.de" rel="noopener">www.baden-wuerttemberg.datenschutz.de</a>.</p>

<h2>10. Pflicht zur Bereitstellung, automatisierte Entscheidungen</h2>
<p>Sie sind nicht verpflichtet, uns personenbezogene Daten bereitzustellen. Ohne Kontaktdaten können wir Ihre Anfrage jedoch nicht beantworten. Eine automatisierte Entscheidungsfindung einschließlich Profiling findet nicht statt.</p>

<h2>11. Änderungen</h2>
<p>Wir passen diese Datenschutzerklärung an, wenn sich die Website oder die eingesetzten Dienste ändern. Es gilt die jeweils hier veröffentlichte Fassung.</p>
"""

AGB = f"""
<p class="meta">Allgemeine Geschäftsbedingungen von Inspekdrohne – Sezer Özgüden, Am Sandbuckel 6, 68809 Neulußheim (nachfolgend „Auftragnehmer“). Stand: {STAND}</p>

<h2>§ 1 Geltungsbereich</h2>
<p>(1) Diese AGB gelten für alle Verträge über Drohnen-Dienstleistungen des Auftragnehmers, insbesondere Inspektionen, Thermografie, Vermessung, Baustellendokumentation sowie Foto- und Videoaufnahmen aus der Luft. Sie gelten gegenüber Verbrauchern (§ 13 BGB) und Unternehmern (§ 14 BGB), soweit nachfolgend nicht unterschieden wird.</p>
<p>(2) Abweichende Bedingungen des Auftraggebers gelten nur, wenn der Auftragnehmer ihnen ausdrücklich in Textform zustimmt.</p>

<h2>§ 2 Angebot und Vertragsschluss</h2>
<p>(1) Darstellungen auf der Website sind kein verbindliches Angebot. Auf Anfrage erstellt der Auftragnehmer ein individuelles Angebot, an das er 30 Tage gebunden ist, sofern im Angebot nichts anderes angegeben ist.</p>
<p>(2) Der Vertrag kommt zustande, wenn der Auftraggeber das Angebot in Textform (z. B. per E-Mail) annimmt oder der Auftragnehmer einen Auftrag in Textform bestätigt.</p>

<h2>§ 3 Leistungsumfang</h2>
<p>(1) Art, Umfang, Ort und Ergebnisformat der Leistung ergeben sich aus dem Angebot bzw. der Auftragsbestätigung.</p>
<p>(2) Inspektions- und Wärmebildaufnahmen dokumentieren den sichtbaren bzw. thermischen Zustand zum Zeitpunkt der Befliegung. Sie ersetzen kein Sachverständigengutachten, keine Bauteilöffnung und keine statische oder energetische Fachplanung, sofern dies nicht ausdrücklich vereinbart ist. Thermografische Auffälligkeiten sind Hinweise, die gegebenenfalls von einem Fachbetrieb vor Ort zu prüfen sind.</p>
<p>(3) Vermessungsergebnisse werden mit der im Angebot genannten bzw. für das Verfahren üblichen Genauigkeit geliefert. Eine amtliche Vermessung ist nicht geschuldet.</p>
<p>(4) Der Auftragnehmer darf zur Leistungserbringung qualifizierte Subunternehmer einsetzen.</p>

<h2>§ 4 Mitwirkungspflichten des Auftraggebers</h2>
<p>(1) Der Auftraggeber stellt sicher, dass er zur Beauftragung von Aufnahmen des Objekts berechtigt ist, und holt, soweit erforderlich, die Zustimmung von Eigentümern, Mietern oder Betreibern ein.</p>
<p>(2) Er ermöglicht zum vereinbarten Termin den Zugang zu einer geeigneten Start- und Landefläche und weist auf besondere Gefahren hin (z. B. Stromleitungen, Kräne, laufender Betrieb, Tiere).</p>
<p>(3) Für Wärmebildaufnahmen schafft er die vereinbarten Rahmenbedingungen (z. B. beheizte Innenräume, Anlage in Betrieb).</p>
<p>(4) Verzögerungen oder Mehraufwand aufgrund fehlender Mitwirkung kann der Auftragnehmer gesondert berechnen.</p>

<h2>§ 5 Flugdurchführung, Wetter, behördliche Vorgaben</h2>
<p>(1) Flüge erfolgen nach den geltenden luftrechtlichen Vorschriften. Die Entscheidung, ob, wann und wie ein Flug sicher durchgeführt werden kann, trifft allein der verantwortliche Fernpilot.</p>
<p>(2) Ist ein Flug wegen Wetter (z. B. Wind, Niederschlag, Nebel), behördlicher Anordnung, Flugbeschränkungen oder sonstiger Sicherheitsgründe nicht möglich, wird der Termin in Abstimmung mit dem Auftraggeber verschoben. Daraus entstehen dem Auftraggeber keine zusätzlichen Kosten; Ansprüche wegen der Verschiebung bestehen nicht.</p>
<p>(3) Erweist sich ein Flug wegen Umständen aus der Sphäre des Auftraggebers als unmöglich (z. B. fehlende Zustimmung, verweigerter Zugang), bleibt der Vergütungsanspruch für bereits erbrachte Leistungen und Anfahrt bestehen.</p>
<p>(4) Der Auftragnehmer unterhält die für den Betrieb unbemannter Fluggeräte vorgeschriebene Haftpflichtversicherung.</p>

<h2>§ 6 Termine und Absage</h2>
<p>(1) Termine werden einvernehmlich vereinbart.</p>
<p>(2) Sagt der Auftraggeber einen bestätigten Termin weniger als 48 Stunden vorher ab, kann der Auftragnehmer die bereits entstandenen Aufwendungen, insbesondere Anfahrt und Flugvorbereitung, oder eine im Angebot vereinbarte Ausfallpauschale berechnen. Dem Auftraggeber bleibt der Nachweis vorbehalten, dass kein oder ein geringerer Aufwand entstanden ist.</p>

<h2>§ 7 Vergütung und Zahlung</h2>
<p>(1) Es gelten die im Angebot genannten Preise. Gegenüber Verbrauchern angegebene Preise sind Endpreise.</p>
<p>(2) Rechnungen sind innerhalb von 14 Tagen nach Rechnungsdatum ohne Abzug zahlbar. Bei größeren Aufträgen kann eine angemessene Anzahlung vereinbart werden.</p>

<h2>§ 8 Nutzungsrechte an Aufnahmen</h2>
<p>(1) Mit vollständiger Bezahlung erhält der Auftraggeber an den gelieferten Aufnahmen ein einfaches, zeitlich und räumlich unbeschränktes Nutzungsrecht für den vereinbarten Zweck. Die Weitergabe an Dritte im Rahmen dieses Zwecks (z. B. an Handwerker, Gutachter, Versicherungen, Kaufinteressenten) ist gestattet.</p>
<p>(2) Eine darüber hinausgehende Nutzung, insbesondere die Veröffentlichung zu Werbezwecken, bedarf einer gesonderten Vereinbarung. Bei Veröffentlichung ist der Urheber nach Möglichkeit mit „Inspekdrohne“ zu nennen.</p>
<p>(3) Der Auftragnehmer verwendet Aufnahmen zu eigenen Referenz- oder Werbezwecken nur mit Zustimmung des Auftraggebers.</p>

<h2>§ 9 Datenlieferung und Aufbewahrung</h2>
<p>(1) Die Ergebnisse werden digital übermittelt, in der Regel per Download-Link. Der Auftraggeber sichert die Daten nach Erhalt selbst.</p>
<p>(2) Rohdaten bewahrt der Auftragnehmer in der Regel drei Monate nach Abschluss des Auftrags auf und löscht sie anschließend. Eine längere Archivierung ist nach Vereinbarung möglich.</p>

<h2>§ 10 Mängel</h2>
<p>(1) Offensichtliche Mängel der gelieferten Ergebnisse sollen innerhalb von 14 Tagen nach Lieferung mitgeteilt werden. Gesetzliche Rechte von Verbrauchern bleiben hiervon unberührt.</p>
<p>(2) Bei berechtigten Mängeln bessert der Auftragnehmer nach, etwa durch Nachbearbeitung oder eine erneute Befliegung. Schlägt die Nacherfüllung fehl, gelten die gesetzlichen Rechte.</p>

<h2>§ 11 Haftung</h2>
<p>(1) Der Auftragnehmer haftet unbeschränkt bei Vorsatz und grober Fahrlässigkeit, bei der Verletzung von Leben, Körper oder Gesundheit sowie nach dem Produkthaftungsgesetz.</p>
<p>(2) Bei leicht fahrlässiger Verletzung wesentlicher Vertragspflichten (Pflichten, deren Erfüllung die ordnungsgemäße Durchführung des Vertrags überhaupt erst ermöglicht und auf deren Einhaltung der Auftraggeber regelmäßig vertrauen darf) ist die Haftung auf den vertragstypischen, vorhersehbaren Schaden begrenzt. Im Übrigen ist die Haftung für leichte Fahrlässigkeit ausgeschlossen.</p>
<p>(3) Für Folgeschäden aus Entscheidungen, die der Auftraggeber allein auf Grundlage der Aufnahmen trifft, haftet der Auftragnehmer nur im Rahmen der Absätze 1 und 2.</p>

<h2>§ 12 Widerrufsrecht für Verbraucher</h2>
<p>Verbrauchern steht bei Verträgen, die ausschließlich über Fernkommunikationsmittel (z. B. E-Mail, Telefon) oder außerhalb von Geschäftsräumen geschlossen werden, ein gesetzliches Widerrufsrecht zu.</p>
<div class="notice">
<h3>Widerrufsbelehrung</h3>
<p><strong>Widerrufsrecht</strong><br>Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen. Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsabschlusses.</p>
<p>Um Ihr Widerrufsrecht auszuüben, müssen Sie uns (Inspekdrohne – Sezer Özgüden, Am Sandbuckel 6, 68809 Neulußheim, Telefon 06205 3646528, E-Mail info@swg-dachbau.de) mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief oder eine E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren. Sie können dafür das beigefügte Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.</p>
<p>Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.</p>
<p><strong>Folgen des Widerrufs</strong><br>Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von Ihnen erhalten haben, unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung Entgelte berechnet.</p>
<p>Haben Sie verlangt, dass die Dienstleistungen während der Widerrufsfrist beginnen sollen, so haben Sie uns einen angemessenen Betrag zu zahlen, der dem Anteil der bis zu dem Zeitpunkt, zu dem Sie uns von der Ausübung des Widerrufsrechts hinsichtlich dieses Vertrags unterrichten, bereits erbrachten Dienstleistungen im Vergleich zum Gesamtumfang der im Vertrag vorgesehenen Dienstleistungen entspricht.</p>
<p><strong>Ende der Belehrung</strong></p>
</div>
<h3>Muster-Widerrufsformular</h3>
<p>(Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses Formular aus und senden Sie es zurück.)</p>
<p>An Inspekdrohne – Sezer Özgüden, Am Sandbuckel 6, 68809 Neulußheim, E-Mail: info@swg-dachbau.de</p>
<p>Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag über die Erbringung der folgenden Dienstleistung (*)<br>
– Bestellt am (*) / erhalten am (*)<br>
– Name des/der Verbraucher(s)<br>
– Anschrift des/der Verbraucher(s)<br>
– Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier)<br>
– Datum</p>
<p>(*) Unzutreffendes streichen.</p>

<h2>§ 13 Schlussbestimmungen</h2>
<p>(1) Es gilt das Recht der Bundesrepublik Deutschland unter Ausschluss des UN-Kaufrechts. Gegenüber Verbrauchern gilt diese Rechtswahl nur, soweit dadurch nicht zwingende Schutzvorschriften des Staates ihres gewöhnlichen Aufenthalts entzogen werden.</p>
<p>(2) Ist der Auftraggeber Kaufmann, juristische Person des öffentlichen Rechts oder öffentlich-rechtliches Sondervermögen, ist Gerichtsstand der Sitz des Auftragnehmers.</p>
<p>(3) Sollten einzelne Bestimmungen unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.</p>
"""

DANKE = """<main id="main" class="page center-page">
  <div class="wrap">
    <p class="eyebrow">Anfrage</p>
    <h1>Danke. <span class="heat-text">Wir melden uns.</span></h1>
    <p id="via-mail" class="notice" hidden><strong>Fast geschafft:</strong> Ihr E-Mail-Programm sollte sich mit der fertigen Anfrage geöffnet haben. Bitte klicken Sie dort noch auf „Senden“. Falls sich nichts geöffnet hat, schreiben Sie uns direkt an <a href="mailto:info@swg-dachbau.de" style="color:var(--hot)">info@swg-dachbau.de</a>.</p>
    <p>Wir sehen uns Ihre Anfrage an und melden uns zeitnah mit Rückfragen oder einem Angebot. Wenn es eilt, erreichen Sie uns telefonisch unter <a href="tel:+4962053646528" style="color:var(--hot)">06205 3646528</a>.</p>
    <div class="actions"><a class="btn" href="/">Zur Startseite <span class="arr">→</span></a><a class="btn ghost" href="/#waermebild">Wärmebild ansehen</a></div>
  </div>
</main>"""

NOTFOUND = """<main id="main" class="page center-page">
  <div class="wrap">
    <span class="bignum heat-text" aria-hidden="true">404</span>
    <h1>Kein Signal.</h1>
    <p>Diese Seite gibt es nicht oder nicht mehr. Vielleicht war es ein alter Link unserer früheren Website.</p>
    <div class="actions"><a class="btn" href="/">Zur Startseite <span class="arr">→</span></a><a class="btn ghost" href="/#kontakt">Kontakt aufnehmen</a></div>
  </div>
</main>"""

PAGES = [
    ("impressum.html", "Impressum | Inspekdrohne", "Impressum von Inspekdrohne – Sezer Özgüden, Luftbildaufnahmen, Am Sandbuckel 6, 68809 Neulußheim.", "/impressum", True,
     legal("Rechtliches", "Impressum", IMPRESSUM)),
    ("datenschutz.html", "Datenschutzerklärung | Inspekdrohne", "Datenschutzerklärung von Inspekdrohne: keine Cookies, kein Tracking, Schriften lokal. Informationen zu Hosting, Kontaktaufnahme und Ihren Rechten.", "/datenschutz", True,
     legal("Rechtliches", "Datenschutz", DATENSCHUTZ)),
    ("agb.html", "AGB | Inspekdrohne", "Allgemeine Geschäftsbedingungen von Inspekdrohne für Drohneninspektion, Thermografie, Vermessung und Luftaufnahmen, inklusive Widerrufsbelehrung.", "/agb", True,
     legal("Rechtliches", "AGB", AGB)),
    ("danke.html", "Danke für Ihre Anfrage | Inspekdrohne", "Ihre Anfrage an Inspekdrohne ist eingegangen.", "/danke", False, DANKE),
    ("404.html", "Seite nicht gefunden | Inspekdrohne", "Diese Seite gibt es nicht. Zurück zur Startseite von Inspekdrohne.", "/404", False, NOTFOUND),
]

for fname, title, desc, path, index, main in PAGES:
    (ROOT / fname).write_text(head(title, desc, path, index) + main + FOOT, encoding="utf-8")
    print("geschrieben:", fname)
