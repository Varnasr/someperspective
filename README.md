# Deployment Guide for someperspective.info

## Project Structure
```
someperspective/
├── index.html          # Main website with visualizations
├── data.json          # All economic data
├── india-economy-paper.md  # Full academic paper
├── README.md          # This deployment guide
├── CNAME             # Domain configuration
└── assets/
    ├── charts/        # Generated chart images
    └── downloads/     # PDF reports and Excel files
```

## Step 1: Prepare GitHub Repository

1. Create a new GitHub repository:
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: India Economy Assessment 2014-2025"

# Create repository on GitHub (via GitHub website)
# Name: someperspective

# Add remote and push
git remote add origin https://github.com/yourusername/someperspective.git
git branch -M main
git push -u origin main
```

2. Create CNAME file for custom domain:
```bash
echo "someperspective.info" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

## Step 2: Deploy to Netlify

1. **Sign up/Login to Netlify**
   - Go to https://app.netlify.com
   - Sign up with GitHub for easy integration

2. **Create New Site**
   - Click "New site from Git"
   - Choose GitHub
   - Authorize Netlify to access your GitHub
   - Select the `someperspective` repository
   - Build settings:
     - Branch to deploy: `main`
     - Build command: (leave empty for static site)
     - Publish directory: `/` or `.`

3. **Deploy Site**
   - Click "Deploy site"
   - Wait for deployment (takes 1-2 minutes)
   - You'll get a temporary URL like `amazing-einstein-123abc.netlify.app`

## Step 3: Configure Custom Domain

1. **In Netlify Dashboard:**
   - Go to Site settings → Domain management
   - Click "Add custom domain"
   - Enter: `someperspective.info`
   - Click "Verify"

2. **Configure DNS (at your domain registrar):**

   **Option A - Using Netlify DNS (Recommended):**
   - Netlify will provide nameservers
   - At your registrar, change nameservers to:
     ```
     dns1.p04.nsone.net
     dns2.p04.nsone.net
     dns3.p04.nsone.net
     dns4.p04.nsone.net
     ```

   **Option B - Using A Records:**
   - Add these DNS records at your registrar:
     ```
     Type: A
     Name: @
     Value: 75.2.60.5
     
     Type: CNAME
     Name: www
     Value: amazing-einstein-123abc.netlify.app
     ```

3. **Enable HTTPS:**
   - In Netlify: Domain settings → HTTPS
   - Click "Verify DNS configuration"
   - Click "Provision certificate"
   - Wait 5-10 minutes for SSL certificate

## Step 4: Add Google Analytics

1. **Get Google Analytics ID:**
   - Go to https://analytics.google.com
   - Create new property for someperspective.info
   - Get Measurement ID (G-XXXXXXXXXX)

2. **Add to index.html:**
```html
<!-- Add before closing </head> tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

3. **Commit and push:**
```bash
git add index.html
git commit -m "Add Google Analytics"
git push
```

## Step 5: Performance Optimization

1. **Enable Netlify optimizations:**
   - Site settings → Build & deploy → Post processing
   - Enable: Asset optimization
   - Enable: Pretty URLs
   - Enable: Bundle CSS
   - Enable: Bundle JS

2. **Add caching headers (_headers file):**
```
# Create _headers file in root
/*
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.json
  Cache-Control: public, max-age=3600
```

3. **Add redirects (_redirects file):**
```
# Redirect www to non-www
https://www.someperspective.info/* https://someperspective.info/:splat 301!

# Redirect common typos
/index.htm /index.html 301
/home / 301
```

## Step 6: Content Updates

### To update data:
1. Edit `data.json` with new values
2. Commit and push:
```bash
git add data.json
git commit -m "Update economic indicators for [month/year]"
git push
```

### To update visualizations:
1. Modify chart configurations in `index.html`
2. Test locally:
```bash
# Simple Python server
python -m http.server 8000
# Open http://localhost:8000
```
3. Commit and push changes

### To add new sections:
1. Add HTML section in `index.html`
2. Add corresponding data in `data.json`
3. Create chart initialization in JavaScript
4. Test and deploy

## Step 7: Monitoring

1. **Netlify Analytics (Free tier):**
   - View in Netlify dashboard
   - Shows page views, top pages, top sources

2. **Google Analytics:**
   - Real-time visitors
   - User demographics
   - Traffic sources
   - Page performance

3. **Uptime Monitoring:**
   - Use UptimeRobot (free for 50 monitors)
   - Set up alerts for downtime

## Step 8: Backup Strategy

1. **GitHub:**
   - All code automatically backed up
   - Enable GitHub Pages as backup hosting

2. **Data Backup:**
```bash
# Create monthly backups
mkdir backups/2025-01
cp data.json backups/2025-01/
git add backups/
git commit -m "Monthly data backup - January 2025"
git push
```

3. **Download Production Site:**
```bash
# Use wget to backup deployed site
wget --mirror --convert-links --page-requisites --no-parent https://someperspective.info
```

## Maintenance Checklist

### Weekly:
- [ ] Check Google Analytics for traffic patterns
- [ ] Monitor site uptime
- [ ] Review any user feedback/comments

### Monthly:
- [ ] Update data.json with latest indicators
- [ ] Backup data files
- [ ] Check for broken links
- [ ] Update paper if new findings

### Quarterly:
- [ ] Comprehensive data review
- [ ] Update all visualizations
- [ ] Performance audit
- [ ] SEO review

## Troubleshooting

**Domain not working:**
- DNS propagation can take 24-48 hours
- Check DNS with: `nslookup someperspective.info`
- Verify nameservers are correct

**SSL Certificate issues:**
- Clear browser cache
- Re-provision certificate in Netlify
- Check DNS configuration

**Charts not loading:**
- Check browser console for errors
- Verify CDN links are working
- Test with different browsers

**Slow performance:**
- Enable Netlify asset optimization
- Compress images
- Minify JavaScript and CSS
- Use Netlify's CDN

## SEO Optimization

Add to `index.html`:
```html
<meta name="description" content="Data-driven analysis of India's economic performance from 2014-2025, examining employment, inequality, and democratic institutions.">
<meta name="keywords" content="India economy, GDP growth, unemployment, inequality, fiscal federalism, democracy">

<!-- Open Graph -->
<meta property="og:title" content="Some Perspective - India's Economic Reality">
<meta property="og:description" content="Where narratives meet numbers: A comprehensive assessment of India's political economy">
<meta property="og:image" content="https://someperspective.info/assets/og-image.png">
<meta property="og:url" content="https://someperspective.info">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="India's Economic Reality 2014-2025">
<meta name="twitter:description" content="Data-driven analysis beyond GDP headlines">
<meta name="twitter:image" content="https://someperspective.info/assets/twitter-card.png">
```

## Contact & Support

- **Netlify Support:** https://www.netlify.com/support/
- **GitHub Issues:** Create issues in your repository
- **Domain Support:** Contact your registrar

## Launch Checklist

- [ ] GitHub repository created and pushed
- [ ] Netlify site deployed
- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] Google Analytics installed
- [ ] All charts loading correctly
- [ ] Mobile responsive tested
- [ ] SEO meta tags added
- [ ] Social media cards configured
- [ ] Backup system in place

---

**Note:** This site is optimized for modern browsers. Minimum supported versions:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Last updated: January 2025