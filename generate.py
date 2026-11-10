"""Writes feed.json: a fresh pick of wallpapers from pool.json under fixed slot names.

The TV launcher downloads feed.json a couple of times a day. `version` is the ISO week, so the pick changes once a
week however often this runs. When `version` changes the launcher downloads each image and saves it
under its slot name (morning-1.jpg, ...), which the theme's wallpaper_moods groups by time of day.

    python generate.py https://<user>.github.io/<repo>
"""
import datetime
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLOTS = {"morning": 4, "evening": 3, "night": 3}


def main(base):
    pool = json.loads((HERE / "pool.json").read_text(encoding="utf-8"))
    now = datetime.datetime.now(datetime.timezone.utc)
    version = now.strftime("%G-W%V")  # ISO year and week: one pick per week
    rng = random.Random(version)  # the same week always gives the same pick
    by_mood = {mood: [p for p in pool if p["mood"] == mood] for mood in ("day", "dusk", "night")}
    morning = rng.sample(by_mood["day"], SLOTS["morning"])
    # Evening runs from noon to after sunset: sunset and dusk pictures first, topped up with unused daytime ones.
    evening_pool = by_mood["dusk"] + [p for p in by_mood["day"] if p not in morning]
    dusk = rng.sample(by_mood["dusk"], min(2, len(by_mood["dusk"])))
    evening = dusk + rng.sample([p for p in evening_pool if p not in dusk], SLOTS["evening"] - len(dusk))
    night = rng.sample(by_mood["night"], SLOTS["night"])
    images = []
    for slot, picks in (("morning", morning), ("evening", evening), ("night", night)):
        for i, p in enumerate(picks, 1):
            images.append({"file": f"{slot}-{i}.jpg", "url": f"{base.rstrip('/')}/pool/{p['id']}.jpg",
                           "caption": p["caption"]})
    feed = {"version": version, "images": images}
    (HERE / "feed.json").write_text(json.dumps(feed, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(version, [p["id"] for p in morning + evening + night])


if __name__ == "__main__":
    main(sys.argv[1])
