from dis import code_info
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect
from .decorators import *


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, "game/index.html",{'modules':module.objects.all()})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def view_team(request):
    thatteam = request.user.playername.first().team
    uniqueplayers = thatteam.get_players()
    print(uniqueplayers)
    return render(request, "game/viewteam.html", {
                        "message": "You exist in this team",
                        "players": uniqueplayers, "code": thatteam.code, "game": game.objects.all(), "team": thatteam.name,
                    })

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmationpassword = request.POST["confirmation-password"]
        if password != confirmationpassword:
            return render(request, "game/register.html", {
                "message": "Passwords does not match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "game/register.html", {
                "message": "Username already taken"
            })
        login(request, user)
        # return render(request, "game/register.html", {
        #     "message": "registered"
        # })
        return redirect('index')
    else: 
        return render(request, "game/register.html")

@login_required(login_url='/accounts/login/')
def createteam(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user.playername.count() == 0:
                try:
                    teamname = request.POST["teamname"]
                    updateteam = team(name=teamname)
                    updateteam.save()
                    uniquecode = team.objects.get(name=teamname)
                    updateteam = team.objects.get(name=teamname)
                    user = request.user.username
                    userid = User.objects.get(username=user)
                    updateplayer = player(name=userid, team=updateteam)
                    updateplayer.save()
                    return render(request, "game/jointeam.html", {
                        "message": f"team created. code: {uniquecode.code} \nPlease keep this safe and share it with your teammates to join the team. Only one person should execute the activity from each team"
                    })
                except IntegrityError:
                    return render(request, "game/createteam.html", {
                        "message": "team already exists with this name"
                    })
            else:
                return render(request, "game/createteam.html", {
                        "message": "User already belongs a team"
                    })
        else:
            return render(request, "game/createteam.html", {
                "message": "user is not authenticated"
            })
    else:
        return render(request, "game/createteam.html")


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_game(request, id):
    g = game.objects.get(pk=id)
    return render(request, "game/play_game.html", {
        "game": g
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_game_scenario(request, id):
    g = game.objects.get(pk=id)
    q_id = g.questions.first().id


    return render(request, "game/play_game_scenario.html", {
        "game": g, "q_id": q_id
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_game_question(request, id, cur_q_id, ans):
    g = game.objects.get(pk=id)
    current_user = request.user
    team = current_user.playername.first().team

    
    if team.questions.filter(id=cur_q_id).count() > 0:
        print('removing last score')
        last_attempt = team.questions.filter(id=cur_q_id).first()
        team.questions.remove(last_attempt)
    
    if question.objects.filter(id=cur_q_id).count() > 0:
        attempted_question = question.objects.filter(id=cur_q_id).first()
        print(cur_q_id, ans, attempted_question.right_answer)
        
        if attempted_question and attempted_question.right_answer == 'Y' and ans == 1:
            team.questions.add(attempted_question)
            print('adding new score - if')
        elif attempted_question and attempted_question.right_answer == 'N' and ans == 0:
            team.questions.add(attempted_question)
            print('adding new score - ifelse')

    team.save()


    if g.questions.filter(id__gt=cur_q_id).count() > 0:
        q = g.questions.filter(id__gt=cur_q_id).first() # ans for prev this

        display_q = question.objects.filter(id__lte=q.id, game=g.id).count()

        return render(request, "game/play_game_question.html", {
            "game": g, "question": q,
            "cur_q_id": q.id,
            "display_q": display_q,
        })
    else:

        if team.scoreteam.count() > 0:
            thatteamscore = team.scoreteam.first()
        else:
            thatteamscore = teamscore(team=team, score=0)
        thatteamscore.score = team.questions.count()*10

        thatteamscore.save()

        return render(request, "game/result.html", {
        "allteamscore": teamscore.objects.all().order_by("score")
    })

@login_required(login_url='/accounts/login/')
def jointeam(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                teamcode = request.POST["teamcode"]
                try:
                    thatteam = team.objects.get(code=teamcode)
                except ValidationError:
                    return render(request, "game/jointeam.html", {
                        "message": "team does not exitsts"
                    })
                thatuser = request.user
                uniqueplayers = []
                playersinthatteam = player.objects.filter(team=thatteam)
                for players in playersinthatteam:
                    if players.name not in uniqueplayers:
                        uniqueplayers.append(players.name)
                if request.user in uniqueplayers:
                    print(thatteam)
                    return HttpResponseRedirect(reverse('view_team'))
                    # return render(request, "game/viewteam.html", {
                    #     "message": "You exist in this team",
                    #     "players": uniqueplayers, "code": thatteam.code, "game": game.objects.all(), "team": thatteam.name,
                    # })
                elif len(uniqueplayers) == 4:
                    return render(request, "game/jointeam.html", {
                        "message": "Team is full"
                    })
                else:
                    player.objects.filter(name=thatuser).delete()
                    thatplayer = player(name=thatuser, team=thatteam)
                    thatplayer.save()
                    uniqueplayers.append(thatplayer.name)
                    print('there')
                    return HttpResponseRedirect(reverse('view_team'))
                    # return render(request, "game/viewteam.html", {
                    #     "players": uniqueplayers, "code": thatteam.code, "game": game.objects.all(), "team": thatteam.name,
                    # })
            except ObjectDoesNotExist:
                return render(request, "game/jointeam.html", {
                    "message": "team does not exists"
                })
        else:
            return render(request, "game/jointeam.html", {
                "message": "User is not authenticated"
            })
    else:
        return render(request, "game/jointeam.html")

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def viewleaderboard(request):
    return render(request, "game/result.html", {
        "allteamscore": teamscore.objects.all().order_by("score")
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_module(request, id):
    m = module.objects.get(pk=id)
    seg = m.segments.first()
    return render(request, "game/play_module.html", {
        "module": m,
        'seg': seg,
        "cur_q_id": 0,
        "ans": 0
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_module_segment(request, id, seg_id, cur_q_id, ans, option):

    current_user = request.user
    team = current_user.playername.first().team
    if team.module_questions.filter(id=cur_q_id).count() > 0:
        print('removing last score')
        last_attempt = team.module_questions.filter(id=cur_q_id).first()
        team.module_questions.remove(last_attempt)
    if module_question.objects.filter(id=cur_q_id).count() > 0:
        attempted_question = module_question.objects.filter(id=cur_q_id).first()
        print(cur_q_id, ans, attempted_question.right_answer)
        
        if attempted_question and attempted_question.right_answer == 'Y' and ans == 1 \
            and attempted_question.right_option.strip().upper() == option.strip().upper():
            team.module_questions.add(attempted_question)
            print('adding new score - if')
        elif attempted_question and attempted_question.right_answer == 'N' and ans == 0:
            team.module_questions.add(attempted_question)
            print('adding new score - ifelse')
    team.save()

    if(seg_id==786):
        m = module.objects.get(pk=id)
        m_games = m.games.all()
        result_set = {}
        atleast_one_retake = False
        atleast_one_passed = False
        for g in m_games:
            correct_ans = team.module_questions.filter(game=g).count()
            total_ques = module_question.objects.filter(game=g).count()
            g_id = g.game.id
            percent_score = correct_ans/total_ques*100
            if percent_score >= 60:
                recommend_retake = False
                atleast_one_passed=True
            else:
                recommend_retake = True
                atleast_one_retake = True
            result_set[g.game.name] = {}
            result_set[g.game.name]['correct_ans'] = correct_ans
            result_set[g.game.name]['total_ques'] = total_ques
            result_set[g.game.name]['g_id'] = g_id
            result_set[g.game.name]['percent_score'] = percent_score
            result_set[g.game.name]['recommend_retake'] = recommend_retake
        return render(request, "game/play_module_results.html",
            {'result_set':result_set,'atleast_one_retake':atleast_one_retake,
            'atleast_one_passed':atleast_one_passed})
    else:
        seg = module_segment.objects.get(pk=seg_id)
        seg_q = seg.module_questions.first().id

        if(module.objects.get(pk=id).segments.first().id==seg.id):
            seg_q = 0
            ans = 0

        return render(request, "game/play_module_segment.html", {
            "seg": seg, 
            "seg_q": seg_q,
            "id":seg.module.id,
            "ans": ans
        })

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def play_module_question(request, id, seg_id, cur_q_id, ans):
    seg = module_segment.objects.get(pk=seg_id)
    seg_q = seg.module_questions.first()

    if module_segment.objects.filter(id__gt=seg_id).count() > 0:
        seg = module_segment.objects.filter(id__gt=seg_id).first().id
    else:
        seg = 786

    return render(request, "game/play_module_question.html", {
        "seg": seg, 
        "seg_q": seg_q,
        "id":id,
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.playername.count() > 0, login_url='/')
def get_module_question_options(request, seg_q_id):
    seg_q = module_question.objects.get(pk=seg_q_id)
    options = {'option_A':'wrong'}

    if seg_q.right_answer=='Y':
        options = {'option_A':seg_q.option_A,
                    'option_B':seg_q.option_B,
                    'option_C':seg_q.option_C}


    return JsonResponse(options)



def credits(request):

    return render(request, "game/credits.html",{'credits':credit.objects.all()})