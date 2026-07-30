"""
Self-built AI code review agent.

Unlike the packaged anthropics/claude-code-action (which just ships the diff
to Claude and posts back comments), this script drives Claude Code's agent
engine directly: it decides its own tool scope, and is instructed to
*actually run the affected tests itself* before commenting, rather than
reasoning over a flat diff alone.

Usage:
    python scripts/ai_review_agent.py <pr_number>
"""
import argparse
import json
import subprocess
import sys

ALLOWED_TOOLS = (
    "Read,Grep,Glob,"
    "Bash(gh pr view:*),Bash(gh pr diff:*),"
    "Bash(python -m pytest:*),Bash(./venv/Scripts/python.exe -m pytest:*)"
)

REVIEW_SYSTEM_PROMPT = """You are a senior reviewer for a Playwright + Python
UI automation suite using the Page Object Model (locators/actions live in
pages/, assertions live in tests/).

For the given PR:
1. Run `gh pr diff <pr_number>` to see the actual change.
2. Read any files touched by the diff for full context (don't review from
   the diff hunks alone).
3. If the change touches test or page-object logic, RUN the relevant test
   file(s) yourself with pytest to confirm they pass before commenting on
   correctness -- do not assume, verify.
4. Check for: POM convention violations, duplicated logic against other
   page objects, missing test coverage for new methods, flaky-test risk
   (missing waits, brittle locators), and hardcoded secrets.
5. Output a concise markdown review: what you checked, what you ran, and
   your findings. Prefix the very first line with "### Self-Built Agent Review"
   so it's distinguishable from other bots.
"""


def run_agent(pr_number: str) -> str:
    prompt = f"Review PR #{pr_number} in this repository following your instructions."
    result = subprocess.run(
        [
            "claude", "-p", prompt,
            "--append-system-prompt", REVIEW_SYSTEM_PROMPT,
            "--allowedTools", ALLOWED_TOOLS,
            "--output-format", "json",
        ],
        capture_output=True, text=True, timeout=600,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"claude CLI exited {result.returncode}")

    payload = json.loads(result.stdout)
    return payload["result"]


def post_comment(pr_number: str, body: str):
    subprocess.run(
        ["gh", "pr", "comment", pr_number, "--body", body],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Self-built AI PR review agent")
    parser.add_argument("pr_number")
    parser.add_argument("--dry-run", action="store_true", help="Print review instead of posting")
    args = parser.parse_args()

    review = run_agent(args.pr_number)

    if args.dry_run:
        print(review)
    else:
        post_comment(args.pr_number, review)
        print(f"Posted review to PR #{args.pr_number}")


if __name__ == "__main__":
    main()
