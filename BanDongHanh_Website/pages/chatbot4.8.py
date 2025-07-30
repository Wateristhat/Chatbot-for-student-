import random
import streamlit as st
import re
import time
import html
from gtts import gTTS         # NEW: Thư viện chuyển văn bản thành giọng nói
from io import BytesIO        # NEW: Dùng để xử lý file âm thanh trong bộ nhớ
import base64                 # NEW: Dùng để mã hóa file âm thanh

# --- 0. CÁC HẰNG SỐ ĐIỀU KHIỂN TRẠNG THÁI ---
STATE_MAIN = 'main'
STATE_TAM_SU_SELECTION = 'tam_su_selection'
STATE_TAM_SU_CHAT = 'tam_su_chat'
STATE_GIAO_TIEP_SELECTION_BASIC = 'giao_tiep_selection_basic'
STATE_GIAO_TIEP_SELECTION_EXTENDED = 'giao_tiep_selection_extended'
STATE_GIAO_TIEP_PRACTICE = 'giao_tiep_practice'
STATE_AWAITING_FOLLOWUP = 'awaiting_followup'

# --- 1. TỐI ƯU HÓA CẤU HÌNH BẰNG CACHING ---
@st.cache_data
def get_config():
    """Tải và trả về toàn bộ cấu hình của chatbot."""
    # ... (Toàn bộ dữ liệu CONFIG chi tiết của bạn được đặt ở đây) ...
    return {
        "ui": { "title": "Bạn đồng hành 💖", "input_placeholder": "Nhập tin nhắn..." },
        "emojis": { "vui": "😄", "buồn": "😔", "tức giận": "😡", "tủi thân": "🥺", "khóc": "😭", "mắc ói": "🤢", "bất ngờ": "😮", "hy vọng": "🙏" },
        "tam_su": {
            "intro_message": "Hôm nay bạn cảm thấy như thế nào nè? Mình luôn sẵn lòng lắng nghe bạn nha 🌟",
            "positive_affirmation_trigger": "🌼 Nghe một lời tích cực",
            "positive_affirmations": [
                "Bạn mạnh mẽ hơn bạn nghĩ rất nhiều.", "Mỗi bước nhỏ bạn đi đều là một thành công lớn.",
                "Cảm xúc của bạn là thật và đáng được tôn trọng.", "Bạn xứng đáng được yêu thương và hạnh phúc.",
                "Hôm nay có thể khó khăn, nhưng ngày mai sẽ tốt hơn."
            ],
            "moods": {
                "😄 Vui": {"keywords": ["vui","dzui","vuii","hạnh phúc","hp","sướng","phấn khích","tuyệt vời","awesome","perfect","quá đã","tự hào","phấn khởi","hào hứng","hớn hở","proud","giỏi","10 điểm","đậu rồi","thành công","đi chơi","picnic","nhận thưởng","được khen", "😄"],"initial": "Tuyệt vời quá! Có chuyện gì vui không, kể mình nghe với nè!","styles": { "Hứng thú & Khuyến khích": ["Nghe là thấy vui giùm bạn luôn á! Kể thêm chút nữa đi!", "Hôm nay chắc là một ngày đặc biệt với bạn đúng không? Chia sẻ cho mình với nhé!"], "Khen ngợi & Khẳng định": ["Wow, bạn làm tốt lắm luôn đó! Mình tự hào về bạn ghê á!", "Bạn giỏi thật sự đó! Những nỗ lực của bạn đã được đền đáp xứng đáng rồi nè."], "Đồng hành & Vui chung": ["Mình rất vui cùng bạn. Bạn muốn chia sẻ thêm gì nữa không?", "Mình cảm nhận được niềm vui của bạn luôn á! Cảm xúc tích cực này truyền năng lượng lắm."], "Lan tỏa niềm vui": ["Bạn muốn làm gì để ăn mừng không? Kể mình nghe để cùng lên kế hoạch vui nè!", "Niềm vui này mà lan sang người khác nữa thì tuyệt vời luôn á!"] }},
                "😔 Buồn": {"keywords": ["buồn","chán","thất vọng","stress","áp lực","cô đơn","nhớ nhà","tệ","bad day","xui xẻo","tụt mood", "😔"],"initial": "Ôi, mình nghe rồi nè, có chuyện gì làm bạn buồn vậy?","styles": { "Lắng nghe nhẹ nhàng": ["Không sao đâu, bạn buồn cũng được mà. Có chuyện gì khiến bạn buồn không?", "Bạn không cần phải vui vẻ suốt ngày đâu. Chỉ cần bạn biết mình đang không ổn – là đã mạnh mẽ rồi đó."], "Khích lệ suy ngẫm": ["Bạn có biết điều gì khiến bạn thấy tụt mood hôm nay không?", "Nếu bạn có thể làm điều gì để cảm thấy nhẹ lòng hơn, bạn sẽ làm gì đầu tiên?"], "Đồng hành & Thấu hiểu": ["Mình từng trải qua những ngày thấy hơi tệ như vậy, nên mình hiểu lắm.", "Bạn không cần phải gồng lên tỏ ra ổn. Cứ là chính mình thôi, và mình luôn bên bạn."], "Hành động nhẹ": ["Bạn muốn thử cùng mình viết ra 3 điều nhỏ làm bạn thấy ổn hơn không? Có thể là trà sữa, mèo, hay ngủ nướng chẳng hạn.", "Hay mình kể cho bạn một chuyện vui nhẹ nhàng nha?"] }},
                "😢 Tủi thân": {"keywords": ["tủi thân","bị bỏ rơi","bị lãng quên","không ai hiểu","thiếu quan tâm","bị coi thường","bị cô lập","thấy mình kém cỏi","trách oan", "🥺", "😭"],"initial": "Tớ hiểu, cảm giác tủi thân không vui chút nào. Kể tớ nghe nha, mình ở đây rồi.","styles": { "Lắng nghe & Vỗ về": ["Bạn không cô đơn đâu. Mình luôn sẵn lòng lắng nghe bạn nè.", "Bạn đã rất mạnh mẽ khi chia sẻ cảm xúc đó. Mình ở đây và sẵn sàng lắng nghe."], "Khích lệ suy ngẫm": ["Có điều gì đã khiến bạn tổn thương hôm nay? Nói ra có thể nhẹ lòng hơn đó.", "Nếu bạn có thể nói điều gì với người làm bạn tổn thương, bạn θα nói gì?"], "Đồng hành & Thấu hiểu": ["Không có ai đáng phải cảm thấy như ‘người vô hình’ cả. Mình thấy bạn, thật sự thấy bạn.", "Những giọt nước mắt của bạn không hề yếu đuối – đó là sức mạnh của sự chân thật."], "Hành động nhẹ": ["Bạn muốn cùng mình viết một lá thư (dù không gửi) cho người làm bạn tổn thương không?", "Hay thử một điều nho nhỏ dễ thương giúp bạn xoa dịu bản thân – như xem ảnh mèo hoặc tô màu?"] }},
                "😡 Tức giận": {"keywords": ["tức","giận","bực mình","khó chịu","điên","phát cáu","ức chế","bất công","bị ép", "😡"],"initial": "Giận dữ làm mình khó chịu lắm. Bạn kể ra đi, đỡ hơn nhiều đó!","styles": { "Xác nhận cảm xúc": ["Cảm xúc của bạn là thật và hoàn toàn có lý. Đừng ngại chia sẻ nha.", "Cảm giác bị ép hay không được tôn trọng dễ làm mình bùng nổ. Mình ở đây để lắng nghe bạn."], "Làm dịu cảm xúc": ["Mình thử hít sâu 3 lần nhé. Hít vào, thở ra... Rồi nói tiếp với mình nha.", "Bạn có muốn thử viết ra hết mấy điều làm bạn tức? Mình đọc cho."], "Khơi gợi suy ngẫm": ["Điều gì khiến bạn cảm thấy bị ép buộc hay mất quyền lựa chọn?", "Nếu bạn được nói thật lòng với người làm bạn bực, bạn muốn nói gì?"], "Định hướng hành động": ["Khi mình tức, mình hay vẽ nguệch ngoạc cho dịu lại. Bạn muốn thử không?", "Bạn có muốn chọn một emoji thể hiện đúng cảm xúc bạn đang có không?"] }},
                "😴 Mệt mỏi": {"keywords": ["mệt", "kiệt sức", "hết pin", "đuối", "nhức đầu", "căng thẳng", "buồn ngủ", "stress", "hết năng lượng", "quá sức"],"initial": "Hôm nay bạn có vẻ mệt. Hít thở sâu nào, rồi kể tiếp cho mình nghe nha.","styles": { "Lắng nghe": ["Bạn cần nghỉ ngơi một chút đó. Mình luôn ở đây nếu cần.", "Nếu không muốn nói gì cũng không sao. Mình chờ bạn."], "Khơi gợi": ["Bạn nghĩ vì sao lại mệt đến vậy?", "Có điều gì nhỏ bạn nghĩ giúp bạn thư giãn không?"], "Thư giãn": ["Bạn muốn gợi ý hoạt động nhẹ giúp thư giãn không?", "Hay thử nhắm mắt 1 phút, hít thở chậm nhé?"] }},
                "🤔 Vô định": {"keywords": ["vô định", "mông lung", "lạc lõng", "trống rỗng", "vô nghĩa", "mơ hồ", "chênh vênh", "không biết làm gì"],"initial": "Đôi khi cảm thấy trống rỗng là dấu hiệu bạn cần kết nối lại với bản thân.","styles": { "Lắng nghe": ["Bạn muốn nói thêm về điều này không? Mình lắng nghe.", "Mình ở đây, bạn cứ thoải mái chia sẻ."], "Suy ngẫm": ["Bạn nghĩ vì sao cảm giác này xuất hiện?", "Bạn mong điều gì nhất lúc này?"], "Hành động nhẹ": ["Bạn có muốn thử viết một câu miêu tả cảm xúc của mình hiện tại không?", "Nếu bạn muốn, mình có thể gửi một vài câu hỏi gợi ý để bạn khám phá bản thân."] }},
                "💔 Buồn vì mối quan hệ": {"keywords": ["bạn bỏ rơi", "bị hiểu lầm", "phản bội", "tổn thương", "thất vọng vì bạn", "cãi nhau", "bị lợi dụng", "mất lòng tin"],"initial": "Tớ nghe bạn nè. Buồn vì mối quan hệ thật khó chịu. Bạn muốn kể rõ hơn không?","styles": { "Lắng nghe": ["Bạn cứ nói thật lòng, mình ở đây để nghe.", "Mình luôn ở đây và thấu hiểu bạn."], "Khơi gợi": ["Bạn nghĩ điều gì khiến mối quan hệ thay đổi?", "Bạn mong điều gì nhất từ người ấy?"], "Hành động": ["Bạn muốn thử viết thư để xả giận không?", "Hay cùng nhau nghĩ hoạt động giúp bạn dễ chịu hơn?"] }},
                "😐 Bình thường": {"keywords": ["bình thường","bt","ổn","ok","tạm ổn","vô vị","lửng lơ","chẳng biết","như mọi ngày","không có gì"],"initial": "Vậy là một ngày bình yên. Nếu có gì muốn kể, mình nghe nè.","styles": { "Lắng nghe & Chấp nhận": ["Không có gì cũng không sao hết. Mình vẫn ở đây nếu bạn muốn nói gì thêm nha.", "Đôi khi không rõ cảm xúc cũng là chuyện thường mà."], "Khích lệ suy ngẫm": ["Bạn nghĩ vì sao hôm nay cảm giác lại lửng lơ như vậy nè?", "Nếu bạn được thay đổi một điều trong ngày hôm nay, bạn sẽ chọn điều gì?"], "Hành động nhẹ": ["Bạn có muốn thử làm một điều nhỏ vui vui hôm nay không? Mình có vài gợi ý nè!", "Mình có một câu hỏi vui nè: nếu bạn được chọn một siêu năng lực ngay bây giờ, bạn muốn có gì?"] }}
            }
        },
        "giao_tiep": {
            "intro_message": "Hãy chọn một tình huống bên dưới để mình cùng luyện tập nhé!",
            "confirm_buttons": {"understood": "✅ Đã hiểu rồi!", "not_understood": "❓ Chưa rõ lắm!"},
            "scenarios_basic": {
                "👋 Chào hỏi bạn bè": {"text": "Bạn có thể nói: ‘Chào bạn, hôm nay vui không?’ Hoặc: ‘Tớ chào cậu nha, hôm nay học tốt không nè?’", "image_url": "https://i.imgur.com/N52udBf.png"},
                "🙋 Hỏi bài thầy cô": {"text": "Bạn thử hỏi thầy/cô như vầy nha: ‘Thầy/cô ơi, em chưa hiểu phần này, thầy/cô giảng lại giúp em được không ạ?’", "image_url": "https://i.imgur.com/gZ10T7k.png"},
                "🧑‍🤝‍🧑 Làm quen bạn mới": {"text": "Bạn có thể bắt đầu bằng: ‘Xin chào, tớ là A, còn bạn tên gì?’ Hoặc: ‘Mình mới vào lớp, cậu có thể chỉ mình vài điều không?’", "image_url": "https://i.imgur.com/kSj9j4s.png"},
                "🙌 Xin lỗi": {"text": "Khi làm bạn buồn, bạn có thể nói: ‘Xin lỗi nha, mình không cố ý đâu.’ hoặc ‘Mình buồn vì đã làm bạn không vui, mong bạn tha lỗi.’", "image_url": "https://i.imgur.com/S6M9aed.png"},
                "🎉 Chúc mừng bạn": {"text": "Bạn có thể nói: ‘Chúc mừng nha, bạn làm tốt lắm!’ hoặc ‘Tuyệt vời quá, mình rất vui cho bạn!’", "image_url": "https://i.imgur.com/e2a8m3d.png"}
            },
            "scenarios_extended": {
                "📚 Nhờ bạn giúp đỡ": {"text": "Bạn thử nói: ‘Cậu giúp mình bài tập này nha, mình chưa hiểu lắm.’ Hoặc: ‘Bạn chỉ mình cách làm phần này với được không?’", "image_url": "https://i.imgur.com/y1C64gq.png"},
                "🕒 Xin phép ra ngoài": {"text": "Bạn có thể nói: ‘Thầy/cô ơi, em xin phép ra ngoài một lát ạ.’ hoặc ‘Em xin phép đi vệ sinh ạ.’", "image_url": "https://i.imgur.com/lJqf2jQ.png"},
                "😔 Nói về việc không vui": {"text": "Bạn có thể nói: ‘Mình hơi buồn hôm nay, cậu có thể trò chuyện với mình một chút không?’", "image_url": "https://i.imgur.com/gR1Yw8C.png"},
                "🧑‍🏫 Cảm ơn thầy cô": {"text": "Bạn có thể nói: ‘Em cảm ơn thầy/cô đã giúp em hiểu bài hơn ạ.’", "image_url": "https://i.imgur.com/1aA2d2t.png"},
                "🏅 Khen": {"text": "Bạn thử nói: ‘Thầy/cô dạy hay lắm ạ.’ hoặc ‘Bạn giỏi ghê á, tớ học hỏi được nhiều từ bạn.’", "image_url": "https://i.imgur.com/o2kZJtG.png"}
            }
        },
        "general": {
            "neutral_replies": [ "Mình chưa hiểu rõ lắm, bạn có thể chia sẻ cụ thể hơn một chút không?", "Cảm ơn bạn đã chia sẻ. Mình sẽ cố gắng hiểu bạn nhiều hơn. Bạn có muốn nói rõ hơn một chút không?", "Mình đang nghe bạn nè, bạn muốn nói thêm điều gì không?" ],
            "follow_up_prompt": "Bạn muốn tiếp tục tâm sự với mình, hay muốn thực hành nói chuyện trong lớp nè?",
            "end_chat_replies": [ "Cảm ơn bạn đã chia sẻ với mình hôm nay nha. Mình luôn sẵn sàng khi bạn cần đó 💖", "Bạn đã làm rất tốt khi chia sẻ cảm xúc của mình. Khi nào cần, mình vẫn luôn ở đây nha 💫", "Trò chuyện cùng bạn làm mình thấy rất vui. Nếu có điều gì cần tâm sự nữa, đừng ngại nói với mình nha 🫶" ]
        }
    }
