# 🤖 Bạn Đồng Hành - Student Mental Health Chatbot

**Bạn Đồng Hành** là một ứng dụng chatbot hỗ trợ sức khỏe tinh thần dành cho học sinh, được xây dựng bằng Streamlit với tích hợp AI tiên tiến.

## ✨ Tính Năng Chính

### 🤖 Trò Chuyện Thông Minh (Enhanced Chat)
- **Tích hợp OpenAI GPT**: Hỗ trợ các mô hình GPT-4o, GPT-4o-mini với khả năng đa phương thức
- **Hỗ trợ ảnh**: Gửi và phân tích hình ảnh trong cuộc trò chuyện  
- **Bộ nhớ dài hạn**: Ghi nhớ ngữ cảnh và lịch sử hội thoại qua các phiên
- **Giao diện thân thiện**: Dark/Light mode, responsive design
- **Tính năng xuất dữ liệu**: Export lịch sử chat và bộ nhớ
- **Gợi ý nhanh**: Câu hỏi mẫu để bắt đầu cuộc trò chuyện

### 🎯 Các Module Hỗ Trợ Khác
- **💖 Trang chủ**: Giới thiệu và điều hướng
- **✨ Liều thuốc tinh thần**: Nội dung động viên và khích lệ
- **🧘 Góc an yên**: Hướng dẫn thư giãn và mindfulness  
- **🍯 Lọ biết ơn**: Ghi nhận những điều tích cực
- **🎨 Bảng màu cảm xúc**: Theo dõi và biểu đạt cảm xúc
- **🎮 Nhanh tay lẹ mắt**: Trò chơi thư giãn
- **❤️ Góc nhỏ**: Không gian riêng tư chia sẻ
- **🆘 Hỗ trợ khẩn cấp**: Thông tin liên hệ hỗ trợ
- **📖 Người kể chuyện**: Câu chuyện và bài học cuộc sống

## 🚀 Cài Đặt và Chạy Ứng Dụng

### 📋 Yêu Cầu Hệ Thống
- Python 3.8+
- pip (Python package manager)
- Kết nối internet (cho API calls)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Wateristhat/Chatbot-for-student-.git
cd Chatbot-for-student-/BanDongHanh_Website
```

### 2️⃣ Tạo Môi Trường Ảo (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Cài Đặt Dependencies

#### Cài đặt đầy đủ (khuyến nghị):
```bash
pip install -r requirements.txt
```

#### Cài đặt tối thiểu (chỉ chat cơ bản):
```bash
pip install -r requirements-min.txt
```

### 4️⃣ Cấu Hình Môi Trường

Sao chép file `.env.example` thành `.env` và cấu hình:
```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với các thông tin sau:

```env
# ================== BẮTT BUỘC ==================
# OpenAI API Key (lấy từ: https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-your-openai-api-key-here

# ================== TÙY CHỌN ==================
# Google AI API Key (cho Gemini models)
GOOGLE_API_KEY=your-google-ai-api-key-here

# App environment
APP_ENV=development
APP_SECRET_KEY=your-secret-key-here
```

### 5️⃣ Chạy Ứng Dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## 🔧 Cấu Hình Nâng Cao

### 🎯 Chỉ sử dụng OpenAI GPT
Cần thiết: `OPENAI_API_KEY` trong file `.env`
- Hỗ trợ: GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- Tính năng: Chat text + image, memory, export

### 🌟 Tích hợp Google Services (Tùy chọn)

#### Google Gemini AI:
```env
GOOGLE_API_KEY=your-google-ai-api-key-here
```

#### Google Cloud Services:
```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
ENABLE_TTS=true
ENABLE_TRANSLATE=true
```

### 📊 Logging Configuration
```env
LOG_LEVEL=INFO
ENABLE_RICH_LOGGING=true
```

## 📁 Cấu Trúc Thư Mục

```
BanDongHanh_Website/
├── app.py                 # Main Streamlit application
├── pages/                 # Streamlit pages
│   ├── 0_💖_Trang_chủ.py
│   ├── 8_💬_Trò_chuyện.py  # Enhanced chat feature
│   └── ...               # Other feature pages
├── data/                  # Data storage
│   ├── .gitkeep          # Ensures directory tracking
│   └── memory_chat.json  # Chat memory (auto-created)
├── utils/                 # Utility modules
│   ├── image_utils.py    # Image processing utilities
│   └── logging_utils.py  # Logging configuration
├── providers/            # AI provider modules
│   ├── openai_provider.py    # OpenAI integration
│   └── memory_utils.py       # Memory management
├── scripts/              # Maintenance scripts
│   └── cleanup_memory.py     # Memory management script
├── requirements.txt      # Full dependencies
├── requirements-min.txt  # Minimal dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md           # This file
```

