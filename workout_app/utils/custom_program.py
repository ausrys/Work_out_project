from workout_app.models import MuscleGroup


def calculate_sets_reps_weight(user, muscle_group, bodyweight=False):
    # Reps based on experience level
    if user.level.level.lower() == 'begginer':
        reps, sets = 10, 3
    elif user.level.level.lower() == 'intermediate':
        reps, sets = 8, 4
    else:
        reps, sets = 6, 5

    # Weight logic (bodyweight exercises vs external weight)
    if bodyweight:
        # Advanced users can do weighted bodyweight
        weight = 0
        if reps <= 6:
            weight = int(user.weight * 0.1)  # Add 10% body weight
    else:
        # External weights based on muscle group
        try:
            muscle = MuscleGroup.objects.get(name__iexact=muscle_group)
            factor = muscle.base_multiplier
        except MuscleGroup.DoesNotExist:
            factor = 0.5  # fallback if group not found
        weight = int(user.weight * factor)

    return reps, sets, weight
