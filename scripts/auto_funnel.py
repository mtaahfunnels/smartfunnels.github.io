import os
import json
import requests
import argparse
from pathlib import Path
from string import Template
from dotenv import load_dotenv

# ----------------------------
# Load GitHub Token and Username from .env
# ----------------------------
load_dotenv()
GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME") or "mtaahfunnels"  # Optional fallback
ORG_NAME = "smartfunnels"

# ----------------------------
# Parse Command-Line Arguments
# ----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--link", required=True)
args = parser.parse_args()
affiliate_link = args.link.strip()

# Extract slug from domain or path
parsed = affiliate_link.split("?")[0].replace("https://", "").replace("http://", "").strip("/")

if "/" in parsed:
    slug = parsed.split("/")[-1].lower() or parsed.split(".")[0].lower()
else:
    slug = parsed.split(".")[0].lower()

tool = slug.replace("-", " ").title()
pain = f"Tired of manually doing what {tool} automates?"

# ----------------------------

# Paths
# ----------------------------
base_path = Path(__file__).resolve().parent.parent
funnel_path = base_path / "tools" / slug
config_path = base_path / "config.json"
funnel_path.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Load form_action from config
# ----------------------------
if not config_path.exists():
    print("❌ Missing config.json")
    exit(1)

with open(config_path) as f:
    config = json.load(f)
    form_action = config.get("form_action", "")

# ----------------------------
# HTML Templates
# ----------------------------
HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>
  <title>Fix SEO Meta Tags Fast</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #f4f6fb;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }
    .box {
      background: white;
      border-radius: 16px;
      padding: 40px 30px;
      max-width: 460px;
      width: 90%;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.07);
      text-align: center;
    }
    h1 {
      font-size: 22px;
      color: #111;
      margin-bottom: 10px;
    }
    p {
      font-size: 16px;
      color: #555;
      margin-bottom: 25px;
    }
    form input[type=\"email\"] {
      width: 100%;
      padding: 14px;
      font-size: 15px;
      border: 1px solid #ccc;
      border-radius: 8px;
      margin-bottom: 16px;
      box-sizing: border-box;
    }
    .btn {
      background: #007bff;
      color: white;
      font-size: 16px;
      padding: 14px;
      width: 100%;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s ease;
    }
    .btn:hover {
      background: #0056b3;
    }
    .footer {
      font-size: 12px;
      color: #888;
      margin-top: 16px;
    }
  </style>
</head>
<body>
  <div class=\"box\">
    <h1>⛔ $pain</h1>
    <p><strong>$tool</strong> helps you solve this in minutes, not hours.</p>
    <form action=\"$form_action\" method=\"post\">
      <input type=\"email\" name=\"email_1\" placeholder=\"Enter your email\" required />
      <input type=\"text\" name=\"a1091816c\" tabindex=\"-1\" value=\"\" style=\"position: absolute; left: -5000px;\" />
      <input type=\"email\" name=\"b1091816c\" tabindex=\"-1\" value=\"\" style=\"position: absolute; left: -5000px;\" />
      <input type=\"checkbox\" name=\"c1091816c\" tabindex=\"-1\" style=\"position: absolute; left: -5000px;\" />
      <input type=\"hidden\" name=\"ok_redirect\" value=\"https://$GITHUB_USERNAME.github.io/smartcontentline-$slug/thankyou.html\" />
      <button class=\"btn\" type=\"submit\">🚀 Show Me the Shortcut</button>
    </form>
    <p class=\"footer\">No spam. Unsubscribe any time.</p>
  </div>
</body>
</html>
""")

THANKYOU_HTML = Template("""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>You're In – Next Steps</title>
  <style>
    body {
      background-color: #f8f9fc;
      font-family: 'Segoe UI', sans-serif;
      text-align: center;
    }
    .container {
      max-width: 600px;
      margin: 60px auto;
      background: #fff;
      padding: 40px;
      border-radius: 12px;
      box-shadow: 0 0 18px rgba(0, 0, 0, 0.05);
    }
    .btn {
      display: inline-block;
      margin-top: 30px;
      padding: 14px 26px;
      background-color: #007bff;
      color: white;
      text-decoration: none;
      font-size: 16px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class=\"container\">
    <h1>You're in! 🎉</h1>
    <p>We’ve sent a shortcut to your inbox. But you can jump straight to the tool:</p>
    <a href=\"$link\" class=\"btn\" target=\"_blank\">👉 Try it Now</a>
    <p class=\"note\">Check your inbox to save the link for later use.</p>
  </div>
</body>
</html>
""")

# ----------------------------
# Write Files
# ----------------------------
index_html = HTML_TEMPLATE.substitute(
    tool=tool,
    pain=pain,
    link=affiliate_link,
    slug=slug,
    form_action=form_action,
    GITHUB_USERNAME=GITHUB_USERNAME
)
thankyou_html = THANKYOU_HTML.substitute(link=affiliate_link)

(funnel_path / "index.html").write_text(index_html.strip(), encoding="utf-8")
(funnel_path / "thankyou.html").write_text(thankyou_html.strip(), encoding="utf-8")

print(f"✅ Funnel created in {funnel_path}")

# ----------------------------
# Post Deploy: Push to GitHub
repo_name = f"smartcontentline-{slug}"

os.chdir(funnel_path)
os.system("git init")
os.system(f"git remote add origin https://github.com/{ORG_NAME}/{repo_name}.git")
os.system("git checkout -b main")
os.system("git add .")
os.system('git commit -m "🚀 Auto-generated funnel"')
os.system("git push -u origin main")

# ----------------------------
# Auto-enable GitHub Pages via GitHub API
# ----------------------------
headers = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github+json"
}

pages_url = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}/pages"

response = requests.post(pages_url, headers=headers, json={
    "source": {
        "branch": "main",
        "path": "/"
    }
})

if response.status_code in [201, 204]:
    print("✅ GitHub Pages enabled successfully.")
    print(f"🌍 Final Live URL: https://{ORG_NAME}.github.io/{repo_name}/")
else:
    print("❌ Failed to enable GitHub Pages.")
    print("Response:", response.status_code, response.text)


print(f"🌍 Deployed to: https://{ORG_NAME}.github.io/{repo_name}/")
