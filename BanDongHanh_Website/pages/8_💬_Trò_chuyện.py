import streamlit as st
import random
import re
import time
import html
import database as db
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

user_id = st.session_state.user_id
user_name = st.session_state.user_name

# --- BỘ LỌC TỪ KHÓA NGUY HIỂM ---
CRISIS_KEYWORDS = [
    "tự tử", "tự sát", "kết liễu", "chấm dứt", "không muốn sống",
    "muốn chết", "kết thúc tất cả", "làm hại bản thân", "tự làm đau",
    "tuyệt vọng", "vô vọng", "không còn hy vọng"
]

# --- CÁC HẰNG SỐ VÀ CẤU HÌNH ---
CHAT_STATE_MAIN = 'main'
CHAT_STATE_TAM_SU_SELECTION = 'tam_su_selection'
CHAT_STATE_TAM_SU_CHAT = 'tam_su_chat'
CHAT_STATE_GIAO_TIEP_SELECTION_BASIC = 'giao_tiep_selection_basic'
CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED = 'giao_tiep_selection_extended'
CHAT_STATE_GIAO_TIEP_PRACTICE = 'giao_tiep_practice'
CHAT_STATE_AWAITING_FOLLOWUP = 'awaiting_followup'

@st.cache_data
def get_config():
    # (Toàn bộ config của bạn được giữ nguyên)
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
                "😢 Tủi thân": {"keywords": ["tủi thân","bị bỏ rơi","bị lãng quên","không ai hiểu","thiếu quan tâm","bị coi thường","bị cô lập","thấy mình kém cỏi","trách oan", "🥺", "😭"],"initial": "Tớ hiểu, cảm giác tủi thân không vui chút nào. Kể tớ nghe nha, mình ở đây rồi.","styles": { "Lắng nghe & Vỗ về": ["Bạn không cô đơn đâu. Mình luôn sẵn lòng lắng nghe bạn nè.", "Bạn đã rất mạnh mẽ khi chia sẻ cảm xúc đó. Mình ở đây và sẵn sàng lắng nghe."], "Khích lệ suy ngẫm": ["Có điều gì đã khiến bạn tổn thương hôm nay? Nói ra có thể nhẹ lòng hơn đó.", "Nếu bạn có thể nói điều gì với người làm bạn tổn thương, bạn sẽ nói gì?"], "Đồng hành & Thấu hiểu": ["Không có ai đáng phải cảm thấy như ‘người vô hình’ cả. Mình thấy bạn, thật sự thấy bạn.", "Những giọt nước mắt của bạn không hề yếu đuối – đó là sức mạnh của sự chân thật."], "Hành động nhẹ": ["Bạn muốn cùng mình viết một lá thư (dù không gửi) cho người làm bạn tổn thương không?", "Hay thử một điều nho nhỏ dễ thương giúp bạn xoa dịu bản thân – như xem ảnh mèo hoặc tô màu?"] }},
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
                "👋 Chào hỏi bạn bè": "Bạn có thể nói: ‘Chào bạn, hôm nay vui không?’ Hoặc: ‘Tớ chào cậu nha, hôm nay học tốt không nè?’",
                "🙋 Hỏi bài thầy cô": "Bạn thử hỏi thầy/cô như vầy nha: ‘Thầy/cô ơi, em chưa hiểu phần này, thầy/cô giảng lại giúp em được không ạ?’",
                "🧑‍🤝‍🧑 Làm quen bạn mới": "Bạn có thể bắt đầu bằng: ‘Xin chào, tớ là A, còn bạn tên gì?’ Hoặc: ‘Mình mới vào lớp, cậu có thể chỉ mình vài điều không?’",
                "🙌 Xin lỗi": "Khi làm bạn buồn, bạn có thể nói: ‘Xin lỗi nha, mình không cố ý đâu.’ hoặc ‘Mình buồn vì đã làm bạn không vui, mong bạn tha lỗi.’",
                "🎉 Chúc mừng bạn": "Bạn có thể nói: ‘Chúc mừng nha, bạn làm tốt lắm!’ hoặc ‘Tuyệt vời quá, mình rất vui cho bạn!’"
            },
            "scenarios_extended": {
                "📚 Nhờ bạn giúp đỡ": "Bạn thử nói: ‘Cậu giúp mình bài tập này nha, mình chưa hiểu lắm.’ Hoặc: ‘Bạn chỉ mình cách làm phần này với được không?’",
                "🕒 Xin phép ra ngoài": "Bạn có thể nói: ‘Thầy/cô ơi, em xin phép ra ngoài một lát ạ.’ hoặc ‘Em xin phép đi vệ sinh ạ.’",
                "😔 Nói về việc không vui": "Bạn có thể nói: ‘Mình hơi buồn hôm nay, cậu có thể trò chuyện với mình một chút không?’",
                "🧑‍🏫 Cảm ơn thầy cô": "Bạn có thể nói: ‘Em cảm ơn thầy/cô đã giúp em hiểu bài hơn ạ.’",
                "🏅 Khen": "Bạn thử nói: ‘Thầy/cô dạy hay lắm ạ.’ hoặc ‘Bạn giỏi ghê á, tớ học hỏi được nhiều từ bạn.’"
            }
        },
        "general": {
            "neutral_replies": [ "Mình chưa hiểu rõ lắm, bạn có thể chia sẻ cụ thể hơn một chút không?", "Cảm ơn bạn đã chia sẻ. Mình sẽ cố gắng hiểu bạn nhiều hơn. Bạn có muốn nói rõ hơn một chút không?", "Mình đang nghe bạn nè, bạn muốn nói thêm điều gì không?" ],
            "follow_up_prompt": "Bạn muốn tiếp tục tâm sự với mình, hay muốn thực hành nói chuyện trong lớp nè?",
            "end_chat_replies": [ "Cảm ơn bạn đã chia sẻ với mình hôm nay nha. Mình luôn sẵn sàng khi bạn cần đó 💖", "Bạn đã làm rất tốt khi chia sẻ cảm xúc của mình. Khi nào cần, mình vẫn luôn ở đây nha 💫", "Trò chuyện cùng bạn làm mình thấy rất vui. Nếu có điều gì cần tâm sự nữa, đừng ngại nói với mình nha 🫶" ]
        }
    }
