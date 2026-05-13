# GitHub Actions Setup Guide

This project uses GitHub Actions for automated content generation, maintenance, and deployment.

## Workflows

### 1. Generate Content (`generate-content.yml`)

**Schedule:** Daily at 2 AM UTC (configurable)

**What it does:**
- Generates next batch of pending terms (default 20)
- Validates with quality gate
- Updates internal links
- Commits changes automatically
- Logs token usage and failures

**Manual trigger:**
```bash
# Via GitHub UI: Actions → Generate Content → Run workflow
# Or via CLI:
gh workflow run generate-content.yml -f batch_size=20 -f priority=1
```

### 2. Maintenance (`maintenance.yml`)

**Schedule:** Weekly on Sunday at 3 AM UTC

**What it does:**
- Scans for duplicate slugs in CSV
- Checks for broken related_terms links
- Validates CSV format
- Generates content statistics
- Commits maintenance logs

### 3. Deploy (`deploy.yml`)

**Trigger:** Push to `main` branch

**What it does:**
- Builds Astro site
- Generates Pagefind search index
- Deploys to Cloudflare Pages
- Comments on PRs with preview link

## Setup Instructions

### Step 1: Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

#### For Content Generation:
```
AI_PROVIDER          = groq (or gemini)
GROQ_API_KEY         = your_groq_api_key
GEMINI_API_KEY       = your_gemini_api_key
DAILY_LIMIT          = 100 (optional, default 100)
```

#### For Cloudflare Deployment:
```
CLOUDFLARE_API_TOKEN = your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID = your_account_id
```

**How to get Cloudflare credentials:**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Create token with "Cloudflare Pages" permissions
3. Copy token and account ID

### Step 2: Enable Workflows

1. Go to **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"
3. Workflows will now run on schedule

### Step 3: Test Workflows

**Test content generation:**
```bash
gh workflow run generate-content.yml -f batch_size=5
```

**Test deployment:**
```bash
git push origin main
```

## Workflow Customization

### Change Generation Schedule

Edit `.github/workflows/generate-content.yml`:

```yaml
on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
```

**Common cron patterns:**
- `0 2 * * *` — Daily at 2 AM UTC
- `0 */6 * * *` — Every 6 hours
- `0 9 * * 1-5` — Weekdays at 9 AM UTC
- `0 0 * * 0` — Weekly on Sunday at midnight UTC

### Change Batch Size

Edit `.github/workflows/generate-content.yml`:

```yaml
batch_size:
  default: '50'  # Change from 20 to 50
```

### Disable Auto-Commit

If you want to review changes before committing, comment out the "Commit and push changes" step:

```yaml
- name: Commit and push changes
  if: false  # Disable auto-commit
```

## Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Click on workflow name
3. See all runs with status, duration, and logs

### Check Logs

Each workflow run shows:
- **Generation Stats:** Token usage, articles written, quality failures
- **Maintenance Report:** Duplicate slugs, broken links, CSV errors, statistics
- **Deployment Summary:** Cloudflare Pages URL and status

### Troubleshooting

**Workflow fails with "API key not found":**
- Check secrets are added correctly in Settings
- Verify secret names match exactly (case-sensitive)

**Generation produces no articles:**
- Check `logs/quality_failures.log` in workflow logs
- Verify `data/terms.csv` has pending terms
- Check daily token limit hasn't been exceeded

**Deployment fails:**
- Verify Cloudflare API token is valid
- Check account ID is correct
- Ensure `dist/` directory exists after build

## Manual Workflow Triggers

### Generate specific priority

```bash
gh workflow run generate-content.yml -f priority=1
```

### Generate single term

```bash
# First, manually run generate.py locally:
npm run generate:single -- what-is-rag

# Then commit and push
git add content/glossary/ data/terms.csv
git commit -m "chore: regenerate what-is-rag"
git push
```

### Run maintenance immediately

```bash
gh workflow run maintenance.yml
```

## Notifications

### Slack Integration (Optional)

Add to workflow after deployment:

```yaml
- name: Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "AI Glossary deployment complete",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "✅ Deployed to Cloudflare Pages\n${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
            }
          }
        ]
      }
```

## Cost Considerations

- **GitHub Actions:** Free tier includes 2,000 minutes/month (sufficient for daily generation)
- **Cloudflare Pages:** Free tier includes unlimited deployments
- **API Costs:** Depends on Groq/Gemini usage (tracked in `logs/usage.log`)

## Best Practices

1. **Monitor token usage:** Check `logs/usage.log` weekly
2. **Review quality failures:** Check `logs/quality_failures.log` after each run
3. **Test locally first:** Run `npm run generate:dry-run` before enabling auto-generation
4. **Keep secrets secure:** Never commit `.env` or API keys
5. **Review generated content:** Spot-check articles for quality
6. **Update terms.csv regularly:** Add new terms to keep pipeline active

## Disabling Workflows

To temporarily disable a workflow:

1. Go to **Actions** tab
2. Click workflow name
3. Click **...** menu → **Disable workflow**

To re-enable:
1. Click **...** menu → **Enable workflow**
