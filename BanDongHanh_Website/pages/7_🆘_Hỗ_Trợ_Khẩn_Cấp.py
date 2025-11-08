# File: pages/7_🆘_Hỗ_Trợ_Khẩn_Cấp.py (TINH CHỈNH CUỐI CÙNG)
import streamlit as st
import requests
import math
import pandas as pd
import tempfile
from io import BytesIO
from gtts import gTTS
import os
import sys
import numpy as np # Thêm numpy cho các thao tác mảng (nếu cần)

# --- THIẾT LẬP CƠ SỞ DỮ LIỆU/DỊCH VỤ ---

@st.cache_data(ttl=60 * 60 * 24)
def geocode_address(address: str):
    """Chuyển đổi địa chỉ sang tọa độ bằng Nominatim (OpenStreetMap)."""
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1, "addressdetails": 1},
            headers={"User-Agent": "BanDongHanh/1.0 (contact: example@example.com)"},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None

def _build_overpass_query(lat: float, lon: float, radius_m: int, tags: list[str]) -> str:
    """Xây dựng truy vấn Overpass API để tìm các cơ sở y tế gần đó."""
    regex = "|".join(tags)
    # Tên thẻ (amenity) đã được hardcode trong query của bạn, giữ nguyên
    q = f"""
    [out:json][timeout:30];
    (
      node["amenity"~"{regex}"](around:{radius_m},{lat},{lon});
      way["amenity"~"{regex}"](around:{radius_m},{lat},{lon});
      relation["amenity"~"{regex}"](around:{radius_m},{lat},{lon});
    );
    out center 100;
    """
    return q

@st.cache_data(ttl=60 * 10)
def query_overpass(lat: float, lon: float, radius_km: int, amenity_tags: list[str]):
    """Thực hiện truy vấn Overpass API."""
    try:
        radius_m = int(radius_km * 1000)
        query = _build_overpass_query(lat, lon, radius_m, amenity_tags)
        resp = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            headers={"User-Agent": "BanDongHanh/1.0 (contact: example@example.com)"},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("elements", [])
    except Exception:
        return []

def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Tính khoảng cách đường chim bay."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def _parse_osm_elements(elements, center_lat, center_lon):
    """Phân tích cú pháp các phần tử từ Overpass API."""
    results = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name:vi") or tags.get("name") or "Chưa rõ tên"
        amenity_type = tags.get("amenity") or tags.get("healthcare") or "unknown"
        
        # Lấy tọa độ
        lat, lon = None, None
        if el.get("lat") and el.get("lon"):
            lat, lon = el["lat"], el["lon"]
        else:
            center = el.get("center") or {}
            lat, lon = center.get("lat"), center.get("lon")
            
        if lat is None or lon is None:
            continue
            
        # Xây dựng địa chỉ
        address = tags.get("addr:full") or tags.get("addr:street") or tags.get("addr") or ""
        
        dist_km = _haversine_km(center_lat, center_lon, lat, lon)
        results.append({
            "Tên": name,
            "Loại": amenity_type,
            "lat": lat,
            "lon": lon,
            "Khoảng cách (km)": round(dist_km, 2),
            "Địa chỉ": address,
        })
    results.sort(key=lambda x: x["Khoảng cách (km)"])
    return results

def create_audio_file(text):
    """Hàm tạo file âm thanh (giữ lại code gốc của bạn)"""
    if not text or not text.strip():
        return None
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception:
        return None
    
# --- BẢO VỆ TRANG (Nếu bạn đã có logic này ở trang chủ) ---
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() 

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="wide")

