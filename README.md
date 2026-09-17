# Flûteur automate 🪈

[![write status](https://github.com/elh/fluteur/actions/workflows/write.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/write.yml)
[![review status](https://github.com/elh/fluteur/actions/workflows/review.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/review.yml)

A self-updating website hosted for free entirely in GitHub using Actions, Pages, Pull Requests. Contents created by GPT.

Flûteur is an early experiment in procedural generation of websites and collaborative agents. It intends to be an unserious automaton curiosity like the [flûteur automate de Vaucanson](https://fr.wikipedia.org/wiki/Fl%C3%BBteur_automate_de_Vaucanson). It runs every two weeks.

A scheduled Action runs `write.py` on Monday to open a PR with a new poem, then `review.py` reviews it on Tuesday. Both use GPT-6 Astra. Accepted poems are merged and automatically deployed to GitHub Pages; otherwise, the PR is closed.
