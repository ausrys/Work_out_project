from django.contrib import admin
from .models import City, SportsmanLevel, BaseExercise, \
    CustomExercise, UserProgram, Sportsman, MuscleGroup, \
    BaseProgram, BaseProgramExercise, Coach, UserLog, \
    Advertiser, AdvertiserAPI, BlogPost
# Register your models here.
admin.site.register(City)
admin.site.register(SportsmanLevel)
admin.site.register(Sportsman)
admin.site.register(BaseExercise)
admin.site.register(CustomExercise)
admin.site.register(UserProgram)
admin.site.register(MuscleGroup)
admin.site.register(BaseProgram)
admin.site.register(BaseProgramExercise)
admin.site.register(Coach)
admin.site.register(UserLog)
admin.site.register(Advertiser)
admin.site.register(AdvertiserAPI)
admin.site.register(BlogPost)