CONFIG = get_config()

# --- 2. THIẾT LẬP GIAO DIỆN & CSS ---
st.set_page_config(page_title=CONFIG["ui"]["title"], layout="wide")
st.markdown(r"""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background-color: #FFFFFF; }
    .chat-container { position: fixed; top: 60px; left: 0; right: 0; bottom: 150px; overflow-y: auto; padding: 1rem; }
    .bot-message-container, .user-message-container { display: flex; margin: 5px 0; }
    .user-message-container { justify-content: flex-end; }
    .bot-message, .user-message { padding: 10px 15px; border-radius: 20px; max-width: 75%; font-size: 1rem; line-height: 1.5; }
    .bot-message { background: #F0F2F5; color: #1E1E1E; border-radius: 20px 20px 20px 5px; }
    .user-message { background: #E5E5EA; color: #1E1E1E; border-radius: 20px 20px 5px 20px; }
    .footer-fixed { position: fixed; bottom: 0; left: 0; right: 0; background: #FFFFFF; box-shadow: 0 -2px 5px rgba(0,0,0,0.05); padding: 10px 15px; z-index: 1000; }
    .buttons-and-input-container { display: flex; flex-direction: column; gap: 10px; }
    .horizontal-buttons-container { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
    .horizontal-buttons-container .stButton button { padding: 8px 16px; border: 1px solid #0084FF; background: #E7F3FF; color: #0084FF; border-radius: 20px; font-size: 0.95rem; font-weight: 500; transition: all 0.2s; }
    .horizontal-buttons-container .stButton button:hover { background: #0084FF; color: white; }
    .input-container { display: flex; align-items: center; gap: 10px; }
    .stTextInput { flex-grow: 1; }
    .stTextInput > div > div > input { border-radius: 25px; border: 1px solid #CDD1D9; padding: 0.75rem 1rem; background-color: #F0F2F6; }
    .emoji-palette { display: flex; gap: 15px; justify-content: center; padding: 5px 0; }
    .emoji-palette button { background: none; border: none; font-size: 1.75rem; cursor: pointer; transition: transform 0.2s; }
    .emoji-palette button:hover { transform: scale(1.2); }
    .typing-indicator span { height: 8px; width: 8px; margin: 0 2px; background-color: #9E9E9E; display: inline-block; border-radius: 50%; opacity: 0.4; animation: bob 1s infinite; }
    @keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
    .typing-indicator span:nth-child(1) { animation-delay: -0.3s; }
    .typing-indicator span:nth-child(2) { animation-delay: -0.15s; }
    .scenario-card { border: 1px solid #EAEAEA; border-radius: 12px; padding: 1rem; text-align: center; transition: all 0.2s; height: 100%; display: flex; flex-direction: column; justify-content: space-between; background-color: #FAFAFA; }
    .scenario-card:hover { border-color: #0084FF; box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-2px); }
    .scenario-card img { max-height: 50px; margin-bottom: 10px; object-fit: contain; }
    .scenario-card .stButton button { background-color: white; width: 100%; border: 1px solid #0084FF; }
</style>
""", unsafe_allow_html=True)


