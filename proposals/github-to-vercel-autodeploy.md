# GitHub → Vercel auto-deploy (the dead-simple version)

## How it works (yes, this is the standard developer workflow)
You save code to **GitHub** (the backup/source of truth). **Vercel watches that repo.** Every time a
change is pushed, Vercel automatically rebuilds and publishes the website. No manual deploy, no CLI, no
alias headaches. Push → live in ~30 seconds. This is exactly how modern web teams ship.

For us: the agents commit work to GitHub (already happening, auto-backup every 30 min) → the site updates
itself. Same pattern works for the Grok Go part of the site, and later the Grok Go stream/YouTube embeds.

## The ONE thing only you can do (2 clicks, ~60 sec)
The two pages I opened in your browser:
1. **Vercel GitHub-app install** (github.com/apps/vercel) → choose **jw83252014-creator**, grant access
   to the **the-device-site** repo (or "all repos"). Click Install/Authorize.
2. **Vercel project Git settings** (the null-axiom project) → "Connect Git Repository" → pick
   **jw83252014-creator/the-device-site** → Connect.

That's it. (Only you can grant the OAuth — it's your account; the CLI isn't allowed to.)

## What I do after (you don't touch this again)
- Confirm the connection (`vercel git connect` finishes cleanly once the app's authorized).
- From then on: agents push to GitHub → Vercel auto-builds → yn-eight.vercel.app updates itself,
  including the new pages (deck, film) that are stuck right now behind the alias issue.
- This also kills the "not a team member / alias frozen" problem — git-integration deploys promote the
  alias automatically.

## Net
After your 2 clicks: the website becomes self-updating. Every piece of work the organism commits shows up
live without anyone deploying by hand. Tell me "connected" and I'll verify + push so the deck + film go live.
