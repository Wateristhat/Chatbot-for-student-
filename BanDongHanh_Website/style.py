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

        /* Tiêu đề chính của trang */
        .app-title-feature {
            font-size: 2.6rem; font-weight: 700; color: #5d3fd3; text-align: center;
            margin-bottom: 1.4rem; margin-top: 0.7rem; display: flex; align-items: center;
            justify-content: center; gap: 1.1rem;
        }
        
        /* Khung trợ lý ảo màu tím */
        .app-assist-box {
            background: linear-gradient(120deg, #e0e7ff 0%, #f3e8ff 100%);
            border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
            padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom: 2.3rem; margin-top: 0.2rem;
            text-align: center; border: 3.5px solid #b39ddb; max-width: 1700px;
            margin-left: auto; margin-right: auto;
        }
        .app-assist-icon { font-size: 3.2rem; margin-bottom: 0.7rem; }
        .app-assist-text { font-size: 1.7rem; font-weight: 700; color: #6d28d9; margin-bottom: 1.1rem; }

        /* Khung nội dung/thẻ card chung */
        .app-card {
            background: #fff;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 5px solid #b39ddb;
            box-shadow: 0 3px 15px rgba(93, 63, 211, 0.08);
        }
    </style>
    """, unsafe_allow_html=True)
