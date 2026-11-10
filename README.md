# TV wallpaper feed

A rotating set of Sikh gurdwara wallpapers for a TV home screen, in the spirit of Windows Spotlight.

Every Monday a GitHub Action picks ten pictures from `pool/` (four for the morning, three for the afternoon and
evening, three for the night), writes them to `feed.json` and publishes it on GitHub Pages. A home-screen launcher that
reads the feed downloads the new set and shows it.

- `pool/`: the pictures, 1920x1080 JPEGs; `pool.json` gives each one a caption and a time of day (`day`, `dusk`, `night`).
- `generate.py`: writes `feed.json`.
- `CREDITS.md`: where every picture comes from and its licence.

To add a picture, put a 1920x1080 JPEG in `pool/`, add its entry to `pool.json` and its credit to `CREDITS.md`, and push.
