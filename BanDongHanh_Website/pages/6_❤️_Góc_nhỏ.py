import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Góc nhỏ", page_icon="❤️", layout="centered")

# --- CSS VÀ FONT CHO HỌC SINH HÒA NHẬP ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Quicksand', Arial, sans-serif; 
        font-size: 1.3rem;
    }
    
    /* Navigation back button */
    .back-btn {
        text-decoration: none !important;
        font-size: 1.1rem !important;
        color: #333 !important;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 15px !important;
        display: inline-block !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
        border: 2px solid #2196f3 !important;
        transition: all 0.3s ease !important;
    }
    
    .back-btn:hover {
        background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3) !important;
    }
    
    /* Main title - larger and more colorful */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        background: linear-gradient(135deg, #e91e63, #9c27b0, #3f51b5) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 2rem 0 !important;
        animation: gentle-bounce 2s ease-in-out infinite !important;
    }
    
    @keyframes gentle-bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    /* Instruction text - larger and friendly */
    .instruction-text {
        font-size: 1.4rem !important;
        color: #333 !important;
        text-align: center !important;
        margin: 1.5rem 0 !important;
        padding: 1.5rem !important;
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%) !important;
        border-radius: 20px !important;
        border-left: 6px solid #ff9800 !important;
        line-height: 1.8 !important;
        font-weight: 500 !important;
    }
    
    /* Activity selection buttons - large, colorful, and accessible */
    .activity-button {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%) !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding: 1.5rem 2rem !important;
        margin: 0.8rem !important;
        border: none !important;
        border-radius: 25px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 1rem !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3) !important;
        text-align: left !important;
        min-height: 70px !important;
    }
    
    .activity-button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
        background: linear-gradient(135deg, #66bb6a 0%, #9ccc65 100%) !important;
    }
    
    .activity-button.selected {
        background: linear-gradient(135deg, #2196f3 0%, #03a9f4 100%) !important;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4) !important;
        border: 3px solid #0d47a1 !important;
    }
    
    .activity-button.selected:hover {
        background: linear-gradient(135deg, #42a5f5 0%, #29b6f6 100%) !important;
    }
    
    .activity-icon {
        font-size: 2rem !important;
        margin-right: 0.5rem !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #333 !important;
        text-align: center !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        background: linear-gradient(135deg, #ff5722, #ff9800) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    /* Success checklist */
    .checklist-item {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        font-size: 1.3rem !important;
        border-left: 6px solid #9c27b0 !important;
        transition: all 0.3s ease !important;
    }
    
    .checklist-item:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.2) !important;
    }
    
    .checklist-item.completed {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%) !important;
        border-left: 6px solid #4caf50 !important;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 700px) {
        .main-title { font-size: 2.5rem !important; }
        .activity-button { 
            font-size: 1.2rem !important; 
            padding: 1.2rem 1.5rem !important; 
        }
        .instruction-text { font-size: 1.2rem !important; }
        .section-header { font-size: 1.8rem !important; }
    }
    
    /* Custom styling for Streamlit elements */
    .stButton > button {
        font-family: 'Quicksand', Arial, sans-serif !important;
    }
    
    /* Make our custom buttons clickable */
    .clickable-activity-button {
        cursor: pointer !important;
        user-select: none !important;
    }
    
    .clickable-activity-button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.markdown('<h1 class="main-title">❤️ Góc nhỏ của bạn</h1>', unsafe_allow_html=True)

# Navigation back button using markdown
st.markdown('<a href="0_💖_Trang_chủ.py" class="back-btn">⬅️ Quay về Trang chủ</a>', unsafe_allow_html=True)

st.markdown('<div class="instruction-text">🌟 Chăm sóc bản thân không phải là ích kỷ, đó là điều cần thiết! Hãy bắt đầu với những hành động nhỏ mỗi ngày nhé. Chỉ cần chạm một lần vào mỗi hoạt động để chọn hoặc bỏ chọn.</div>', unsafe_allow_html=True)

# Ngân hàng các hành động nhỏ để tự chăm sóc với biểu tượng
MICRO_ACTIONS = [
    {"text": "Uống một ly nước đầy", "icon": "💧", "color": "#2196f3"},
    {"text": "Vươn vai và duỗi người trong 1 phút", "icon": "🤸‍♀️", "color": "#ff9800"},
    {"text": "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp", "icon": "☁️", "color": "#87ceeb"},
    {"text": "Nghe một bài hát bạn yêu thích", "icon": "🎵", "color": "#e91e63"},
    {"text": "Viết ra 1 điều bạn tự hào về bản thân", "icon": "✍️", "color": "#9c27b0"},
    {"text": "Rửa mặt với nước mát", "icon": "🚿", "color": "#00bcd4"},
    {"text": "Sắp xếp lại góc học tập/làm việc", "icon": "📚", "color": "#4caf50"},
    {"text": "Mỉm cười với chính mình trong gương", "icon": "😊", "color": "#ffc107"}
]

# --- PHẦN LÊN KẾ HOẠCH ---
st.markdown('<h2 class="section-header">🎯 Xây dựng kế hoạch cho hôm nay</h2>', unsafe_allow_html=True)
st.markdown('<div class="instruction-text">💝 Hãy chọn những việc nhỏ bạn muốn làm hôm nay để chăm sóc bản thân. Chỉ cần bấm một lần để chọn hoặc bỏ chọn!</div>', unsafe_allow_html=True)

if 'selected_actions' not in st.session_state:
    st.session_state.selected_actions = []

# Display activity buttons in a more accessible way
st.markdown("### 🌈 Chọn từ ngân hàng hoạt động:")

# Create columns for better layout on larger screens
col1, col2 = st.columns(2)

for i, action in enumerate(MICRO_ACTIONS):
    # Alternate between columns
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        # Check if this action is selected
        is_selected = action["text"] in st.session_state.selected_actions
        
        # Create unique key for each button
        button_key = f"activity_btn_{i}"
        
        # Button text with selection indicator
        button_text = f'{action["icon"]} {action["text"]}'
        if is_selected:
            button_text += " ✓"
        
        # Create button with appropriate styling
        button_type = "primary" if is_selected else "secondary"
        
        if st.button(
            button_text,
            key=button_key,
            help=f"Bấm để {'bỏ chọn' if is_selected else 'chọn'} hoạt động này",
            use_container_width=True,
            type=button_type
        ):
            if action["text"] in st.session_state.selected_actions:
                st.session_state.selected_actions.remove(action["text"])
                st.toast(f"❌ Đã bỏ chọn: {action['text']}", icon="ℹ️")
            else:
                st.session_state.selected_actions.append(action["text"])
                st.toast(f"✅ Đã chọn: {action['text']}", icon="🎉")
            st.rerun()

# Add custom CSS to style all buttons uniformly
st.markdown(f"""
<style>
.stButton > button {{
    font-family: 'Quicksand', Arial, sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    padding: 1.5rem 2rem !important;
    border-radius: 25px !important;
    min-height: 70px !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
}}

.stButton > button[kind="secondary"] {{
    background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%) !important;
    color: white !important;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3) !important;
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #2196f3 0%, #03a9f4 100%) !important;
    color: white !important;
    border: 3px solid #0d47a1 !important;
    box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4) !important;
}}

.stButton > button:hover {{
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# --- PHẦN HIỂN THỊ CHECKLIST ---
if not st.session_state.selected_actions:
    st.markdown("""
    <div class="instruction-text" style="background: linear-gradient(135deg, #ffecb3 0%, #ffe0b2 100%) !important; border-left: 6px solid #ffa000 !important;">
        🌟 Hãy chọn ít nhất một hành động để bắt đầu kế hoạch của bạn nhé! Mỗi bước nhỏ đều có ý nghĩa lớn.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<h2 class="section-header">📋 Danh sách việc cần làm của bạn hôm nay:</h2>', unsafe_allow_html=True)
    
    # Add instructions for the checklist
    st.markdown("""
    <div class="instruction-text" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%) !important; border-left: 6px solid #4caf50 !important;">
        💡 Hướng dẫn: Bấm vào từng mục khi bạn hoàn thành để đánh dấu ✓. Bạn sẽ thấy thông báo chúc mừng!
    </div>
    """, unsafe_allow_html=True)
    
    all_done = True
    
    for i, action in enumerate(st.session_state.selected_actions):
        # Find the corresponding icon
        action_icon = "💝"  # Default icon
        for micro_action in MICRO_ACTIONS:
            if micro_action["text"] == action:
                action_icon = micro_action["icon"]
                break
        
        if f"action_{action}" not in st.session_state:
            st.session_state[f"action_{action}"] = False
        
        is_done = st.session_state[f"action_{action}"]
        
        # Create styled checklist item
        item_class = "checklist-item completed" if is_done else "checklist-item"
        status_icon = "✅" if is_done else "⬜"
        
        # Display the checklist item with better styling
        col1, col2 = st.columns([0.1, 0.9])
        
        with col1:
            # Use a checkbox that's more accessible
            checkbox_key = f"cb_{action}_{i}"  # More unique key
            new_state = st.checkbox(
                "", 
                key=checkbox_key, 
                value=is_done,
                help=f"Bấm để đánh dấu {'hoàn thành' if not is_done else 'chưa hoàn thành'}"
            )
        
        with col2:
            item_html = f'''
            <div class="{item_class}">
                <span style="font-size: 1.8rem; margin-right: 1rem;">{action_icon}</span>
                <span style="font-weight: 600;">{action}</span>
                <span style="margin-left: auto; font-size: 1.5rem;">{status_icon}</span>
            </div>
            '''
            st.markdown(item_html, unsafe_allow_html=True)
        
        # Handle state changes
        if new_state != is_done:
            if new_state:
                st.toast(f"🎉 Tuyệt vời! Bạn đã hoàn thành: {action}", icon="🌟")
                st.balloons()
            else:
                st.toast(f"📝 Đã bỏ đánh dấu: {action}", icon="ℹ️")
            st.session_state[f"action_{action}"] = new_state
        
        if not new_state:
            all_done = False

    # Show completion celebration
    if all_done and st.session_state.selected_actions:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 50%, #ff6f00 100%);
            border-radius: 25px;
            padding: 2.5rem;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 30px rgba(255, 152, 0, 0.3);
            animation: celebration-pulse 2s ease-in-out infinite;
        ">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem; color: #e65100;">
                🎉 CHÚC MỪNG! 🎉
            </h2>
            <p style="font-size: 1.5rem; font-weight: 600; color: #bf360c; margin-bottom: 1rem;">
                Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!
            </p>
            <p style="font-size: 1.3rem; color: #d84315;">
                🌟 Bạn thật tuyệt vời! Hãy tự hào về bản thân nhé! 🌟
            </p>
        </div>
        <style>
        @keyframes celebration-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.03); }
        }
        </style>
        """, unsafe_allow_html=True)
        st.balloons()

# Add footer with encouragement
st.markdown("---")
st.markdown("""
<div class="instruction-text" style="
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%) !important; 
    border-left: 6px solid #9c27b0 !important;
    text-align: center !important;
">
    💜 <strong>Nhớ nhé:</strong> Mỗi hành động nhỏ đều là một bước tiến lớn trong việc chăm sóc bản thân. 
    Hãy kiên nhẫn và yêu thương chính mình! 💜
</div>
""", unsafe_allow_html=True)
