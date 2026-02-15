# 🚀 GitHub Pages Deployment Guide

## Get Your Site Live at: `yourusername.github.io/valentine`

---

## 📋 Prerequisites

- GitHub account (free) - Sign up at https://github.com/signup if you don't have one
- Your `index.html` file downloaded

---

## 🎯 Step-by-Step Instructions

### STEP 1: Create a New Repository

1. **Go to GitHub** and log in
   - Visit: https://github.com

2. **Click the "+" icon** (top right corner) → Select **"New repository"**
   - Or go directly to: https://github.com/new

3. **Fill in the details:**
   ```
   Repository name: valentine
   Description: AI-powered romantic monsoon experience 💝
   Visibility: ✅ Public (must be public for free GitHub Pages)
   
   ❌ Do NOT check "Add a README file"
   ❌ Do NOT add .gitignore
   ❌ Do NOT choose a license (yet)
   ```

4. **Click "Create repository"** (green button at bottom)

---

### STEP 2: Upload Your File

You'll see a page with setup instructions. Choose the **easiest method**:

#### Method A: Upload via Web Interface (Easiest!)

1. On the repository page, click **"uploading an existing file"** (in the blue hint box)
   
2. **Drag and drop** your `index.html` file into the box
   - Or click "choose your files" and select it

3. **Scroll down** and click **"Commit changes"** (green button)

#### Method B: Using Git Command Line (Advanced)

```bash
# Navigate to your folder
cd /path/to/your/folder

# Initialize git
git init

# Add your file
git add index.html

# Commit
git commit -m "Initial commit - Ente Valentine"

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/valentine.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### STEP 3: Enable GitHub Pages

1. **Go to your repository settings**
   - Click the **"Settings"** tab (top menu)

2. **Find "Pages" in the left sidebar**
   - Scroll down the left menu
   - Click **"Pages"**

3. **Configure the source**
   - Under "Build and deployment"
   - **Source:** Deploy from a branch
   - **Branch:** Select `main` (or `master`)
   - **Folder:** Select `/ (root)`
   
4. **Click "Save"**

5. **Wait 2-3 minutes** for deployment

---

### STEP 4: Access Your Live Site! 🎉

1. **Refresh the Pages settings page** after 2-3 minutes

2. You'll see a message:
   ```
   Your site is live at https://YOUR-USERNAME.github.io/valentine/
   ```

3. **Click the link** or visit:
   ```
   https://YOUR-USERNAME.github.io/valentine/
   ```

4. **Share this URL** with everyone! 🎊

---

## 🌐 Your Live URLs

If your GitHub username is `johndoe`, your site will be at:

```
https://johndoe.github.io/valentine/
```

**Share Links:**
```
Direct link:
https://johndoe.github.io/valentine/

With pre-filled name:
https://johndoe.github.io/valentine/?name=Sarah

With mode selected:
https://johndoe.github.io/valentine/?name=Sarah&mode=cinematic
```

---

## 🔄 How to Update Your Site

Made changes to `index.html`? Here's how to update:

### Via Web Interface:

1. Go to your repository: `https://github.com/YOUR-USERNAME/valentine`

2. Click on **`index.html`**

3. Click the **pencil icon** (✏️ Edit this file)

4. Make your changes

5. Scroll down, click **"Commit changes"**

6. Wait 1-2 minutes for the site to update

### Via Git Command Line:

```bash
# Make your changes to index.html

# Stage the changes
git add index.html

# Commit
git commit -m "Updated design/features"

# Push to GitHub
git push

# Wait 1-2 minutes for deployment
```

---

## 📱 Sharing Your Site

### QR Code Generator
Create a QR code for easy mobile sharing:
1. Go to: https://qr-code-generator.com
2. Enter your URL: `https://YOUR-USERNAME.github.io/valentine/`
3. Download and share!

### Social Media Templates

**WhatsApp:**
```
Check out this romantic AI experience I made! 💝

Try it: https://YOUR-USERNAME.github.io/valentine/

Challenge: Try to click the NO button 😂
```

**Instagram Bio:**
```
💝 Try my Valentine AI experience
🔗 [username].github.io/valentine
```

**Twitter/X:**
```
Built an AI-powered Valentine experience with:
✨ Personalized romantic messages
😂 An impossible-to-click NO button
🌧️ Monsoon vibes

Try it: https://YOUR-USERNAME.github.io/valentine/

Can you click NO? I bet you can't 😏
```

