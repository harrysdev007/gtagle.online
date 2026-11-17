# GTAXIOM — Grand Theft Memes

A GTA meme discovery site with a Vice City sunset, neon pink interface, live search, GIFs and a private browser collection.

Run locally with `node tools/serve.cjs`, then open http://127.0.0.1:8000. No build or server dependencies are required.

Navigation uses clean History API URLs (`/search`, `/settings`, `/tags`, `/folders`). The local server serves `index.html` for these routes, while missing assets return 404. Other hosting must provide the same SPA fallback for direct links and refreshes. Old `#/…` bookmarks are converted automatically.

Use the top-right **Terminal / Classic** switch to choose the compact table/Pulse layout or restore the original Vice City hero and card grid. The choice persists in `vicefeed.layout`; saved memes and search settings are shared. Direct layout links also work: `/?layout=classic` and `/?layout=terminal`. Classic styles remain in `css/vicefeed.css`; the alternate layout is isolated in `css/terminal.css` and `js/terminal.js`.

Discovery searches Lemmy, Reddit, Bluesky and Mastodon for GTA VI, V, IV, Online, San Andreas, Vice City, characters and meme phrases. Topic chips and query aliases live in `js/gta.js`. Tenor, Giphy and Imgur work with optional user API keys. A shared metadata/community filter rejects unrelated content across result streams and the local library. This is metadata filtering, not image recognition. Four original local GTA meme cards remain available when public APIs are unavailable.

GTAXIOM uses separate browser storage (`vicefeed`), preserving earlier libraries. An unofficial fan project, unaffiliated with Rockstar Games.

![GTAXIOM](assets/gta/city.svg)

Third-party meme source URLs are retained in data/memes.json. Keep LICENSE and NOTICE with redistributions.