# --- CSS (Giữ nguyên) ---
st.markdown("""
<style>
/* ... CSS của bạn ... */
.hotline-container {
    background-color: #FFF0F0;
    border: 2px solid #D9534F;
    border-radius: 15px;
    padding: 40px;
    margin: 25px 0;
    text-align: center;
}
/* ... CSS khác ... */
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.title("🆘 HỖ TRỢ KHẨN CẤP")
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
st.markdown("Khi bạn hoặc ai đó bạn biết đang gặp khủng hoảng, hãy tìm đến sự giúp đỡ ngay lập tức.")
st.write("---")

# --- CẢNH BÁO QUAN TRỌNG (Giữ nguyên) ---
st.markdown("""
<div class="emergency-warning-box">
    <p><strong>ỨNG DỤNG NÀY KHÔNG PHẢI LÀ DỊCH VỤ CẤP CỨU.</strong></p>
    <p>Nếu bạn hoặc người thân đang ở trong tình huống nguy hiểm đến tính mạng, vui lòng gọi <strong class="emergency-number">115</strong> (Cấp cứu y tế) hoặc đến cơ sở y tế gần nhất.</p>
</div>
""", unsafe_allow_html=True)

st.header("Các đường dây nóng hỗ trợ sức khỏe tinh thần tại Việt Nam")

# --- HIỂN THỊ CÁC ĐƯỜNG DÂY NÓNG (Giữ nguyên) ---
st.markdown("""
<div class="hotline-container">
    <p class="hotline-title"><strong>Tổng đài Quốc gia Bảo vệ Trẻ em</strong></p>
    <p class="hotline-number">111</p>
    <p class="hotline-description">Miễn phí, hoạt động 24/7</p>
</div>
""", unsafe_allow_html=True)
# ... (Đường dây 096 357 94 88)

st.write("---")

# --- THÔNG ĐIỆP ĐỘNG VIÊN (Giữ nguyên) ---
st.info(
    """
    **Hãy nhớ rằng:** Việc tìm kiếm sự giúp đỡ là một hành động dũng cảm và mạnh mẽ. Bạn không hề đơn độc.
    """
)

st.write("---")
st.header("🩺 Tra cứu cơ sở y tế gần bạn")
st.markdown("""
Nhập địa chỉ hoặc mô tả vị trí (ví dụ: *"Bến Thành, Quận 1, TP.HCM"*). Ứng dụng sẽ tìm **Bệnh viện**, **Phòng khám**, **Nhà thuốc** và **Bác sĩ** trong bán kính bạn chọn.
""")

# --- INPUTS (Sử dụng lại cấu trúc cột của bạn) ---
col_addr, col_radius = st.columns([2,1])
with col_addr:
    address_input = st.text_input("📍 Địa chỉ của bạn", placeholder="Ví dụ: 1600 Đường Nguyễn Văn Cừ, Quận 5, TP.HCM", key="address_input")
with col_radius:
    radius_km = st.slider("Bán kính (km)", min_value=1, max_value=25, value=10, step=1, key="radius_slider")

# --- DANH MỤC CƠ SỞ Y TẾ (Amenities) ---
facility_map = {
    "Bệnh viện": "hospital",
    "Phòng khám": "clinic",
    "Nhà thuốc": "pharmacy",
    "Bác sĩ": "doctors",
}

selected_facilities = st.multiselect(
    "Loại cơ sở y tế",
    options=list(facility_map.keys()),
    default=["Bệnh viện", "Phòng khám", "Nhà thuốc"],
    help="Chọn một hoặc nhiều loại để lọc kết quả",
    key="facility_multiselect"
)

search_btn = st.button("🔍 Tìm cơ sở gần tôi", type="primary")

# --- LOGIC TÌM KIẾM ---
if search_btn:
    if not address_input.strip():
        st.warning("Vui lòng nhập địa chỉ trước khi tìm kiếm.")
        st.stop()
        
    if not selected_facilities:
        st.warning("Vui lòng chọn ít nhất một loại cơ sở y tế để tìm kiếm.")
        st.stop()
        
    with st.spinner("Đang xác định tọa độ..."):
        # SỬ DỤNG HÀM GEOCODING CỦA BẠN
        coords = geocode_address(address_input.strip())
        
    if not coords:
        st.error("Không tìm được tọa độ cho địa chỉ này. Hãy thử cụ thể hơn hoặc thêm tên tỉnh/thành.")
    else:
        lat, lon = coords
        st.success(f"Đã tìm thấy tọa độ. Đang tìm kiếm cơ sở y tế trong bán kính {radius_km} km...")
        
        amenity_tags = [facility_map[f] for f in selected_facilities]
        
        with st.spinner("Đang truy vấn dữ liệu OpenStreetMap (Overpass)..."):
            raw = query_overpass(lat, lon, radius_km, amenity_tags)
            
        if not raw:
            st.info("Không tìm thấy cơ sở nào hoặc API đang bị quá tải. Thử lại sau ít phút.")
        else:
            parsed = _parse_osm_elements(raw, lat, lon)
            
            if not parsed:
                st.info("Không có kết quả hợp lệ.")
            else:
                st.write(f"Tìm thấy {len(parsed)} cơ sở.")
                df = pd.DataFrame(parsed)
                
                # Sửa lỗi hiển thị bản đồ (Sử dụng tên cột lat/lon đã chuẩn hóa)
                map_df = df[["lat", "lon", "Tên", "Loại", "Khoảng cách (km)"]].copy()
                st.dataframe(df, use_container_width=True)
                
                # Hiển thị bản đồ
                st.map(map_df, latitude="lat", longitude="lon", zoom=13)

                with st.expander("ℹ️ Ghi chú / Disclaimer"):
                    st.markdown("""
                    - Dữ liệu lấy từ OpenStreetMap (cộng đồng) — có thể thiếu hoặc chưa cập nhật.
                    - Nếu không có kết quả: thu nhỏ bán kính hoặc nhập địa chỉ cụ thể hơn.
                    - API Overpass có giới hạn tốc độ: tránh gửi quá nhiều yêu cầu liên tiếp.
                    - Khoảng cách là tính theo đường thẳng (Haversine), thực tế có thể dài hơn.
                    """)
                    
                tts_option = st.checkbox("🔊 Đọc to số lượng kết quả", key="tts_checkbox")
                if tts_option:
                    audio_file = create_audio_file(f"Có {len(parsed)} cơ sở y tế gần bạn trong bán kính {radius_km} km.")
                    if audio_file:
                        with open(audio_file, 'rb') as f:
                            st.audio(f.read(), format='audio/mpeg')
                        try:
                            os.unlink(audio_file)
                        except Exception:
                            pass


