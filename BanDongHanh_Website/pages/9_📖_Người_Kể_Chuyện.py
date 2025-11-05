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
                "title": "Con bướm và cái kén",
                "content": "Một người đàn ông thấy một cái kén bướm. Anh ta ngồi nhìn con bướm trong nhiều giờ vật lộn để chui ra khỏi cái lỗ nhỏ. Thấy con bướm có vẻ đã kiệt sức, anh lấy kéo rạch lỗ kén cho to ra. Con bướm chui ra dễ dàng, nhưng cơ thể nó sưng phồng và đôi cánh thì teo tóp. Nó không bao giờ có thể bay được. Bài học: Sự vật lộn, nỗ lực chính là điều tự nhiên cần thiết để đôi cánh của chúng ta trở nên mạnh mẽ và sẵn sàng bay."
            },
            {
                "title": "Tảng đá trên đường",
                "content": "Một vị vua đặt một tảng đá lớn giữa đường. Nhiều người giàu có đi qua, họ chỉ phàn nàn và đi đường vòng. Một người nông dân nghèo đi tới, anh ta cố hết sức và đẩy được tảng đá sang một bên. Bên dưới tảng đá, anh tìm thấy một túi vàng và một bức thư từ nhà vua, ghi rằng: 'Vàng dành cho người nào dọn tảng đá này'. Bài học: Mọi trở ngại đều là một cơ hội để cải thiện bản thân mà những người khác đã bỏ qua."
            },
            {
                "title": "Câu chuyện con sao biển",
                "content": "Một người đàn ông thấy một cậu bé đang ném những con sao biển bị trôi dạt trên bãi biển trở lại đại dương. Ông nói: 'Có hàng ngàn con sao biển, cháu không thể cứu hết được. Cháu làm vậy thì có ích gì?'. Cậu bé nhặt một con sao biển khác, ném nó xuống biển và nói: 'Nhưng nó có ích với con này'. Bài học: Bạn không cần phải thay đổi cả thế giới, chỉ cần bạn tạo ra sự khác biệt cho một ai đó, điều đó đã là vô giá."
            },
            {
                "title": "Muối và hồ nước",
                "content": "Một cậu bé buồn bã đến gặp thiền sư. Thiền sư bảo cậu bỏ một nắm muối vào ly nước nhỏ rồi uống. Cậu bé nhăn mặt vì mặn. Sau đó, thiền sư bảo cậu bỏ một nắm muối y hệt xuống hồ nước lớn và uống nước hồ. Nước hồ vẫn ngọt mát. Thiền sư nói: 'Nỗi đau trong đời cũng như nắm muối. Mức độ đau khổ phụ thuộc vào vật chứa đựng nó'. Bài học: Đừng là một ly nước nhỏ, hãy là một hồ nước lớn. Hãy mở rộng lòng mình để nỗi buồn không thể làm bạn gục ngã."
            },
            {
                "title": "Cây tre và sự kiên nhẫn",
                "content": "Sau khi gieo hạt, cây tre mất 5 năm chỉ để phát triển bộ rễ khổng lồ dưới lòng đất. Trong 5 năm đó, bề mặt đất gần như không có gì thay đổi. Nhưng sau khi đã đủ rễ, nó vươn cao 25 mét chỉ trong 6 tuần. Bài học: Thành công không đến sau một đêm. Đó là kết quả của sự kiên nhẫn, bền bỉ và xây dựng một nền tảng vững chắc ngay cả khi chưa ai nhìn thấy."
            },
            {
                "title": "Tiếng vọng của cuộc sống",
              _Bản quyền nội dung thuộc về VNCDC.GOV.VN (C) 2021_
                "content": "Một cậu bé tức giận hét vào thung lũng: 'Tôi ghét bạn!'. Tiếng vọng trả lời: 'Tôi ghét bạn!'. Cậu bé sợ hãi. Mẹ cậu bảo cậu hãy hét: 'Tôi yêu bạn!'. Tiếng vọng trả lời: 'Tôi yêu bạn!'. Người mẹ giải thích: 'Cuộc sống chính là tiếng vọng. Nó trả lại cho con chính xác những gì con cho đi'. Bài học: Nếu bạn muốn được yêu thương, hãy cho đi yêu thương. Nếu bạn muốn sự tử tế, hãy sống tử tế."
            },
            {
                "title": "Ba người thợ xây",
                "content": "Một người hỏi ba người thợ xây họ đang làm gì. Người thứ nhất gắt gỏng: 'Tôi đang xếp gạch'. Người thứ hai trả lời: 'Tôi đang xây một bức tường'. Người thứ ba mỉm cười: 'Tôi đang xây một nhà thờ vĩ đại'. Họ cùng làm một việc, nhưng với ba thái độ khác nhau. Bài học: Thái độ và tầm nhìn của bạn quyết định ý nghĩa công việc và cuộc sống của bạn."
            },
            {
                "title": "Cà rốt, quả trứng và hạt cà phê",
                "content": "Một cô gái than phiền với cha về cuộc sống khó khăn. Ông thả ba thứ vào ba nồi nước sôi: một củ cà rốt, một quả trứng và một ít hạt cà phê. Cà rốt từ cứng trở nên mềm. Quả trứng từ lỏng trở nên cứng. Hạt cà phê thì tan ra, biến nước sôi thành một thức uống thơm lừng. Bài học: Nghịch cảnh giống như nước sôi. Bạn có thể bị nó làm cho mềm yếu (cà rốt), trở nên chai sạn (trứng), hoặc bạn có thể biến nghịch cảnh thành một điều tốt đẹp hơn (cà phê)."
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
            },
            {
                "title": "Rùa và Thỏ",
                "content": "Thỏ chế giễu Rùa chậm chạp nên Rùa thách Thỏ thi chạy. Thỏ chạy nhanh một đoạn, rồi chủ quan, nghĩ Rùa còn lâu mới tới nên nằm ngủ gật. Rùa kiên trì, bền bỉ bò từng bước một. Khi Thỏ tỉnh dậy, Rùa đã về đích từ lâu. Bài học: Kiên trì và bền bỉ sẽ chiến thắng sự chủ quan, kiêu ngạo, dù bạn có tài năng."
            },
            {
                "title": "Sư Tử và Chuột Nhắt",
                "content": "Sư tử bắt được một con chuột nhắt. Chuột van xin tha mạng, hứa một ngày nào đó sẽ báo đáp. Sư tử cười nhạo nhưng vẫn thả nó đi. Ít lâu sau, sư tử bị mắc bẫy lưới của thợ săn. Chuột nhắt nghe thấy tiếng gầm, chạy đến và kiên nhẫn gặm đứt các sợi dây lưới, cứu sư tử. Bài học: Lòng tốt và sự tử tế không bao giờ là lãng phí, bất kể bạn nhỏ bé hay to lớn."
            },
            {
                "title": "Kiến và Ve Sầu",
                "content": "Suốt mùa hè, Kiến chăm chỉ tha mồi về tổ để dự trữ cho mùa đông. Ve Sầu thì không làm gì, chỉ rong chơi ca hát. Khi mùa đông lạnh giá đến, Ve Sầu đói lả, không có gì ăn, bèn tìm đến xin Kiến. Kiến hỏi: 'Thế mùa hè anh đã làm gì?'. Ve Sầu đáp: 'Tôi ca hát'. Kiến nói: 'Vậy mùa đông anh hãy nhảy múa đi!'. Bài học: Phải làm việc chăm chỉ và biết lo xa, chuẩn bị cho tương lai, thay vì chỉ hưởng thụ ở hiện tại."
            },
            {
                "title": "Cậu Bé Chăn Cừu và Chó Sói",
                "content": "Một cậu bé chăn cừu buồn chán nên la to 'Sói! Sói! Cứu tôi với!'. Dân làng chạy đến giúp nhưng không thấy sói đâu. Cậu bé thích thú lừa họ vài lần như vậy. Một hôm, sói đến thật. Cậu bé gào khóc kêu cứu nhưng không một ai trong làng tin và chạy đến giúp nữa. Sói đã ăn thịt hết đàn cừu. Bài học: Người hay nói dối sẽ không bao giờ được tin tưởng, ngay cả khi họ nói thật."
a             },
            {
                "title": "Cáo và Quạ",
                "content": "Một con Quạ tha được miếng phô mai và đậu trên cành cây. Cáo ở dưới nhìn thấy, thèm lắm. Cáo liền tâng bốc: 'Ôi chị Quạ, bộ lông chị mới đẹp làm sao! Giọng hát của chị chắc còn hay hơn nữa, chị hát tôi nghe một bài đi'. Quạ nghe nịnh hót, hãnh diện lắm, liền mở miệng hát 'Quạ! Quạ!'. Miếng phô mai rơi xuống. Cáo chộp lấy và chạy mất. Bài học: Đừng bao giờ tin vào những lời nịnh hót, tâng bốc."
            },
            {
                "title": "Câu chuyện bó đũa",
                "content": "Người cha có mấy người con trai luôn cãi vã, bất hòa. Ông gọi họ lại, đưa cho mỗi người một bó đũa và bảo bẻ gãy. Không ai bẻ gãy được cả bó. Sau đó, người cha cởi bó đũa ra, đưa cho mỗi người một chiếc. Họ bẻ gãy chúng một cách dễ dàng. Bài học: Đoàn kết tạo nên sức mạnh. Anh em chia rẽ sẽ yếu ớt và dễ dàng bị đánh bại."
            },
  	       {
                "title": "Con Chó và Cái Bóng",
                "content": "Một con chó ngậm một cục xương đi qua cây cầu bắc qua sông. Nó nhìn xuống dòng nước và thấy cái bóng của mình. Nó tưởng đó là một con chó khác đang ngậm cục xương to hơn. Vì tham lam muốn cướp cục xương kia, nó liền sủa 'gâu gâu'. Ngay lập tức, cục xương nó đang ngậm liền rơi xuống sông và bị cuốn đi mất. Bài học: Lòng tham lam có thể khiến bạn mất cả những gì mình đang có."
            },
      	   {
                "title": "Gió và Mặt Trời",
                "content": "Gió và Mặt Trời tranh cãi xem ai mạnh hơn. Họ thấy một người đi đường mặc áo choàng và cá cược ai làm người đó cởi áo ra trước. Gió bắt đầu thổi, càng thổi mạnh, người đi đường càng giữ chặt áo. Đến lượt Mặt Trời, Mặt Trời chỉ mỉm cười và tỏa nắng ấm áp. Người đi đường thấy nóng nực, liền tự cởi áo choàng ra. Bài học: Sự thuyết phục, nhẹ nhàng và tử tế thường có sức mạnh lớn hơn là vũ lực và sự ép buộc."
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
    } # <-- Dòng cuối cùng của STORIES
