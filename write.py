import os
import argparse
from datetime import datetime
import re
import yaml
import random
import uuid
from dotenv import load_dotenv
from git import Repo
from github import Github
from gpt_util import chat_completion

"""
write generates a new post in a new file and creates a new commit

Usage: python write.py [--prompt prompts/write/poem.yml] [--commit] [--pull]
"""

REPO = "elh/fluteur"


def sanitize_url(input):
    alphanumeric_chars = re.sub(r"\W+", " ", input)
    return alphanumeric_chars.replace(" ", "-")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt", type=str, default="prompts/write/poem.yml", help="prompt template"
    )
    parser.add_argument(
        "--commit",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="if true, create commit",
    )
    parser.add_argument(
        "--pull",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="if true, create pull request",
    )
    args = parser.parse_args()

    prompt = None
    with open(args.prompt, "r") as f:
        prompt = yaml.safe_load(f)

    # generate new post
    system_prompt = prompt["system_prompt"]
    user_prompt = random.choice(prompt["user_prompts"])
    output = chat_completion(system_prompt, user_prompt)

    title = output.split("\n")[0]
    body = "\n".join(output.split("\n")[1:])
    body_md = re.sub(r"\n", "\n<br>\n", body).strip().strip("<br>").strip()

    # create file
    now = datetime.now()
    sanitized_title = f"{now.strftime('%Y-%m-%d')}-{sanitize_url(title)}"
    file_name = f"docs/_posts/{sanitized_title}.markdown"
    with open(file_name, "w") as f:
        front = """---
layout:     post
title:      {title}
date:       {date}
author:     Flûteur (gpt-3.5-turbo)
categories: {categories}
---
""".format(
            title=title,
            date=now.strftime("%Y-%m-%d %H:%M:%S %z"),
            categories=prompt["categories"],
        )
        f.write(front + body_md)

    # if --commit, commit change on a new branch
    repo = Repo(".")
    if args.commit or args.pull:
        repo.git.checkout("HEAD", b=sanitized_title)
        repo.index.add([file_name])
        repo.index.commit(f"Wrote {file_name}")

    # if --pull, push to remote and create a pull request tagged with "gen"
    if args.pull:
        gh_token = os.getenv("GH_TOKEN")
        remote_url = f"https://{gh_token}@github.com/{REPO}.git"
        remote = repo.create_remote(
            name=f"origin_{str(uuid.uuid4())[:6]}", url=remote_url
        )
        remote.push(refspec=f"HEAD:{sanitized_title}")

        g = Github(gh_token)
        repo = g.get_repo(REPO)

        pull = repo.create_pull(
            title=f'Add "{title}"', body=output, head=sanitized_title, base="main"
        )
        pull.set_labels("gen")


if __name__ == "__main__":
    main()
