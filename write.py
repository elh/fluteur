import os
import argparse
import time
from datetime import datetime
import re
import yaml
import random
from dotenv import load_dotenv
from git import Repo
import openai

"""
write generates a new post in a new file and creates a new commit

Usage: python write.py [-p prompt] [-c]
"""

def sanitize_url(input):
  alphanumeric_chars = re.sub(r'\W+', ' ', input)
  return alphanumeric_chars.replace(' ', '-')

def main():
  load_dotenv()
  parser = argparse.ArgumentParser()
  parser.add_argument("--prompt", type=str, default='prompting/poem.yml',
                      help="prompt template")
  parser.add_argument("--commit", type=bool, default=False,
                      action=argparse.BooleanOptionalAction, help="if true, create commit")
  parser.add_argument("--pull", type=bool, default=False,
                      action=argparse.BooleanOptionalAction, help="if true, create pull request")
  args = parser.parse_args()

  prompting = None
  with open(args.prompt, 'r') as f:
    prompting = yaml.safe_load(f)

  # generate new post
  openai.api_key = os.getenv("OPENAI_API_KEY")
  start = time.time()
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": prompting['system_prompt'],
      },
      {
        "role": "user",
        # select a random prompt from the list
        "content": random.choice(prompting['user_prompts']),
      }
    ],
    temperature=1.0,
    stream=True
  )
  output = ''
  for event in response:
    content = event["choices"][0].get("delta", {}).get("content")
    if content is not None:
      output += content
      print(content, end='')
  print(f"\nDone in {(time.time() - start):.2f}")

  title = output.split('\n')[0]
  body = '\n'.join(output.split('\n')[1:])
  body = re.sub(r'\n', '\n<br>\n', body).strip().strip('<br>').strip()

  # create file
  now = datetime.now()
  sanitized_title = f"{now.strftime('%Y-%m-%d')}-{sanitize_url(title)}"
  file_name = f"docs/_posts/{sanitized_title}.markdown"
  with open(file_name, 'w') as f:
    front = '''---
layout: post
title:  {title}
date:   {date} -0700
---
'''.format(title=title, date=now.strftime('%Y-%m-%d %H:%M:%S'))
    f.write(front + body)

  # if commit flag is set, commit
  repo = Repo('.')
  if args.commit or args.pull:
    repo.git.checkout("HEAD", b=sanitized_title)
    repo.index.add([file_name])
    repo.index.commit(f"Wrote {file_name}")

  # if pull, push to remote and create a pull request
  if args.pull:
    origin = repo.remote(name='origin')
    origin.push(sanitized_title).raise_if_error()

    # TODO: create github pull request

if __name__ == "__main__":
  main()
