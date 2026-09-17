import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import review


class ReviewPublishingTests(unittest.TestCase):
    def setUp(self):
        self.repo = Mock()
        self.pull = Mock(
            number=1,
            title="Test poem",
            body="Test poem\nA line of poetry.",
            labels=[SimpleNamespace(name="gen")],
        )
        self.pull.merge.return_value = SimpleNamespace(merged=True)
        self.repo.get_pulls.return_value = [self.pull]

    def run_review(self, responses, merge=True):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "output"
            with (
                patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}),
                patch.object(review, "load_dotenv"),
                patch.object(review, "Github") as github,
                patch.object(review, "chat_completion", side_effect=responses),
                patch("sys.argv", ["review.py"] + (["--merge"] if merge else [])),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                github.return_value.get_repo.return_value = self.repo
                error = None
                try:
                    review.main()
                except RuntimeError as exc:
                    error = exc
            return output.read_text() if output.exists() else "", error

    def test_successful_merge_requests_publication(self):
        output, error = self.run_review(["Good work.\nAccept"])
        self.assertIsNone(error)
        self.pull.merge.assert_called_once()
        self.assertEqual(output, "merged=true\n")

    def test_rejection_does_not_request_publication(self):
        output, error = self.run_review(["Try again.\nReject"])
        self.assertIsNone(error)
        self.pull.edit.assert_called_once_with(state="closed")
        self.pull.merge.assert_not_called()
        self.assertEqual(output, "")

    def test_comment_only_does_not_request_publication(self):
        output, error = self.run_review(["Good work.\nAccept"], merge=False)
        self.assertIsNone(error)
        self.pull.merge.assert_not_called()
        self.assertEqual(output, "")

    def test_no_submissions_does_not_request_publication(self):
        self.repo.get_pulls.return_value = []
        output, error = self.run_review([])
        self.assertIsNone(error)
        self.assertEqual(output, "")

    def test_failed_merge_fails_without_requesting_publication(self):
        self.pull.merge.return_value = SimpleNamespace(
            merged=False, message="Merge conflict"
        )
        output, error = self.run_review(["Good work.\nAccept"])
        self.assertIsInstance(error, RuntimeError)
        self.assertIn("Merge conflict", str(error))
        self.assertEqual(output, "")

    def test_later_failure_still_publishes_prior_merge(self):
        self.repo.get_pulls.return_value = [self.pull, self.pull]
        output, error = self.run_review([
            "Good work.\nAccept", RuntimeError("Review unavailable")
        ])
        self.assertIsInstance(error, RuntimeError)
        self.pull.merge.assert_called_once()
        self.assertEqual(output, "merged=true\n")


if __name__ == "__main__":
    unittest.main()
