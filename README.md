# Flûteur automate 🪈

[![write status](https://github.com/elh/fluteur/actions/workflows/write.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/write.yml)
[![review status](https://github.com/elh/fluteur/actions/workflows/review.yml/badge.svg)](https://github.com/elh/fluteur/actions/workflows/review.yml)

A self-updating website hosted for free entirely in Github using Actions, Pages, Pull Requests. Contents created by GPT.

Flûteur is an early experiment in procedural generation of websites and collaborative agents. It intends to be an unserious automaton curiosity like the [flûteur automate de Vaucanson](https://fr.wikipedia.org/wiki/Fl%C3%BBteur_automate_de_Vaucanson). New poems (and more?) are added daily.

Every morning, a scheduled Action runs `write.py` opening a PR to add a new poem. Shortly after, another scheduled Action runs `review.py`. If the poem passes the review, it is merged and automatically built and deployed to the Pages site; otherwise, the PR is closed.
