from django.db import models


class Candidate(models.Model):
    """A person registered to take an exam."""
    name = models.CharField(max_length=120)
    email = models.EmailField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Question(models.Model):
    """One MCQ question. The answer is intentionally never sent to the template."""
    order = models.PositiveSmallIntegerField(unique=True)
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.PositiveSmallIntegerField(help_text="0=A, 1=B, 2=C, 3=D")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:55]}"


class ExamAttempt(models.Model):
    """One timed attempt and its calculated final result."""
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    answered_count = models.PositiveSmallIntegerField(default=0)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["candidate", "is_submitted"])]

    def __str__(self):
        return f"Attempt #{self.id} - {self.candidate.name}"


class Answer(models.Model):
    """The selected option for a question within an attempt."""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    selected_option = models.PositiveSmallIntegerField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["attempt", "question"], name="one_answer_per_question")]

    def __str__(self):
        return f"Attempt {self.attempt_id}, Question {self.question.order}"
