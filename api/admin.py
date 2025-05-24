# from django.contrib import admin
# from .models import User, WatchedAnime
# from django.contrib.auth.admin import UserAdmin

# admin.site.register(User, UserAdmin)
# admin.site.register(WatchedAnime)

from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, WatchedAnime
import requests

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'view_recommendations_link')

    def view_recommendations_link(self, obj):
        return format_html(
            '<a class="button" href="recommendations/{}/">View Recommendations</a>', obj.pk
        )
    view_recommendations_link.short_description = 'Recommendations'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('recommendations/<int:user_id>/', self.admin_site.admin_view(self.recommendations_view)),
        ]
        return custom_urls + urls

    def recommendations_view(self, request, user_id):
        user = User.objects.get(pk=user_id)
        preferences = user.preferences or ''
        genres = [g.strip() for g in preferences.split(",") if g.strip()]

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
                continue

        return TemplateResponse(request, "admin/user_recommendations.html", {
            "user": user,
            "recommendations": recommendations
        })

# ✅ No need to unregister first
admin.site.register(User, CustomUserAdmin)
admin.site.register(WatchedAnime)
