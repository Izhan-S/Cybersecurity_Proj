from unicodedata import name
import uuid
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("create_team", views.createteam, name="createteam"),
    path("join_team", views.jointeam, name="jointeam"),
    path("view_team", views.view_team, name="view_team"),
    path("result", views.viewleaderboard, name="leaderboard"),

    path("play_game/<int:id>", views.play_game, name="play_game"),
    path("play_game/<int:id>/question/<int:cur_q_id>/<int:ans>", views.play_game_question, name="play_game_question"),
    path("play_game/<int:id>/scenario", views.play_game_scenario, name="play_game_scenario"),

    path("play_module/<int:id>", views.play_module, name="play_module"),
    path("play_module/<int:id>/segment/<int:seg_id>/question/<int:cur_q_id>/<int:ans>/video/<str:option>", views.play_module_segment, name="play_module_segment"),
    path("play_module/<int:id>/segment/<int:seg_id>/question/<int:cur_q_id>/<int:ans>/question", views.play_module_question, name="play_module_question"),
    path("play_module/<int:seg_q_id>/options", views.get_module_question_options, name="get_module_question_options"),

    path("credits", views.credits, name="credits"),
    
]



if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)