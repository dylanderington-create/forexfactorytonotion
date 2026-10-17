# Inspekdrohne – Website

Statische Website, keine Datenbank und kein Build-Schritt. Auf Vercel als Projekt mit Framework-Preset **Other** anlegen. Die Einstellungen in `vercel.json` greifen automatisch: saubere URLs, Weiterleitungen und Sicherheits-Header.

## Inhalt

| Datei | Zweck |
|---|---|
| `index.html` | Startseite |
| `impressum.html`, `datenschutz.html`, `agb.html` | Rechtstexte (erreichbar als `/impressum`, `/datenschutz`, `/agb`) |
| `danke.html` | Danke-Seite nach dem Absenden des Formulars |
| `404.html` | Eigene Fehlerseite |
| `assets/` | CSS, JavaScript, Schriften (lokal), Logo, Icons, Vorschaubild für Social Media |
| `vercel.json` | Weiterleitungen (www, alte WordPress-Adressen), Sicherheits-Header, Caching |
| `robots.txt`, `sitemap.xml`, `site.webmanifest` | Suchmaschinen und App-Icons |
| `tools/build-pages.py` | Erzeugt die Unterseiten neu, wenn Texte in Impressum/Datenschutz/AGB geändert werden |

**Hinweis:** Die Slider-Fotos `assets/img/haus-tageslicht.webp` und `haus-waermebild.webp` (1600 × 900) sind in der ausgelieferten ZIP enthalten, aber nicht in diesem Repo.

`tools/` und diese README werden über `.vercelignore` nicht veröffentlicht.

## Stand der Checkliste

**Erledigt**
- Impressum (§ 5 DDG), Datenschutzerklärung (Hosting, Logfiles, Kontakt, Drohnenflüge, Rechte), AGB-Entwurf mit Widerrufsbelehrung
- Keine Cookies, kein Tracking, keine externen Verbindungen. Schriften und Skripte liegen lokal.
- Cookie-Banner („Nur notwendige“ / „Einstellungen“ / „Alle akzeptieren“, gleichwertige Buttons), jederzeit änderbar über „Cookie-Einstellungen“ im Footer. Optionale Dienste laden erst nach Zustimmung.
- Barrierefreiheit: Kontraste geprüft, Tastaturbedienung, Fokus-Rahmen, Skip-Link, Formular-Labels und Fehlermeldungen. Automatischer axe-Test (WCAG 2.1 AA) ohne Befund auf allen Seiten.
- Echte Kontaktdaten und Adresse
- Title und Description pro Seite, Open-Graph-/Twitter-Bild, Favicons, robots.txt, sitemap.xml, Canonical-Tags, genau eine H1 pro Seite, strukturierte Daten (LocalBusiness, WebSite, FAQPage), `lang="de"`
- 301-Weiterleitungen der alten Adressen (`/uber-uns/`, `/datenschutzrichtlinien/`, `/kontakt` …) . Die Hauptadresse ist www.inspekdrohne.de (Umleitung von inspekdrohne.de ohne www stellt Vercel unter Settings → Domains ein)
- CTA im sichtbaren Bereich, Mobile-Layouts, Kontakt-Leiste unten auf dem Handy, eigene 404-Seite, Formular-Fallback ohne JavaScript
- Sicherheits-Header (HSTS, CSP, X-Frame-Options …), Spamschutz im Formular (verstecktes Feld + Mindest-Ausfüllzeit), Danke-Seite

**Später (abgesprochen)**
1. **Formular-Versand:** In `assets/js/main.js` oben bei `FORM_ENDPOINT` und `FORM_KEY` eintragen (z. B. Web3Forms: `https://api.web3forms.com/submit` + Access-Key). Dann:
   - in `vercel.json` bei `connect-src` die Adresse ergänzen (z. B. `https://api.web3forms.com`)
   - in `datenschutz.html` Abschnitt 4 um den Dienst ergänzen
2. **Analytics:** In `assets/js/main.js` bei `SERVICES.statistik.load` das Lade-Skript eintragen (lädt nur nach Zustimmung), Text `desc` anpassen, Dienst in `vercel.json` (CSP) freigeben und in der Datenschutzerklärung (Abschnitt 6) nennen.
3. **Google Search Console** und **Google Business Profile** einrichten, Sitemap `https://inspekdrohne.de/sitemap.xml` einreichen.
4. **AGB** vor Veröffentlichung einmal anwaltlich prüfen lassen.
5. Social Proof (Referenzen, Kundenstimmen) und Social-Media-Links, sobald vorhanden.

## Lizenzen
Schriften: Big Shoulders Display, Archivo, JetBrains Mono (SIL Open Font License). Animationen: GSAP 3 (kostenlose Standardlizenz).
