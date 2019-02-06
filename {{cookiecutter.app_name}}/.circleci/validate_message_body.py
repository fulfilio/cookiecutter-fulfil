from gitlint.rules import CommitRule, RuleViolation
import re

issue_id_regex = r'\[(FP|Z|S)-(\d+)\]'


class IssueID(CommitRule):
    """
    This rule will enforce that each commit contains a reference
    to a sentry issue, jira issue or zendesk case.

    Can be
    * Jira:     [FP-1234]
    * Zendesk:  [Z-1234]
    * Sentry:   [S-12345]
    """
    # A rule MUST have a human friendly name
    name = "body-requires-issue-id"

    # A rule MUST have an *unique* id, we recommend starting
    # with UC (for User-defined Commit-rule).
    id = "UC2"

    def validate(self, commit):
        result = re.search(issue_id_regex, commit.message.full, re.MULTILINE)
        if result:
            return []

        return [
            RuleViolation(
                self.id,
                "Body does not contain issue ID.",
                line_nr=1
            )
        ]
