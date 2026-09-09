# audit.py - Free SEO Audit Tool
import requests
from bs4 import BeautifulSoup
import re

def quick_audit(url):
    """
    Perform a quick SEO audit on the given URL.
    Returns a dict with:
        title, has_meta, h1_count, word_count, speed_score,
        fix_1, fix_2, fix_3, link_spots
    """
    # ----- 1. Fetch HTML -----
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        return {
            "title": "Error fetching URL",
            "has_meta": False,
            "h1_count": 0,
            "word_count": 0,
            "speed_score": 0,
            "fix_1": f"Could not fetch: {str(e)}",
            "fix_2": "",
            "fix_3": "",
            "link_spots": 0
        }

    # ----- 2. Parse with BeautifulSoup -----
    soup = BeautifulSoup(html, 'html.parser')

    # Title
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else "No title found"
    title_len = len(title)

    # Meta description
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    has_meta = bool(meta_tag and meta_tag.get('content'))

    # H1 count
    h1_tags = soup.find_all('h1')
    h1_count = len(h1_tags)

    # Word count (strip tags, split)
    text = soup.get_text(separator=' ')
    words = re.findall(r'\w+', text)
    word_count = len(words)

    # External link count (sellable spots)
    links = soup.find_all('a', href=True)
    external_links = [a for a in links if a['href'].startswith('http') and not a['href'].startswith(url)]
    link_spots = len(external_links)

    # ----- 3. Google PageSpeed Insights (free, no API key required for limited use) -----
    speed_score = 0
    try:
        pagespeed_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
        ps_resp = requests.get(pagespeed_url, timeout=15)
        if ps_resp.status_code == 200:
            data = ps_resp.json()
            speed_score = data.get('lighthouseResult', {}).get('categories', {}).get('performance', {}).get('score', 0) * 100
            speed_score = int(speed_score)
    except Exception:
        speed_score = 0

    # ----- 4. Generate actionable fixes -----
    fixes = []
    if not has_meta:
        fixes.append("Add a meta description to improve click-through rates.")
    if h1_count == 0:
        fixes.append("Add at least one H1 heading to structure your content.")
    elif h1_count > 1:
        fixes.append("Multiple H1s found – consider using one main H1.")
    if title_len < 30:
        fixes.append("Your title is too short – aim for 50-60 characters.")
    elif title_len > 60:
        fixes.append("Your title is too long – keep it under 60 characters.")
    if word_count < 300:
        fixes.append("Aim for at least 300 words per page for better SEO.")
    if speed_score < 50:
        fixes.append("Page speed is low – optimize images and reduce server response time.")
    elif speed_score < 80:
        fixes.append("Improve performance to reach 80+ score.")

    while len(fixes) < 3:
        fixes.append("Regularly update your content to stay fresh.")

    fix_1, fix_2, fix_3 = fixes[0], fixes[1], fixes[2]

    return {
        "title": title,
        "has_meta": has_meta,
        "h1_count": h1_count,
        "word_count": word_count,
        "speed_score": speed_score,
        "fix_1": fix_1,
        "fix_2": fix_2,
        "fix_3": fix_3,
        "link_spots": link_spots
    }