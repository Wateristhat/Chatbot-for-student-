# File: pages/9_📖_Người_Kể_Chuyện.py (Thêm 5 truyện chữa lành mới)
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import sys 
import os 
import tempfile
from datetime import datetime

# --- BẢO VỆ TRANG ---
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() 

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI ---
current_user_id = st.session_state.user_id

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="wide")

# --- CSS GIAO DIỆN ---
st.markdown("""
<style>
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

# --- NỘI DUNG TRUYỆN ---
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
            {
                "title": "Bảy lần ngã, Tám lần đứng dậy",
                "content": "Một võ sĩ Sumo đang học việc bị mọi người chế giễu vì vóc dáng nhỏ bé và liên tục thất bại trong các trận đấu tập. Anh nản lòng và muốn bỏ cuộc. Người thầy của anh chỉ nói: 'Thất bại không phải là xấu hổ. Đáng xấu hổ là khi con không chịu đứng dậy sau thất bại.' Võ sĩ nhớ lời thầy, mỗi khi ngã, anh lại đứng dậy, tập luyện điên cuồng. Cuối cùng, anh trở thành một trong những đô vật vĩ đại nhất. Bài học: Thành công không đến từ việc không bao giờ thất bại, mà đến từ sự kiên trì và khả năng phục hồi sau mỗi lần gục ngã."
            },
            {
                "title": "Chiếc gương và người đánh giày",
                "content": "Một người đàn ông giàu có muốn mua một chiếc gương lớn và hoàn hảo. Ông đến hỏi một ông chủ cửa hàng đồ cũ, ông này trả lời: 'Không có chiếc gương nào hoàn hảo, thưa ngài. Chỉ có gương và bụi.' Sau đó, ông thấy một người đánh giày với khuôn mặt rạng rỡ, dù công việc rất vất vả. Ông hỏi bí quyết. Người đánh giày đáp: 'Tôi luôn thấy hạnh phúc khi làm việc của mình, và tôi không bao giờ nhìn vào những thứ không phải là công việc của tôi.' Bài học: Hạnh phúc không nằm ở sự hoàn hảo hay giàu có, mà ở cách chúng ta nhìn nhận công việc và cuộc sống của mình."
            },
            {
                "title": "Quy tắc của cây Tre",
                "content": "Cây tre là biểu tượng của sự kiên cường. Sau khi gieo trồng, người nông dân phải mất đến 5 năm để chăm sóc mà không thấy bất kỳ sự phát triển nào trên mặt đất. Nhưng trong 5 năm đó, rễ tre đã lan rộng và đan xen vào nhau dưới lòng đất. Và rồi, sau 5 năm, cây tre Trung Quốc có thể cao thêm 90 feet (khoảng 27 mét) chỉ trong 6 tuần. Bài học: Sự kiên nhẫn và nỗ lực âm thầm là nền tảng để đạt được sự phát triển đột phá. Đừng nản lòng khi chưa thấy kết quả ngay lập tức."
            },
            {
                "title": "Sự lựa chọn của người chèo thuyền",
                "content": "Một người chèo thuyền luôn than phiền về thời tiết xấu, dòng nước ngược và những cơn gió mạnh. Một người chèo thuyền khác mỉm cười và nói: 'Thời tiết và dòng nước luôn là như vậy. Thay vì than phiền, hãy học cách dùng mái chèo để vượt qua chúng.' Người chèo thuyền đầu tiên đã nhận ra rằng anh ta không thể thay đổi được thế giới, nhưng anh ta có thể thay đổi cách anh ta hành động và phản ứng. Bài học: Cuộc sống đầy rẫy những trở ngại ngoài tầm kiểm soát của chúng ta. Sức mạnh thật sự là khả năng điều chỉnh và tận dụng những gì chúng ta có."
            },
            {
                "title": "Hố sâu và chiếc thang",
                "content": "Một người đang đi trên đường thì bị rơi xuống một cái hố sâu. Anh ta cố gắng kêu cứu nhưng không ai nghe thấy. Anh tuyệt vọng. Một lúc sau, một người đi qua, thấy anh ta và quăng xuống một sợi dây thừng. Anh ta leo lên được. Sau này, anh ta thấy một người khác cũng bị rơi xuống hố đó. Thay vì quăng dây thừng, anh ta nhảy xuống hố. Người bị nạn hoảng hốt: 'Anh làm gì vậy?' Anh ta mỉm cười và nói: 'Tôi hiểu cảm giác của anh. Tôi đã từng ở đây. Tôi biết đường ra.' Bài học: Sự đồng cảm và kinh nghiệm vượt qua khó khăn là món quà lớn nhất mà chúng ta có thể chia sẻ với người khác."
            },
        ],
        "Truyện ngụ ngôn": [
            {
                "title": "Ếch ngồi đáy giếng",
                "content": "Có một con ếch sống lâu năm trong một cái giếng. Nó nhìn lên và chỉ thấy một khoảng trời bé bằng miệng giếng. Nó tự hào nghĩ rằng bầu trời chỉ to có vậy. Một ngày, trời mưa to, nước giếng dâng lên và đưa ếch ra ngoài. Lần đầu tiên, nó thấy một bầu trời rộng lớn bao la và nhận ra sự hiểu biết hạn hẹp của mình. Bài học: Môi trường sống hạn hẹp có thể che lấp tầm nhìn của chúng ta. Đừng vội cho rằng những gì mình biết là tất cả."
            },
            {
                "title": "Cáo và chùm nho",
                "content": "Một con cáo đói đi qua một vườn nho. Nó thấy một chùm nho chín mọng lủng lẳng trên giàn cao. Cáo nhảy lên nhiều lần nhưng không thể với tới. Cuối cùng, nó bỏ đi và tự nhủ: 'Nho còn xanh lắm, ăn vào chỉ chua thôi!'. Bài học: Nhiều người thường chê bai những thứ họ không thể đạt được để tự an ủi bản thân."
            },
            {
                "title": "Thỏ và rùa",
                "content": "Một con thỏ kiêu ngạo luôn khoe khoang về tốc độ của mình và thách thức một con rùa chậm chạp thi chạy. Trong cuộc đua, thỏ chạy nhanh hơn rùa rất nhiều và tự tin rằng mình sẽ thắng, nên nó dừng lại và ngủ một giấc. Rùa cứ từ từ bò, không ngừng nghỉ. Khi thỏ tỉnh dậy, nó thấy rùa đã bò đến đích và thắng cuộc. Bài học: Chậm mà chắc, kiên trì và không tự mãn mới là chìa khóa của thành công."
            },
            {
                "title": "Kiến và ve sầu",
                "content": "Suốt mùa hè, kiến chăm chỉ tha mồi và dự trữ lương thực cho mùa đông, trong khi ve sầu chỉ biết ca hát và vui chơi. Khi mùa đông đến, ve sầu đói rét và gần như chết cóng, nó đến xin kiến thức ăn. Kiến từ chối và nói: 'Mùa hè bạn ca hát, thì mùa đông bạn hãy nhảy múa đi.' Bài học: Phải biết nhìn xa trông rộng, chăm chỉ làm việc và chuẩn bị cho tương lai, thay vì chỉ sống cho hiện tại."
            },
            {
                "title": "Bó đũa",
                "content": "Một người cha già gọi các con lại và đưa cho chúng một bó đũa, yêu cầu chúng bẻ gãy. Từng người một cố gắng nhưng không ai bẻ gãy được. Sau đó, ông tháo bó đũa ra và yêu cầu chúng bẻ từng chiếc. Lần này, mọi người đều dễ dàng bẻ gãy. Người cha nói: 'Các con thấy không, nếu các con đoàn kết với nhau, không ai có thể đánh bại được các con. Nhưng nếu các con chia rẽ, từng người sẽ dễ dàng bị đánh bại.' Bài học: Sức mạnh nằm ở sự đoàn kết và hợp lực."
            },
            {
                "title": "Chó sói và cừu",
                "content": "Một con chó sói muốn ăn thịt một con cừu đang lạc đàn. Nó giả vờ bị thương và kêu gọi lòng thương hại của cừu. Cừu thấy sói đáng thương nên tiến lại gần. Ngay lập tức, sói bật dậy và vồ lấy cừu. Bài học: Đừng tin vào lời nói ngọt ngào hay vẻ ngoài đáng thương của kẻ thù, đặc biệt là khi bạn đang ở trong tình thế dễ bị tổn thương."
            },
            {
                "title": "Chim bồ câu và kiến",
                "content": "Một con kiến bị trượt chân và rơi xuống sông. Một con chim bồ câu thấy vậy, nhanh chóng thả một chiếc lá xuống nước. Kiến bám vào chiếc lá và thoát chết. Ít lâu sau, một người thợ săn giương súng định bắn bồ câu. Kiến nhìn thấy, bèn bò đến và cắn vào chân người thợ săn. Người thợ săn giật mình làm rơi súng, bồ câu nghe tiếng động nên bay đi thoát nạn. Bài học: Hãy luôn giúp đỡ người khác khi họ gặp khó khăn, vì một ngày nào đó, bạn cũng sẽ nhận lại sự giúp đỡ."
            }
        ],
        "Truyện chữa lành": [
            {
                "title": "Dòng sông không vội vã",
                "content": "Không một dòng sông nào vội vã. Nó chảy theo nhịp điệu của riêng mình, lúc êm đềm, lúc cuộn trào, nhưng luôn tiến về phía trước. Dòng sông biết rằng, rồi nó sẽ đến được biển lớn. Hãy sống như một một dòng sông, chấp nhận mọi khúc quanh của cuộc đời và tin tưởng vào hành trình của chính mình. Đừng so sánh tốc độ của bạn với người khác, vì mỗi người đều có một con đường riêng."
            },
            {
                "title": "Chiếc bình nứt",
                "content": "Một người gánh nước có hai chiếc bình, một chiếc lành lặn và một chiếc bị nứt. Chiếc bình nứt luôn cảm thấy tự ti vì nó chỉ giữ được một nửa phần nước. Một ngày, nó xin lỗi người chủ. Người chủ mỉm cười và nói: 'Con có thấy những luống hoa xinh đẹp bên đường không? Đó là nhờ ta đã gieo hạt ở phía bên con. Mỗi ngày, những giọt nước từ vết nứt của con đã tưới cho chúng'. Bài học: Những khuyết điểm của bạn có thể lại là điều tạo nên vẻ đẹp và giá trị riêng biệt mà bạn không ngờ tới."
            },
            {
                "title": "Con sâu bướm và sự thay đổi",
                "content": "Một con sâu bướm dành cả cuộc đời bò trên mặt đất, luôn ước ao được bay như những loài chim. Nó sợ hãi khi phải cuộn mình trong cái kén tối tăm. Nhưng sau một thời gian kiên nhẫn và chịu đựng, nó phá kén chui ra, hóa thành một con bướm xinh đẹp. Bài học: Đôi khi, những giai đoạn khó khăn và cô đơn nhất trong đời lại là quá trình 'hóa kén' để bạn trở thành phiên bản tốt hơn và rực rỡ hơn của chính mình."
            },
            {
                "title": "Tiếng chuông lặng im",
                "content": "Trong một ngôi đền cổ, có một chiếc chuông lớn đã bị nứt. Mỗi khi có lễ hội, các nhà sư đều dùng chuông lành lặn để đánh. Một du khách hỏi tại sao không sửa chiếc chuông nứt. Một nhà sư trả lời: 'Nó đã được hàn lại nhiều lần nhưng tiếng kêu không còn ngân vang như trước. Chúng tôi giữ nó ở đây để nhắc nhở rằng, có những nỗi đau hay tổn thương không thể xóa bỏ hoàn toàn, nhưng chúng ta vẫn có thể tìm thấy sự bình yên trong sự chấp nhận lặng im của nó'. Bài học: Chấp nhận những 'vết nứt' trong tâm hồn là bước đầu tiên để tìm lại sự bình yên."
            },
            {
                "title": "Đóa hoa sen trong bùn",
                "content": "Hoa sen luôn được ngưỡng mộ vì vẻ đẹp thanh cao. Nhưng để nở rộ, nó phải lớn lên từ lớp bùn lầy dơ bẩn. Bùn chính là nguồn dinh dưỡng duy nhất để nó vươn lên và tỏa sáng trên mặt nước. Bài học: Những khó khăn, những 'vũng bùn' trong quá khứ hay hiện tại không định nghĩa bạn. Chúng chính là chất dinh dưỡng giúp bạn mạnh mẽ hơn, trưởng thành hơn và cuối cùng là nở rộ với vẻ đẹp riêng biệt của mình."
            },
            {
                "title": "Chiếc áo choàng của thời gian",
                "content": "Một người luôn buồn bã vì những lỗi lầm trong quá khứ, không thể tha thứ cho chính mình. Một nhà hiền triết đưa cho anh ta một chiếc áo choàng nặng nề và bảo anh ta mặc. Sau đó, nhà hiền triết nói: 'Chiếc áo này là quá khứ của cậu. Nó quá nặng và cản bước cậu đi. Thời gian sẽ dần cởi bỏ nó, nhưng cậu phải tự quyết định có để nó giữ chân mình mãi mãi hay không.' Bài học: Thời gian là liều thuốc chữa lành tốt nhất, nhưng chúng ta phải chủ động buông bỏ gánh nặng của quá khứ để cho phép quá trình chữa lành diễn ra."
            },
            {
                "title": "Bữa tiệc của ánh sáng và bóng tối",
                "content": "Trong một căn phòng, ánh sáng và bóng tối sống chung. Ánh sáng luôn cố gắng xua đuổi bóng tối, và bóng tối luôn tìm cách che giấu ánh sáng. Cuối cùng, một vị khách bước vào và nói: 'Hai bạn thật ngốc nghếch. Ánh sáng và bóng tối không phải kẻ thù. Nếu không có bóng tối, chúng ta sẽ không bao giờ biết được ánh sáng rực rỡ đến mức nào. Hãy tổ chức một bữa tiệc.' Bài học: Cuộc sống không thể chỉ có niềm vui (ánh sáng). Hãy học cách chấp nhận và biết ơn cả những ngày buồn bã (bóng tối), vì chúng giúp chúng ta trân trọng những khoảnh khắc hạnh phúc."
            }
        ]
    }
STORIES = load_stories()

# --- TRỢ LÝ ẢO & TÊN TÍNH NĂNG ---
ASSISTANT_MESSAGES = [
    ("📖", "Hãy chọn một thể loại và lắng nghe một câu chuyện nhỏ để xoa dịu tâm hồn nhé."),
    ("✨", "Mỗi câu chuyện là một bài học. Cùng khám phá với Bee nào!"),
    ("🎧", "Sẵn sàng lắng nghe chưa? Bee sẽ kể cho bạn những câu chuyện hay nhất!"),
]
if "nkc_assistant_message" not in st.session_state:
    st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
avatar, msg = st.session_state.nkc_assistant_message

def create_audio_file(text):
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.name = tmp_file.name # Bắt buộc phải có
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        # st.error(f"Lỗi tạo file âm thanh: {e}")
        return None

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
        audio_file = create_audio_file(msg)
        if audio_file:
            try:
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mpeg")
                os.unlink(audio_file) # Xóa file tạm thời
            except Exception as e:
                st.error(f"Không thể phát âm thanh: {e}")

st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
st.write("---")

selected_category = st.selectbox(
    "**Chọn thể loại truyện bạn muốn nghe:**",
    options=list(STORIES.keys())
)
st.write("---")

if selected_category:
    st.subheader(f"Các câu chuyện về {selected_category.lower()}:")
    for i, story in enumerate(STORIES[selected_category]):
        with st.expander(f"**{story['title']}**"):
            st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.6;'>{story['content']}</p>", unsafe_allow_html=True)
            
            if st.button("Nghe truyện 🎧", key=f"listen_{selected_category}_{i}"):
                with st.spinner("Đang chuẩn bị âm thanh..."):
                    full_text = f"Câu chuyện {story['title']}. {story['content']}"
                    audio_file = create_audio_file(full_text)
                    if audio_file:
                        try:
                            with open(audio_file, 'rb') as f:
                                audio_bytes = f.read()
                            st.audio(audio_bytes, format="audio/mpeg")
                            os.unlink(audio_file) # Xóa file tạm thời
                        except Exception as e:
                            st.error(f"Lỗi khi phát âm thanh: {e}")
