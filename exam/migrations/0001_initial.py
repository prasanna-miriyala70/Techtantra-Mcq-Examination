import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Candidate", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)), ("email", models.EmailField(db_index=True, max_length=254)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name="Question", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("order", models.PositiveSmallIntegerField(unique=True)), ("text", models.TextField()),
            ("option_a", models.CharField(max_length=500)), ("option_b", models.CharField(max_length=500)),
            ("option_c", models.CharField(max_length=500)), ("option_d", models.CharField(max_length=500)),
            ("correct_option", models.PositiveSmallIntegerField(help_text="0=A, 1=B, 2=C, 3=D")),
        ], options={"ordering": ["order"]}),
        migrations.CreateModel(name="ExamAttempt", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("started_at", models.DateTimeField(auto_now_add=True)), ("expires_at", models.DateTimeField()),
            ("submitted_at", models.DateTimeField(blank=True, null=True)), ("score", models.PositiveSmallIntegerField(default=0)),
            ("answered_count", models.PositiveSmallIntegerField(default=0)), ("is_submitted", models.BooleanField(default=False)),
            ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="attempts", to="exam.candidate")),
        ]),
        migrations.CreateModel(name="Answer", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("selected_option", models.PositiveSmallIntegerField()), ("is_correct", models.BooleanField(default=False)),
            ("attempt", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="exam.examattempt")),
            ("question", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="exam.question")),
        ]),
        migrations.AddConstraint(model_name="answer", constraint=models.UniqueConstraint(fields=("attempt", "question"), name="one_answer_per_question")),
        migrations.AddIndex(model_name="examattempt", index=models.Index(fields=["candidate", "is_submitted"], name="attempt_candidate_idx")),
    ]
