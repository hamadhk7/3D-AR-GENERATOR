# 🚀 API Setup Guide - After Online Transaction

Congratulations on completing your online transaction! Your API account is now funded and ready to use. Here's how to activate it:

## 📋 Prerequisites
- ✅ Online transaction completed
- ✅ API credits available (200 API credits + 5600 free credits)
- ✅ API key received (starts with `tsk_`)

## 🔧 Step 1: Configure Your API Key

1. **Create environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file** and replace:
   ```
   TRIPO_API_KEY=your_tripo_api_key_here
   ```
   
   With your actual API key:
   ```
   TRIPO_API_KEY=tsk_your_actual_api_key_here
   ```

## 🧪 Step 2: Test Your API Connection

Run the test script to verify everything works:

```bash
python test_api_connection.py
```

This will:
- ✅ Test API connectivity
- ✅ Verify your API key is valid
- ✅ Check credit balance
- ✅ Optionally test model generation

## 🌐 Step 3: Start Your Web Application

### Option 1: Start Web Server Only
```bash
python scripts/start_web_server.py
```

### Option 2: Start Both Servers (Recommended)
```bash
# Terminal 1 - Start MCP Server
python scripts/start_mcp_server.py

# Terminal 2 - Start Web Server  
python scripts/start_web_server.py
```

## 🎯 Step 4: Access Your 3D AR Demo

Once started, open your browser and go to:
- **Main Demo:** http://localhost:5000
- **AR Viewer:** http://localhost:5000/ar-viewer
- **Model List:** http://localhost:5000/models

## 💰 Credit Usage Information

Your current balance:
- **API Wallet:** 200 credits (100 frozen)
- **Free Wallet:** 5600 credits (valid until 2025-08-19)

**Credit costs per model:**
- Low quality: ~1-2 credits
- Medium quality: ~3-5 credits  
- High quality: ~8-12 credits

## 🎨 Using the Demo

1. **Generate Models:**
   - Go to the main page
   - Enter a description (e.g., "A red sports car")
   - Choose quality and format
   - Click "Generate Model"

2. **View in AR:**
   - Click on any generated model
   - Use the AR viewer to place it in your environment
   - Take screenshots or record videos

3. **Download Models:**
   - Models are saved in `data/generated_models/`
   - Available formats: GLB, OBJ, USDZ

## 🔧 Troubleshooting

### API Key Issues
- Ensure your API key starts with `tsk_`
- Check that the `.env` file is in the project root
- Verify no extra spaces in the API key

### Connection Issues
- Check your internet connection
- Ensure the API URL is correct: `https://api.tripo3d.ai/v2/openapi`
- Try the test script: `python test_api_connection.py`

### Model Generation Issues
- Check your credit balance
- Try lower quality settings to save credits
- Ensure your prompt is clear and descriptive

## 📞 Support

If you encounter issues:
1. Check the logs in `data/logs/`
2. Run the test script for diagnostics
3. Verify your API key and credits in the Tripo dashboard

## 🎉 You're Ready!

Your 3D AR demo is now fully functional with your funded API account. Start generating amazing 3D models and experiencing them in AR!

---

**Next Steps:**
- Generate your first model
- Try the AR viewer
- Experiment with different prompts
- Share your creations!

Happy 3D modeling! 🎨✨ 