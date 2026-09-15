from django.contrib import admin
from .models import Answer, Candidate, ExamAttempt, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "short_text", "correct_option")
    list_editable = ("correct_option",)
    ordering = ("order",)

    @admin.display(description="Question")
    def short_text(self, item):
        return item.text[:70]


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "selected_option", "is_correct")
    can_delete = False


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "score", "answered_count", "is_submitted", "started_at", "submitted_at")
    list_filter = ("is_submitted", "submitted_at")
    search_fields = ("candidate__name", "candidate__email")
    readonly_fields = ("started_at", "expires_at", "submitted_at", "score", "answered_count")
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_option", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("attempt__candidate__name", "attempt__candidate__email")