CONFIG = get_config()

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False

st.set_page_config(page_title=CONFIG["ui"]["title"], layout="wide")
st.markdown(r"""<style>...</style>""", unsafe_allow_html=True) # Giữ nguyên CSS của bạn

# --- KHỞI TẠO VÀ TẢI DỮ LIỆU ---
if "chat_initialized" not in st.session_state:
    st.session_state.chat_state = CHAT_STATE_MAIN
    st.session_state.history = db.get_chat_history(user_id)
    if not st.session_state.history:
        initial_message = f"Chào {user_name}, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"
        st.session_state.history = [{"sender": "bot", "text": initial_message}]
        db.add_chat_message(user_id, "bot", initial_message)
    st.session_state.turns = 0
    st.session_state.current_mood = None
    st.session_state.current_scenario = None
    st.session_state.user_input = ""
    st.session_state.chat_initialized = True

# --- CÁC HÀM TIỆN ÍCH ---
def check_for_crisis(text):
    lowered_text = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in lowered_text:
            return True
    return False

def render_crisis_response():
    st.error("...") # Giữ nguyên nội dung thông báo khẩn cấp của bạn
    st.stop()

def add_message_and_save(sender, text):
    st.session_state.history.append({"sender": sender, "text": text})
    db.add_chat_message(user_id, sender, text)

# (Các hàm tiện ích cũ của bạn được giữ nguyên)
@st.cache_data
def text_to_speech(text):
    try:
        audio_bytes = BytesIO(); tts = gTTS(text=text, lang='vi'); tts.write_to_fp(audio_bytes); audio_bytes.seek(0); return audio_bytes.read()
    except Exception: return None
def autoplay_audio(audio_data: bytes):
    try:
        b64 = base64.b64encode(audio_data).decode(); md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'; st.components.v1.html(md, height=0)
    except Exception: pass
def stream_response_generator(text):
    for word in text.split(): yield word + " "; time.sleep(0.05)
def set_chat_state(state, **kwargs):
    st.session_state.chat_state = state;
    for key, value in kwargs.items(): st.session_state[key] = value
