# Sửa file: pages/9_📖_Người_Kể_Chuyện.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import sys # ### <<< SỬA ĐỔI: Thêm import
import os  # ### <<< SỬA ĐỔI: Thêm import

# --- BẢO VỆ TRANG ---
### <<< SỬA ĐỔI: Thêm bảo vệ trang ở đầu file >>>
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() # Dừng chạy code của trang này

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI (Để đó, có thể dùng sau) ---
current_user_id = st.session_state.user_id

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="wide")

# --- CSS GIAO DIỆN (Giữ nguyên) ---
st.markdown("""
<style>
/* (Toàn bộ CSS của bạn được giữ nguyên) */
.stButton > button {
    padding: 0.8rem 1.2rem; font-size: 1.15rem; font-weight: 600; width: 100%;
    margin-bottom: 0.7rem; border-radius: 12px; border: 2px solid #b39ddb;
    background-color: #f9f9fb; color: #6d28d9;
}
.stButton > button:hover {
    background-color: #f3e8ff; border-color: #5d3fd3; color: #5d3fd3;
}
.nkc-title-feature {
    font-size: 2.6rem; font-weight: 700; color: #5d3fd3; text-align: center;
    margin-bottom: 1.4rem; margin-top: 0.7rem; display: flex; align-items: center;
    justify-content: center; gap: 1.1rem;
}
.nkc-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom: 2.3rem; margin-top: 0.2rem;
    text-align: center; border: 3.5px solid #b39ddb; max-width: 1700px;
    margin-left: auto; margin-right: auto;
}
.nkc-assist-icon { font-size: 3.2rem; margin-bottom: 0.7rem; }
.nkc-assist-text { font-size: 1.7rem; font-weight: 700; color: #6d28d9; margin-bottom: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# --- NỘI DUNG TRUYỆN (Giữ nguyên) ---
@st.cache_data
def load_stories():
    return {
        "Truyện truyền cảm hứng": [
            {
                "title": "Câu chuyện về hai hạt giống",
                "content": "Có hai hạt giống nằm cạnh nhau. Hạt giống thứ nhất nói: 'Tôi muốn vươn lên! Tôi muốn bén rễ sâu xuống lòng đất và đâm chồi nảy lộc trên mặt đất.' Và rồi, hạt giống đó vươn mình phát triển. Hạt giống thứ hai nói: 'Tôi sợ hãi. Nếu rễ của tôi đâm xuống lòng đất, tôi không biết sẽ gặp phải điều gì. Tốt hơn là tôi nên chờ đợi.' Một con gà đi qua, thấy hạt giống nằm trơ trọi trên mặt đất và mổ ăn mất. Bài học: Những ai không dám mạo hiểm và vươn lên sẽ bị cuộc đời đào thải."
            },
            {
                "title": "Chuyện tảng đá",
                "content": "Một chàng trai trẻ liên tục thất bại nên rất chán nản. Anh đến hỏi một ông lão thông thái. Ông lão đưa anh một hòn đá và nói: 'Cậu hãy mang hòn đá này ra chợ bán, nhưng không được bán nó, chỉ cần xem người ta trả giá bao nhiêu.' Ở chợ, người ta chỉ trả vài đồng. Ông lão lại bảo anh mang vào tiệm vàng, ông chủ tiệm trả giá 500 đồng. Cuối cùng, anh mang đến một chuyên gia đá quý, người này hét lên: 'Đây là một viên ngọc quý hiếm, vô giá!'. Ông lão nói: 'Cuộc đời con cũng giống như hòn đá này. Giá trị của con không phải do người khác quyết định, mà do con đặt mình vào đâu.'"
            },
            # (Tất cả các câu chuyện khác của bạn được giữ nguyên)
            # ...
            {
                "title": "Phép màu của sự bắt đầu",
                "content": "Nhà văn người Brazil Paulo Coelho từng nói: 'Khi bạn thực sự muốn điều gì đó, cả vũ trụ sẽ hợp lực giúp bạn đạt được điều đó.' Nhiều người trì hoãn ước mơ vì sợ thất bại. Nhưng câu chuyện này dạy rằng, bước đi đầu tiên, dù nhỏ bé đến đâu, là điều kiện tiên quyết để tạo ra 'phép màu' của sự hỗ trợ từ bên ngoài. Bài học: Hãy bắt đầu. Chỉ khi bạn bắt đầu hành động, những cơ hội, sự giúp đỡ và nguồn lực cần thiết mới xuất hiện để hỗ trợ bạn trên hành trình của mình."
            }
        ],
        "Truyện ngụ ngôn": [
            # (Tất cả truyện ngụ ngôn của bạn được giữ nguyên)
            # ...
            {
                "title": "Chim bồ câu và kiến",
                "content": "Một con kiến bị trượt chân và rơi xuống sông. Một con chim bồ câu thấy vậy, nhanh chóng thả một chiếc lá xuống nước. Kiến bám vào chiếc lá và thoát chết. Ít lâu sau, một người thợ săn giương súng định bắn bồ câu. Kiến nhìn thấy, bèn bò đến và cắn vào chân người thợ săn. Người thợ săn giật mình làm rơi súng, bồ câu nghe tiếng động nên bay đi thoát nạn. Bài học: Hãy luôn giúp đỡ người khác khi họ gặp khó khăn, vì một ngày nào đó, bạn cũng sẽ nhận lại sự giúp đỡ."
            }
        ],
        "Truyện chữa lành": [
            # (Tất cả truyện chữa lành của bạn được giữ nguyên)
            # ...
            {
                "title": "Chiếc bình nứt",
                "content": "Một người gánh nước có hai chiếc bình, một chiếc lành lặn và một chiếc bị nứt. Chiếc bình nứt luôn cảm thấy tự ti vì nó chỉ giữ được một nửa phần nước. Một ngày, nó xin lỗi người chủ. Người chủ mỉm cười và nói: 'Con có thấy những luống hoa xinh đẹp bên đường không? Đó là nhờ ta đã gieo hạt ở phía bên con. Mỗi ngày, những giọt nước từ vết nứt của con đã tưới cho chúng'. Bài học: Những khuyết điểm của bạn có thể lại là điều tạo nên vẻ đẹp và giá trị riêng biệt mà bạn không ngờ tới."
            }
        ]
    }
STORIES = load_stories()

# --- TRỢ LÝ ẢO & TÊN TÍNH NĂNG (Giữ nguyên) ---
ASSISTANT_MESSAGES = [
    ("📖", "Hãy chọn một thể loại và lắng nghe một câu chuyện nhỏ để xoa dịu tâm hồn nhé."),
    ("✨", "Mỗi câu chuyện là một bài học. Cùng khám phá với Bee nào!"),
    ("🎧", "Sẵn sàng lắng nghe chưa? Bee sẽ kể cho bạn những câu chuyện hay nhất!"),
]
if "nkc_assistant_message" not in st.session_state:
    st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
avatar, msg = st.session_state.nkc_assistant_message

# --- GIAO DIỆN CHÍNH (Giữ nguyên) ---
st.markdown(
    '<div class="nkc-title-feature">'
    ' <span style="font-size:2.3rem;">📖</span> Người Kể Chuyện'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(f"""
<div class="nkc-assist-bigbox">
    <div class="nkc-assist-icon">{avatar}</div>
    <div class="nkc-assist-text">{msg}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("💬 Thông điệp mới", key="new_msg_story"):
        st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe trợ lý ảo", key="tts_msg_story"):
        audio_bytes = BytesIO()
        tts = gTTS(text=msg, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format="audio/mp3")

### <<< SỬA ĐỔI: Thay thế thẻ <a> bằng st.page_link >>>
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
# st.markdown("⬅️ [Quay về Trang chủ](/)", unsafe_allow_html=True) # Xóa dòng này

st.write("---")

selected_category = st.selectbox(
    "**Chọn thể loại truyện bạn muốn nghe:**",
    options=list(STORIES.keys())
)
st.write("---")

# (Toàn bộ logic hiển thị truyện và TTS bên dưới được giữ nguyên)
if selected_category:
    st.subheader(f"Các câu chuyện về {selected_category.lower()}:")
    for i, story in enumerate(STORIES[selected_category]):
        with st.expander(f"**{story['title']}**"):
            st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.6;'>{story['content']}</p>", unsafe_allow_html=True)
            
            if st.button("Nghe truyện 🎧", key=f"listen_{selected_category}_{i}"):
                with st.spinner("Đang chuẩn bị âm thanh..."):
                    full_text = f"Câu chuyện {story['title']}. {story['content']}"
                    try:
                        tts = gTTS(text=full_text, lang='vi', slow=False)
                        fp = BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        st.audio(fp, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Lỗi khi tạo âm thanh: {e}")
