from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import CandidateForm
from .models import Answer, Candidate, ExamAttempt, Question


EXAM_DURATION = timedelta(minutes=40)


def instructions(request):
    return render(request, "exam/instructions.html")


@never_cache
def register_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()

            existing_candidate = Candidate.objects.filter(
                email__iexact=email
            ).first()

            if existing_candidate:
                form.add_error(
                    "email",
                    "This email has already been used for an examination."
                )
            else:
                candidate = Candidate.objects.create(
                    name=form.cleaned_data["name"],
                    email=email
                )

                attempt = ExamAttempt.objects.create(
                    candidate=candidate,
                    expires_at=timezone.now() + EXAM_DURATION
                )

                request.session["attempt_id"] = attempt.id

                return redirect("exam")

    else:
        form = CandidateForm()

    return render(
        request,
        "exam/register.html",
        {"form": form}
    )


@never_cache
def exam(request):
    attempt_id = request.session.get("attempt_id")

    # No active candidate session.
    if not attempt_id:
        return redirect("instructions")

    attempt = get_object_or_404(
        ExamAttempt,
        id=attempt_id
    )

    # Submitted exams must never be opened again.
    if attempt.is_submitted:
        return redirect("result", attempt_id=attempt.id)

    # Automatically submit when the 40-minute period ends.
    if timezone.now() >= attempt.expires_at:
        return submit_attempt(request, attempt)

    # Correct answers are never sent to the frontend.
    questions = Question.objects.values(
        "id",
        "order",
        "text",
        "option_a",
        "option_b",
        "option_c",
        "option_d"
    )

    return render(
        request,
        "exam/exam.html",
        {
            "attempt": attempt,
            "questions": questions
        }
    )


@require_POST
@never_cache
def submit_exam(request):
    attempt_id = request.session.get("attempt_id")

    if not attempt_id:
        return redirect("instructions")

    attempt = get_object_or_404(
        ExamAttempt,
        id=attempt_id
    )

    return submit_attempt(request, attempt)


def submit_attempt(request, attempt):
    """
    Saves answers and calculates the score only once.
    Database locking prevents duplicate submissions.
    """

    with transaction.atomic():
        attempt = ExamAttempt.objects.select_for_update().get(
            id=attempt.id
        )

        # Exam was already submitted.
        if attempt.is_submitted:
            return redirect("result", attempt_id=attempt.id)

        saved_answers = []

        for question in Question.objects.all():
            value = request.POST.get(f"question_{question.id}")

            if value not in {"0", "1", "2", "3"}:
                continue

            selected_option = int(value)

            saved_answers.append(
                Answer(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option,
                    is_correct=(
                        selected_option == question.correct_option
                    )
                )
            )

        Answer.objects.bulk_create(saved_answers)

        attempt.answered_count = len(saved_answers)
        attempt.score = sum(
            answer.is_correct for answer in saved_answers
        )
        attempt.submitted_at = timezone.now()
        attempt.is_submitted = True

        attempt.save(
            update_fields=[
                "answered_count",
                "score",
                "submitted_at",
                "is_submitted"
            ]
        )

    return redirect("result", attempt_id=attempt.id)


@never_cache
def result(request, attempt_id):
    attempt = get_object_or_404(
        ExamAttempt.objects.select_related("candidate"),
        id=attempt_id
    )

    return render(
        request,
        "exam/result.html",
        {"attempt": attempt}
    )