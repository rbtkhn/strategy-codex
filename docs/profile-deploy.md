# Deploy the profile to grace-mar.com

The profile is static HTML generated from the instance profile. To serve it at **https://grace-mar.com**, use GitHub Pages with a custom domain. **Domains (grace-mar.com, companion-self.com) are registered with Namecheap** â€” DNS steps below use Namecheapâ€™s Advanced DNS.

---

## 1. One-time: Enable GitHub Pages and custom domain

### 1.1 Turn on Pages

1. In your repo: **Settings** â†’ **Pages** (under â€œCode and automationâ€).
2. Under **Build and deployment**:
   - **Source:** Deploy from a branch.
   - **Branch:** `gh-pages` / `/(root)`.
3. Save. The site will be available at `https://<org>.github.io/grace-mar/` (or your user/org URL) once the workflow has run.

### 1.2 Add grace-mar.com as custom domain

1. Still in **Settings** â†’ **Pages**.
2. Under **Custom domain**, enter: `grace-mar.com`.
3. Click **Save**. GitHub will show the DNS records you need.

### 1.3 Configure DNS at your registrar

Where you manage grace-mar.com (e.g. **Namecheap**, Cloudflare, Google Domains):

#### Namecheap (grace-mar.com, companion-self.com)

1. Log in at [namecheap.com](https://www.namecheap.com) â†’ **Domain List** â†’ click **Manage** next to the domain.
2. Open the **Advanced DNS** tab.
3. **For apex (grace-mar.com)** â€” Add four **A Record** entries:
   - Host: `@` | Type: `A Record` | Value: `185.199.108.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.109.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.110.153`  | TTL: Automatic
   - Host: `@` | Type: `A Record` | Value: `185.199.111.153`  | TTL: Automatic  
   Remove any existing **URL Redirect** or **A Record** for `@` if they conflict.
4. **Optional â€” www redirect:** If you want `www.grace-mar.com` to work, add a **CNAME Record**: Host `www` â†’ Value `rbtkhn.github.io` (or `<your-org>.github.io`). Then in GitHub Pages you can add `www.grace-mar.com` as well, or use Namecheapâ€™s â€œURL Redirectâ€ to send www to grace-mar.com.
5. Save. DNS can take 5â€“30 minutes to propagate.

Repeat the same A records for **companion-self.com** (or another host) if you point that domain at a different service later.

#### Other registrars

**Option A â€” Apex domain (grace-mar.com):**

- Add **A** records pointing to GitHubâ€™s IPs. GitHub shows these in the Pages custom-domain section; as of 2024 they are:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`

**Option B â€” Subdomain (e.g. www.grace-mar.com):**

- Add a **CNAME** record: `www` â†’ `<org>.github.io` (or `rbtkhn.github.io` if itâ€™s a user repo). Then in GitHub Pages custom domain, use `www.grace-mar.com` instead of `grace-mar.com`.

**If you use Cloudflare:** Turn **Proxy** (orange cloud) off for the A or CNAME record so GitHub can validate and serve the site, or use â€œDNS onlyâ€.

Wait for DNS to propagate (minutes to a few hours). Back in **Settings** â†’ **Pages**, GitHub will show â€œDNS check successfulâ€ and will issue an HTTPS certificate for grace-mar.com.

---

## 2. Deploy the profile (every time you want to update)

Two workflows can deploy the profile:

- **`.github/workflows/deploy-profile.yml`** (recommended) â€” Uses official GitHub Actions (`upload-pages-artifact` + `deploy-pages`). Ensures `profile/CNAME` contains `grace-mar.com` so the custom domain works. **Requires:** In repo **Settings â†’ Pages**, set **Source** to **GitHub Actions** (not "Deploy from a branch"). Triggers on push to `main` when `**`, `scripts/generate_profile.py`, `profile/CNAME`, or the workflow file change.
- **`.github/workflows/pages.yml`** â€” Uses `peaceiris/actions-gh-pages` to push the `profile/` folder to the `gh-pages` branch. Use when Pages is set to **Deploy from a branch** (branch: `gh-pages`, folder: root). Also add `profile/CNAME` with `grace-mar.com` so the custom domain is set.

Pushes that only touch docs or other paths skip the deploy. You can also run either workflow manually.

### Fast loop â€” Local preview (seconds, no push)

See profile changes immediately without pushing:

```bash
python3 scripts/generate_profile.py
open profile/index.html   # macOS; on Linux: xdg-open profile/index.html
```

Or use the preview script (generates + opens):

```bash
./scripts/preview_profile.sh
```

When youâ€™re happy, push to `main`; the workflow will run and update grace-mar.com in about a minute.

### Option A â€” Push to main

```bash
git add -A
git commit -m "Update profile"
git push origin main
```

The **Deploy profile to Pages** workflow runs `python3 scripts/generate_profile.py`, ensures `profile/CNAME` is set for grace-mar.com, and publishes the `profile/` folder (via `gh-pages` branch or GitHub Actions artifact). In a minute or two, https://grace-mar.com will show the new content.

### Option B â€” Run the workflow manually

1. **Actions** â†’ **Deploy profile to Pages** â†’ **Run workflow** â†’ **Run workflow**.
2. The workflow uses the current `main`; it will generate the profile and update `gh-pages`.

### Option C â€” Build and push gh-pages yourself

If you donâ€™t want to use the workflow:

```bash
python3 scripts/generate_profile.py
git checkout gh-pages   # or create branch: git checkout -b gh-pages
git add profile/
git commit -m "Profile update"
git push origin gh-pages
git checkout main
```

---

## 3. Verify

- **https://grace-mar.com** â€” Landing page with buttons: Profile, Telegram, WeChat, LLM.
- **https://grace-mar.com/profile** â€” Full profile view (identity, pipeline, SKILLS, benchmarks).
- **https://grace-mar.com/telegram** â€” If configured, opens the Telegram chat with your Grace-Mar bot (instant redirect to `t.me/YourBotUsername`). To enable: create `telegram_bot_username.txt` with one line, your botâ€™s username from @BotFather (e.g. `MyGraceMarBot`, no `@`). Regenerate the profile and redeploy.
- **https://grace-mar.com/llm** â€” Full PRP prompt text only, one-tap copy. Paste into any LLM (ChatGPT, Claude, etc.). Content is from `grace-mar-llm.txt`; regenerate with `export_prp.py` and redeploy to refresh.
- **https://grace-mar.com/wechat** â€” If configured, redirects to your WeChat Official Account URL (e.g. mp.weixin.qq.com link). Add the URL in one line to `WECHAT_ACCOUNT_URL.txt`, regenerate the profile, and redeploy. See `bot/wechat-setup.md`.
- **https://grace-mar.com/playlist** â€” Placeholder; playlist feature coming later.
- In the Telegram bot, set `PROFILE_MINIAPP_URL=https://grace-mar.com` (or `DASHBOARD_MINIAPP_URL`) so the menu button opens this URL.

---

## 4. Troubleshooting

| Issue | What to do |
|-------|------------|
| â€œDNS check failedâ€ | Wait longer for DNS; ensure A or CNAME matches what GitHub shows. **Namecheap:** Use Advanced DNS (not â€œRedirect Domainâ€); remove conflicting URL Redirect or A records for `@`. If using Cloudflare, try DNS only (grey cloud). |
| 404 after deploy | Confirm Pages source is branch `gh-pages`, folder `/ (root)`. Confirm the workflow ran and updated `gh-pages`. |
| Old content still showing | Hard refresh (Ctrl+Shift+R / Cmd+Shift+R) or wait for CDN; re-run the workflow if needed. |
| Certificate / â€œNot secureâ€ | GitHub provisions HTTPS for the custom domain after DNS validates; can take up to an hour. |

---

**Documentation site (MkDocs):** The repo includes `mkdocs.yml` for a navigable docs site. Build with `mkdocs build` (output in `site/`). To deploy docs alongside the profile, add a step that runs `pip install mkdocs mkdocs-readthedocs-theme` and `mkdocs build`, then copy `site/` into `profile/docs/` before uploading the artifact so that https://grace-mar.com/docs/ serves the MkDocs site. See [MkDocs](https://www.mkdocs.org/) for local preview (`mkdocs serve`).

**See also:** [namecheap-guide.md](namecheap-guide.md) (simple Namecheap steps), [miniapp-setup.md](miniapp-setup.md) (profile vs Q&A app), [telegram-webhook-setup.md](telegram-webhook-setup.md) (bot menu button).

---

## 5. Accelerating the loop (HTML â†” Cursor â†” Telegram)

| What you want | What to do |
|---------------|------------|
| **See profile changes in seconds** | Run `./scripts/preview_profile.sh` (or `python3 scripts/generate_profile.py` then `open profile/index.html`). No push required. |
| **Deploy only when profile changes** | The workflow runs only when `**`, `scripts/generate_profile.py`, or the workflow file change. Doc-only pushes skip the deploy. |
| **Re-run deploy without a new commit** | **Actions** â†’ **Deploy profile to Pages** â†’ **Run workflow**. Uses current `main`. |
| **Telegram â†’ Cursor** | If the bot runs **locally** (e.g. `python -m bot.bot`), SESSION-TRANSCRIPT, RECURSION-GATE, and archive updates land in your repo immediately. If it runs on a server (e.g. Render), you need a sync step (e.g. pull from server or run the bot locally for development) so Cursor and the profile see the latest. |

