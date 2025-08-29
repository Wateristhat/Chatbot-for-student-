# pages/9_📖_Người_Kể_Chuyện.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import base64

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="centered")

# --- Không cần đăng nhập nữa ---

# --- NỘI DUNG TRUYỆN ---
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

# --- CÁC HÀM HỖ TRỢ ---
@st.cache_data
def text_to_speech(text):
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Lỗi tạo âm thanh: {e}")
        return None

# --- GIAO DIỆN CHÍNH ---
st.title("📖 Người Kể Chuyện")

# *** SỬA LẠI ĐÚNG ĐƯỜNG DẪN ***
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown("Hãy chọn một thể loại và lắng nghe một câu chuyện nhỏ để xoa dịu tâm hồn nhé.")
st.write("---")

# Chọn thể loại truyện
selected_category = st.selectbox(
    "Chọn thể loại truyện bạn muốn nghe:",
    options=list(STORIES.keys())
)

st.write("---")

# Hiển thị danh sách các câu chuyện trong thể loại đã chọn
if selected_category:
    st.subheader(f"Các câu chuyện về {selected_category.lower()}:")
    
    for i, story in enumerate(STORIES[selected_category]):
        with st.expander(story["title"]):
            st.write(story["content"])
            
            if st.button("Nghe truyện 🎧", key=f"listen_{selected_category}_{i}"):
                with st.spinner("Đang chuẩn bị âm thanh..."):
                    audio_data = text_to_speech(f"Câu chuyện {story['title']}. {story['content']}")
                    if audio_data:
                        st.audio(audio_data, format="audio/mp3")
                    else:
                        st.warning("Không thể tạo file âm thanh cho truyện này.")
