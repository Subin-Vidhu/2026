# 💝 Ente Valentine - Monsoon Romance Experience

> A world-class, AI-powered romantic web experience that combines Kerala monsoon aesthetics with interactive storytelling.

![Version](https://img.shields.io/badge/version-6.1-ff6b9d) ![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

### 🎬 Cinematic Experience
- **Atmospheric Effects**: Rain animation, fireflies, lightning flashes
- **4 Romantic Modes**: College Nostalgia, Cinematic Confession, Modern Romance, Poetic Soul
- **AI-Powered Messages**: Personalized romantic confessions using AI
- **Interactive Proposal**: Gamified "YES/NO" buttons with playful dodging mechanics

### 🎨 Design Excellence
- Glassmorphism UI with backdrop blur effects
- Smooth animations and micro-interactions
- Responsive design (mobile-first)
- Dark/Light mode toggle
- Professional typography with Google Fonts

### 💾 Features
- Local statistics tracking (YES clicks, NO attempts)
- Share link generation with URL parameters
- Screenshot capture functionality
- Confetti celebration animations
- Sound effects (rain, toggleable)

## 🚀 Quick Start

### Option 1: Direct Use (Simplest)
1. Download `index.html`
2. Open it in any modern browser
3. That's it! It works completely offline.

### Option 2: GitHub Pages Deployment

1. **Create a new repository on GitHub**
   ```bash
   # Name it something like: ente-valentine
   ```

2. **Upload the file**
   - Go to your repository
   - Click "Add file" > "Upload files"
   - Upload `index.html`
   - Commit changes

3. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select `main` branch
   - Click "Save"

4. **Access your site**
   - Your site will be live at: `https://yourusername.github.io/ente-valentine/`
   - Wait 2-3 minutes for initial deployment

### Option 3: Custom Domain (Advanced)

1. Buy a domain (e.g., `entevalentine.com`)
2. Add a `CNAME` file to your repository with your domain
3. Configure DNS records:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: CNAME
   Name: www
   Value: yourusername.github.io
   ```

## 📱 How It Works

### User Journey

1. **Step 1: Invitation**
   - User enters their name
   - Ambient rain and fireflies create atmosphere
   - Typewriter effect on subtitle

2. **Step 2: Choose Mood**
   - Select from 4 romantic vibes
   - Each has unique styling and AI prompt
   - Cards with glassmorphism effects

3. **Step 3: AI Magic**
   - Loading animation with rotating messages
   - AI generates personalized romantic message
   - Typewriter reveal effect
   - Copy/Share functionality

4. **Step 4: The Proposal**
   - "Will You Be My Valentine?"
   - YES button (grows bigger with each NO attempt)
   - NO button (dodges clicks, shrinks, moves randomly)
   - Confetti celebration on YES

5. **Success Screen**
   - Celebration message
   - Screenshot option
   - Share functionality
   - Restart option

## 🛠️ Technical Details

### Stack
- **Frontend**: Pure HTML5, CSS3, Vanilla JavaScript
- **AI Integration**: Llama3 API endpoint
- **Libraries**: 
  - html2canvas (for screenshots)
  - Google Fonts (Playfair Display + Inter)
- **Canvas**: For rain, fireflies, and confetti animations

### Browser Support
- ✅ Chrome/Edge 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Mobile browsers (iOS 14+, Android 10+)

### Performance
- 60fps animations
- Optimized canvas rendering
- Mobile-first responsive design
- Lazy loading for heavy features
- Respects `prefers-reduced-motion`

## 🎨 Customization

### Change Colors
Edit the CSS variables in the `<style>` section:

```css
:root {
    --accent: #ff6b9d;        /* Change to your color */
    --glow: rgba(255, 107, 157, 0.5);
}
```

### Modify AI Prompts
Find the `prompts` object in the JavaScript:

```javascript
const prompts = {
    college: `Your custom prompt here...`,
    // ... modify other modes
};
```

### Add Sound Effects
The template includes a placeholder for rain sound. To add real audio:

1. Get rain sound MP3 file
2. Host it (GitHub, Cloudflare R2, etc.)
3. Update the `<audio>` source:

```html
<audio id="rainSound" loop>
    <source src="your-rain-sound.mp3" type="audio/mpeg">
</audio>
```

### Adjust Particle Counts

```javascript
// Line ~267: Rain drops
const raindrops = Array.from({ length: 200 }, () => new RainDrop());

// Line ~327: Fireflies
const fireflies = Array.from({ length: 30 }, () => new Firefly());

// Line ~795: Confetti
const confettiPieces = Array.from({ length: 200 }, () => new Confetti());
```

## 🌍 SEO & Sharing

The site includes proper meta tags for social sharing:
- Open Graph (Facebook)
- Twitter Cards
- Schema.org markup ready

When someone shares your link, it will show:
- Preview image (add `og-image.png`)
- Title: "Ente Valentine - Monsoon Romance"
- Description: Custom preview text

## 📊 Analytics (Optional)

To add privacy-friendly analytics:

1. **Plausible** (Recommended)
   ```html
   <script defer data-domain="yourdomain.com" 
           src="https://plausible.io/js/script.js"></script>
   ```

2. **Simple Analytics**
   ```html
   <script async defer src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
   ```

Both are GDPR-compliant and don't require cookie consent.

## 🐛 Troubleshooting

### AI Not Working?
- The API endpoint `https://llama3.protosonline.in/v1/chat/completions` must be accessible
- Check browser console for errors
- Fallback messages will show if API fails
- You can replace with OpenAI API or other compatible endpoints

### Rain Not Showing?
- Check if rain toggle is enabled (🌧️ button)
- Verify canvas is rendering (browser console)
- Try refreshing the page

### Screenshot Not Working?
- Ensure html2canvas CDN is loading
- Check browser console for errors
- Some browsers block third-party scripts - use a local copy

### Buttons Not Responding?
- Disable browser extensions (adblockers)
- Check browser console for JavaScript errors
- Try in incognito mode

## 🚀 Making It Viral

### Content Ideas
1. **TikTok/Reels**: Screen record the NO button dodging
2. **Instagram Story**: Screenshot the AI message + share link
3. **Twitter**: "Try to click NO... I dare you 😏"
4. **Reddit**: Post to r/InternetIsBeautiful, r/webdev

### Growth Hacks
- Add referral tracking in URLs
- Create shareable moments (AI messages are unique!)
- Make it seasonal (Valentine's, Monsoon season)
- Encourage screenshot sharing

### Hashtags
```
#EnteValentine #MonsoonRomance #ValentinesDay
#AILoveLetters #KeralaMonsoon #InteractiveLove
```

## 📄 License

MIT License - Feel free to use, modify, and distribute!

## 🙏 Credits

- Fonts: Google Fonts (Playfair Display, Inter)
- Icons: Unicode Emoji
- Screenshot: html2canvas library
- Inspiration: Kerala monsoon evenings, Malayalam cinema

## 💝 Support

If you love this project:
- ⭐ Star the repository
- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔗 Share with friends!

---

**Made with 💝 and ☕**

For questions or collaboration: [Your Contact]

Live Demo: [Your GitHub Pages URL]
