from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Issue
from issuestracker.serializers.bakery.IssuePage import IssueSerializer


class BakeryIssue(BakeryBase):
    def get(self, request, issue=None):
        return Response(
            {
                "candidates": self.get_all_candidates(),
                "issue": IssueSerializer(
                    Issue.live.get(slug=self.kwargs["issue"])
                ).data,
            }
        )
