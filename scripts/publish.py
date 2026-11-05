#!/usr/bin/env python3
"""Assemble the public repo (github.com/Amh-42/ageligil-foods) on the Vault.

  python3 publish.py            # refresh /Volumes/Vault/Ageligil/foods/repo from foods.json + cut photos
  then: cd /Volumes/Vault/Ageligil/foods/repo && git add -A && git commit && git push

Only dishes that have a cut photo get image URLs; the rest carry image: null until their grid is made.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = '/Volumes/Vault'
PHOTOS = f'{VAULT}/Ageligil/foods/photos'
REPO = f'{VAULT}/Ageligil/foods/repo'
BASE = 'https://raw.githubusercontent.com/Amh-42/ageligil-foods/main'

if not os.path.isdir(VAULT):
    sys.exit('Vault not mounted: nothing was published. Attach it and run again.')

data = json.load(open(os.path.join(HERE, 'foods.json')))
os.makedirs(f'{REPO}/photos', exist_ok=True)
os.makedirs(f'{REPO}/thumbs', exist_ok=True)

have = 0
for it in data['items']:
    f = f"{it['slug']}.webp"
    full, thumb = f'{PHOTOS}/{f}', f'{PHOTOS}/thumbs/{f}'
    if os.path.exists(full) and os.path.exists(thumb):
        shutil.copy2(full, f'{REPO}/photos/{f}')
        shutil.copy2(thumb, f'{REPO}/thumbs/{f}')
        it['image'] = f'{BASE}/photos/{f}'
        it['thumb'] = f'{BASE}/thumbs/{f}'
        have += 1
    else:
        it['image'] = None
        it['thumb'] = None

# drop photos for slugs that no longer exist (renamed dishes)
slugs = {f"{it['slug']}.webp" for it in data['items']}
for d in ('photos', 'thumbs'):
    for f in os.listdir(f'{REPO}/{d}'):
        if f.endswith('.webp') and f not in slugs:
            os.remove(f'{REPO}/{d}/{f}')

data['version'] = 1
data['count'] = len(data['items'])
data['with_photo'] = have
data['image_base'] = BASE
json.dump(data, open(f'{REPO}/foods.json', 'w'), ensure_ascii=False, indent=1)
# a small index for fast matching in the app: no descriptions
lite = [{k: it[k] for k in ('id', 'slug', 'name', 'name_am', 'category', 'tags', 'image', 'thumb')} for it in data['items']]
json.dump({'version': 1, 'count': len(lite), 'items': lite}, open(f'{REPO}/foods.min.json', 'w'), ensure_ascii=False, separators=(',', ':'))

shutil.copytree(os.path.join(HERE, 'prompts'), f'{REPO}/prompts', dirs_exist_ok=True)
os.makedirs(f'{REPO}/scripts', exist_ok=True)
for s in ('build_foods.py', 'slice.mjs', 'publish.py'):
    shutil.copy2(os.path.join(HERE, s), f'{REPO}/scripts/{s}')

cats = {}
for it in data['items']:
    c = cats.setdefault(it['category'], [0, 0]); c[0] += 1; c[1] += it['image'] is not None
rows = '\n'.join(f'| {c} | {n} | {p} |' for c, (n, p) in sorted(cats.items(), key=lambda x: -x[1][0]))

open(f'{REPO}/README.md', 'w').write(f"""# Ageligil food library

{data['count']:,} dishes served in Ethiopia, from doro wot and shiro to burgers, juices and cakes, each with a photo.
Used by [Ageligil](https://ageligil.et) to suggest a photo when a restaurant adds a dish without one.

**{have:,} of {data['count']:,} dishes have a photo so far.** The rest have `image: null` until their grid is generated.

## Use it

```
{BASE}/foods.json        full list with descriptions
{BASE}/foods.min.json    compact list for matching (no descriptions)
{BASE}/photos/<slug>.webp   square photo, up to 1024 px
{BASE}/thumbs/<slug>.webp   400 px thumbnail
```

Each item:

```json
{{"id": "f0001", "slug": "doro-wot", "name": "Doro Wot", "name_am": "ዶሮ ወጥ", "category": "stews (wot)",
 "tags": ["spicy"], "desc": "...", "image": "{BASE}/photos/doro-wot.webp", "thumb": "{BASE}/thumbs/doro-wot.webp"}}
```

`review: "native-check"` marks Ethiopian names and Amharic spellings that still need a native speaker's review.

## Categories

| Category | Dishes | With photo |
|---|---|---|
{rows}

## How the photos are made

AI-generated food photography (Gemini), 25 dishes per image in a 5x5 grid, then cut into single photos.

- `prompts/grid-NN.md`: the prompt for each grid (cell order = `grid` and `cell` in `foods.json`)
- `scripts/build_foods.py`: builds `foods.json` and the prompts
- `scripts/slice.mjs`: finds the gutters in each grid and cuts it into 25 named photos
- `scripts/publish.py`: assembles this repo

Photos are illustrations of a typical serving, not of any specific restaurant's food.
""")
print(f'{REPO}: {data["count"]} dishes, {have} with photos')
