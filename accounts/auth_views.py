from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from datetime import timedelta
from django.contrib.auth import authenticate
from .serializers import UserSerializer  # UserSerializer 추가


@api_view(["POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response(
            {
                "access": access_token,
                "user": UserSerializer(
                    user
                ).data,  # 사용자 정보를 직렬화하여 반환
            }
        )

        # 쿠키 설정
        cookie_settings = {
            "httponly": True,
            "samesite": "None",  # CORS 요청에 대응하기 위해 None 설정
            "secure": False,  # 개발 환경에서는 False로, 배포 시 True로 변경 필요
            "path": "/",
            "max_age": 30 * 24 * 60 * 60,  # 30일 유효기간
        }

        response.set_cookie("refresh_token", str(refresh), **cookie_settings)

        return response

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response(
            {"detail": "로그인에 실패했습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response({"detail": "로그아웃되었습니다."})
        response.delete_cookie(
            "refresh_token", path="/", samesite="None", secure=False
        )  # 쿠키 삭제
        return response
    except Exception:
        return Response(
            {"detail": "로그아웃 처리 중 오류가 발생했습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def token_refresh(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken(refresh_token)

        if refresh.check_blacklist():
            return Response(
                {"detail": "Refresh token is blacklisted"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = str(refresh.access_token)

        response = Response({"access": access_token})

        # 리프레시 토큰 회전이 설정된 경우 새로운 리프레시 토큰 발급 및 쿠키 설정
        if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS", False):
            refresh.blacklist()
            new_refresh = RefreshToken.for_user(refresh.get_user())

            cookie_settings = {
                "httponly": True,
                "samesite": "None",  # CORS 요청에 대응하기 위해 None 설정
                "secure": False,  # 개발 환경에서는 False로, 배포 시 True로 변경 필요
                "path": "/",
                "max_age": 30 * 24 * 60 * 60,  # 30일 유효기간
            }

            response.set_cookie(
                "refresh_token", str(new_refresh), **cookie_settings
            )

        return response

    except Exception as e:
        print(f"Token refresh error: {str(e)}")  # 디버깅용 로그 추가
        return Response(
            {"detail": "토큰 갱신에 실패했습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
