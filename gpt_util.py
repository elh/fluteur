
import time
from openai import OpenAI

MODEL = "gpt-6-astra"

# our default gpt chat call
def chat_completion(system_prompt, user_prompt):
  start = time.time()
  client = OpenAI(timeout=120.0)
  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      {
        "role": "system",
        "content": system_prompt,
      },
      {
        "role": "user",
        "content": user_prompt,
      }
    ],
    reasoning_effort="low",
    max_completion_tokens=8192,
    stream=True
  )

  output = ''
  finish_reason = None
  with response:
    for event in response:
      if not event.choices:
        continue
      choice = event.choices[0]
      if choice.delta.content is not None:
        output += choice.delta.content
        print(choice.delta.content, end='', flush=True)
      if choice.finish_reason is not None:
        finish_reason = choice.finish_reason
  if finish_reason != "stop" or not output.strip():
    raise RuntimeError(f"Model did not return a complete response ({finish_reason})")
  print(f"\nDone in {(time.time() - start):.2f}")

  return output
