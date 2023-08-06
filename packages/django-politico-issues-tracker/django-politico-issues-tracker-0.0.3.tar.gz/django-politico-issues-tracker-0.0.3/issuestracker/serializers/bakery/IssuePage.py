from rest_framework import serializers
from issuestracker.models import Faq, Story, Position, Issue


class PositionSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()

    def get_candidates(self, obj):
        return [candidate.slug for candidate in obj.candidates.all()]

    class Meta:
        model = Position
        fields = ("name", "explanation", "candidates")


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ("question", "answer")


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ("headline", "link")


class IssueSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    faq_set = FaqSerializer(many=True, read_only=True)
    story_set = StorySerializer(many=True, read_only=True)
    position_set = PositionSerializer(many=True, read_only=True)

    def get_category(self, obj):
        return str(obj.category)

    def get_category_slug(self, obj):
        return obj.category.slug

    class Meta:
        model = Issue
        fields = (
            "name",
            "slug",
            "category",
            "category_slug",
            "summary",
            "faq_set",
            "story_set",
            "position_set",
        )