# --- 3. KHỞI TẠO SESSION STATE ---
if "state" not in st.session_state:
    st.session_state.state = STATE_MAIN
    st.session_state.history = [{"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}]
    st.session_state.turns = 0
    st.session_state.current_mood = None
    st.session_state.current_scenario = None
    st.session_state.show_emojis = False
    st.session_state.user_input = ""


# --- 4. CÁC HÀM TIỆN ÍCH & LOGIC ---

# NEW: Hàm chuyển văn bản thành giọng nói và tự động phát
@st.cache_data
def text_to_speech(text):
    """Chuyển văn bản thành dữ liệu âm thanh."""
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi')
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        print(f"Lỗi gTTS: {e}")
        return None

def autoplay_audio(audio_data: bytes):
    """Tạo một trình phát âm thanh ẩn và tự động chạy."""
    try:
        b64 = base64.b64encode(audio_data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        print(f"Lỗi phát âm thanh: {e}")

def stream_response_generator(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

def add_message(sender, text):
    st.session_state.history.append({"sender": sender, "text": text})

def set_state(state, **kwargs):
    st.session_state.state = state
    for key, value in kwargs.items():
        st.session_state[key] = value

def detect_mood_from_text(text):
    lowered_text = text.lower()
    user_words = set(re.findall(r'\b\w+\b', lowered_text))
    user_words.update(char for char in text if char in CONFIG["emojis"].values())
    matched_mood, max_matches = None, 0
    for mood, config in CONFIG["tam_su"]["moods"].items():
        matches = len(user_words.intersection(set(config['keywords'])))
        if matches > max_matches:
            max_matches, matched_mood = matches, mood
    return matched_mood


# --- 5. CÁC HÀM CALLBACK ---
def main_button_callback(action):
    if action == "tam_su":
        add_message("user", "Mình muốn tâm sự")
        set_state(STATE_TAM_SU_SELECTION)
        st.session_state.next_bot_response = CONFIG["tam_su"]["intro_message"]
    elif action == "giao_tiep":
        add_message("user", "Mình muốn luyện tập giao tiếp")
        set_state(STATE_GIAO_TIEP_SELECTION_BASIC)
        st.session_state.next_bot_response = CONFIG["giao_tiep"]["intro_message"]

def mood_selection_callback(mood):
    add_message("user", mood)
    set_state(STATE_TAM_SU_CHAT, current_mood=mood, turns=0)
    st.session_state.next_bot_response = CONFIG["tam_su"]["moods"][mood]["initial"]

def scenario_selection_callback(scenario_title):
    add_message("user", f"Luyện tập: {scenario_title}")
    scenario_data = CONFIG["giao_tiep"]["scenarios_basic"].get(scenario_title) or CONFIG["giao_tiep"]["scenarios_extended"].get(scenario_title)
    set_state(STATE_GIAO_TIEP_PRACTICE, current_scenario=scenario_title)
    st.session_state.next_bot_response = scenario_data["text"]

def practice_button_callback(action):
    if action == "understood":
        add_message("user", CONFIG["giao_tiep"]["confirm_buttons"]["understood"])
        set_state(STATE_GIAO_TIEP_SELECTION_EXTENDED)
        st.session_state.next_bot_response = "Tuyệt vời! Bạn làm tốt lắm. Giờ mình cùng xem qua các tình huống mở rộng nhé!"
    else: # not_understood
        add_message("user", CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"])
        scenario_title = st.session_state.current_scenario
        scenario_data = CONFIG["giao_tiep"]["scenarios_basic"].get(scenario_title) or CONFIG["giao_tiep"]["scenarios_extended"].get(scenario_title)
        st.session_state.next_bot_response = f"Không sao cả, mình nói lại nhé:\n\n{scenario_data['text']}"

def end_chat_callback():
    set_state(STATE_MAIN)
    st.session_state.next_bot_response = random.choice(CONFIG["general"]["end_chat_replies"])

def positive_affirmation_callback():
    add_message("user", CONFIG["tam_su"]["positive_affirmation_trigger"])
    set_state(STATE_MAIN)
    st.session_state.next_bot_response = random.choice(CONFIG["tam_su"]["positive_affirmations"])

def user_input_callback():
    user_text = st.session_state.get("user_input", "")
    if not user_text: return
    add_message("user", user_text)
    st.session_state.turns += 1
    if st.session_state.state == STATE_TAM_SU_CHAT:
        mood = st.session_state.current_mood
        response_text = random.choice(sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), []))
        if st.session_state.turns >= 2:
            set_state(STATE_AWAITING_FOLLOWUP)
            st.session_state.next_bot_response = f"{response_text} {CONFIG['general']['follow_up_prompt']}"
        else:
            st.session_state.next_bot_response = response_text
    else:
        detected_mood = detect_mood_from_text(user_text)
        if detected_mood:
            set_state(STATE_TAM_SU_CHAT, current_mood=detected_mood, turns=0)
            st.session_state.next_bot_response = CONFIG["tam_su"]["moods"][detected_mood]["initial"]
        else:
            set_state(STATE_AWAITING_FOLLOWUP)
            st.session_state.next_bot_response = random.choice(CONFIG["general"]["neutral_replies"])
    st.session_state.user_input = ""


# --- 6. VẼ GIAO DIỆN CHÍNH ---
st.markdown(f"<h1 style='color: #1E1E1E; text-align: center; position: fixed; top: 0; left: 0; right: 0; background: #FFFFFF; z-index: 999; padding: 5px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>{CONFIG['ui']['title']}</h1>", unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.history:
        sender_class = "user-message-container" if message["sender"] == "user" else "bot-message-container"
        message_class = "user-message" if message["sender"] == "user" else "bot-message"
        escaped_text = html.escape(message['text'])
        st.markdown(f"<div class='{sender_class}'><div class='{message_class}'>{escaped_text}</div></div>", unsafe_allow_html=True)

    if "next_bot_response" in st.session_state:
        bot_response_text = st.session_state.pop("next_bot_response")
        
        # NEW: Tạo và phát âm thanh trước khi hiển thị tin nhắn
        audio_data = text_to_speech(bot_response_text)
        if audio_data:
            autoplay_audio(audio_data)

        bot_message_placeholder = st.empty()
        indicator_html = "<div class='bot-message-container'><div class='bot-message typing-indicator'><span></span><span></span><span></span></div></div>"
        bot_message_placeholder.markdown(indicator_html, unsafe_allow_html=True)
        time.sleep(0.5)
        
        full_response_html = ""
        for chunk in stream_response_generator(bot_response_text):
            full_response_html += chunk
            escaped_chunk = html.escape(full_response_html)
            styled_html = f"<div class='bot-message-container'><div class='bot-message'>{escaped_chunk}</div></div>"
            bot_message_placeholder.markdown(styled_html, unsafe_allow_html=True)
        
        add_message("bot", bot_response_text)

    st.markdown("</div>", unsafe_allow_html=True)


# --- 7. VẼ THANH FOOTER VÀ CÁC NÚT BẤM ---
footer = st.container()
with footer:
    st.markdown("<div class='footer-fixed'>", unsafe_allow_html=True)
    st.markdown("<div class='buttons-and-input-container'>", unsafe_allow_html=True)
    
    def render_scenario_cards(scenarios):
        num_columns = 5
        scenario_items = list(scenarios.items())
        for i in range(0, len(scenario_items), num_columns):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                if i + j < len(scenario_items):
                    with cols[j]:
                        title, data = scenario_items[i+j]
                        with st.container():
                            st.markdown(f"<div class='scenario-card'>", unsafe_allow_html=True)
                            st.image(data["image_url"], width=64)
                            st.button(title, key=f"btn_{title}", on_click=scenario_selection_callback, args=(title,), use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
    
    state = st.session_state.state

    if state == STATE_GIAO_TIEP_SELECTION_BASIC:
        render_scenario_cards(CONFIG["giao_tiep"]["scenarios_basic"])
    elif state == STATE_GIAO_TIEP_SELECTION_EXTENDED:
        render_scenario_cards(CONFIG["giao_tiep"]["scenarios_extended"])
    else:
        st.markdown("<div class='horizontal-buttons-container'>", unsafe_allow_html=True)
        if state in [STATE_MAIN, STATE_AWAITING_FOLLOWUP]:
            st.button("💖 Tâm sự", on_click=main_button_callback, args=("tam_su",))
            st.button("🗣️ Giao tiếp", on_click=main_button_callback, args=("giao_tiep",))
        elif state == STATE_TAM_SU_SELECTION:
            moods = list(CONFIG["tam_su"]["moods"].keys())
            cols = st.columns(len(moods))
            for i, mood in enumerate(moods):
                with cols[i]:
                    st.button(mood, on_click=mood_selection_callback, args=(mood,), use_container_width=True)
        elif state == STATE_TAM_SU_CHAT:
            st.button(CONFIG["tam_su"]["positive_affirmation_trigger"], on_click=positive_affirmation_callback)
            st.button("🏁 Kết thúc", on_click=end_chat_callback)
        elif state == STATE_GIAO_TIEP_PRACTICE:
            buttons_cfg = CONFIG["giao_tiep"]["confirm_buttons"]
            st.button(buttons_cfg["understood"], on_click=practice_button_callback, args=("understood",))
            st.button(buttons_cfg["not_understood"], on_click=practice_button_callback, args=("not_understood",))
            st.button("Dừng nhé", on_click=end_chat_callback)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.text_input("Input", placeholder=CONFIG["ui"]["input_placeholder"], key="user_input", on_change=user_input_callback, label_visibility="collapsed")
    if col2.button("😊", key="toggle_emoji", help="Chọn biểu cảm nhanh"):
        st.session_state.show_emojis = not st.session_state.get('show_emojis', False)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)