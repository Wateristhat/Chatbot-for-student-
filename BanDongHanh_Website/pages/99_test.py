# file: pages/99_🧪_Test_AI.py
import streamlit as st
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("🧪 Trang Chẩn Đoán Lỗi Kết Nối Gemini AI")
st.write("---")

st.header("Bước 1: Kiểm tra API Key")

# Lấy API key từ Streamlit Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔴 LỖI: Không tìm thấy `GOOGLE_API_KEY` trong file secrets.toml.")
    st.info("Nguyên nhân phổ biến nhất là file `secrets.toml` của bạn đang bị đặt sai vị trí.")
    st.write("Cấu trúc thư mục đúng phải là:")
    st.code("""
BanDongHanh_Website/
├── .streamlit/            <-- Thư mục có dấu chấm ở đầu
│   └── secrets.toml       <-- File API Key phải nằm ở đây
└── pages/
    └── ... (các trang con)
    """, language="text")
    st.stop()
else:
    st.success("✅ Đã tìm thấy API Key trong secrets!")
    st.write("---")

st.header("Bước 2: Kiểm tra Cấu hình và Kết nối Model")

try:
    genai.configure(api_key=api_key)
    st.success("✅ Cấu hình API Key thành công!")

    model_names = [
        "gemini-1.5-flash-latest",
        "gemini-1.0-pro",
        "gemini-pro"
    ]
    
    st.info(f"Đang thử kết nối lần lượt đến các model: {model_names}...")
    
    model_found = False
    for model_name in model_names:
        with st.spinner(f"Đang thử model: `{model_name}`..."):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Chào bạn, bạn có khỏe không?", generation_config={"max_output_tokens": 10})
                
                st.success(f"🎉 KẾT NỐI THÀNH CÔNG VỚI MODEL: `{model_name}`!")
                st.write("Phản hồi từ AI:", response.text)
                st.balloons()
                model_found = True
                break 
            except Exception as e:
                st.warning(f"⚠️ Không thể kết nối với model `{model_name}`. Lỗi: {e}")
    
    st.write("---")
    st.header("Bước 3: Kết Luận")
    if not model_found:
        st.error("🔴 LỖI CUỐI CÙNG: Đã thử tất cả các model nhưng không thể kết nối với bất kỳ model Gemini nào.")
        st.warning(
            "**Nguyên nhân có thể là:**\n"
            "1.  **API Key không hợp lệ:** Key bạn sao chép đã sai hoặc hết hạn.\n"
            "2.  **API chưa được bật:** Bạn cần bật 'Generative Language API' trong tài khoản Google Cloud của mình.\n"
            "3.  **Lỗi kết nối mạng:** Mạng của bạn hoặc của server đang chặn kết nối đến Google."
        )
        st.info("**Cách khắc phục:** Hãy vào [Google AI Studio](https://aistudio.google.com/), tạo một API Key **mới hoàn toàn**, và dán lại vào file `secrets.toml`.")

except Exception as e:
    st.error(f"🚨 LỖI NGHIÊM TRỌNG: Lỗi ngay từ bước cấu hình genai. Điều này gần như chắc chắn là do API Key của bạn không hợp lệ.")
    st.exception(e)
