import time
import schedule
import subprocess
import os
import sys

# Add scripts directory to path to import generators
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
import news_gen
import cve_gen

def check_news():
    print("Executing news check...")
    result = news_gen.main()
    if result:
        print(f"News generated: {result}. Committing...")
        subprocess.run(["sh", "run_forge.sh", "docs: update TIL with latest tech news"])

def check_sec():
    print("Executing security check...")
    result = cve_gen.main()
    if result:
        print(f"Security log generated: {result}. Committing...")
        subprocess.run(["sh", "run_forge.sh", "docs: log latest security update"])

def run_weekly():
    print("Running weekly cycle...")
    subprocess.run(["sh", "run_weekly.sh"])

# Polling every 15 minutes for organic, event-driven updates.
schedule.every(15).minutes.do(check_news)
schedule.every(20).minutes.do(check_sec)

# Weekly PR
schedule.every().sunday.at("23:00").do(run_weekly)

if __name__ == "__main__":
    print("AI-Powered Scheduler started. Waiting for real-world events...")
    
    # Run once at startup to populate initial data
    check_news()
    check_sec()
    
    while True:
        schedule.run_pending()
        time.sleep(60)
