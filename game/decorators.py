from django.contrib.auth.decorators import user_passes_test

def team_required():
    def in_team(u):
        if u.is_authenticated:
            if u.playername.count() > 0:
                return True
        return False
    return user_passes_test(in_team)