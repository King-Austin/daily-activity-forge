import os
import json
import requests
from datetime import datetime, timezone
import groq_client

SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_news.json")

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen[-50:], f) # keep last 50 to avoid infinite growth

def main():
    print("Checking Hacker News for new top story...")
    try:
        # Get top stories
        resp = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        resp.raise_for_status()
        top_ids = resp.json()[:5]
        
        seen = load_seen()
        
        for item_id in top_ids:
            if item_id not in seen:
                # Fetch details
                item_resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=10)
                item_resp.raise_for_status()
                item = item_resp.json()
                
                title = item.get("title", "")
                url = item.get("url", f"https://news.ycombinator.com/item?id={item_id}")
                
                print(f"Found new trending story: {title}")
                
                prompt = f"I just read this trending Hacker News article titled: '{title}'. The URL is {url}. Write a short, single-paragraph 'Today I Learned' (TIL) entry about the potential implications or technical takeaways of this news for a software developer. Do not use generic filler, make it sound like a real developer's note."
                
                content = groq_client.ask_groq(prompt)
                
                # Write to file
                now = datetime.now(timezone.utc)
                date_str = now.strftime("%Y-%m-%d")
                hour_str = now.strftime("%H")
                time_str = now.strftime("%H:%M UTC")
                
                md_content = f"# TIL: {title}\n\n_{date_str} {time_str}_\n\n[Original Source]({url})\n\n{content}\n"
                
                os.makedirs(os.path.join(os.path.dirname(__file__), "..", "til"), exist_ok=True)
                out_path = f"til/{date_str}-{hour_str}-{item_id}.md"
                full_out_path = os.path.join(os.path.dirname(__file__), "..", out_path)
                
                with open(full_out_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                
                seen.append(item_id)
                save_seen(seen)
                
                print(f"news_gen: wrote {out_path}")
                return out_path
                
        print("No new stories found on Hacker News.")
        return None
        
    except Exception as e:
        print(f"Error in news_gen: {e}")
        return None

if __name__ == "__main__":
    main()
