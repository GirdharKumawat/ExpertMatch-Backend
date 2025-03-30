
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import  UserInfo ,User
from django.http import JsonResponse
import json
import ast

from .utils import extract_text_from_pdf,Gemini_api_call,ScoreMatchResult,create_score_matches


@api_view(['POST'])
def userRegister(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def userLogin(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET'])
def profile(request, id):
    profile = get_object_or_404(UserInfo, user_id=id)
    return Response({
        "info_id": profile.id,
        "extracted_text": profile.info
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def allExperts(request):
    experts = User.objects.filter(role='expert')
    serializer = UserSerializer(experts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def allCandidates(request):
    candidates = User.objects.filter(role='candidate')
    serializer = UserSerializer(candidates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addUser(request):
    name = request.data.get('name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    role = request.data.get('role')
    password = request.data.get('password')
    user = User.objects.create_user(name=name, email=email, phone=phone, role=role, password=password)
    resume = request.FILES.get("resume") 
    resume_text = extract_text_from_pdf(resume)
    extracted_text = Gemini_api_call(resume_text)
    print(f"---------------------------------------Extracted text: {extracted_text}")  # Debugging Line
    
    info_entry = UserInfo.objects.create(user=user, info=extracted_text)
    
    return Response({
        "message": "User added successfully",
        "user_id": user.id,
        "info_id": info_entry.id,
        "extracted_text": extracted_text
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def userinfo(request, id):
    user = get_object_or_404(User, id=id)
    user_info = get_object_or_404(UserInfo, user=user)
    data_dict = ast.literal_eval(user_info.info)
   
    return Response({
        "info_id": user_info.id,
        "extracted_text":data_dict
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def scoreMatch(request, id):
    try:
        user = get_object_or_404(User, id=id)
        print(f"API called for user: {user.name} ({user.role})")  # Debugging Line
        
        create_score_matches(user)  # Ensure this function is only called once

        # Fetch scores with related expert details
        score_list = ScoreMatchResult.objects.filter(candidate=user).select_related('expert').values(
            'id', 'candidate_id', 'expert_id', 'education_score', 'skills_score', 
            'experience_score', 'project_score', 'total_score', 'created_at',
            'candidate__name', 'expert__name'
        )

        # Modify the output to include names
        formatted_scores = [
            {
                "id": item["id"],
                "candidate_id": item["candidate_id"],
                "candidate_name": item["candidate__name"],  # Adding Candidate Name
                "expert_id": item["expert_id"],
                "expert_name": item["expert__name"],  # Adding Expert Name
                "education_score": item["education_score"],
                "skills_score": item["skills_score"],
                "experience_score": item["experience_score"],
                "project_score": item["project_score"],
                "total_score": item["total_score"],
                "created_at": item["created_at"],
            }
            for item in score_list
        ]

        return JsonResponse({"status": "success", "message": "Scores calculated.", "scoreList": formatted_scores}, status=200)

    except Exception as e:
        print(f"API Error: {e}")  # Debugging Line
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
