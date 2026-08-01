# YouTube Channel & Video Search CLI

A command-line tool for searching YouTube channels and videos using the
YouTube Data API v3. Given a channel name, it looks up the channel,
pulls its uploads playlist, and fetches details for the videos in it.
Video search is partially wired up but not finished yet.

## Project Status

Started this to mess around with the YouTube API and get comfortable chaining a few requests together (search for a channel, grab its ID, get the uploads playlist, then pull the videos). Channel search actually works. Video search fetches the data fine but I never got round to actually printing it out, so right now it just... does nothing. Output is also just raw JSON dumped to the terminal, not cleaned up yet.

Putting this down for a while but I'll come back and finish it. If you spot something or want to fix it up yourself, feel free.

> **Status: work in progress.** This is not a finished project — see
> [What's Not Done Yet](#whats-not-done-yet) below before relying on it.

## Features (currently working)

- **Search by channel name** → resolves the channel, prints its name,
  total videos, and subscriber count, then dumps the raw JSON details
  for its most recent uploads.
- Basic error handling for no internet connection, bad/empty API
  responses, and unexpected exceptions.

## Features (not working / not finished)

- **Search by video keyword** — the request to the API is made, but
  `display_Video_details()` is an empty stub (`pass`), so results are
  fetched and then silently thrown away. Nothing is printed to the user.
- Output is raw, unformatted JSON (`display_Channel_videos_detail`) —
  no clean per-video summary yet.

## Requirements

- Python 3.10+ (the code uses nested f-strings with double quotes
  inside double quotes, e.g. `f"{response["items"][0]...}"`, which
  requires Python 3.12+ specifically — on older versions this will
  raise a `SyntaxError`)
- A YouTube Data API v3 key from the
  [Google Cloud Console](https://console.cloud.google.com/)
- Packages:
  ```
  pip install requests python-dotenv
  ```

## Setup

1. Clone/download this project.
2. Create a `.env` file in the project root (already in `.gitignore`,
   so it won't be committed):
   ```
   Api_key = "YOUR_YOUTUBE_API_KEY_HERE"
   ```
3. Install dependencies:
   ```
   pip install requests python-dotenv
   ```
4. Run it:
   ```
   python get.py
   ```

## Usage

On launch you'll see a menu:

```
========================================
                YouTube
========================================
1. Search for channel...
2. Search video...
3. exit
?:
```

- **Option 1** — enter a channel name. The tool resolves the channel ID,
  fetches its uploads playlist, prints subscriber/video counts, and
  dumps details for up to 50 recent videos.
- **Option 2** — enter a search keyword. Currently fetches results
  from the API but does not display anything (see known issues).
- **Option 3** — exits the program.

## Project structure

```
.
├── get.py        # main script - all logic currently lives here
├── .env          # holds Api_key (not committed)
└── .gitignore    # excludes .env
```

## What's Not Done Yet

This is your own running list to pick back up from later:

- [ ] Implement `display_Video_details()` — currently a no-op `pass`,
      so video search results are fetched but never shown
- [ ] Clean up `display_Channel_videos_detail()` — currently dumps raw
      JSON instead of a readable summary (title, views, likes, etc.)
- [ ] Remove leftover debug prints (`print(11)`, `print(23)`, `print(40)`,
      `print(response)`) scattered through the code
- [ ] Fix `response.raise_for_status` in `get_channel_id()` — missing
      `()`, so it's referencing the method instead of calling it and
      currently does nothing
- [ ] Decide on consistent key casing — the API key env var is read as
      `Api_key`, mixing capitalization conventions
- [ ] Consider splitting `get.py` into modules (API calls / display
      logic / CLI menu) as the project grows
- [ ] Add handling for a channel name that returns zero search results
      (currently assumes `response["items"][0]` always exists)

## Known Issues

- Nested double quotes inside f-strings (`f"{response["items"][0]..."`)
  require Python 3.12+; will throw a `SyntaxError` on older versions.
- `get_channel_playlist_id()` mutates the shared `params` dict
  (deleting keys from it) — if reused elsewhere afterward, those keys
  will already be gone.
- Bare `except Exception` blocks in a few places will also catch
  genuine bugs (e.g. `KeyError`, `IndexError`) and relabel them all as
  a generic `UnexpectedError`, which can make debugging harder.

## License

Not yet decided.
