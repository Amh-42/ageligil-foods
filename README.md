# Ageligil food library

1,025 dishes served in Ethiopia, from doro wot and shiro to burgers, juices and cakes, each with a photo.
Used by [Ageligil](https://ageligil.et) to suggest a photo when a restaurant adds a dish without one.

**675 of 1,025 dishes have a photo so far.** The rest have `image: null` until their grid is generated.

## Use it

```
https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/foods.json        full list with descriptions
https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/foods.min.json    compact list for matching (no descriptions)
https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/photos/<slug>.webp   square photo, up to 1024 px
https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/thumbs/<slug>.webp   400 px thumbnail
```

Each item:

```json
{"id": "f0001", "slug": "doro-wot", "name": "Doro Wot", "name_am": "ዶሮ ወጥ", "category": "stews (wot)",
 "tags": ["spicy"], "desc": "...", "image": "https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/photos/doro-wot.webp", "thumb": "https://raw.githubusercontent.com/Amh-42/ageligil-foods/main/thumbs/doro-wot.webp"}
```

`review: "native-check"` marks Ethiopian names and Amharic spellings that still need a native speaker's review.

## Categories

| Category | Dishes | With photo |
|---|---|---|
| cakes and pastries | 111 | 50 |
| grill and meat | 89 | 30 |
| juice | 85 | 65 |
| pasta and rice | 65 | 35 |
| soups and salads | 58 | 30 |
| burgers and sandwiches | 55 | 40 |
| sides and breakfast (café) | 55 | 55 |
| coffee and tea | 51 | 45 |
| pizza | 40 | 30 |
| fasting dishes | 35 | 35 |
| international | 35 | 15 |
| desserts | 32 | 15 |
| catering | 25 | 25 |
| breakfast | 22 | 15 |
| fish | 22 | 15 |
| tibs | 20 | 20 |
| fast food | 20 | 20 |
| soft drinks | 19 | 0 |
| stews (wot) | 16 | 16 |
| bread | 15 | 15 |
| drinks (traditional) | 15 | 15 |
| regional | 15 | 15 |
| beer and drinks (bar) | 15 | 15 |
| bakery | 15 | 15 |
| fruit | 15 | 15 |
| snacks | 15 | 9 |
| bowls and healthy | 14 | 0 |
| wraps and street food | 11 | 0 |
| raw and minced meat | 10 | 10 |
| combos | 10 | 10 |
| kids menu | 10 | 0 |
| sauces and dips | 10 | 0 |

## How the photos are made

AI-generated food photography (Gemini), 25 dishes per image in a 5x5 grid, then cut into single photos.

- `prompts/grid-NN.md`: the prompt for each grid (cell order = `grid` and `cell` in `foods.json`)
- `scripts/build_foods.py`: builds `foods.json` and the prompts
- `scripts/slice.mjs`: finds the gutters in each grid and cuts it into 25 named photos
- `scripts/publish.py`: assembles this repo

Photos are illustrations of a typical serving, not of any specific restaurant's food.
