#from asyncio.windows_events import NULL
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class game(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    image = models.ImageField(upload_to='upload')
    video = models.FileField(upload_to='videos_uploaded',null=True,
            validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    intro = models.TextField()
    def __str__(self):
        return f"{self.name}"

class question(models.Model):
    scenario = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='upload')
    right_answer = models.CharField(max_length=1, default='Y')
    game = models.ForeignKey(game, on_delete=models.CASCADE, related_name="questions")
    def __str__(self):
        return f"{self.game}, {self.scenario[:75]}"

##
class module(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    intro = models.TextField(max_length=1000)
    def __str__(self):
        return f"{self.name}"

class module_game(models.Model):
    #name = models.CharField(max_length=1000, unique=True)
    game = models.ForeignKey(game, on_delete=models.CASCADE, related_name="module_games", unique=True)
    module = models.ForeignKey(module, on_delete=models.CASCADE, related_name="games")
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.game}"

class module_segment(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    video = models.FileField(upload_to='videos_uploaded',null=True,
            validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    module = models.ForeignKey(module, on_delete=models.CASCADE, related_name="segments")
    def __str__(self):
        return f"{self.name}"

class module_question(models.Model):
    scenario = models.TextField(max_length=1000)
    right_answer = models.CharField(max_length=1, default='Y')
    game = models.ForeignKey(module_game, on_delete=models.CASCADE, related_name="module_questions")
    segment = models.ForeignKey(module_segment, on_delete=models.CASCADE, related_name="module_questions")
    option_A = models.CharField(max_length=1000)
    option_B = models.CharField(max_length=1000)
    option_C = models.CharField(max_length=1000)
    right_option = models.CharField(max_length=1, default='A')
    def __str__(self):
        return f"{self.segment} {self.game}"

class team(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    code = models.UUIDField(default=uuid.uuid4, primary_key=True) # editable=False,
    questions = models.ManyToManyField(question)
    module_questions = models.ManyToManyField(module_question)
    def __str__(self):
        return f"{self.name}"

    def get_player_names(self):
        players = player.objects.filter(team=self)
        names = []
        for p in players:
            names.append(p.name.__str__())
        return ','.join(names)

    def get_players(self):
        return player.objects.filter(team=self)

class player(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="playername", default=0)
    team = models.ForeignKey(team, on_delete=models.CASCADE, null=True, related_name="playerteam", default=0)
    def __str__(self):
        return f"{self.name}, {self.team}"

class teamscore(models.Model):
    team = models.ForeignKey(team, on_delete=models.CASCADE, related_name="scoreteam", unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team}, {self.score}"

class credit(models.Model):
    name = models.CharField(max_length=1000)
    credit_text = models.TextField(max_length=1000)
    def __str__(self):
        return f"{self.name[:100]}"