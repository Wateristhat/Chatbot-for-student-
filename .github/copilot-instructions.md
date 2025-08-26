# Bạn Đồng Hành - Vietnamese Student Support Chatbot

Bạn Đồng Hành (Companion Friend) is a Streamlit-based Vietnamese web application providing mental health support features for students. The application includes motivational content, breathing exercises, gratitude journaling, emotion drawing, games, self-care planning, AI chat, emergency support resources, and AI storytelling.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Run the Application
Execute these commands in sequence to get the application running:

```bash
cd BanDongHanh_Website
python3 --version  # Verify Python 3.12+ available
pip3 install -r requirements.txt  # Takes ~30 seconds. NEVER CANCEL
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

**TIMING EXPECTATIONS:**
- Dependency installation: ~30 seconds - NEVER CANCEL during pip install
- Application startup: ~5 seconds after streamlit command
- First page load: ~3 seconds for initial database creation
- Page navigation: ~2 seconds between features

### API Key Configuration (Required for AI Features)
AI features (Chat and Storytelling) require Google Gemini API key configuration:

1. Create `.streamlit/secrets.toml` in the `BanDongHanh_Website` directory:
```toml
GOOGLE_API_KEY = "your-google-gemini-api-key-here"
```

2. If API keys are not configured, these features will display fallback messages:
   - Chat: Limited to predefined responses
   - Storytelling: Shows "Cannot connect to AI" message

3. All other features work without API keys and should be tested first.

## Core Features and Validation

### Always Test These User Scenarios After Changes

**1. Complete User Registration Flow (CRITICAL)**
- Navigate to application home page (http://localhost:8501)
- Click "✨ Người dùng mới" tab
- Fill registration form:
  - Name: "Test User"
  - Birth year: Any year from dropdown (e.g., 2012)
  - School: "Test School"
  - Issues: "Test concern"
- Click "💖 Tạo tài khoản và bắt đầu!" button
- Verify dashboard loads with user greeting
- EXPECTED: User redirected to features dashboard

**2. Feature Navigation and Core Functionality**
- Test sidebar navigation to each page:
  - ✨ Liều thuốc tinh thần (Spiritual Medicine)
  - 🧘 Góc an yên (Peaceful Corner) 
  - 🍯 Lọ biết ơn (Gratitude Jar)
  - 🎨 Bảng màu cảm xúc (Emotion Color Board)
  - 🎲 Nhanh tay lẹ mắt (Quick Games)
  - ❤️ Góc nhỏ (Self-care Corner)
  - 🆘 Hỗ Trợ Khẩn Cấp (Emergency Support)
  - 💬 Trò chuyện (Chat) - requires API key
  - 📖 Người Kể Chuyện (Storyteller) - requires API key

**3. Spiritual Medicine Feature Test**
- Navigate to "Liều thuốc tinh thần" 
- Click any category button (📣 Cần Cổ Vũ, 😄 Muốn Vui Vẻ, 🧘 Tìm Bình Yên)
- Verify motivational message displays
- Click "🔄 Nhận một thông điệp khác cùng loại" for another message
- EXPECTED: Different message from same category

**4. Drawing Board Functionality**
- Navigate to "Bảng màu cảm xúc"
- Verify canvas loads with drawing tools
- Test drawing functionality by making marks on canvas
- EXPECTED: Responsive drawing interface with color/brush options

## Database and Persistence

**Database Auto-Creation**
- SQLite database (`ban_dong_hanh_data.db`) auto-creates on first application run
- Contains tables: `users`, `gratitude_notes`, `chat_history`
- Database persists user data between sessions
- No manual database setup required

**Testing Database Functionality**
- Register a new user and verify data persists after restart
- Add gratitude notes and verify they save correctly
- Check that user login works with existing accounts

## Common Issues and Workarounds

**Known Limitations:**
- Chat and Storytelling features require Google API keys - they will show error messages without keys
- Drawing board requires `streamlit-drawable-canvas` - already included in requirements.txt
- External fonts and CDN resources may be blocked in some environments - application still functions

**Development Workarounds:**
- Use sidebar navigation instead of dashboard links for reliable page access
- Test core features (Spiritual Medicine, Drawing Board, Gratitude Jar) before AI features
- If pages show 404 errors, use sidebar navigation rather than direct URLs

## File Structure and Key Components

### Repository Root
```
BanDongHanh_Website/
├── app.py              # Main application entry point
├── database.py         # SQLite database management
├── requirements.txt    # Python dependencies
├── pages/             # Streamlit multipage structure
│   ├── 1_✨_Liều_thuốc_tinh_thần.py
│   ├── 2_🧘_Góc_an_yên.py
│   ├── 3_🍯_Lọ_biết_ơn.py
│   ├── 4_🎨_Bảng_màu_cảm_xúc.py
│   ├── 5_🎲_Nhanh_tay_lẹ_mắt.py
│   ├── 6_❤️_Góc_nhỏ.py
│   ├── 7_🆘_Hỗ_Trợ_Khẩn_Cấp.py
│   ├── 8_💬_Trò_chuyện.py
│   └── 9_📖_Người_Kể_Chuyện.py
├── game.html          # HTML5 game for quick games feature
└── game_app.py        # Game integration
```

### Key Dependencies (requirements.txt)
- `streamlit` - Main web framework
- `pandas` - Data manipulation
- `google-generativeai` - AI chat functionality
- `streamlit-drawable-canvas` - Drawing board
- `gtts` - Text-to-speech features

## Testing and Validation Guidelines

**No Formal Test Suite**
- This repository has no automated tests or linting configuration
- Manual testing through UI interaction is the primary validation method
- Focus on user workflow testing rather than unit tests

**Manual Validation Checklist:**
- [ ] Application starts successfully
- [ ] User registration creates database entry
- [ ] User login works with existing accounts  
- [ ] All sidebar navigation links work
- [ ] Core features load without errors
- [ ] Drawing board renders and functions
- [ ] Database persists data between restarts
- [ ] Error handling works for missing API keys

**Browser Testing:**
- Application works in modern browsers
- JavaScript must be enabled for full functionality
- Some external CDN resources may be blocked - this is normal

## Critical Reminders

- **NEVER CANCEL** pip install commands - dependencies take ~30 seconds to install
- **ALWAYS** test user registration and login flow after making authentication changes
- **API keys are optional** - test core features first before configuring AI functionality
- **Use sidebar navigation** for reliable page access instead of dashboard links
- **Database auto-creates** - no manual setup required for SQLite functionality
- **Vietnamese interface** - application is entirely in Vietnamese language