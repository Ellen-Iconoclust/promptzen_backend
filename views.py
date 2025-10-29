from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User, Prompt
from .serializers import (
    UserSerializer, UserRegistrationSerializer, 
    LoginSerializer, PromptSerializer, PromptCreateSerializer
)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_prompts(request):
    # Show only approved prompts to regular users, all to admins
    user = request.user
    if user.is_authenticated and user.role == 'admin':
        prompts = Prompt.objects.all()
    else:
        prompts = Prompt.objects.filter(status='approved')
    
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_prompt(request):
    serializer = PromptCreateSerializer(data=request.data)
    if serializer.is_valid():
        prompt = serializer.save()
        
        # Handle image upload
        if 'image' in request.FILES:
            prompt.image = request.FILES['image']
            # Image URL will be set automatically in save method
        
        prompt.save()
        
        return Response(PromptSerializer(prompt).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_prompts(request):
    if request.user.role == 'admin':
        prompts = Prompt.objects.all()
    else:
        prompts = Prompt.objects.filter(username=request.user.username)
    
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_prompt_status(request, prompt_id):
    if request.user.role != 'admin':
        return Response({'error': 'Only admins can update prompt status'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        prompt = Prompt.objects.get(id=prompt_id)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    is_trending = request.data.get('is_trending')
    
    if status_value and status_value in ['pending', 'approved', 'rejected']:
        prompt.status = status_value
    
    if is_trending is not None:
        prompt.is_trending = is_trending
    
    prompt.save()
    
    return Response(PromptSerializer(prompt).data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_pending_prompts(request):
    if request.user.role != 'admin':
        return Response({'error': 'Only admins can view pending prompts'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    prompts = Prompt.objects.filter(status='pending')
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data)
