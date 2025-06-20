# import requests
# from bs4 import BeautifulSoup
# import openai
# import time
# import os

# # ✅ OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # ✅ ClickUp credentials
# CLICKUP_LIST_ID = "901607808438"  # ✅ Your actual List ID
# CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")

# # ✅ List of plugin review URLs
# REVIEW_URLS = [
#     "https://wordpress.org/support/plugin/the-plus-addons-for-elementor-page-builder/reviews/",
#     "https://wordpress.org/support/plugin/nexter-extension/reviews/",
#     "https://wordpress.org/support/plugin/the-plus-addons-for-block-editor/reviews/",
#     "https://wordpress.org/support/plugin/wdesignkit/reviews/",
#     "https://wordpress.org/support/plugin/uichemy/reviews/",
# ]

# SEEN_FILE = "seen_reviews.txt"


# # 🔍 Step 1: Scrape latest review topic links
# def get_review_links(base_url, limit=5):
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     links = []

#     topic_links = soup.select("a.bbp-topic-permalink")
#     for topic in topic_links[:limit]:
#         title = topic.get_text(strip=True)
#         url = topic["href"]
#         links.append((title, url))

#     return links


# # 📄 Step 2: Extract full review content from each link
# def get_review_content(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     review_box = soup.find("div", class_="bbp-topic-content")
#     return review_box.get_text(strip=True) if review_box else "[No review text found]"


# # ✍️ Step 3: Generate a response using OpenAI
# def generate_response(review):
#     prompt = f"""
# You are an assistant helping Posimyth respond to WordPress plugin reviews for products like The Plus Addons, UiChemy, Nexter, and WDesignKit.

# Here is a review from a user:
# \"{review}\"

# 👉 Core Instructions:

# ✅ Positive Review Responses (5-star)
# - Thank the user warmly for their feedback.
# - Mention that only a few users leave reviews and it means a lot.
# - Acknowledge what they appreciated (e.g., features, support).
# - Let them know you're always available to help.
# - Subtly mention other tools (WDesignKit, UiChemy, Nexter) as complements.
# - Sign off: “Kind Regards, The Plus Addons Team”

# ❗ For Negative Reviews (1–3 stars)
# - Use neutral, respectful language—avoid emotional words.
# - Acknowledge feedback and invite more details for support.
# - Suggest possible causes (plugin conflicts, setup) without blame.
# - Reassure that help is available.
# - Keep it short, helpful, and professional.

# ⭐ For 4-star Reviews
# - Thank the user and ask what would’ve made it a 5-star experience.

# 📌 General Guidelines
# - Be warm, friendly, and human.
# - Avoid corporate or robotic tone.
# - Use phrases like “Thanks a lot!” or “Feel free to reply anytime.”
# - Never sound defensive, even if the review is wrong.

# ✍️ Write a response that fits the tone based on the review. Keep it brief and natural.
# """
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=250
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"[ERROR generating response: {e}]"


# # 🗂️ Step 4: Create a task in ClickUp
# def create_clickup_task(title, review_url, review_text, response_text, clickup_list_id, clickup_api_token):
#     url = f"https://api.clickup.com/api/v2/list/{clickup_list_id}/task"

#     headers = {
#         "Authorization": clickup_api_token,
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "name": f"Review: {title}",
#         "description": f"""🔗 Review URL: {review_url}

# 📝 **Review Content**
# {review_text}

# 💬 **Generated Response**
# {response_text}
# """,
#         "status": "to do"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code in [200, 201]:
#         print(f"✅ Task created for: {title}")
#     else:
#         print(f"❌ Failed to create task for: {title}")
#         print(f"➡️ Status Code: {response.status_code}")
#         print(f"🧾 Response: {response.text}")


# # ✅ Step 5: Track seen reviews to avoid duplicates
# def load_seen_reviews():
#     if not os.path.exists(SEEN_FILE):
#         return set()
#     with open(SEEN_FILE, "r") as f:
#         return set(line.strip() for line in f)


# def save_seen_review(url):
#     with open(SEEN_FILE, "a") as f:
#         f.write(url + "\n")


# # 🚀 Run the bot
# if __name__ == "__main__":
#     print("🔍 Checking for new reviews...")
#     seen_reviews = load_seen_reviews()
#     new_count = 0

#     for base_url in REVIEW_URLS:
#         print(f"\n🔗 Scanning: {base_url}")
#         review_links = get_review_links(base_url, limit=10)

#         for title, link in review_links:
#             if link in seen_reviews:
#                 print(f"✅ Already processed: {link}")
#                 continue

#             review_text = get_review_content(link)
#             response_text = generate_response(review_text)

#             create_clickup_task(
#                 title=title,
#                 review_url=link,
#                 review_text=review_text,
#                 response_text=response_text,
#                 clickup_list_id=CLICKUP_LIST_ID,
#                 clickup_api_token=CLICKUP_API_TOKEN
#             )

#             save_seen_review(link)
#             new_count += 1
#             time.sleep(2)  # 🛡️ Respect ClickUp rate limits