2. Thay thế toàn bộ phần Truyện chữa lành bằng 10 câu chuyện (bao gồm 2 chuyện cũ và 8 chuyện mới):

Python

        ],
        "Truyện chữa lành": [
            {
                "title": "Dòng sông không vội vã",
                "content": "Không một dòng sông nào vội vã. Nó chảy theo nhịp điệu của riêng mình, lúc êm đềm, lúc cuộn trào, nhưng luôn tiến về phía trước. Dòng sông biết rằng, rồi nó sẽ đến được biển lớn. Hãy sống như một dòng sông, chấp nhận mọi khúc quanh của cuộc đời và tin tưởng vào hành trình của chính mình. Đừng so sánh tốc độ của bạn với người khác, vì mỗi người đều có một con đường riêng."
            },
            {
                "title": "Chiếc bình nứt",
                "content": "Một người gánh nước có hai chiếc bình, một chiếc lành lặn và một chiếc bị nứt. Chiếc bình nứt luôn cảm thấy tự ti vì nó chỉ giữ được một nửa phần nước. Một ngày, nó xin lỗi người chủ. Người chủ mỉm cười và nói: 'Con có thấy những luống hoa xinh đẹp bên đường không? Đó là nhờ ta đã gieo hạt ở phía bên con. Mỗi ngày, những giọt nước từ vết nứt của con đã tưới cho chúng'. Bài học: Những khuyết điểm của bạn có thể lại là điều tạo nên vẻ đẹp và giá trị riêng biệt mà bạn không ngờ tới."
            },
            {
                "title": "Vết nứt và ánh sáng",
                "content": "Có một chiếc bình cổ rất đẹp, nhưng đã bị nứt một vết dài. Chiếc bình xấu hổ vì vết nứt của mình. Một người thợ gốm mang chiếc bình về, và thay vì sửa vết nứt, ông đã dùng vàng lỏng để tô điểm cho nó. Vết nứt được ánh vàng làm nổi bật, trở nên rực rỡ và độc đáo. Người thợ gốm nói: 'Vết nứt không làm con mất giá trị, nó làm con trở nên quý giá hơn'. Bài học: Những tổn thương và khuyết điểm trong cuộc sống không làm giảm giá trị của bạn, mà là dấu ấn của sự kiên cường và kinh nghiệm đã giúp bạn trở nên khác biệt."
            },
            {
                "title": "Cái ôm của cây sồi",
                "content": "Một cây sồi già sống trên đỉnh đồi luôn lo lắng về những chiếc lá rụng. Mỗi khi lá vàng, nó đều sợ hãi. Nhưng rồi, nó nhận ra rằng việc rụng lá là cần thiết để nó nghỉ ngơi và chuẩn bị cho sự phát triển mới. Mùa xuân đến, những chiếc lá non xanh mơn mởn mọc ra. Bài học: Buông bỏ những điều đã cũ, dù là nỗi buồn hay thói quen cũ, là cách để tạo không gian cho những điều mới mẻ và tươi đẹp đến với cuộc sống của bạn."
            },
            {
                "title": "Tấm thảm chấp nhận",
                "content": "Một cô gái dệt một tấm thảm. Cô cố gắng làm cho mọi sợi chỉ phải hoàn hảo, nhưng càng cố, thảm càng bị rối và lỗi. Cô thất vọng định vứt đi. Một người phụ nữ lớn tuổi bảo cô lật mặt sau của tấm thảm lại. Mặt sau trông lộn xộn, nhưng cô gái thấy mọi nút thắt, mọi sợi chỉ rối lại tạo thành một bức tranh hoa văn độc đáo, đầy màu sắc. Bài học: Cuộc sống của bạn cũng vậy. Những rắc rối, hỗn độn bạn gặp phải chính là những nút thắt tạo nên vẻ đẹp riêng biệt và sức mạnh nội tại của bạn."
            },
            {
                "title": "Hòn đá và dòng suối",
                "content": "Một hòn đá sắc nhọn nằm trên đường đi của dòng suối. Dòng suối không cố gắng phá vỡ hòn đá, mà nhẹ nhàng chảy qua nó, làm mòn dần những góc cạnh sắc bén. Theo thời gian, hòn đá trở nên tròn trịa và mịn màng, nằm yên bình dưới đáy suối. Bài học: Đừng đấu tranh hay tức giận với những khó khăn. Hãy học cách nhẹ nhàng chấp nhận, và thời gian sẽ làm dịu đi những 'góc cạnh' đau khổ trong tâm hồn bạn."
            },
            {
                "title": "Ánh sáng bên trong",
                "content": "Một ngọn hải đăng rất buồn vì nó không thể chiếu sáng cả đại dương, nó chỉ chiếu sáng được một vùng nhỏ. Một người đi biển nói với nó: 'Nhiệm vụ của con không phải là chiếu sáng cả đại dương, mà là chiếu sáng đủ một vùng để tàu thuyền thấy đường đi'. Bài học: Bạn không cần phải là người hoàn hảo hay giải quyết hết mọi vấn đề. Chỉ cần bạn làm tốt vai trò của mình, mang lại giá trị cho những người xung quanh, bạn đã là một nguồn sáng mạnh mẽ."
            },
            {
                "title": "Bài hát không lời",
                "content": "Một chú chim hót được những giai điệu tuyệt vời nhưng không thể cất lên thành lời. Nó buồn bã cho rằng mình vô dụng. Một nhạc sĩ nghe thấy tiếng hót, ghi lại giai điệu đó và biến nó thành một bản nhạc kinh điển, giúp hàng triệu người được chữa lành. Bài học: Không phải lúc nào bạn cũng cần phải 'nói' hay 'làm' một cách hoàn hảo. Giá trị của bạn nằm ở bản chất, ở sự chân thành mà bạn mang lại, ngay cả khi bạn cảm thấy mình chưa trọn vẹn."
            },
            {
                "title": "Người làm vườn và cỏ dại",
                "content": "Một người làm vườn luôn cố gắng nhổ sạch hết cỏ dại trong khu vườn của mình, nhưng cỏ dại luôn mọc lại. Cô mệt mỏi và chán nản. Một người bạn đến thăm nói: 'Đừng gọi chúng là cỏ dại. Hãy gọi chúng là những bông hoa không mời mà đến'. Bài học: Đôi khi, những điều ta xem là phiền phức hoặc lỗi lầm lại là một phần của bức tranh tổng thể. Học cách chấp nhận sự không hoàn hảo sẽ giúp tâm hồn bạn nhẹ nhàng hơn rất nhiều."
            },
            {
                "title": "Chiếc ô và trận mưa",
                "content": "Một chiếc ô không thể ngăn mưa rơi, nhưng nó giúp bạn không bị ướt. Cuộc sống cũng đầy những 'trận mưa' bất ngờ và khó khăn. Chiếc ô không phải là thứ biến mất cơn mưa, mà là sự kiên cường và những kỹ năng bạn tích lũy để bảo vệ chính mình trong bão tố. Bài học: Đừng cố gắng kiểm soát những gì xảy ra. Thay vào đó, hãy chuẩn bị cho bản thân một 'chiếc ô' vững chắc để đối phó với nó. Bạn có sức mạnh để vượt qua mọi thứ."
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
        st.audio(audio_bytes.read(), format="audio/mpeg")

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
                        st.audio(fp, format="audio/mpeg")
                    except Exception as e:
                        st.error(f"Lỗi khi tạo âm thanh: {e}")
