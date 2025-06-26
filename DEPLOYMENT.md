# 🚀 Deployment Guide - C Code Analyzer

## Vercel Deployment (Recommended)

### Quick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/prakhar315/Code_analyzer)

### Manual Deployment Steps

1. **Fork the Repository**
   - Go to [GitHub Repository](https://github.com/prakhar315/Code_analyzer)
   - Click "Fork" to create your own copy

2. **Connect to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub
   - Click "New Project"
   - Import your forked repository

3. **Configure Deployment**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (no build required)
   - **Output Directory**: `frontend`
   - **Install Command**: Leave empty

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at `https://your-app-name.vercel.app`

### Environment Variables
No environment variables required - this is a static site!

---

## Alternative Hosting Options

### GitHub Pages
1. Go to your repository settings
2. Navigate to "Pages" section
3. Select source: "Deploy from a branch"
4. Choose branch: `master`
5. Folder: `/ (root)`
6. Your site will be available at `https://username.github.io/repository-name`

### Netlify
1. Visit [netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Build settings:
   - **Build command**: Leave empty
   - **Publish directory**: `frontend`
4. Deploy

### Local Development
```bash
# Clone the repository
git clone https://github.com/prakhar315/Code_analyzer.git
cd Code_analyzer

# Option 1: Simple HTTP server (Python)
python -m http.server 3000 --directory frontend

# Option 2: Node.js HTTP server
npx http-server frontend -p 3000

# Option 3: Just open the file
# Open frontend/index.html in your browser
```

---

## 🔧 Technical Details

### Project Structure for Deployment
```
C-Code-Analyzer/
├── frontend/              # Main application files
│   ├── index.html        # Entry point
│   ├── c-analyzer.js     # Core analyzer logic
│   ├── script.js         # UI logic
│   └── style.css         # Styling
├── vercel.json           # Vercel configuration
├── package.json          # Project metadata
└── README.md             # Documentation
```

### Vercel Configuration (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "rewrites": [
    {
      "source": "/",
      "destination": "/frontend/index.html"
    }
  ]
}
```

### Why This Works for Vercel
- **Static Site**: No server-side processing required
- **Client-side Logic**: All analysis runs in the browser
- **No Dependencies**: Pure HTML, CSS, and JavaScript
- **Fast Loading**: Optimized for performance
- **Mobile Friendly**: Responsive design

---

## 🎯 Post-Deployment

### Testing Your Deployment
1. **Basic Functionality**
   - Enter sample C code
   - Test lexical analysis
   - Test parse tree generation
   - Verify mobile responsiveness

2. **Sample Test Code**
   ```c
   #include <stdio.h>
   
   int main() {
       int x = 5;
       if (x > 0) {
           printf("Positive number");
       }
       return 0;
   }
   ```

3. **Expected Results**
   - Lexical analysis should show tokens with types
   - Parse tree should show hierarchical structure
   - No server errors (everything runs client-side)

### Custom Domain (Vercel)
1. Go to your project dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

### Performance Optimization
- **Already Optimized**: Minimal JavaScript, no external dependencies
- **CDN**: Vercel provides global CDN automatically
- **Caching**: Static files cached automatically
- **Compression**: Gzip compression enabled by default

---

## 🐛 Troubleshooting

### Common Issues

1. **Blank Page**
   - Check browser console for JavaScript errors
   - Ensure all files are in the `frontend/` directory
   - Verify `vercel.json` configuration

2. **Analysis Not Working**
   - Check if `c-analyzer.js` is loaded
   - Verify browser supports modern JavaScript
   - Test with simple C code first

3. **Mobile Issues**
   - Check responsive CSS
   - Test on different screen sizes
   - Verify touch interactions work

### Debug Mode
Open browser developer tools (F12) to see:
- Console errors
- Network requests
- JavaScript execution

---

## 📈 Analytics & Monitoring

### Vercel Analytics
- Enable in project settings
- Track page views and performance
- Monitor Core Web Vitals

### Custom Analytics
Add Google Analytics or other tracking:
```html
<!-- Add to frontend/index.html <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

---

## 🔄 Updates & Maintenance

### Automatic Deployments
- Push to `master` branch triggers automatic deployment
- No manual intervention required
- Rollback available in Vercel dashboard

### Version Control
- Tag releases: `git tag v2.0.0`
- Use semantic versioning
- Update `package.json` version

### Monitoring
- Check Vercel dashboard for deployment status
- Monitor error rates and performance
- Set up alerts for downtime

---

## 🎉 Success!

Your C Code Analyzer is now live and ready to showcase! 

**Share your deployment:**
- Add the live URL to your GitHub repository description
- Share on social media
- Include in your portfolio
- Use for educational purposes

**Next Steps:**
- Customize the design
- Add more C language features
- Implement additional analysis types
- Collect user feedback
