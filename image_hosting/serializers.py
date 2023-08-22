from rest_framework import serializers
from .models import ImageStorage, Subscription, Plan
from easy_thumbnails.files import get_thumbnailer
from django.utils import timezone
from django.conf import settings

# Image Serializer
class ImageSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = ImageStorage
        fields = [
            'username',
        ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        subscription = Subscription.objects.filter(user_id=request.user).values_list('plan_id', flat=True)[0]
        plan = Plan.objects.filter(id=subscription).values_list('plan_name', flat=True)[0]
        if plan.lower() == 'basic':
            fields['image'] = serializers.FileField(write_only=True)
            fields['thumbnail200_url'] = serializers.SerializerMethodField()
        if plan.lower() == 'premium':
            fields['image'] = serializers.FileField()
            fields['thumbnail200_url'] = serializers.SerializerMethodField()
            fields['thumbnail400_url'] = serializers.SerializerMethodField()
        if plan.lower() == 'enterprise':
            fields['image'] = serializers.FileField()
            fields['valid'] = serializers.IntegerField(write_only=True)
            fields['thumbnail200_url'] = serializers.SerializerMethodField()
            fields['thumbnail400_url'] = serializers.SerializerMethodField()        

        return fields

    def get_thumbnail200_url(self, obj):
        request = self.context.get('request')
        thumbnail_size = settings.THUMBNAIL_ALIASES
        thumbnail_options = thumbnail_size['']['avtar200']
        thumbnail_url = get_thumbnailer(obj.image).get_thumbnail(thumbnail_options).url
        if request:
            return request.build_absolute_uri(thumbnail_url)
        return thumbnail_url

    def get_thumbnail400_url(self, obj):
        request = self.context.get('request')
        thumbnail_size = settings.THUMBNAIL_ALIASES
        thumbnail_options = thumbnail_size['']['avtar400']
        thumbnail_url = get_thumbnailer(obj.image).get_thumbnail(thumbnail_options).url
        if request:
            return request.build_absolute_uri(thumbnail_url)
        return thumbnail_url
    
