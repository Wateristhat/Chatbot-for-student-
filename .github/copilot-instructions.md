# Vietnamese Student Mental Health Chatbot - "Bạn Đồng Hành" (Companion Friend)

**ALWAYS FOLLOW THESE INSTRUCTIONS FIRST.** Only search for additional information or context if these instructions are incomplete or found to be incorrect.

"Bạn Đồng Hành" is a Vietnamese Streamlit web application designed to support student mental health. It features meditation exercises, gratitude journaling, AI chatbot interaction, emotional expression tools, mini-games, and emergency support resources.

## Working Effectively

### Bootstrap and Dependencies
- Install Python dependencies: `cd BanDongHanh_Website && python -m pip install -r requirements.txt`
  - Takes ~45 seconds to complete. NEVER CANCEL. Set timeout to 60+ minutes for safety.
  - All required packages: streamlit, pandas, gtts, google-generativeai, streamlit-drawable-canvas, google-cloud-texttospeech, google-cloud-aiplatform, bcrypt
- Validate installation: `python -c "import streamlit; print('Dependencies ready')"`
  - Takes <1 second to complete.

### Running the Application
- **Start the application**: `cd BanDongHanh_Website && python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false`
  - Takes ~10 seconds to start. NEVER CANCEL applications during startup.
  - Application accessible at http://localhost:8501
  - Creates SQLite database (app_data.db) automatically on first run
- **Stop the application**: Use Ctrl+C or stop the process

### Build and Testing
- **No separate build process required** - Python interpreted application
- **Syntax validation**: `find BanDongHanh_Website -name "*.py" -exec python -m py_compile {} \;`
  - Takes <5 seconds to complete
- **Database validation**: `python -c "import database; print('Database module ready')"`
  - Takes <1 second to complete

## Validation Scenarios

### **CRITICAL: Always test these complete end-to-end scenarios after making changes**

#### User Registration and Navigation Workflow
1. Navigate to http://localhost:8501
2. Fill out user registration form:
   - Enter name: "Test User"
   - Select birth year: any year from dropdown
   - Enter school: "Test School"  
   - Enter current difficulties: "Testing the application"
3. Click "💖 Lưu thông tin và bắt đầu!" (Save information and start)
4. Verify welcome message shows: "Chào mừng Test User đến với Bạn Đồng Hành!"
5. Test navigation: Click sidebar links to visit each feature page
6. **EXPECTED RESULT**: Most pages will show "Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé!" due to authentication bug

#### Basic Functionality Testing (LIMITED SCOPE)
1. **Home page**: User registration form works
2. **Navigation**: Sidebar menu appears and links work
3. **Authentication**: Only home page properly recognizes logged-in user
4. **Database**: app_data.db file gets created
5. **NOTE**: Do NOT test feature functionality (gratitude journal, chat, etc.) - they have known bugs

### Manual Validation Requirements
- **ALWAYS test the complete user registration workflow before considering changes complete**
- **ALWAYS verify that home page user registration works and shows welcome message**
- **ALWAYS verify that sidebar navigation appears and links work**
- **EXPECT authentication errors on most feature pages due to known bugs**
- Do NOT test individual feature functionality (gratitude journal, chat, etc.) due to implementation issues

## Application Structure

### Key Files and Directories
```
BanDongHanh_Website/
├── app.py                          # Main entry point - redirects to home page
├── database.py                     # SQLite database operations
├── requirements.txt                # Python dependencies
├── pages/                          # Streamlit multi-page structure
│   ├── 0_💖_Trang_chủ.py           # Home page with user registration
│   ├── 1_✨_Liều_thuốc_tinh_thần.py # Inspirational messages
│   ├── 2_🧘_Góc_an_yên.py          # Meditation and breathing exercises
│   ├── 3_🍯_Lọ_biết_ơn.py          # Gratitude journal
│   ├── 4_🎨_Bảng_màu_cảm_xúc.py    # Emotional expression drawing canvas
│   ├── 5_🎮_Nhanh_tay_lẹ_mắt.py    # Mini-game for stress relief
│   ├── 6_❤️_Góc_nhỏ.py             # Self-care activity planner
│   ├── 7_🆘_Hỗ_Trợ_Khẩn_Cấp.py     # Emergency support resources
│   ├── 8_💬_Trò_chuyện.py          # AI chatbot interface
│   └── 9_📖_Người_Kể_Chuyện.py     # Story/inspirational content
├── game.html                       # HTML5 game for stress relief
├── game_app.py                     # Game page wrapper
└── mood_journal.csv               # Sample mood tracking data
```

