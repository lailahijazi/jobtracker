from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Vi använder samma idé som tidigare: spara allt i en JSON-fil
DATA_FILE = Path("jobs.json")


def load_jobs():
    """Läs in alla sparade jobb från jobs.json."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Om filen är trasig börjar vi om med tom lista
        return []


def save_jobs(jobs):
    """Spara listan med jobb till jobs.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)


def get_next_id(jobs):
    """Ge nästa lediga id, t.ex. 1, 2, 3, ..."""
    if not jobs:
        return 1
    return max(job["id"] for job in jobs) + 1


@app.route("/")
def index():
    """Visa startsidan med alla jobb."""
    filter_value = request.args.get("filter", "all")
    jobs = load_jobs()

    if filter_value == "open":
        jobs = [job for job in jobs if not job.get("applied")]

    return render_template("index.html", jobs=jobs, filter_value=filter_value)


@app.route("/add", methods=["POST"])
def add_job():
    """Ta emot formuläret och lägga till ett jobb."""
    jobs = load_jobs()

    title = request.form.get("title", "").strip()
    company = request.form.get("company", "").strip()
    link = request.form.get("link", "").strip()
    notes = request.form.get("notes", "").strip()

    if not title or not company:
        # Om du inte fyllt i det viktigaste – skit i det och gå tillbaka
        return redirect(url_for("index"))

    new_job = {
        "id": get_next_id(jobs),
        "title": title,
        "company": company,
        "link": link or None,
        "notes": notes or None,
        "applied": False,
        "date_applied": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    jobs.append(new_job)
    save_jobs(jobs)

    return redirect(url_for("index"))


@app.route("/apply/<int:job_id>", methods=["POST"])
def mark_applied(job_id):
    """Markera ett jobb som sökt."""
    jobs = load_jobs()

    for job in jobs:
        if job["id"] == job_id:
            job["applied"] = True
            job["date_applied"] = datetime.now().strftime("%Y-%m-%d")
            break

    save_jobs(jobs)
    return redirect(url_for("index"))


@app.route("/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    """Ta bort ett jobb helt."""
    jobs = load_jobs()
    jobs = [job for job in jobs if job["id"] != job_id]
    save_jobs(jobs)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
