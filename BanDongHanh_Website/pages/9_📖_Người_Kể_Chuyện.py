Kể chuyện
# pages/9_📖_Người_Kể_Chuyện.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO

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
            },
            {
                "title": "Bảy lần ngã, Tám lần đứng dậy",
                "content": "Một võ sĩ Sumo đang học việc bị mọi người chế giễu vì vóc dáng nhỏ bé và liên tục thất bại trong các trận đấu tập. Anh nản lòng và muốn bỏ cuộc. Người thầy của anh chỉ nói: 'Thất bại không phải là xấu hổ. Đáng xấu hổ là khi con không chịu đứng dậy sau thất bại.' Võ sĩ nhớ lời thầy, mỗi khi ngã, anh lại đứng dậy, tập luyện điên cuồng. Cuối cùng, anh trở thành một trong những đô vật vĩ đại nhất. Bài học: Thành công không đến từ việc không bao giờ thất bại, mà đến từ sự kiên trì và khả năng phục hồi sau mỗi lần gục ngã."
            },
            {
                "title": "Chiếc gương và người đánh giày",
                "content": "Một người đàn ông giàu có muốn mua một chiếc gương lớn và hoàn hảo. Ông đến một tiệm gương và hỏi liệu có chiếc gương nào không tì vết không. Người thợ gương trả lời: 'Không có chiếc gương nào hoàn hảo, thưa ngài. Chỉ có gương và bụi.' Sau đó, ông thấy một người đánh giày với khuôn mặt rạng rỡ, dù công việc rất vất vả. Ông hỏi bí quyết. Người đánh giày đáp: 'Tôi luôn thấy hạnh phúc khi làm việc của mình, và tôi không bao giờ nhìn vào những thứ không phải là công việc của tôi.' Bài học: Hạnh phúc không nằm ở sự hoàn hảo hay giàu có, mà ở cách chúng ta nhìn nhận công việc và cuộc sống của mình."
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
            # --- 5 TRUYỆN TRUYỀN CẢM HỨNG MỚI ĐƯỢC THÊM VÀO ---
            {
                "title": "Người thợ gốm và chiếc bình hỏng",
                "content": "Một người thợ gốm luôn giữ lại những chiếc bình bị nứt hoặc méo mó, dù chúng không bán được. Khi người học việc hỏi tại sao, ông nói: 'Bình lành lặn dùng để đựng nước, nhưng những chiếc bình hỏng này lại tạo ra âm thanh độc đáo khi gió thổi qua. Chúng dùng để tạo ra âm nhạc.' Bài học: Những khiếm khuyết hay sai lầm của bạn không phải là vô dụng. Chúng có thể tạo ra những giá trị và ý nghĩa khác biệt mà bạn không ngờ tới."
            },
            {
                "title": "Nghệ sĩ vĩ cầm trên phố",
                "content": "Một nghệ sĩ vĩ cầm nổi tiếng thế giới, đã bán hết vé cho các buổi hòa nhạc lớn, quyết định xuống ga tàu điện ngầm để chơi nhạc trong giờ cao điểm. Anh chơi những bản nhạc kinh điển bằng cây đàn trị giá hàng triệu đô la. Hầu hết mọi người đi ngang qua đều vội vã, chỉ có vài người dừng lại nghe trong chốc lát và bỏ một ít tiền lẻ. Bài học: Giá trị và tài năng thực sự không được định đoạt bởi bối cảnh. Đừng bao giờ chờ đợi sự công nhận của đám đông. Điều quan trọng là bạn có dám theo đuổi đam mê của mình, dù ở nơi nào hay không."
            },
            {
                "title": "Chiếc thuyền buồm ngược gió",
                "content": "Hai chiếc thuyền buồm cùng căng buồm ra khơi. Một chiếc than phiền: 'Gió ngược quá, tôi không thể đi được.' Chiếc kia, bằng cách điều chỉnh góc cánh buồm, lại dùng chính sức gió ngược đó để đẩy mình tiến lên. Bài học: Cuộc sống không phải là việc chờ đợi những cơn gió thuận lợi, mà là học cách điều chỉnh cánh buồm để đi đến đích bằng mọi loại gió. Khó khăn có thể là lực đẩy nếu chúng ta biết cách xoay chuyển tình thế."
            },
            {
                "title": "Sự kiên nhẫn của chiếc đồng hồ cát",
                "content": "Một chiếc đồng hồ cát không bao giờ cố gắng đẩy cát nhanh hơn. Nó chỉ lật lại và để cho cát chảy theo đúng nhịp điệu tự nhiên của nó. Nếu cố gắng ép buộc tốc độ, nó sẽ bị tắc nghẽn và ngừng hoạt động. Bài học: Mọi thứ trong cuộc sống đều có thời điểm của nó. Thay vì cố gắng vội vã, hãy kiên nhẫn và tin tưởng vào quá trình. Hãy để mọi thứ diễn ra một cách tự nhiên."
            },
            {
                "title": "Phép màu của sự bắt đầu",
                "content": "Nhà văn người Brazil Paulo Coelho từng nói: 'Khi bạn thực sự muốn điều gì đó, cả vũ trụ sẽ hợp lực giúp bạn đạt được điều đó.' Nhiều người trì hoãn ước mơ vì sợ thất bại. Nhưng câu chuyện này dạy rằng, bước đi đầu tiên, dù nhỏ bé đến đâu, là điều kiện tiên quyết để tạo ra 'phép màu' của sự hỗ trợ từ bên ngoài. Bài học: Hãy bắt đầu. Chỉ khi bạn bắt đầu hành động, những cơ hội, sự giúp đỡ và nguồn lực cần thiết mới xuất hiện để hỗ trợ bạn trên hành trình của mình."
            }
            # --- KẾT THÚC CÁC TRUYỆN MỚI ---
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
                    try:
                        tts = gTTS(text=full_text, lang='vi', slow=False)
                        fp = BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        st.audio(fp, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Lỗi khi tạo âm thanh: {e}")
