from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'source': {
                'name': instance.sname,
                'id': instance.sid
            },
            'aid': instance.aid,
            'headline': instance.headline,
            'section': instance.section,
            'url': instance.url,
            'publishedAt': instance.published_at,
        }
