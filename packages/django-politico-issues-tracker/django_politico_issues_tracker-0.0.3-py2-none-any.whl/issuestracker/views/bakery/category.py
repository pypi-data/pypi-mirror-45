from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Category, Candidate
from issuestracker.serializers.bakery.CategoryPage import CategorySerializer


class BakeryCategory(BakeryBase):
    def get(self, request, category=None):
        return Response(
            {
                "candidate_count": Candidate.objects.count(),
                "categories": CategorySerializer(
                    Category.live.get(slug=self.kwargs["category"])
                ).data,
            }
        )
