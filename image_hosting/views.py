from rest_framework.generics import (
    CreateAPIView,
    ListAPIView
)
from rest_framework import status
from rest_framework.response import Response
from .models import ImageStorage, Subscription, Plan
from .serializers import ImageSerializer
from django.utils import timezone
from rest_framework.views import APIView

    
class ImageUploadAPI(CreateAPIView):
    queryset = ImageStorage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):        
        time = request.data.get('valid')

        # Check Time
        if time != None:
            if int(time) < 5 or int(time) > 50:
                data = {
                    "statusCode" : status.HTTP_400_BAD_REQUEST,
                    "status" : 'error',
                    "message": "Expire time should be between 5 to 50 miniutes"
                }
                return Response(data, status=201)
        # Validate Data 
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            data = {
                "statusCode" : response.status_code,
                "status" : 'success',
                "message": "Image Upload successfully",
                "Link" : "http://127.0.0.1:8000/api/image/image-list/"
            }
            return Response(data, status=201)
        return response

    def perform_create(self, serializer):
        try:
            valid_till = serializer.validated_data['valid']
        except Exception as e:
            valid_till = Plan.objects.filter(id=Subscription.objects.filter(user_id=self.request.user).values_list('plan_id', flat=True)[0]).values_list('expiring_link', flat=True)[0]/60
        time = timezone.now() + timezone.timedelta(minutes=valid_till)
        serializer.validated_data.pop('valid', None)
        serializer.save(user_id=self.request.user, valid_till=time)


class ImageListAPI(ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        subscription = Subscription.objects.filter(user_id=self.request.user).values_list('plan_id', flat=True)[0]
        plan = Plan.objects.filter(id=subscription).values_list('plan_name', flat=True)[0]
        if plan.lower() == 'basic':
            image_data = ImageStorage.objects.filter(user_id=self.request.user, valid_till__gt=timezone.now())
        if plan.lower() == 'premium':
            image_data = ImageStorage.objects.filter(user_id=self.request.user, valid_till__gt=timezone.now())
        if plan.lower() == 'enterprise':
            image_data = ImageStorage.objects.filter(user_id=self.request.user)
        return image_data
