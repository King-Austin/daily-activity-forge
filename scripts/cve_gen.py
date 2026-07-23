import os
import json
import requests
from datetime import datetime, timezone
import groq_client

SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_sec.json")

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen[-50:], f)

def main():
    print("Checking The Hacker News for new cybersecurity developments...")
    try:
        # Use rss2json to parse the Hacker News RSS feed reliably
        rss_url = "https://feeds.feedburner.com/TheHackersNews"
        api_url = f"https://api.rss2json.com/v1/api.json?rss_url={rss_url}"
        
        resp = requests.get(api_url, timeout=10)
        
        if resp.status_code != 200:
            print(f"Failed to fetch security news: {resp.status_code}")
            return None
            
        posts = resp.json().get("items", [])
        seen = load_seen()
        
        for post in posts:
            post_id = post.get("guid") or post.get("link")
            
            if post_id and post_id not in seen:
                title = post.get("title", "")
                url = post.get("link", "")
                
                print(f"Found new security post: {title}")
                
                prompt = f"I am maintaining a developer log. I just saw a cybersecurity update titled: '{title}'. The link is {url}. Write a concise, 2-3 sentence devlog entry summarizing the potential threat or technical insight here. Keep it professional and act as if I am keeping tabs on industry security."
                
                content = groq_client.ask_groq(prompt)
                
                now = datetime.now(timezone.utc)
                date_str = now.strftime("%Y-%m-%d")
                hour_str = now.strftime("%H")
                time_str = now.strftime("%H:%M UTC")
                
                md_content = f"# Security Update: {title}\n\n_{date_str} {time_str}_\n\n[Source]({url})\n\n{content}\n"
                
                os.makedirs(os.path.join(os.path.dirname(__file__), "..", "devlog"), exist_ok=True)
                import hashlib
                safe_id = hashlib.md5(post_id.encode()).hexdigest()[:8]
                out_path = f"devlog/{date_str}-{hour_str}-{safe_id}.md"
                full_out_path = os.path.join(os.path.dirname(__file__), "..", out_path)
                
                with open(full_out_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                
                seen.append(post_id)
                save_seen(seen)
                
                print(f"cve_gen: wrote {out_path}")
                return out_path
                
        print("No new security posts found.")
        return None
        
    except Exception as e:
        print(f"Error in cve_gen: {e}")
        return None

if __name__ == "__main__":
    main()
