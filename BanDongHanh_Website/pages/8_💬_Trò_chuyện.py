import streamlit as st
import time
from datetime import datetime, date, timedelta
from pathlib import Path
import json, io, base64, os
from typing import List, Dict, Any, Optional

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(page_title="Trò chuyện - Bạn Đồng Hành", page_icon="🤖", layout="wide")

# ================== HẰNG SỐ & CẤU HÌNH ==================
SYSTEM_PROMPT = (
    "Bạn là 'Bạn Đồng Hành' – một trợ lý thân thiện, ấm áp, hỗ trợ cảm xúc. "
    "Không chẩn đoán y khoa. Giữ câu trả lời tự nhiên, khích lệ, dùng tiếng Việt gần gũi. "
    "Khi người dùng mô tả cảm xúc tiêu cực, hãy thừa nhận cảm xúc đó và gợi ý hành vi nhẹ nhàng. "
    "Tránh hứa hẹn tuyệt đối. Có thể đặt câu hỏi mở để họ chia sẻ thêm."
)

# Danh sách model ưu tiên (nếu có OpenAI)
MODEL_PREFERRED = [
    # Model đa phương thức (ảnh + văn bản)
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
    # Model text fallback
    "gpt-3.5-turbo"
]

MEMORY_DIR = Path("data")
MEMORY_DIR.mkdir(exist_ok=True)
MEMORY_FILE = MEMORY_DIR / "memory_chat.json"

# Ngưỡng cập nhật bộ nhớ (số message user+assistant)
MEMORY_UPDATE_INTERVAL = 12

