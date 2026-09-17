# Flûteur automate 🪈

[![write status](https://github.com/elh/fluteur/actions/workflows/write.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/write.yml)
[![review status](https://github.com/elh/fluteur/actions/workflows/review.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/review.yml)

A self-updating website hosted for free entirely in Github using Actions, Pages, Pull Requests. Contents created by GPT.

Flûteur is an early experiment in procedural generation of websites and collaborative agents. It intends to be an unserious automaton curiosity like the [flûteur automate de Vaucanson](https://fr.wikipedia.org/wiki/Fl%C3%BBteur_automate_de_Vaucanson). When enabled, the jobs run every two weeks: write on Monday and review on Tuesday at 16:00 UTC.

The cadence is anchored to September 21–22, 2026, then October 5–6, and every 14 days afterward. GitHub checks the schedule weekly; `cadence.py` skips setup and model calls on alternate weeks. Both jobs share this date check so they stay aligned across month and year boundaries. Manual runs bypass the cadence check.

On a cadence, a scheduled Action runs `write.py` opening a PR to add a new poem, then another scheduled Action runs `review.py`. If the poem passes the review, it is merged and automatically built and deployed to the Pages site; otherwise, the PR is closed.

Both scripts use GPT-6 Astra with low reasoning effort and a maximum of 8,192 completion tokens per call (including reasoning). The model is configured in `gpt_util.py`. Set `OPENAI_API_KEY` in a local `.env` file or the repository's Actions secrets; publishing also requires `GH_TOKEN` (the workflow uses `GITHUB_TOKEN`). Python 3.11 or newer is required.

To check the saved API key without opening a poem PR, manually run the **write** workflow with **preview** enabled. It makes a real model request and saves the generated post as the `poem-preview` artifact. With the default settings, the job opens a poem PR as before. A disabled workflow must be temporarily enabled to dispatch a test; disable it again afterward to keep the schedule paused.

The About page bundles the original public-domain Vaucanson engraving in `docs/assets/images/automates-vaucanson.jpg`, with its source credited on the page, so it does not depend on Wikimedia thumbnail URLs.
