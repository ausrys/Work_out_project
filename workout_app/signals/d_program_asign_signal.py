
# in signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from workout_app.models import Sportsman, UserProgram, CustomExercise, \
    BaseProgramExercise, BaseProgram
# You’ll create this
from workout_app.utils.custom_program import calculate_sets_reps_weight


@receiver(post_save, sender=Sportsman)
def assign_default_programs(sender, instance, created, **kwargs):
    if not created:
        return

    # Assign a few base programs (or filter/select)
    base_programs = BaseProgram.objects.all()[:2]  # First 2 for example

    for base_program in base_programs:
        user_program = UserProgram.objects.create(
            user=instance,
            name=base_program.name,
            description=base_program.description,
            is_custom=False
        )

        base_exercises = BaseProgramExercise.objects.filter(
            program=base_program)

        for base_ex in base_exercises:
            reps, sets, weight = calculate_sets_reps_weight(
                instance,
                base_ex.exercise.muscle_group.name,
                bodyweight=base_ex.exercise.bodyweight
            )

            CustomExercise.objects.create(
                user=instance,
                program=user_program,
                base_exercise=base_ex.exercise,
                reps=reps,
                sets=sets,
                weight=weight
            )
