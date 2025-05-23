from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, WatchedAnime
from .serializers import UserSerializer, WatchedAnimeSerializer
import requests


# ✅ /auth/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ✅ /user/preferences/
class UserPreferencesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'preferences': request.user.preferences or ''})

    def post(self, request):
        preferences = request.data.get('preferences')
        if not preferences:
            return Response({"error": "Preferences are required"}, status=400)

        request.user.preferences = preferences
        request.user.save()
        return Response({'message': 'Preferences updated successfully'})


# ✅ /anime/search/?search=naruto
class AnimeSearchView(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        if not search:
            return Response({"error": "search query param is required"}, status=400)

        query = """
        query ($search: String) {
            Media(search: $search, type: ANIME) {
                id
                title { romaji }
                genres
                popularity
            }
        }"""

        try:
            response = requests.post(
                'https://graphql.anilist.co',
                json={'query': query, 'variables': {'search': search}}
            )
            response.raise_for_status()
            data = response.json()
            return Response(data)
        except requests.RequestException as e:
            return Response({"error": "Failed to fetch from AniList", "details": str(e)}, status=500)


# ✅ /anime/recommendations/
class AnimeRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        preferences = request.user.preferences
        if not preferences:
            return Response({"error": "User has no preferences set"}, status=400)

        genres = [g.strip() for g in preferences.split(",") if g.strip()]
        if not genres:
            return Response({"error": "No valid genres found in preferences"}, status=400)

        query = """
        query ($genre: String) {
            Page(perPage: 5) {
                media(genre: $genre, type: ANIME, sort: POPULARITY_DESC) {
                    id
                    title { romaji }
                    genres
                }
            }
        }"""

        recommendations = []
        for genre in genres:
            try:
                response = requests.post(
                    'https://graphql.anilist.co',
                    json={'query': query, 'variables': {'genre': genre}}
                )
                response.raise_for_status()
                media = response.json().get("data", {}).get("Page", {}).get("media", [])
                recommendations.extend(media)
            except requests.RequestException:
                continue  # skip failed genre fetch

        return Response(recommendations)


# ✅ /anime/watched/ and /anime/watched/<int:pk>/
class WatchedAnimeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = WatchedAnime.objects.filter(user=request.user)
        return Response(WatchedAnimeSerializer(qs, many=True).data)

    def post(self, request):
        ser = WatchedAnimeSerializer(data={**request.data, "user": request.user.id})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=201)

    def delete(self, request, pk):
     try:
        obj = WatchedAnime.objects.get(id=pk, user=request.user)
        obj.delete()
        return Response({"message": "Deleted successfully"}, status=200)
     except WatchedAnime.DoesNotExist:
        return Response({"message": "No record found"}, status=404)