### Generated Files (DO NOT COMMIT)
- `__pycache__/` directories - Python bytecode cache
- `app_data.db` - SQLite database with user data
- `*.pyc` files - Compiled Python files

## Common Development Tasks

### Making Code Changes
1. **ALWAYS start the application first** using the commands above
2. **ALWAYS test the user registration workflow** before making changes
3. Make your code changes
4. Restart the application to see changes: Ctrl+C then restart streamlit
5. **ALWAYS re-test the complete validation scenarios** above
6. **ALWAYS verify database operations still work** after changes

### Session State Management
- User data stored in `st.session_state.user_name`, `st.session_state.user_info` (home page only)
- **AUTHENTICATION BUG**: Other pages check for `st.session_state.user_id` which is never set
- Most feature pages show authentication error due to this mismatch
- Session lost on page refresh or direct URL navigation - normal Streamlit behavior
- **ALWAYS start testing from home page (http://localhost:8501) and register user first**
- **EXPECT most feature pages to show authentication warning**

### Database Operations
- All database functions in `database.py`
- Creates tables automatically via `create_tables()` called in app.py
- Main operations: user management, chat history, gratitude notes
- Database file created automatically on first run

### Adding New Features
1. Create new page file in `pages/` directory with proper naming: `N_emoji_Page_Name.py`
2. Follow existing authentication pattern: check `st.session_state.get('user_id')`
3. Add navigation link in sidebar (automatically appears in Streamlit)
4. Test complete user workflow including new feature

## Troubleshooting

### Common Issues and Solutions
- **Import errors**: Run `pip install -r requirements.txt` again
- **Database errors**: Check that `app_data.db` has write permissions
- **Authentication issues**: CRITICAL BUG - Home page sets `user_name` but other pages check for `user_id`. Most features will show login warning.
- **"Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé!" message**: This appears on most pages due to authentication bug above
- **Gratitude journal and other features not working**: Missing database functions (`add_gratitude_note`, `get_gratitude_notes`, `delete_gratitude_note`)
- **Streamlit not starting**: Check port 8501 is available, kill existing processes

### Known Limitations
- **AUTHENTICATION BUG**: Only home page and basic navigation work properly. Most features will show authentication errors.
- **MISSING DATABASE FUNCTIONS**: Gratitude journal and other database features are not implemented
- **LIMITED TESTING SCOPE**: Only test user registration and navigation between pages. Do NOT test feature functionality.

### Performance Notes
- **Application startup**: 10 seconds typical, up to 30 seconds acceptable
- **Page navigation**: Instantaneous within app
- **Database operations**: Sub-second response times
- **AI features**: May have longer response times or be offline (uses external APIs)

### File Permissions
- Application creates database file automatically
- Requires write access to `BanDongHanh_Website/` directory
- No special permissions needed for Python files

## External Dependencies

### Required Services (Optional)
- **Google Generative AI**: For chatbot functionality (may work offline with fallback responses)
- **Google Text-to-Speech**: For audio features (may fail gracefully)
- **Internet connection**: For some AI features and external fonts

### Core Dependencies Always Required
- Python 3.8+
- Streamlit (web framework)
- SQLite (embedded database)
- All packages in requirements.txt

Remember: **ALWAYS validate your changes using the complete user scenarios above**. The application should work end-to-end without errors before considering development complete.