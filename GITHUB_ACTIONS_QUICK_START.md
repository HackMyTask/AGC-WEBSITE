# GitHub Actions Quick Reference

## Set & Forget Setup (5 minutes)

### 1. Add Secrets to GitHub

Go to **Settings → Secrets and variables → Actions** and add:

```
AI_PROVIDER = groq
GROQ_API_KEY = your_key_here
CLOUDFLARE_API_TOKEN = your_token_here
CLOUDFLARE_ACCOUNT_ID = your_account_id_here
```

### 2. Enable Workflows

Go to **Actions** tab → Click "I understand my workflows, go ahead and enable them"

### 3. Done! 🎉

Workflows now run automatically:
- **Daily at 2 AM UTC:** Generate 20 new articles
- **Weekly Sunday 3 AM UTC:** Maintenance checks
- **On push to main:** Deploy to Cloudflare Pages

## Manual Triggers

```bash
# Generate 5 articles (test)
gh workflow run generate-content.yml -f batch_size=5

# Generate priority 1 terms only
gh workflow run generate-content.yml -f priority=1

# Run maintenance now
gh workflow run maintenance.yml

# Deploy now
gh workflow run deploy.yml
```

## Monitor Progress

1. Go to **Actions** tab
2. Click workflow name
3. See real-time logs and stats

## What Gets Automated

| Task | Schedule | Status |
|------|----------|--------|
| Generate articles | Daily 2 AM UTC | ✅ Automated |
| Validate quality | Per generation | ✅ Automated |
| Update links | Per generation | ✅ Automated |
| Maintenance checks | Weekly Sunday | ✅ Automated |
| Deploy to Cloudflare | On push to main | ✅ Automated |
| Commit changes | Per generation | ✅ Automated |

## Logs & Monitoring

- **Token usage:** `logs/usage.log`
- **File writes:** `logs/writes.log`
- **Quality failures:** `logs/quality_failures.log`

All visible in workflow run logs on GitHub.

## Troubleshooting

**Workflow not running?**
- Check secrets are added (Settings → Secrets)
- Check workflow is enabled (Actions tab)
- Check branch is `main` for deployment

**Generation produces no articles?**
- Check `logs/quality_failures.log` in workflow logs
- Verify `data/terms_*.csv` has pending terms
- Check API key is valid

**Need to disable?**
- Go to Actions → Click workflow → ... menu → Disable workflow