---

## 🎨 Custom Domain (Optional - Advanced)

Want `valentine.yourname.com` instead of `username.github.io/valentine`?

1. **Buy a domain** (from Namecheap, Google Domains, etc.)

2. **Add DNS records** in your domain provider:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   ```

3. **In your repository**, create a file named `CNAME` (no extension)
   - Content: `valentine.yourname.com`

4. **In GitHub Pages settings**, enter your custom domain

5. **Wait 24-48 hours** for DNS propagation

---

## 🐛 Troubleshooting

### "404 - File not found"
- ✅ Check that file is named exactly `index.html` (lowercase)
- ✅ Verify it's in the root folder (not in a subfolder)
- ✅ Wait 5 minutes and try again
- ✅ Hard refresh: Ctrl + Shift + R (Windows) or Cmd + Shift + R (Mac)

### "Site not loading"
- ✅ Check repository is Public (Settings → Danger Zone)
- ✅ Verify Pages is enabled (Settings → Pages)
- ✅ Wait up to 10 minutes for first deployment
- ✅ Clear browser cache

### "Changes not showing"
- ✅ Hard refresh the page
- ✅ Check commit went through (look at repository)
- ✅ Wait 2-3 minutes for rebuild
- ✅ Try incognito/private browsing mode

### "NO button not working"
- ✅ Enable sounds first (click 🔊)
- ✅ Make sure you're on Step 4 (Proposal screen)
- ✅ Try a different browser
- ✅ Check browser console (F12) for errors

---

## 📊 Track Your Visitors (Optional)

Want to know how many people visit? Add analytics:

### Option 1: GitHub Traffic Stats (Built-in)
1. Go to repository
2. Click **"Insights"** tab
3. Click **"Traffic"** in left menu
4. See views and clones (last 14 days)

### Option 2: Plausible Analytics (Privacy-Friendly)
1. Sign up at https://plausible.io (paid, but privacy-friendly)
2. Add this before `</head>` in index.html:
   ```html
   <script defer data-domain="yourusername.github.io" 
           src="https://plausible.io/js/script.js"></script>
   ```

### Option 3: Simple Analytics
1. Sign up at https://simpleanalytics.com
2. Add their script tag to your HTML

---

## 🚀 Going Viral Checklist

- [ ] Site is live and working
- [ ] NO button dodges properly (impossible to click!)
- [ ] Sound effects work (enable with 🔊)
- [ ] AI messages are romantic
- [ ] Mobile-friendly (test on phone!)
- [ ] Share link copied
- [ ] Posted on social media with hashtags
- [ ] Asked 5 friends to try and share
- [ ] Created QR code for easy sharing
- [ ] Made a TikTok/Reel of NO button dodging

---

## 📈 Expected Timeline

```
Minute 0: Upload file to GitHub
Minute 1: Enable GitHub Pages
Minute 3: Site goes live ✅
Minute 5: Share on social media
Hour 1: First 10 visitors
Day 1: 50-100 visitors (if shared well)
Week 1: Potentially viral if content is good! 🚀
```

---

## 💡 Pro Tips

1. **Short URL matters**: Keep repo name short (`valentine` is perfect!)

2. **Test before sharing**: Go through entire flow yourself

3. **Mobile test**: 60%+ of traffic will be mobile

4. **Best sharing time**: 
   - Instagram: 11 AM - 1 PM, 7 PM - 9 PM
   - Twitter: 12 PM - 1 PM, 5 PM - 6 PM
   - TikTok: 6 AM - 10 AM, 7 PM - 11 PM

5. **Engage**: Reply to everyone who shares/comments

6. **Create content**: Screen record the NO button, make it a challenge

---

## 🎉 You're Ready!

Your complete URL will be:

```
https://YOUR-USERNAME.github.io/valentine/
```

Replace `YOUR-USERNAME` with your actual GitHub username!

**Example:**
- Username: `alexsmith`
- Repository: `valentine`
- Live URL: `https://alexsmith.github.io/valentine/`

---

## 📞 Need Help?

- **GitHub Pages Docs**: https://docs.github.com/pages
- **This Project Issues**: Create an issue in your repo
- **Community**: Stack Overflow, GitHub Discussions

---

**Now go make it VIRAL! 🚀💝**

Share, share, share! The NO button challenge is your viral hook! 😄
