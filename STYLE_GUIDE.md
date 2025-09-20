# Style Guide - Hướng Dẫn Chỉnh Sửa Giao Diện

## Font và Typography

### Font Chính - Quicksand
Tất cả các trang nên sử dụng font Quicksand để đảm bảo tính nhất quán:

```css
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; }
```

### Kích Thước Font
- **Tiêu đề chính**: `font-size: 3rem;` (48px)
- **Tiêu đề phụ**: `font-size: 2rem;` (32px)  
- **Nội dung thông điệp**: `font-size: 1.3rem;` (20.8px)
- **Văn bản thường**: `font-size: 1.2rem;` (19.2px)
- **Văn bản nhỏ**: `font-size: 1.1rem;` (17.6px)

### Font Weight
- **Tiêu đề quan trọng**: `font-weight: 700;` (Bold)
- **Tiêu đề phụ**: `font-weight: 600;` (SemiBold)  
- **Nhấn mạnh**: `font-weight: 500;` (Medium)
- **Văn bản thường**: `font-weight: 400;` (Regular)

## Màu Sắc

### Màu Chủ Đạo
- **Gradient chính**: `linear-gradient(45deg, #FFD700, #FFA500, #FF69B4)`
- **Màu accent**: `#4169E1` (Royal Blue)
- **Màu thành công**: `#32CD32` (Lime Green)
- **Màu cảnh báo**: `#FFB6C1` (Light Pink)

### Màu Nền
- **Nền chính**: `linear-gradient(135deg, #FFE4E1, #F0F8FF)`
- **Nền timeline**: `linear-gradient(135deg, #FFF8DC, #FFFACD)`
- **Nền gợi ý**: `linear-gradient(135deg, #E6E6FA, #F5F5DC)`

## Layout và Spacing

### Border Radius
- **Thẻ lớn**: `border-radius: 20px;`
- **Thẻ trung bình**: `border-radius: 15px;`
- **Nút tròn**: `border-radius: 50%;`
- **Nút thường**: `border-radius: 25px;`

### Padding và Margin
- **Padding thẻ lớn**: `padding: 2rem 1.3rem;`
- **Padding thẻ trung bình**: `padding: 1.5rem;`
- **Margin giữa thành phần**: `margin: 1rem 0;`

### Box Shadow
- **Shadow nhẹ**: `box-shadow: 0 3px 10px rgba(0,0,0,0.1);`
- **Shadow trung bình**: `box-shadow: 0 4px 15px rgba(0,0,0,0.2);`
- **Shadow nổi bật**: `box-shadow: 0 6px 20px rgba(0,0,0,0.3);`

## Animation và Hiệu Ứng

### Transition Cơ Bản
```css
transition: all 0.3s ease;
```

### Hover Effects
```css
:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
```

### Animation Nhẹ Nhàng
```css
@keyframes gentle-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}
animation: gentle-pulse 3s ease-in-out infinite;
```

## Responsive Design

### Media Queries
```css
@media (max-width: 700px) {
    .main-title { font-size: 2rem; }
    .content-text { font-size: 1rem; }
    padding: 0.8rem 0.4rem;
}
```

## Quy Tắc Chung

### 1. Nhất Quán Font
- Tất cả các trang sử dụng Quicksand
- Tránh trộn lẫn nhiều font khác nhau

### 2. Màu Sắc Hài Hòa  
- Giữ palette màu nhất quán
- Sử dụng gradient để tạo sự sang trọng

### 3. Kích Thước Phù Hợp
- Font đủ lớn cho học sinh đọc dễ dàng
- Khoảng cách hợp lý giữa các thành phần

### 4. Accessibility
- Đảm bảo contrast đủ cao
- Font size không nhỏ hơn 1rem
- Focus states rõ ràng cho keyboard navigation

## Ví Dụ Áp Dụng

### Cập Nhật Font Cho Trang Mới
```python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; }

.main-title {
    font-family: 'Quicksand', Arial, sans-serif;
    font-size: 3rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)
```

### CSS Class Chuẩn
```css
.content-card {
    font-family: 'Quicksand', Arial, sans-serif;
    font-size: 1.2rem;
    background: linear-gradient(135deg, #FFE4E1, #F0F8FF);
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}
```

Hướng dẫn này đảm bảo tính nhất quán và chuyên nghiệp cho toàn bộ ứng dụng.