# ================== KHỞI TẠO SESSION STATE ==================
def _init_state():
    defaults = {
        "chat_history": [],   # list[ {role, content, time, images?} ]
        "theme": "light",
        "show_suggestions": True,
        "pending_user_msg": None,
        "fullscreen": False,
        "memory_summary": "",
        "memory_version": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ================== HÀM BỘ NHỚ DÀI HẠN (MEMORY) ==================
def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            st.session_state.memory_summary = data.get("summary", "")
            st.session_state.memory_version = data.get("version", 0)
        except Exception:
            st.session_state.memory_summary = ""
            st.session_state.memory_version = 0
    else:
        st.session_state.memory_summary = ""
        st.session_state.memory_version = 0

def save_memory():
    out = {
        "summary": st.session_state.memory_summary,
        "version": st.session_state.memory_version,
        "updated_at": datetime.now().isoformat()
    }
    MEMORY_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

load_memory()

# ================== CÔNG CỤ ƯỚC LƯỢNG TOKEN ĐƠN GIẢN ==================
def approximate_tokens(text: str) -> int:
    # Ước tính thô (1 token ~ 4 ký tự latin/tiếng Việt trung bình)
    return max(1, len(text) // 4)

def total_tokens_history(messages: List[Dict[str, Any]]) -> int:
    return sum(approximate_tokens(m["content"]) for m in messages)

# ================== HÀM TIỆN ÍCH CHAT ==================
def add_message(role: str, content: str, images: Optional[List[bytes]] = None):
    st.session_state.chat_history.append({
        "role": role,
        "content": content.strip(),
        "time": datetime.now(),
        "images": images or []
    })

def export_chat_txt() -> bytes:
    buf = io.StringIO()
    buf.write("=== LỊCH SỬ TRÒ CHUYỆN - Bạn Đồng Hành ===\n")
    if st.session_state.memory_summary:
        buf.write("\n--- TÓM TẮT BỘ NHỚ (LONG-TERM) ---\n")
        buf.write(st.session_state.memory_summary + "\n\n")
    for m in st.session_state.chat_history:
        ts = m["time"].strftime("%Y-%m-%d %H:%M")
        who = "Người dùng" if m["role"] == "user" else "Bạn Đồng Hành"
        buf.write(f"[{ts}] {who}: {m['content']}\n")
        if m.get("images"):
            buf.write(f"  (Đính kèm {len(m['images'])} ảnh)\n")
    return buf.getvalue().encode("utf-8")

def export_memory_txt() -> bytes:
    buf = io.StringIO()
    buf.write("=== BỘ NHỚ DÀI HẠN - Bạn Đồng Hành ===\n")
    buf.write("Version: " + str(st.session_state.memory_version) + "\n\n")
    buf.write(st.session_state.memory_summary or "(Trống)\n")
    return buf.getvalue().encode("utf-8")

# ================== HÀM PHÂN TÁCH NGÀY ==================
def format_day_separator(dt: datetime) -> str:
    d = dt.date()
    today = date.today()
    if d == today:
        return "HÔM NAY"
    if d == today - timedelta(days=1):
        return "HÔM QUA"
    return d.strftime("%d/%m/%Y").upper()

# ================== HỖ TRỢ ENCODE ẢNH ==================
def image_bytes_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")

# ================== TẠO YÊU CẦU MODEL (OPENAI HOẶC FALLBACK) ==================
def select_model():
    # Ở đây chỉ đơn giản trả về model đầu tiên có trong danh sách
    return MODEL_PREFERRED[0]

def call_openai_api(messages: List[Dict[str, Any]]) -> str:
    """
    Gọi OpenAI ChatCompletion (multi-modal nếu có ảnh).
    Yêu cầu: đặt OPENAI_API_KEY trong biến môi trường.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None  # báo để fallback

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception:
        return None

    model_name = select_model()

    # Xây dựng messages theo định dạng OpenAI
    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in messages:
        role = "assistant" if m["role"] == "assistant" else "user"
        # Nếu có ảnh -> nội dung multi-part
        if m.get("images"):
            parts = [{"type": "text", "text": m["content"]}]
            for img_b in m["images"]:
                b64 = image_bytes_to_base64(img_b)
                parts.append({
                    "type": "image",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64}"
                    }
                })
            openai_messages.append({"role": role, "content": parts})
        else:
            openai_messages.append({"role": role, "content": m["content"]})

    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=openai_messages,
            temperature=0.7,
            max_tokens=600,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Mình gặp chút sự cố khi gọi mô hình: {e}"

# ================== TÓM TẮT BỘ NHỚ (CÓ MODEL HOẶC FALLBACK) ==================
def summarize_history_for_memory(history: List[Dict[str, Any]], current_summary: str) -> str:
    """
    Nếu có OpenAI API -> dùng model để tóm tắt.
    Nếu không -> làm heuristic đơn giản.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    # Lấy tối đa 40 message gần nhất để tóm
    recent = history[-40:]
    raw_text = []
    if current_summary:
        raw_text.append("TÓM TẮT HIỆN TẠI:\n" + current_summary + "\n\nTHÊM NỘI DUNG MỚI:\n")
    for m in recent:
        prefix = "User:" if m["role"] == "user" else "AI:"
        raw_text.append(f"{prefix} {m['content']}")
    combined = "\n".join(raw_text)

    # Nếu có API -> dùng tóm tắt
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            model_name = select_model()
            prompt = (
                "Hãy cập nhật bản tóm tắt dài hạn ngắn gọn (dưới 180 từ) về người dùng/hoàn cảnh/cảm xúc/"
                "mục tiêu/thói quen. Không lặp lại chi tiết vụn vặt. "
                "Giữ giọng trung lập.\n\n"
                f"Nội dung:\n{combined}"
            )
            resp = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Bạn là công cụ tóm tắt."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            pass  # fallback heuristic

    # Heuristic đơn giản
    lines = [l for l in combined.splitlines() if l.strip()]
    # Lấy vài dòng tiêu biểu (cắt ngắn)
    out = []
    seen_user = 0
    for ln in reversed(lines):
        if ln.startswith("User:") and seen_user < 5:
            out.append(ln)
            seen_user += 1
    out = list(reversed(out))
    heuristic = "Tóm tắt (heuristic): " + " | ".join(
        l.replace("User:", "").strip() for l in out
    )
    if current_summary:
        heuristic = (current_summary[:400] + " ... ") + heuristic
    return heuristic[:900]

# ================== SINH TRẢ LỜI AI (KẾT HỢP MEMORY) ==================
def generate_ai_reply(user_input: str, images: Optional[List[bytes]] = None) -> str:
    # Gom lịch sử để gửi (kết hợp summary như context)
    working_history = []
    if st.session_state.memory_summary:
        working_history.append({
            "role": "assistant",
            "content": f"(TÓM TẮT BỐI CẢNH TRƯỚC ĐÓ: {st.session_state.memory_summary})",
            "time": datetime.now()
        })
    # Thêm lịch sử thực tế
    working_history.extend(st.session_state.chat_history)

    reply = call_openai_api(working_history + [{
        "role": "user",
        "content": user_input,
        "images": images or [],
        "time": datetime.now()
    }])

    if reply is None:  # fallback mô phỏng
        canned = [
            "Mình hiểu cảm xúc của bạn. Bạn có thể kể rõ hơn không? 💖",
            "Cảm ơn bạn đã chia sẻ. Điều đó không hề dễ dàng. 🌱",
            "Bạn đã cố gắng rất nhiều rồi, đừng quên dành thời gian nghỉ ngơi nhé. ✨",
            "Mình ở đây và lắng nghe bạn. Bạn muốn tiếp tục nói về điều gì? 💬"
        ]
        idx = len(user_input.strip()) % len(canned)
        reply = canned[idx]
    return reply.strip()

# ================== CSS (THÊM FULLSCREEN / DARK MODE) ==================
PRIMARY_GRADIENT = "linear-gradient(135deg,#ff82ac 0%,#fd5e7c 55%,#ff9e7b 100%)"
LIGHT_BG = "#f5f7fa"
DARK_BG = "#121417"

light_css = f"""
:root {{
  --bg-app: {LIGHT_BG};
  --bg-panel: #ffffff;
  --bg-bubble-user: #4f9cff;
  --bg-bubble-ai: #ffffff;
  --border-bubble: #e5e8ec;
  --text-primary: #1d232a;
  --text-secondary: #4a5562;
  --accent: #fd5e7c;
  --scroll-track: #f1f3f5;
  --scroll-thumb: #d2d8de;
}}
"""
dark_css = f"""
:root {{
  --bg-app: {DARK_BG};
  --bg-panel: #1d2329;
  --bg-bubble-user: #2563eb;
  --bg-bubble-ai: #27313a;
  --border-bubble: #2d353d;
  --text-primary: #e6ecf2;
  --text-secondary: #b6c2ce;
  --accent: #ff6b8a;
  --scroll-track: #1d2329;
  --scroll-thumb: #39434d;
}}
"""

fullscreen_css = """
[data-testid="stSidebar"] {display:none !important;}
header, footer {visibility:hidden !important; height:0 !important;}
"""

st.markdown(f"""
<style>
{dark_css if st.session_state.theme=='dark' else light_css}
html, body, [class*="css"] {{
  font-family: 'Quicksand', Arial, sans-serif;
  background: var(--bg-app);
}}
{"".join(fullscreen_css) if st.session_state.fullscreen else ""}

.chat-wrapper {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 .6rem 4rem .6rem;
}}
.top-bar {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background: var(--bg-panel);
  padding:.85rem 1.1rem;
  border-radius: 16px;
  border:1px solid var(--border-bubble);
  box-shadow:0 4px 18px rgba(0,0,0,.05);
  margin-bottom:1rem;
  flex-wrap:wrap;
  gap:.7rem;
}}
.top-title {{
  font-size:1.25rem;
  font-weight:800;
  background:{PRIMARY_GRADIENT};
  -webkit-background-clip:text;
  color:transparent;
  letter-spacing:.4px;
  display:flex;
  align-items:center;
  gap:.55rem;
}}
.toolbar {{
  display:flex;
  gap:.5rem;
  flex-wrap:wrap;
}}
.btn-mini {{
  background:var(--bg-bubble-ai);
  border:1px solid var(--border-bubble);
  color:var(--text-primary);
  padding:.5rem .85rem;
  border-radius:10px;
  cursor:pointer;
  font-size:.74rem;
  font-weight:600;
  transition:.18s;
}}
.btn-mini:hover {{
  background:var(--accent);
  color:#fff;
}}
.chat-panel {{
  background:var(--bg-panel);
  border:1px solid var(--border-bubble);
  border-radius: 22px;
  padding:1rem 1rem 1.4rem 1rem;
  display:flex;
  flex-direction:column;
  height:calc(100vh - 235px);
  max-height:860px;
  position:relative;
  overflow:hidden;
  box-shadow:0 8px 28px -4px rgba(0,0,0,.06);
}}
.messages-scroll {{
  overflow-y:auto;
  padding-right:.4rem;
  scroll-behavior:smooth;
}}
.messages-scroll::-webkit-scrollbar {{width:10px;}}
.messages-scroll::-webkit-scrollbar-track {{
  background:var(--scroll-track);border-radius:10px;
}}
.messages-scroll::-webkit-scrollbar-thumb {{
  background:var(--scroll-thumb);border-radius:10px;
}}
.msg-block {{
  display:flex;
  gap:.75rem;
  margin-bottom:1rem;
  align-items:flex-end;
  animation:fadeIn .45s ease;
}}
.msg-avatar {{
  width:42px;height:42px;border-radius:14px;
  background:var(--bg-bubble-ai);
  display:flex;align-items:center;justify-content:center;
  font-size:1.25rem;flex-shrink:0;
  box-shadow:0 3px 8px rgba(0,0,0,.08);
}}
.msg-user .msg-avatar {{background:var(--bg-bubble-user);color:#fff;}}
.msg-bubble {{
  padding:.7rem 1rem .85rem 1rem;
  border-radius:18px;
  max-width:72ch;
  line-height:1.5;
  font-size:.95rem;
  position:relative;
  border:1px solid var(--border-bubble);
  word-wrap:break-word;
  white-space:pre-wrap;
  background:var(--bg-bubble-ai);
  color:var(--text-primary);
}}
.msg-user .msg-bubble {{
  background:var(--bg-bubble-user);
  border:1px solid rgba(255,255,255,0.18);
  color:#fff;
}}
.msg-meta {{
  font-size:.62rem;
  opacity:.65;
  margin-top:.35rem;
  text-align:right;
}}
.day-separator {{
  text-align:center;
  font-size:.66rem;
  font-weight:600;
  letter-spacing:1px;
  opacity:.55;
  margin:1.15rem 0 .8rem 0;
  position:relative;
}}
.day-separator:before, .day-separator:after {{
  content:"";
  position:absolute;top:50%;
  width:38%;height:1px;
  background:var(--border-bubble);
}}
.day-separator:before {{left:0;}}
.day-separator:after {{right:0;}}
.typing-indicator {{
  display:inline-flex;
  gap:4px;
  align-items:center;
  padding:.55rem .85rem;
  background:var(--bg-bubble-ai);
  border-radius:16px;
  border:1px solid var(--border-bubble);
  font-size:.72rem;
  margin-left:55px;
  margin-bottom:1rem;
}}
.typing-indicator span {{
  width:6px;height:6px;
  background:var(--text-secondary);
  display:block;
  border-radius:50%;
  animation:blink 1s infinite ease-in-out;
}}
.typing-indicator span:nth-child(2) {{animation-delay:.2s;}}
.typing-indicator span:nth-child(3) {{animation-delay:.4s;}}
.quick-suggestions {{
  display:flex;flex-wrap:wrap;
  gap:.55rem;
  margin:.5rem 0 1rem 0;
}}
.suggestion-pill {{
  background:var(--bg-bubble-ai);
  border:1px solid var(--border-bubble);
  padding:.45rem .75rem;
  border-radius:40px;
  font-size:.68rem;
  cursor:pointer;
  font-weight:600;
  color:var(--text-secondary);
  transition:.15s;
}}
.suggestion-pill:hover {{
  background:var(--accent);
  color:#fff;
  border-color:var(--accent);
}}
.img-list {{
  display:flex;
  flex-wrap:wrap;
  gap:.5rem;
  margin-top:.45rem;
}}
.img-list img {{
  max-width:160px;
  border-radius:12px;
  border:1px solid var(--border-bubble);
  box-shadow:0 2px 8px rgba(0,0,0,.08);
}}
.footer-note {{
  font-size:.65rem;
  text-align:center;
  opacity:.55;
  margin-top:.5rem;
}}
.memory-box {{
  background:var(--bg-bubble-ai);
  border:1px solid var(--border-bubble);
  padding:.75rem .9rem;
  border-radius:14px;
  margin-bottom:.8rem;
  font-size:.72rem;
  line-height:1.35;
  color:var(--text-secondary);
}}
@keyframes fadeIn {{
  from {{opacity:0; transform:translateY(4px);}}
  to {{opacity:1; transform:translateY(0);}}
}}
@keyframes blink {{
  0%,80%,100% {{opacity:.2;}}
  40% {{opacity:1;}}
}}
</style>
""", unsafe_allow_html=True)

# ================== THANH CÔNG CỤ TRÊN CÙNG ==================
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="top-bar">', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.2], gap="small")

with col_left:
    st.markdown('<div class="top-title">🤖 Trò chuyện cùng <span style="font-weight:900;">Bạn Đồng Hành</span></div>',
                unsafe_allow_html=True)

with col_right:
    tool_cols = st.columns([1,1,1,1,1,1,1,1])
    with tool_cols[0]:
        if st.button("🌗 Theme", help="Đổi Light/Dark"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    with tool_cols[1]:
        if st.button("🧹 Xóa Chat", help="Xóa lịch sử hội thoại"):
            st.session_state.chat_history = []
            st.session_state.pending_user_msg = None
            st.session_state.show_suggestions = True
            st.rerun()
    with tool_cols[2]:
        if st.button("🧠 Xóa Memory", help="Xóa bộ nhớ dài hạn"):
            st.session_state.memory_summary = ""
            st.session_state.memory_version = 0
            if MEMORY_FILE.exists():
                MEMORY_FILE.unlink()
            st.rerun()
    with tool_cols[3]:
        chat_data = export_chat_txt()
        st.download_button("💾 Chat", data=chat_data, file_name="lich_su_tro_chuyen.txt",
                           mime="text/plain", help="Tải lịch sử")
    with tool_cols[4]:
        mem_data = export_memory_txt()
        st.download_button("🗂 Memory", data=mem_data, file_name="bo_nho_dai_han.txt",
                           mime="text/plain", help="Tải tóm tắt bộ nhớ")
    with tool_cols[5]:
        if st.button("💡 Gợi ý", help="Ẩn/hiện gợi ý nhanh"):
            st.session_state.show_suggestions = not st.session_state.show_suggestions
    with tool_cols[6]:
        if st.button("🧷 Full", help="Bật/tắt toàn màn hình"):
            st.session_state.fullscreen = not st.session_state.fullscreen
            st.rerun()
    with tool_cols[7]:
        if st.button("🧠 Info", help="Hiện/ẩn bộ nhớ đang lưu"):
            st.session_state.show_memory_box = not st.session_state.get("show_memory_box", False)

st.markdown('</div>', unsafe_allow_html=True)

# ================== PANEL CHAT ==================
st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

# Hộp hiển thị memory (nếu có)
if st.session_state.get("show_memory_box", False) and st.session_state.memory_summary:
    st.markdown(f"""
    <div class="memory-box">
        <b>TÓM TẮT BỘ NHỚ (v{st.session_state.memory_version}):</b><br>
        {st.session_state.memory_summary}
    </div>
    """, unsafe_allow_html=True)

# Khung scroll
st.markdown('<div class="messages-scroll" id="messages-scroll">', unsafe_allow_html=True)

last_day_key = None
for m in st.session_state.chat_history:
    day_key = m["time"].date()
    if day_key != last_day_key:
        st.markdown(f'<div class="day-separator">{format_day_separator(m["time"])}</div>', unsafe_allow_html=True)
        last_day_key = day_key

    avatar = "😊" if m["role"] == "user" else "🤖"
    role_class = "msg-user" if m["role"] == "user" else "msg-ai"
    time_str = m["time"].strftime("%H:%M")
    images_html = ""
    if m.get("images"):
        imgs = []
        for img_bytes in m["images"]:
            b64 = image_bytes_to_base64(img_bytes)
            imgs.append(f'<img src="data:image/png;base64,{b64}" />')
        images_html = f'<div class="img-list">{"".join(imgs)}</div>'

    st.markdown(f"""
    <div class="msg-block {role_class}">
      <div class="msg-avatar">{avatar}</div>
      <div style="display:flex;flex-direction:column;">
        <div class="msg-bubble">{m["content"]}{images_html}</div>
        <div class="msg-meta">{time_str}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Typing indicator
if st.session_state.pending_user_msg is not None:
    st.markdown("""
    <div class="typing-indicator">
      <span></span><span></span><span></span>
      <div style="margin-left:6px; font-weight:600; font-size:.62rem; letter-spacing:.5px; opacity:.7;">ĐANG SOẠN...</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end messages-scroll

# ================== GỢI Ý NHANH ==================
if st.session_state.show_suggestions and len(st.session_state.chat_history) == 0:
    suggestions = [
        "Mình đang cảm thấy khá căng thẳng...",
        "Làm sao để tập trung học tốt hơn?",
        "Mình khó ngủ nhiều ngày rồi.",
        "Làm sao vượt qua cảm giác lo âu?",
        "Gợi ý giúp mình thói quen lành mạnh nhé!"
    ]
    st.markdown('<div class="quick-suggestions">', unsafe_allow_html=True)
    sug_cols = st.columns(min(5, len(suggestions)))
    for i, s in enumerate(suggestions):
        if sug_cols[i % 5].button(s, key=f"sugg_{i}"):
            add_message("user", s)
            st.session_state.pending_user_msg = s
            st.rerun()  # Changed from experimental_rerun
    st.markdown('</div>', unsafe_allow_html=True)

# ================== FORM GỬI TIN + ẢNH ==================
with st.container():
    up_col1, up_col2 = st.columns([4, 1.4])
    with up_col1:
        # chat_input (dưới phiên bản Streamlit mới)
        user_text = st.chat_input("Nhập điều bạn muốn chia sẻ...")
    with up_col2:
        uploaded_imgs = st.file_uploader("Ảnh (tùy chọn)", type=["png", "jpg", "jpeg"], accept_multiple_files=True,
                                         label_visibility="collapsed")

if user_text:
    # Lưu ảnh bytes
    imgs_bytes = []
    if uploaded_imgs:
        for f in uploaded_imgs:
            imgs_bytes.append(f.read())
    add_message("user", user_text, images=imgs_bytes)
    st.session_state.pending_user_msg = user_text
    st.rerun()  # Changed from experimental_rerun

# ================== XỬ LÝ TRẢ LỜI AI ==================
if st.session_state.pending_user_msg is not None:
    time.sleep(0.8)
    # Lấy ảnh của message vừa gửi
    last_user_msg = st.session_state.chat_history[-1]
    ai_reply = generate_ai_reply(last_user_msg["content"], images=last_user_msg.get("images"))
    add_message("assistant", ai_reply)
    st.session_state.pending_user_msg = None

    # Cập nhật memory nếu đạt ngưỡng
    if (len([m for m in st.session_state.chat_history if m["role"] != "system"]) %
            MEMORY_UPDATE_INTERVAL == 0):
        new_summary = summarize_history_for_memory(st.session_state.chat_history,
                                                   st.session_state.memory_summary)
        st.session_state.memory_summary = new_summary
        st.session_state.memory_version += 1
        save_memory()
    st.rerun()  # Changed from experimental_rerun

# ================== FOOTER NOTE ==================
st.markdown("""
<div class="footer-note">
Trò chuyện không thay thế tư vấn tâm lý chuyên nghiệp. Nếu bạn có nguy cơ tự gây hại, hãy tìm sự trợ giúp trực tiếp ngay lập tức. 💖
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end chat-panel
st.markdown('</div>', unsafe_allow_html=True)  # end chat-wrapper

# ================== AUTO SCROLL SCRIPT ==================
st.markdown("""
<script>
const el = window.parent.document.querySelector('#messages-scroll');
if (el) { el.scrollTop = el.scrollHeight; }
</script>
""", unsafe_allow_html=True)
