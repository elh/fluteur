import os
import argparse
import yaml
import random
from dotenv import load_dotenv
from github import Github
from gpt_util import chat_completion

"""
merge reviews "gen" PRs and then optionally closes or merges them

Usage: python review.py --merge
"""

REPO = "elh/fluteur"
REVIEW_PROMPT = "prompts/review/poem.yml"

def main():
  load_dotenv()
  parser = argparse.ArgumentParser()
  parser.add_argument("--merge", type=bool, default=False,
                      action=argparse.BooleanOptionalAction,
                      help="if true, close or merge PRs")
  args = parser.parse_args()
  gh_token = os.getenv('GH_TOKEN')

  prompt = None
  with open(REVIEW_PROMPT, 'r') as f:
    prompt = yaml.safe_load(f)

  g = Github(gh_token)
  repo = g.get_repo(REPO)

  # NOTE: not actually reading PR files, just using the PR body
  pulls = repo.get_pulls(state='open', base='main')
  for pull in pulls:
    if 'gen' not in [label.name for label in pull.labels]:
      continue
    print(f"reviewing {pull.title}...")

    # generate new post
    system_prompt = prompt['system_prompt']
    user_prompt = random.choice(prompt['user_prompts']) + '\n\n' + pull.body
    output = chat_completion(system_prompt, user_prompt)

    # if --merge, close or merge PR. otherwise, just comment
    if args.merge:
      recommendation = output.splitlines()[-1]    # last line
      body = '\n'.join(output.splitlines()[:-1])  # everything else

      if 'Accept' in recommendation:
        # TODO: actually approve pull request via event="APPROVE". currently,
        # cannot approve own PRs while using default github action token
        pull.create_review(body=body, event="COMMENT")
        pull.merge(commit_title=f"Merge pull request #{pull.number}: {pull.title}")
      elif 'Reject' in recommendation:
        pull.create_review(body=body, event="COMMENT")
        pull.edit(state="closed")
      else:
        print(f"unknown recommendation: {recommendation}")
    else:
      pull.create_review(body=output, event="COMMENT")

if __name__ == "__main__":
  main()
