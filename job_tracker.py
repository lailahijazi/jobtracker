import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("jobs.json")

def load_jobs():
    if not DATA_FILE.exists(): return[]
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Filen jobs.json är korrupt. Börja om med tom lista.")
        return[]
    
def save_jobs(jobs):
    """Spara jobb till fil."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

def get_next_id(jobs):
    """Hitta nästa lediga ID."""
    if not jobs: 
        return 1 
    return max(job["id"] for job in jobs) + 1

def add_job():
    jobs = load_jobs()

    print("\n--- Lägg till nytt jobb ---")
    title= input("Jobbtitel: ").strip()
    company = input("Företag: ").strip()
    link = input("Länk till annons (valfritt): ").strip()
    notes = input("Anteckningar (valfritt): ").strip()

    if not title or not company: 
        print("Titel och företag måste fyllas i. Försök igen.")
        return
    
    new_job= {
        "id": get_next_id(jobs),
        "title": title,
        "company": company,
        "link": link if link else None,
        "notes": notes if notes else None,
        "applied": False,
        "date_applied": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    jobs.append(new_job)
    save_jobs(jobs)
    print(f"\n✅ Lagt till jobb #{new_job['id']} - {new_job['title']} på {new_job['company']}")

def list_jobs(only_not_applied=False):
    jobs = load_jobs()
    if not jobs:
        print("\n(Inga jobb sparade än.)")
        return
    filtered = [job for job in jobs if not job["applied"]]
    if not filtered:
        print("\n( Inga jobb matchar filtret. )")
        return
    
    print("\n--- Jobb ---")
    for job in filtered:
        status = "✅ SÖKT" if job["applied"] else " INTE SÖKT "
        print(f"\nID: {job['id']} | {status}")
        print(f" Title: {job['title']}")
        print(f" Företag: {job['company']}")
        if job.get("link"):
            print(f" Länk: {job['link']}")
        if job.get("notes"):
            print(f" Notis: {job['notes']}")
        if job["applied"] and job.get("date_applied"):
            print(f" Datum sökt: {job['date_applied']}")

def mark_as_applied():
    jobs = load_jobs()
    if not jobs: 
        print("\nDet finns inga jobb att markera")
        return
    list_jobs(only_not_applied=True)
    
    try: 
        job_id = int(input("\nSkriv ID på det jobb du har sökt: "))
    except ValueError:
        print("Ogiltigt ID (måste vara en siffra).")
        return
    
    for job in jobs: 
        if job["id"] == job_id:
            if job["applied"]:
                print("Det här jobbet är redan markerat som sökt")
                return
            job["applied"] = True
            job["date_applied"] = datetime.now().strftime("%Y-%m-%d")
            save_jobs(jobs)
            print(f"\n Markerade jobb #{job_id} som sökt.")
            return
        print("Hittade inget jobb med det ID:t.")

def main_menu(): 
    while True: 
        print("\n===========================")
        print("   DIN JOBBLISTA    ")
        print("=============================")
        print("1) Lägg till jobb")
        print("2) Visa alla jobb")
        print("3) Visa endast INTE sökta jobb")
        print("4) Markera jobb som SÖKT")
        print("5) Avsluta")

        choice = input("\nVälj (1-5): ").strip()

        if choice == "1":
            add_job()
        elif choice == "2":
            list_jobs()
        elif choice == "3":
            list_jobs(only_not_applied=True)
        elif choice == "4":
            mark_as_applied()
        elif choice == "5": 
            print("\nHejdå. Gå och sök fler jobb.")
            break
        else: 
            print("Ogiltigt val, försök igen.")

if __name__== "__main__":
    main_menu()

    
