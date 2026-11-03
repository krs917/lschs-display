# La Salle Daily Display

A full-screen 16:9 display for La Salle College High School's TVs and digital signage. It shows the letter day, bell schedule with a live "right now" countdown, weather, today's and upcoming games, a spotlight image, upcoming calendar items, and the Explorer mascot walking the header.

## Publish it on GitHub Pages (public link)

1. Sign in at github.com and click **New repository**. Name it (for example `lschs-display`), set it to **Public**, and click **Create repository**.
2. On the new repo page, click **uploading an existing file**. Drag in everything from this folder: `index.html`, `sprites.js`, `README.md`, and the `data` folder. Click **Commit changes**.
3. Go to **Settings > Pages**. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch to **main** and folder **/ (root)**, then **Save**.
4. After a minute or two, your link appears at the top of that page: `https://YOUR-USERNAME.github.io/lschs-display/`

Point each TV's browser or signage player at that link and run it full screen (kiosk mode). The layout scales to any 16:9 screen, with 1920x1080 as the target.

## What updates on its own

- **Clock, current period, countdown, letter day and schedule:** update automatically every 15 seconds from the files in `data/`.
- **Weather:** pulled live from Open-Meteo every 10 minutes. If that fails, it falls back to `data/weather.json`.
- **Data files:** re-read every 10 minutes, so edits you commit show up on the TVs without touching them.
- **Daily reload:** the page reloads itself once a day around 5 AM.

## Making changes (edit a file on GitHub, then Commit)

| To change | Edit | Notes |
|---|---|---|
| Snow delay or a one-day schedule change | `data/overrides.json` | Add `{"date": "2026-12-10", "schedule": "2-Hour Delay", "note": "Weather delay"}`. Schedule names: Regular, Community Time, Liturgy, PM Meeting, Extended Homeroom, PM Block, AM Block, 2-Hour Delay, No School |
| Games | `data/athletics.json` | One entry per game: date, time, sortMin, sport, opponent, homeAway (Home/Away/TBD), location |
| Spotlight slides | `data/announcements.json` | Each item has title, detail, start, end dates and an optional image |
| Letter days / special days | `data/calendar.json` | One row per date |
| Bell times | `data/bells.json` | Times per schedule |

Dates are `YYYY-MM-DD`. Note that everything in a public repo can be seen by anyone with the link.
