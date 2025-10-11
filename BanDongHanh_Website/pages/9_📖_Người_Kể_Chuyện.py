# pages/9_📖_Người_Kể_Chuyện.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="wide")

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé! ❤️")
    st.stop()

# --- CSS HOÀN CHỈNH VÀ SẠCH SẼ ---
st.markdown("""
<style>
/* CSS chung cho các nút bấm */
.stButton > button {
    padding: 0.8rem 1.2rem; font-size: 1.15rem; font-weight: 600; width: 100%;
    margin-bottom: 0.7rem; border-radius: 12px; border: 2px solid #b39ddb;
    background-color: #f9f9fb; color: #6d28d9;
}
.stButton > button:hover { background-color: #f3e8ff; border-color: #5d3fd3; color: #5d3fd3; }

/* CSS cho tiêu đề và khung trợ lý ảo */
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

/* --- CSS CUỐI CÙNG CHO Ô CHỌN (SELECTBOX) --- */

/* Làm to nhãn (chữ bên trên) */
div[data-testid="stSelectbox"] > label {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #333 !important;
    padding-bottom: 0.5rem !important;
}

/* Làm to cái hộp */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 2px solid #b39ddb !important;
    background-color: #FFFFFF !important;
}

/* Làm to và hiện chữ bên trong hộp (selector mạnh nhất) */
div[data-testid="stSelectbox"] div[data-testid="stText"] {
    font-size: 1.3rem !important;
    color: #333 !important; /* DÒNG QUAN TRỌNG NHẤT ĐỂ HIỆN CHỮ */
}
</style>
""", unsafe_allow_html=True)

# --- NỘI DUNG TRUYỆN (ĐÃ PHỤC HỒI ĐẦY ĐỦ) ---
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
            }
        ],
        "Truyện ngụ ngôn": [
            {
                "title": "Ếch ngồi đáy giếng",
                "content": "Có một con ếch sống lâu năm trong một cái giếng. Nó nhìn lên và chỉ thấy một khoảng trời bé bằng miệng giếng. Nó tự hào nghĩ rằng bầu trời chỉ to có vậy. Một ngày, trời mưa to, nước giếng dâng lên và đưa ếch ra ngoài. Lần đầu tiên, nó thấy một bầu trời rộng lớn bao la và nhận ra sự hiểu biết hạn hẹp của mình. Bài học: Môi trường sống hạn hẹp có thể che lấp tầm nhìn của chúng ta. Đừng vội cho rằng những gì mình biết là tất cả."
            },
            {
                "title": "Cáo và chùm nho",
                "content": "Một con cáo đói đi qua một vườn nho. Nó thấy một chùm nho chín mọng lủng lẳng trên giàn cao. Cáo nhảy lên nhiều lần nhưng không thể với tới. Cuối cùng, nó bỏ đi và tự nhủ: 'Nho còn xanh lắm, ăn vào chỉ chua thôi!'. Bài học: Nhiều người thường chê bai những thứ họ không thể đạt được để tự an ủi bản thân."
            }
        ],
        "Truyện chữa lành": [
            {
                "title": "Dòng sông không vội vã",
                "content": "Không một dòng sông nào vội vã. Nó chảy theo nhịp điệu của riêng mình, lúc êm đềm, lúc cuộn trào, nhưng luôn tiến về phía trước. Dòng sông biết rằng, rồi nó sẽ đến được biển lớn. Hãy sống như một dòng sông, chấp nhận mọi khúc quanh của cuộc đời và tin tưởng vào hành trình của chính mình. Đừng so sánh tốc độ của bạn với người khác, vì mỗi người đều có một con đường riêng."
            },
            {
                "title": "Chiếc bình nứt",
                "content": "Một người gánh nước có hai chiếc bình, một chiếc lành lặn và một chiếc bị nứt. Chiếc bình nứt luôn cảm thấy tự ti vì nó chỉ giữ được một nửa phần nước. Một ngày, nó xin lỗi người chủ. Người chủ mỉm cười và nói: 'Con có thấy những luống hoa xinh đẹp bên đường không? Đó là nhờ ta đã gieo hạt ở phía bên con. Mỗi ngày, những giọt nước từ vết nứt của con đã tưới cho chúng'. Bài học: Những khuyết điểm của bạn có thể lại là điều tạo nên vẻ đẹp và giá trị riêng biệt mà bạn không ngờ tới."
            }
        ]
    }
STORIES = load_stories()

# --- TRỢ LÝ ẢO ---
ASSISTANT_MESSAGES = [
    ("📖", "Hãy chọn một thể loại và lắng nghe một câu chuyện nhỏ để xoa dịu tâm hồn nhé."),
    ("✨", "Mỗi câu chuyện là một bài học. Cùng khám phá với Bee nào!"),
    ("🎧", "Sẵn sàng lắng nghe chưa? Bee sẽ kể cho bạn những câu chuyện hay nhất!"),
]
if "nkc_assistant_message" not in st.session_state:
    st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
avatar, msg = st.session_state.nkc_assistant_message

# --- GIAO DIỆN CHÍNH ---
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

st.markdown("⬅️ [Quay về Trang chủ](/)", unsafe_allow_html=True)
st.write("---")

# --- PHẦN CHỌN TRUYỆN (SỬ DỤNG NHÃN MẶC ĐỊNH) ---
selected_category = st.selectbox(
    "Chọn thể loại truyện bạn muốn nghe:", # Sử dụng lại nhãn mặc định
    options=list(STORIES.keys())
)
st.write("---")

# --- PHẦN HIỂN THỊ TRUYỆN ---
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
