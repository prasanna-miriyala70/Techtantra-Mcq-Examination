# Tech Tantra Solution MCQ Examination - Django + MySQL

This is a Django version of the MCQ examination website. It keeps the original 40 TTS Set D questions, 40-minute timer, camera preview, instructions, candidate registration, score calculation, and result page.

## What is stored in MySQL

- **Candidate**: name and email.
- **Question**: question text, four options, and the correct option (only on the server).
- **ExamAttempt**: start time, end time, number of answered questions, score, and submission status.
- **Answer**: the selected answer and whether it was correct.

Correct answers are never added to the exam HTML page. Django calculates the score on the backend after submission.

## 1. Install the required programs on Windows

Install these first:

1. Python 3.10 or newer.
2. MySQL Server 8 or MariaDB Server.
3. MySQL Workbench (optional but useful for beginners).

Open PowerShell in this project folder and create a virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `mysqlclient` does not install on Windows, install the official MySQL Server and its C++ build tools, then rerun the final `pip install` command. The MySQL server must be running.

## 2. Create the MySQL database

Open MySQL Workbench or a MySQL command prompt, sign in as the MySQL root user, and run these commands. Change `choose_a_strong_password` before running them.

```sql
CREATE DATABASE mcq_exam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mcq_exam_user'@'localhost' IDENTIFIED BY 'choose_a_strong_password';
GRANT ALL PRIVILEGES ON mcq_exam_db.* TO 'mcq_exam_user'@'localhost';
FLUSH PRIVILEGES;
```

## 3. Create the `.env` file

Copy `.env.example` and rename the copy to `.env`. Put your real MySQL password in `MYSQL_PASSWORD` and create a long private value for `DJANGO_SECRET_KEY`.

Example local values:

```text
DJANGO_SECRET_KEY=a-long-random-private-value-not-shared-online
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
MYSQL_DATABASE=mcq_exam_db
MYSQL_USER=mcq_exam_user
MYSQL_PASSWORD=choose_a_strong_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Never upload `.env` to GitHub or send it to anyone, because it contains passwords and the Django secret key.

## 4. Prepare and run the application

With the virtual environment active, run these commands in order:

```powershell
python manage.py migrate
python manage.py load_tts_questions
python manage.py createsuperuser
python manage.py runserver
```

Open the candidate site at `http://127.0.0.1:8000/`.

Open the admin panel at `http://127.0.0.1:8000/admin/` and sign in using the superuser you created. The admin panel lets an administrator manage questions, candidates, attempts/results, and saved answers.

## Hostinger VPS deployment hand-off

This project is ready to hand to a deployment team. Do **not** run `runserver` in production.

1. Use a Hostinger **VPS** with Python/Django support; a normal shared plan is not sufficient for Django.
2. Create a production MySQL/MariaDB database and a limited database user.
3. Upload the project without `.env` and then create a protected `.env` on the server.
4. Set `DJANGO_DEBUG=False` and set `DJANGO_ALLOWED_HOSTS` to the real domain name.
5. Create a Linux virtual environment and install `requirements.txt`.
6. Run `python manage.py migrate`, `python manage.py load_tts_questions`, `python manage.py collectstatic --noinput`, and `python manage.py createsuperuser`.
7. Run the application using Gunicorn behind Hostinger's reverse proxy/OpenLiteSpeed or Nginx. Example Gunicorn command:

```bash
gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000 --timeout 60
```

8. Configure HTTPS/SSL before setting `DJANGO_DEBUG=False`; the project enables secure cookies and HTTPS redirect when debug mode is off.
9. Load-test the VPS, database, and worker settings before claiming any exact concurrent-user number.

## Concurrency note

The project uses MySQL, indexed attempt queries, server-side expiry, and an atomic database transaction while saving answers. These are good foundations for 500-1000 users, but actual capacity depends on the VPS CPU/RAM, database configuration, web-server configuration, and test traffic. It must be load-tested before making a performance guarantee.
