import os
import argparse
import json
from pathlib import Path
from string import Template

# ----------------------------
# Load Config (form_action from config.json)
# ----------------------------
base_path = Path(__file__).resolve().parent.parent  # smartcontentline/
config_path = base_path / "config.json"

if not config_path.exists():
    raise FileNotFoundError("config.json not found in project root.")

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

form_action = config.get("form_action")
if not form_action:
    raise ValueError("Missing 'form_action' in config.json")


# ----------------------------
# HTML Templates
# ----------------------------
HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
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
    form input[type="email"] {
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
  <div class="box">
    <h1>⛔ Still wasting time on SEO meta tags?</h1>
    <p>Generate high-converting titles & descriptions in seconds — no guesswork, no manual writing.</p>

    <form action="$form_action" method="post">
      <input type="email" name="email_1" placeholder="Enter your email" required />
      <input type="text" name="a1091816c" tabindex="-1" value="" style="position: absolute; left: -5000px;" />
      <input type="email" name="b1091816c" tabindex="-1" value="" style="position: absolute; left: -5000px;" />
      <input type="checkbox" name="c1091816c" tabindex="-1" style="position: absolute; left: -5000px;" />
      <input type="hidden" name="ok_redirect" value="https://mtaahfunnels.github.io/smartcontentline-$slug/thankyou.html" />
      <button class="btn" type="submit">🚀 Show Me the Shortcut</button>
    </form>

    <p class="footer">No spam. Unsubscribe any time.</p>
  </div>
</body>
</html>
""")

THANKYOU_HTML = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>You're In – Next Steps</title>
  <style>
    body {
      background-color: #f8f9fc;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      text-align: center;
    }
    .container {
      max-width: 600px;
      margin: 60px auto;
      background: #fff;
      padding: 40px 30px;
      border-radius: 12px;
      box-shadow: 0 0 18px rgba(0, 0, 0, 0.05);
    }
    h1 {
      color: #333;
    }
    p {
      color: #555;
      line-height: 1.6;
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
      transition: background-color 0.3s ease;
    }
    .btn:hover {
      background-color: #0056b3;
    }
    .note {
      margin-top: 20px;
      font-size: 14px;
      color: #888;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>You're in! 🎉</h1>
    <p>We’ve sent a shortcut to your inbox.</p>
    <p>In the meantime, you can go straight to the tool here:</p>
    <a href="$link" target="_blank" class="btn">👉 Go to Your Tool Now</a>
    <p class="note">Check your inbox to save the link for later use.</p>
  </div>
</body>
</html>
""")


# ----------------------------
# CLI Argument Parser
# ----------------------------
parser = argparse.ArgumentParser(description="Generate a funnel folder and files.")
parser.add_argument("--tool", required=True, help="Name of the SaaS tool")
parser.add_argument("--slug", required=True, help="URL-friendly folder name (e.g. blog-helper)")
parser.add_argument("--pain", required=True, help="Pain point the tool solves")
parser.add_argument("--link", required=True, help="Your affiliate link")

args = parser.parse_args()

# ----------------------------
# Create Output Folder
# ----------------------------
target_folder = base_path / "tools" / args.slug
target_folder.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Write index.html
# ----------------------------
index_html = HTML_TEMPLATE.substitute(
    tool=args.tool,
    pain=args.pain,
    link=args.link,
    slug=args.slug,
    form_action=form_action
)
(target_folder / "index.html").write_text(index_html.strip(), encoding="utf-8")

# ----------------------------
# Write thankyou.html
# ----------------------------
thankyou_html = THANKYOU_HTML.substitute(link=args.link)
(target_folder / "thankyou.html").write_text(thankyou_html.strip(), encoding="utf-8")

print(f"✅ Funnel created: {target_folder}")
print(f"   - index.html")
print(f"   - thankyou.html")