#     print(f"\n✅ Done. New tasks created: {new_count}")

import requests
from bs4 import BeautifulSoup
import openai
import time
import os

# ✅ OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# ✅ ClickUp credentials
CLICKUP_LIST_ID = "901607387060"
CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")

# ✅ List of plugin review URLs
REVIEW_URLS = [
    "https://wordpress.org/support/plugin/the-plus-addons-for-elementor-page-builder/reviews/",
    "https://wordpress.org/support/plugin/nexter-extension/reviews/",
    "https://wordpress.org/support/plugin/the-plus-addons-for-block-editor/reviews/",
    "https://wordpress.org/support/plugin/wdesignkit/reviews/",
    "https://wordpress.org/support/plugin/uichemy/reviews/",
]

SEEN_FILE = "seen_reviews.txt"


# 🔍 Step 1: Scrape latest review topic links
def get_review_links(base_url, limit=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(base_url, headers=headers)
    # print(f"[DEBUG HTML FROM] {base_url}\n{response.text[:1000]}")
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    topic_links = soup.select("a.bbp-topic-permalink") or soup.select("li.review a")
    if not topic_links:
        print("⚠️ No topic links found on the page!")

    for topic in topic_links[:limit]:
        title = topic.get_text(strip=True)
        url = topic["href"]
        links.append((title, url))

    return links


# 📄 Step 2: Extract full review content from each link
def get_review_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    review_box = soup.find("div", class_="bbp-topic-content")
    return review_box.get_text(strip=True) if review_box else "[No review text found]"


# ✍️ Step 3: Generate a response using OpenAI
def generate_response(review):
    prompt = f"""
You are an assistant helping Posimyth respond to WordPress plugin reviews for products like The Plus Addons, UiChemy, Nexter, and WDesignKit.

Here is a review from a user:
\"{review}\"

👉 Core Instructions:

✅ Positive Review Responses (5-star)
- Thank the user warmly for their feedback.
- Mention that only a few users leave reviews and it means a lot.
- Acknowledge what they appreciated (e.g., features, support).
- Let them know you're always available to help.
- Subtly mention other tools (WDesignKit, UiChemy, Nexter) as complements.
- Sign off: “Kind Regards, The Plus Addons Team”

❗ For Negative Reviews (1–3 stars)
- Use neutral, respectful language—avoid emotional words.
- Acknowledge feedback and invite more details for support.
- Suggest possible causes (plugin conflicts, setup) without blame.
- Reassure that help is available.
- Keep it short, helpful, and professional.

⭐ For 4-star Reviews
- Thank the user and ask what would’ve made it a 5-star experience.

📌 General Guidelines
- Be warm, friendly, and human.
- Avoid corporate or robotic tone.
- Use phrases like “Thanks a lot!” or “Feel free to reply anytime.”
- Never sound defensive, even if the review is wrong.

✍️ Write a response that fits the tone based on the review. Keep it brief and natural.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR generating response: {e}]"


# 🗂️ Step 4: Create a task in ClickUp
def create_clickup_task(title, review_url, review_text, response_text, clickup_list_id, clickup_api_token):
    url = f"https://api.clickup.com/api/v2/list/{clickup_list_id}/task"

    headers = {
        "Authorization": clickup_api_token,
        "Content-Type": "application/json"
    }

    payload = {
        "name": f"Review: {title}",
        "description": f"""🔗 Review URL: {review_url}

📝 **Review Content**
{review_text}

💬 **Generated Response**
{response_text}
""",
        "status": "to do",
         "assignees": [94894049, 94894033, 94892542]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        print(f"✅ Task created for: {title}")
    else:
        print(f"❌ Failed to create task for: {title}")
        print(f"➡️ Status Code: {response.status_code}")
        print(f"🧾 Response: {response.text}")


# ✅ Step 5: Track seen reviews to avoid duplicates
def load_seen_reviews():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)


def save_seen_review(url):
    with open(SEEN_FILE, "a") as f:
        f.write(url + "\n")


# 🚀 Run the bot
if __name__ == "__main__":
    print("🔍 Checking for new reviews...")
    seen_reviews = load_seen_reviews()
    new_count = 0

    for base_url in REVIEW_URLS:
        print(f"\n🔗 Scanning: {base_url}")
        review_links = get_review_links(base_url, limit=10)

        for title, link in review_links:
            if link in seen_reviews:
                print(f"✅ Already processed: {link}")
                continue

            review_text = get_review_content(link)
            response_text = generate_response(review_text)

            create_clickup_task(
                title=title,
                review_url=link,
                review_text=review_text,
                response_text=response_text,
                clickup_list_id=CLICKUP_LIST_ID,
                clickup_api_token=CLICKUP_API_TOKEN
            )

            save_seen_review(link)
            new_count += 1
            time.sleep(2)  # 🛡️ Respect ClickUp rate limits

    print(f"\n✅ Done. New tasks created: {new_count}")


