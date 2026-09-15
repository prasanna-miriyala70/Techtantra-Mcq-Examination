from django.core.management.base import BaseCommand
from exam.models import Question


# TTS Set D: text, four options, correct option number (0=A, 1=B, 2=C, 3=D).
QUESTION_DATA = [
    ("If 30% of a number is 90, the number is:", ["200", "250", "300", "350"], 2),
    ("A shirt marked at Rs. 2,000 is sold at a 15% discount. What is the selling price?", ["Rs. 1,600", "Rs. 1,650", "Rs. 1,700", "Rs. 1,750"], 2),
    ("The average of 10 numbers is 45. Their total is:", ["400", "450", "500", "550"], 1),
    ("A car travels at 60 km/h. How far will it travel in 45 minutes?", ["30 km", "40 km", "45 km", "50 km"], 2),
    ("The ratio 24:36 in its simplest form is:", ["2:3", "3:4", "4:5", "5:6"], 0),
    ("If the cost price is Rs. 500 and selling price is Rs. 575, the profit is:", ["10%", "12%", "15%", "18%"], 2),
    ("What is the next prime number after 29?", ["30", "31", "33", "35"], 1),
    ("A sum doubles in 5 years under simple interest. The annual interest rate is:", ["10%", "15%", "20%", "25%"], 2),
    ("If 3x = 45, then x + 5 =", ["15", "18", "20", "25"], 2),
    ("A and B can complete a work in 10 and 15 days respectively. Together they take:", ["5 days", "6 days", "7 days", "8 days"], 1),
    ("Find the next number: 5, 10, 20, 40, ?", ["60", "70", "80", "100"], 2),
    ("If PEN is coded as QFO, how is BOOK coded?", ["CPPL", "CQQM", "APPL", "CPOK"], 0),
    ("Find the odd one out:", ["Square", "Triangle", "Circle", "Cube"], 3),
    ("A is the brother of B. B is the sister of C. What is A's relationship with C?", ["Father", "Brother", "Uncle", "Cousin"], 1),
    ("Find the missing number: 4, 8, 16, 32, ?", ["48", "56", "64", "72"], 2),
    ("If SOUTH is written as HTUOS, how is NORTH written?", ["HTRON", "HTRNO", "HORTN", "HNORT"], 0),
    ("A man faces east. He turns left, then right, then right again. Which direction is he facing?", ["North", "South", "East", "West"], 1),
    ("Statement: Some students are athletes. All athletes are disciplined. Which conclusion follows?", ["Some students are disciplined", "All students are disciplined", "No students are disciplined", "All disciplined people are athletes"], 0),
    ("Find the next pair: AZ, BY, CX, DW, ?", ["EV", "FU", "EX", "EW"], 0),
    ("Complete the analogy: Doctor : Hospital :: Teacher : ?", ["Court", "School", "Bank", "Factory"], 1),
    ("What is the passage mainly about?", ["Employee salaries", "Effective leadership", "Business competition", "Recruitment procedures"], 1),
    ("A good leader should:", ["Only give instructions", "Avoid employees", "Communicate and listen", "Make all decisions alone"], 2),
    ("Leaders can improve productivity by:", ["Ignoring strengths", "Assigning responsibilities according to abilities", "Reducing teamwork", "Avoiding communication"], 1),
    ("The passage suggests that people:", ["Have identical strengths", "Have different strengths", "Should perform the same tasks", "Cannot learn new skills"], 1),
    ("The word ‘responsibility’ most nearly means:", ["Duty", "Reward", "Complaint", "Vacation"], 0),
    ("Synonym of DILIGENT:", ["Lazy", "Hardworking", "Careless", "Weak"], 1),
    ("Antonym of TRANSPARENT:", ["Clear", "Visible", "Opaque", "Bright"], 2),
    ("Synonym of EVALUATE:", ["Assess", "Ignore", "Reject", "Delay"], 0),
    ("Antonym of GENEROUS:", ["Kind", "Helpful", "Selfish", "Charitable"], 2),
    ("‘The proposal was feasible.’ Feasible means:", ["Impossible", "Practical", "Expensive", "Uncertain"], 1),
    ("Choose the correctly spelled word:", ["Privilege", "Privelege", "Priviledge", "Privilage"], 0),
    ("Synonym of ABOLISH:", ["Establish", "Eliminate", "Continue", "Support"], 1),
    ("Antonym of FREQUENT:", ["Regular", "Common", "Rare", "Repeated"], 2),
    ("‘The candidate was articulate.’ Articulate means:", ["Able to express ideas clearly", "Unable to speak", "Nervous", "Confused"], 0),
    ("Synonym of RESILIENT:", ["Fragile", "Adaptable", "Weak", "Passive"], 1),
    ("Choose the synonym of PRUDENT:", ["Careless", "Wise", "Reckless", "Impulsive"], 1),
    ("Choose the antonym of SCARCE:", ["Rare", "Limited", "Abundant", "Insufficient"], 2),
    ("The word ‘AMBIGUOUS’ means:", ["Very clear", "Having more than one possible meaning", "Extremely simple", "Completely accurate"], 1),
    ("Choose the synonym of ENHANCE:", ["Improve", "Reduce", "Damage", "Remove"], 0),
    ("Choose the antonym of CONCISE:", ["Brief", "Precise", "Lengthy", "Clear"], 2),
]


class Command(BaseCommand):
    help = "Create or update the 40 questions from TTS Set D."

    def handle(self, *args, **options):
        for order, (text, answers, correct_option) in enumerate(QUESTION_DATA, start=1):
            Question.objects.update_or_create(order=order, defaults={
                "text": text, "option_a": answers[0], "option_b": answers[1],
                "option_c": answers[2], "option_d": answers[3], "correct_option": correct_option,
            })
        self.stdout.write(self.style.SUCCESS("40 TTS Set D questions are ready."))