def detect_mood_from_text(text):
    # (Logic phát hiện cảm xúc của bạn giữ nguyên)
    return None
def call_gemini_with_memory(user_prompt):
    if not AI_ENABLED: return "Xin lỗi, tính năng AI hiện không khả dụng."
    context_history = db.get_chat_history(user_id, limit=10)
    system_prompt = f"Bạn là Chip, một AI thân thiện. Bạn đang nói chuyện với {user_name}. Hãy trả lời ngắn gọn."
    try:
        gemini_history = [{"role": "user" if msg["sender"] == "user" else "model", "parts": [msg["text"]]} for msg in context_history]
        chat = gemini_model.start_chat(history=gemini_history); response = chat.send_message(system_prompt + "\nCâu hỏi: " + user_prompt); return response.text
    except Exception as e: return f"Lỗi AI: {e}"

# --- CÁC HÀM CALLBACK ĐÃ SỬA LỖI ---
def main_chat_button_callback(action):
    add_message_and_save("user", action)
    if action == "Tâm sự":
        set_chat_state(CHAT_STATE_TAM_SU_SELECTION)
        st.session_state.next_bot_response = CONFIG["tam_su"]["intro_message"]
    elif action == "Giao tiếp":
        set_chat_state(CHAT_STATE_GIAO_TIEP_SELECTION_BASIC)
        st.session_state.next_bot_response = CONFIG["giao_tiep"]["intro_message"]

def mood_selection_callback(mood):
    add_message_and_save("user", mood)
    set_chat_state(CHAT_STATE_TAM_SU_CHAT, current_mood=mood, turns=0)
    st.session_state.next_bot_response = CONFIG["tam_su"]["moods"][mood]["initial"]

def scenario_selection_callback(scenario_title):
    add_message_and_save("user", f"Luyện tập: {scenario_title}")
    response_text = CONFIG["giao_tiep"]["scenarios_basic"].get(scenario_title) or CONFIG["giao_tiep"]["scenarios_extended"].get(scenario_title)
    set_chat_state(CHAT_STATE_GIAO_TIEP_PRACTICE, current_scenario=scenario_title)
    st.session_state.next_bot_response = response_text

def practice_button_callback(action):
    if action == "understood":
        add_message_and_save("user", CONFIG["giao_tiep"]["confirm_buttons"]["understood"])
        set_chat_state(CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED)
        st.session_state.next_bot_response = "Tuyệt vời! Bạn làm tốt lắm. Giờ mình cùng xem qua các tình huống mở rộng nhé!"
    else:
        add_message_and_save("user", CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"])
        scenario_title = st.session_state.current_scenario
        response_text = CONFIG["giao_tiep"]["scenarios_basic"].get(scenario_title) or CONFIG["giao_tiep"]["scenarios_extended"].get(scenario_title)
        st.session_state.next_bot_response = f"Không sao cả, mình nói lại nhé:\n\n{response_text}"

def end_chat_callback():
    set_chat_state(CHAT_STATE_MAIN)
    st.session_state.next_bot_response = random.choice(CONFIG["general"]["end_chat_replies"])

def positive_affirmation_callback():
    add_message_and_save("user", CONFIG["tam_su"]["positive_affirmation_trigger"])
    set_chat_state(CHAT_STATE_MAIN)
    st.session_state.next_bot_response = random.choice(CONFIG["tam_su"]["positive_affirmations"])

def user_input_callback():
    user_text = st.session_state.get("user_input", "")
    if not user_text: return
    
    if check_for_crisis(user_text):
        add_message_and_save("user", user_text)
        st.session_state.crisis_detected = True
        st.session_state.user_input = ""
        st.rerun()
        return

    add_message_and_save("user", user_text)
    st.session_state.turns += 1
    # ... (logic còn lại của hàm user_input_callback)

# --- GIAO DIỆN CHÍNH ---
st.title("💬 Trò chuyện cùng Bot")

if st.session_state.get('crisis_detected'):
    render_crisis_response()

def render_chat_ui():
    # (Toàn bộ code render_chat_ui của bạn được giữ nguyên)
    pass

render_chat_ui()
