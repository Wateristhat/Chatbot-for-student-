# file: style.py
import streamlit as st

def apply_global_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* --- FONT CHUNG --- */
        html, body, [class*="css"] {
            font-family: 'Quicksand', Arial, sans-serif;
        }

        /* --- SỬA LỖI CHIỀU CAO SIDEBAR --- */
        [data-testid="stSidebarNavItems"] li a {
            height: 2.75rem; 
            display: flex;
            align-items: center;
        }

        /* --- STYLE CHUNG CHO CÁC NÚT BẤM --- */
        .stButton > button {
            padding: 0.8rem 1.2rem !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            width: 100%;
            margin-bottom: 0.7rem !important;
            border-radius: 12px !important;
            border: 2.5px solid #d1c4e9 !important;
            background-color: #f9f9fb !important;
            color: #5d3fd3 !important;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #f3e8ff !important;
            border-color: #5d3fd3 !important;
            color: #5d3fd3 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(93, 63, 211, 0.15);
        }

        /* --- STYLE CHUNG CHO Ô CHỌN (SELECTBOX) --- */
        div[data-testid="stSelectbox"] > label {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: #333 !important;
            padding-bottom: 0.5rem !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            padding: 1rem !important;
            border-radius: 12px !important;
            border: 2px solid #b39ddb !important;
            background-color: #FFFFFF !important;
        }
        div[data-testid="stSelectbox"] div[data-testid="stText"] {
            font-size: 1.3rem !important;
            color: #333 !important;
        }

        /* --- CÁC CLASS GIAO DIỆN DÙNG CHUNG --- */
        .app-title-feature {
            font-size: 2.6rem; font-weight: 700; color: #5d3fd3; text-align: center;
            margin-bottom: 1.4rem; margin-top: 0.7rem; display: flex; align-items: center;
            justify-content: center; gap: 1.1rem;
        }
        .app-assist-box {
            background: linear-gradient(120deg, #e0e7ff 0%, #f3e8ff 100%);
            border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
            padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom: 2.3rem; margin-top: 0.2rem;
            text-align: center; border: 3.5px solid #b39ddb; max-width: 1700px;
            margin-left: auto; margin-right: auto;
        }
        .app-assist-icon { font-size: 3.2rem; margin-bottom: 0.7rem; }
        .app-assist-text { font-size: 1.7rem; font-weight: 700; color: #6d28d9; margin-bottom: 1.1rem; }
        .app-card {
            background: #fff;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 5px solid #b39ddb;
            box-shadow: 0 3px 15px rgba(93, 63, 211, 0.08);
        }

        /* --- (MỚI) SIÊU KHỐI CSS TƯƠNG THÍCH ĐIỆN THOẠI --- */
        @media (max-width: 900px) {
            
            /* --- NÚT BẤM (BUTTONS) --- */
            .stButton > button {
                width: 100% !important;
                max-width: 100% !important;
                margin-bottom: 0.8rem !important; 
            }

            /* --- KHUNG TRỢ LÝ (ASSISTANT BOXES) --- */
            .app-assist-box, .lo-assist-bigbox, .bmcx-assist-bigbox, 
            .lttt-assist-bigbox, .gn-assist-bigbox, .nkc-assist-bigbox {
                padding: 2rem 1rem !important; 
                max-width: 96vw !important; 
            }

            /* --- TIÊU ĐỀ TRANG (TITLES) --- */
            .app-title-feature, .lo-title-feature, .bmcx-title-feature, 
            .lttt-title-feature, .gn-title, .nkc-title-feature, .game-title {
                font-size: 1.8rem !important; 
            }
            .game-subtitle {
                font-size: 1.3rem !important;
            }

            /* --- TEXT TRỢ LÝ (ASSISTANT TEXT) --- */
            .app-assist-text, .lo-assist-text, .bmcx-assist-text, 
            .lttt-assist-text, .gn-assist-text, .nkc-assist-text {
                font-size: 1.2rem !important; 
            }

            /* --- CÁC HỘP NỘI DUNG (CONTENT CARDS) --- */
            .app-card, .lo-box, .timeline-item, .lo-footer, 
            .bmcx-palette-box, .bmcx-note-box, .bmcx-history-box, .bmcx-footer,
            .lttt-box, .lttt-card, .lttt-footer, .lttt-history-box,
            .gn-checklist-item, .gn-congrats, .gn-footer,
            .nkc-story-card, .nkc-footer, .encouragement-box,
            .assistant-card, .exercise-card, .inclusive-instruction, .progress-container,
            .hotline-container, .emergency-warning-box {
                max-width: 96vw !important;
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                font-size: 1rem !important;
            }

            /* --- CÁC TRƯỜNG HỢP ĐẶC BIỆT --- */

            /* (Trang chủ) Thu nhỏ menu */
            .menu-card { padding: 1rem 0.8rem; gap: 1rem; }
            .menu-icon { font-size: 1.8rem; }
            .menu-title { font-size: 1.05rem; }
            .menu-desc { font-size: 0.9rem; }

            /* (Bảng Màu) Thu nhỏ các vòng tròn emoji */
            .bmcx-emotion-circle {
                width: 80px !important; height: 80px !important;
                font-size: 1.5rem !important;
                margin: 0 5px 1rem 5px !important;
            }
            .bmcx-emotion-label { font-size: 0.9rem !important; }
            
            /* --- (MỚI) SỬA LỖI GAME BỊ CẮT 1/2 --- */
            canvas[width] { /* Chỉ nhắm vào canvas của game */
                width: 100% !important;     /* Ép canvas vừa 100% màn hình */
                max-width: 100% !important;
                height: auto !important;     /* Tự động chỉnh chiều cao */
            }

        }
        /* --- KẾT THÚC SIÊU KHỐI --- */

    </style>
    """, unsafe_allow_html=True)