## 🛠️ Quản Lý Bộ Nhớ

Ứng dụng có script tiện ích để quản lý bộ nhớ chat:

```bash
# Xem thống kê bộ nhớ
python scripts/cleanup_memory.py --stats

# Tạo backup bộ nhớ
python scripts/cleanup_memory.py --backup

# Xóa bộ nhớ (có tạo backup tự động)
python scripts/cleanup_memory.py --clear

# Xem danh sách backup
python scripts/cleanup_memory.py --list-backups

# Khôi phục từ backup
python scripts/cleanup_memory.py --restore backup_file.json

# Dọn dẹp backup cũ
python scripts/cleanup_memory.py --cleanup-old --keep-days 7
```

## 🧪 Testing và Development

### Kiểm tra cài đặt tối thiểu:
```bash
pip install -r requirements-min.txt
streamlit run app.py
```

### Test các module:
```bash
# Test image utilities
python -c "from utils.image_utils import compress_image; print('Image utils OK')"

# Test OpenAI provider
python -c "from providers.openai_provider import OpenAIProvider; print('OpenAI provider OK')"

# Test memory utilities  
python -c "from providers.memory_utils import MemoryManager; print('Memory utils OK')"

# Test logging utilities
python -c "from utils.logging_utils import setup_basic_logging; print('Logging utils OK')"
```

## 🔐 Bảo Mật và Quyền Riêng Tư

### 🛡️ Bảo Mật Dữ Liệu
- **API Keys**: Được lưu trong file `.env` (không commit lên Git)
- **Chat Memory**: Lưu trữ cục bộ trong `data/memory_chat.json` (bị ignore bởi Git)
- **Logs**: Không lưu nội dung chat nhạy cảm
- **Session State**: Chỉ tồn tại trong phiên browser hiện tại

### 🔒 Thông Tin Quan Trọng
- **KHÔNG** chia sẻ API keys với người khác
- **KHÔNG** commit file `.env` lên repository public
- Dữ liệu chat được lưu cục bộ và không gửi đến server nào khác ngoài OpenAI/Google APIs
- Ứng dụng chỉ lưu tóm tắt ngữ cảnh, không lưu toàn bộ hội thoại chi tiết

### 📜 Disclaimer
- Ứng dụng **KHÔNG** thay thế tư vấn tâm lý chuyên nghiệp
- Không sử dụng để chẩn đoán hoặc điều trị y khoa
- Trong trường hợp khẩn cấp, hãy liên hệ với các dịch vụ hỗ trợ chuyên nghiệp

## 🆘 Hỗ Trợ Khẩn Cấp

**Nếu bạn đang gặp nguy hiểm hoặc có ý định tự hại, hãy liên hệ ngay:**

📞 **Đường dây nóng 24/7:**
- Tổng đài tư vấn tâm lý: **1900 0123**
- Cấp cứu: **115**
- Công an: **113**

🌐 **Hỗ trợ trực tuyến:**
- Website tư vấn tâm lý: [https://dinhhuongvietnam.org](https://dinhhuongvietnam.org)
- Chat hỗ trợ: Messenger "Định Hướng Việt"

## 🐛 Troubleshooting

### Lỗi thường gặp:

#### 1. "No module named 'openai'"
```bash
pip install openai
# hoặc
pip install -r requirements.txt
```

#### 2. "OpenAI API key not found"
- Kiểm tra file `.env` có tồn tại và có `OPENAI_API_KEY`
- Đảm bảo API key hợp lệ từ OpenAI Platform

#### 3. "Memory file permission error"
```bash
# Tạo thư mục data nếu chưa có
mkdir -p data
chmod 755 data
```

#### 4. "Streamlit app không khởi động"
- Kiểm tra Python version >= 3.8
- Cài đặt lại Streamlit: `pip install --upgrade streamlit`

#### 5. "Rich logging không hoạt động"
```bash
pip install rich
```

### Log files:
- Xem logs trong thư mục `logs/` (nếu được cấu hình)
- Check console output khi chạy `streamlit run app.py`

## 🤝 Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📝 License

Dự án này được phân phối dưới license MIT. Xem file `LICENSE` để biết chi tiết.

## 📞 Liên Hệ

- **GitHub**: [Wateristhat](https://github.com/Wateristhat)
- **Repository**: [Chatbot-for-student-](https://github.com/Wateristhat/Chatbot-for-student-)

---

### 💝 Lời Cảm Ơn

Cảm ơn bạn đã sử dụng **Bạn Đồng Hành**! Hy vọng ứng dụng này sẽ mang lại giá trị tích cực cho hành trình phát triển của bạn.

**Hãy nhớ**: Bạn không đơn độc, và luôn có người sẵn sàng lắng nghe và hỗ trợ bạn! 💚