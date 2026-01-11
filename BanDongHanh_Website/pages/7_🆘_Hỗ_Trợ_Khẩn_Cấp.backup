# pages/7_🆘_Hỗ_trợ_khẩn_cấp.py
import streamlit as st
import requests
import math
import pandas as pd
import tempfile
from io import BytesIO
from gtts import gTTS

@st.cache_data(ttl=60 * 60 * 24)
def geocode_address(address: str):
    """
    Tìm tọa độ từ địa chỉ tiếng Việt với nhiều fallback:
    1. Nominatim (primary)
    2. Photon API (fallback cho Streamlit Cloud)
    3. Simplified query với cả 2 services
    """
    import time
    import sys
    
    # --- METHOD 1: Nominatim (OpenStreetMap) ---
    def try_nominatim(query, max_retries=2):
        for attempt in range(max_retries):
            try:
                resp = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": query,
                        "format": "json",
                        "limit": 5,
                        "addressdetails": 1,
                        "countrycodes": "vn",
                    },
                    headers={"User-Agent": "BanDongHanh/1.0 (contact: bandonghanh@streamlit.app)"},
                    timeout=15,
                )
                
                # Check for rate limiting
                if resp.status_code == 429:
                    print(f"[Nominatim] Rate limited, attempt {attempt+1}/{max_retries}", file=sys.stderr)
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    return None
                
                resp.raise_for_status()
                data = resp.json()
                
                if data:
                    best = max(data, key=lambda x: float(x.get("importance", 0)))
                    return float(best["lat"]), float(best["lon"])
            except Exception as e:
                print(f"[Nominatim Error] {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(1)
        return None
    
    # --- METHOD 2: Photon API (Fallback, không có rate limit khắt khe) ---
    def try_photon(query):
        try:
            resp = requests.get(
                "https://photon.komoot.io/api/",
                params={
                    "q": query,
                    "limit": 5,
                    "lang": "vi",
                    "osm_tag": "place",  # Ưu tiên địa danh
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            
            features = data.get("features", [])
            if features:
                # Lọc kết quả có country = Vietnam
                vn_features = [f for f in features if f.get("properties", {}).get("country") == "Việt Nam"]
                if not vn_features:
                    vn_features = features  # Fallback all results
                
                # Chọn feature đầu tiên (relevance cao nhất)
                coords = vn_features[0]["geometry"]["coordinates"]
                return float(coords[1]), float(coords[0])  # Photon trả [lon, lat]
        except Exception as e:
            print(f"[Photon Error] {e}", file=sys.stderr)
        return None
    
    # --- TRY FULL ADDRESS ---
    result = try_nominatim(address)
    if result:
        return result
    
    # Fallback to Photon
    result = try_photon(address)
    if result:
        return result
    
    # --- TRY SIMPLIFIED ADDRESS (last 2 parts) ---
    parts = [p.strip() for p in address.split(",")]
    if len(parts) > 1:
        simple_query = ", ".join(parts[-2:])
        if simple_query != address:
            result = try_nominatim(simple_query)
            if result:
                return result
            
            result = try_photon(simple_query)
            if result:
                return result
    
    # --- TRY CITY/PROVINCE ONLY (last part) ---
    if len(parts) > 0:
        city_only = parts[-1].strip()
        result = try_nominatim(city_only)
        if result:
            return result
        
        result = try_photon(city_only)
        if result:
            return result
    
    print(f"[Geocoding Failed] All methods exhausted for: {address}", file=sys.stderr)
    return None

def _build_overpass_query(lat: float, lon: float, radius_m: int, tags: list[str]) -> str:
    regex = "|".join(tags)
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
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def _parse_osm_elements(elements, center_lat, center_lon):
    results = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:vi") or "Chưa rõ tên"
        amenity_type = tags.get("amenity") or tags.get("healthcare") or "unknown"
        if "lat" in el and "lon" in el:
            lat, lon = el["lat"], el["lon"]
        else:
            center = el.get("center") or {}
            lat, lon = center.get("lat"), center.get("lon")
        if lat is None or lon is None:
            continue
        addr_parts = []
        for k in ["addr:full", "addr:housenumber", "addr:street", "addr:suburb", "addr:city", "addr:district", "addr:state"]:
            if tags.get(k):
                addr_parts.append(tags[k])
        address = ", ".join(addr_parts) if addr_parts else tags.get("addr", "") or ""
        dist_km = _haversine_km(center_lat, center_lon, lat, lon)
        results.append({
            "Tên": name,
            "Loại": amenity_type,
            "lat": lat,
            "lon": lon,
            "Khoảng cách (km)": round(dist_km, 2),
            "Địa chỉ": address,
        })
    results.sort(key=lambda x: x["Khoảng cách (km)"])  # gần nhất lên đầu
    return results

def create_audio_file(text):
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception:
        return None
  
# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="wide")

# --- CSS HOÀN CHỈNH VÀ SẠCH SẼ ---
st.markdown("""
<style>
/* --- CSS CHO KHUNG HOTLINE --- */
.hotline-container {
    background-color: #FFF0F0;
    border: 2px solid #D9534F;
    border-radius: 15px;
    padding: 40px;
    margin: 25px 0;
    text-align: center;
}
.hotline-title {
    font-size: 1.5rem !important;
    font-weight: 700;
    display: block;
    margin-bottom: 1rem;
    color: #333;
}
.hotline-description {
    font-size: 1.3rem !important;
    margin-top: 1rem;
    color: #555;
}

/* --- CSS CHO KHUNG CẢNH BÁO 115 --- */
.emergency-warning-box {
    background-color: #FFF0F0;
    border: 2px solid #D9534F;
    border-radius: 15px;
    padding: 40px;
    margin: 25px 0;
}
.emergency-warning-box p {
    font-size: 1.3rem;
    text-align: center;
    margin-bottom: 1rem;
}
.emergency-warning-box strong {
    font-size: 1.5rem;
    display: block;
    margin-bottom: 1rem;
}

/* --- CSS CHUNG ĐỂ CÁC SỐ GIỐNG HỆT NHAU --- */
.hotline-number, .emergency-number {
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 1.8rem !important;
    font-weight: 900 !important;
    color: #D9534F !important;
    letter-spacing: 3px !important;
    display: inline-block; /* Giúp hiển thị ổn định hơn */
}
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.title("🆘 HỖ TRỢ KHẨN CẤP")
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
st.markdown("Khi bạn hoặc ai đó bạn biết đang gặp khủng hoảng, hãy tìm đến sự giúp đỡ ngay lập tức.")
st.write("---")

# --- CẢNH BÁO QUAN TRỌNG ---
st.markdown("""
<div class="emergency-warning-box">
    <p><strong>ỨNG DỤNG NÀY KHÔNG PHẢI LÀ DỊCH VỤ CẤP CỨU.</strong></p>
    <p>Nếu bạn hoặc người thân đang ở trong tình huống nguy hiểm đến tính mạng, vui lòng gọi <strong class="emergency-number">115</strong> (Cấp cứu y tế) hoặc đến cơ sở y tế gần nhất.</p>
</div>
""", unsafe_allow_html=True)

st.header("Các đường dây nóng hỗ trợ sức khỏe tinh thần tại Việt Nam")

# --- HIỂN THỊ CÁC ĐƯỜNG DÂY NÓNG ---
st.markdown("""
<div class="hotline-container">
    <p class="hotline-title"><strong>Tổng đài Quốc gia Bảo vệ Trẻ em</strong></p>
    <p class="hotline-number">111</p>
    <p class="hotline-description">Miễn phí, hoạt động 24/7</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hotline-container">
    <p class="hotline-title"><strong>Đường dây nóng Ngày Mai</strong></p>
    <p class="hotline-number">096 357 94 88</p>
    <p class="hotline-description">Hỗ trợ người trầm cảm và các vấn đề sức khỏe tinh thần</p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# --- THÔNG ĐIỆP ĐỘNG VIÊN ---
st.info(
    """
    **Hãy nhớ rằng:** Việc tìm kiếm sự giúp đỡ là một hành động dũng cảm và mạnh mẽ. Bạn không hề đơn độc.
    """
)

st.write("---")
st.header("🩺 Tra cứu cơ sở y tế gần bạn")
st.markdown("""
Nhập địa chỉ hoặc mô tả vị trí. Ứng dụng sẽ tìm **Bệnh viện**, **Phòng khám**, **Nhà thuốc** và **Bác sĩ** trong bán kính bạn chọn.

**Mẹo:** Nhập tên quận/huyện và tỉnh/thành cho kết quả tốt nhất (ví dụ: *"Quận 1, TP.HCM"*, *"Hoàn Kiếm, Hà Nội"*)
""")

# CSS bổ sung cho mobile responsive
st.markdown("""
<style>
@media (max-width: 640px) {
  .hotline-container, .emergency-warning-box {padding: 24px !important;}
  .hotline-title {font-size:1.2rem !important;}
  .hotline-description {font-size:1.05rem !important;}
  .hotline-number, .emergency-number {font-size:1.4rem !important; letter-spacing:2px !important;}
}
</style>
""", unsafe_allow_html=True)

col_addr, col_radius = st.columns([2,1])
with col_addr:
    address_input = st.text_input("📍 Địa chỉ của bạn", placeholder="Ví dụ: Quận 1, TP.HCM hoặc Hoàn Kiếm, Hà Nội")
with col_radius:
    radius_km = st.slider("Bán kính (km)", min_value=1, max_value=25, value=10, step=1)

# Địa chỉ mẫu để test nhanh
with st.expander("💡 Địa chỉ mẫu để thử nghiệm"):
    st.markdown("""
    **TP. Hồ Chí Minh:**
    - `Quận 1, TP.HCM`
    - `Bến Thành, Quận 1, TP.HCM`
    - `Thủ Đức, TP.HCM`
    
    **Hà Nội:**
    - `Hoàn Kiếm, Hà Nội`
    - `Hồ Gươm, Hà Nội`
    - `Cầu Giấy, Hà Nội`
    
    **Đà Nẵng:**
    - `Hải Châu, Đà Nẵng`
    - `Cầu Rồng, Đà Nẵng`
    
    **Khác:**
    - `Huế` | `Nha Trang` | `Cần Thơ` | `Vũng Tàu`
    """)

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
    help="Chọn một hoặc nhiều loại để lọc kết quả"
)

# Debug mode toggle (ẩn trong expander)
debug_mode = st.checkbox("🔧 Chế độ debug (hiển thị chi tiết API)", value=False)

search_btn = st.button("🔍 Tìm cơ sở gần tôi", type="primary")
if search_btn:
    if not address_input.strip():
        st.warning("Vui lòng nhập địa chỉ trước khi tìm kiếm.")
    else:
        status_placeholder = st.empty()
        if debug_mode:
            status_placeholder.info("🔄 Đang thử Nominatim API...")
        
        with st.spinner("Đang xác định tọa độ (thử nhiều API)..."):
            coords = geocode_address(address_input.strip())
        
        if debug_mode:
            status_placeholder.empty()
        if not coords:
            st.error("❌ Không tìm được tọa độ cho địa chỉ này.")
            st.warning("""
            **Có thể do:**
            - API geocoding đang quá tải hoặc bị rate limit trên Streamlit Cloud
            - Địa chỉ không đủ cụ thể hoặc không tồn tại trong bản đồ OpenStreetMap
            """)
            st.info("""
            **Gợi ý khắc phục:**
            
            1️⃣ **Thử các địa chỉ đơn giản hơn:**
            - `Quận 1, TP.HCM` hoặc `Quận 1, Hồ Chí Minh`
            - `Hoàn Kiếm, Hà Nội`
            - `Đà Nẵng` (chỉ tên thành phố)
            
            2️⃣ **Hoặc thử các địa điểm nổi tiếng:**
            - `Bến Thành, TP.HCM`
            - `Hồ Gươm, Hà Nội`
            - `Cầu Rồng, Đà Nẵng`
            
            3️⃣ **Nếu vẫn lỗi:** Đợi vài phút rồi thử lại (có thể API đang bị giới hạn tạm thời)
            """)
        else:
            lat, lon = coords
            st.success(f"Tọa độ: {lat:.5f}, {lon:.5f}")
            amenity_tags = [facility_map[f] for f in selected_facilities] or list(facility_map.values())
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
                    st.dataframe(df, use_container_width=True)
                    map_df = df[["lat", "lon"]].copy()
                    st.map(map_df, latitude="lat", longitude="lon")

                    with st.expander("ℹ️ Ghi chú / Disclaimer"):
                        st.markdown("""
                        - Dữ liệu lấy từ OpenStreetMap (cộng đồng) — có thể thiếu hoặc chưa cập nhật.
                        - Nếu không có kết quả: thu nhỏ bán kính hoặc nhập địa chỉ cụ thể hơn.
                        - API Overpass có giới hạn tốc độ: tránh gửi quá nhiều yêu cầu liên tiếp.
                        - Khoảng cách là tính theo đường thẳng (Haversine), thực tế có thể dài hơn.
                        """)

                    tts_option = st.checkbox("🔊 Đọc to số lượng kết quả")
                    if tts_option:
                        audio_file = create_audio_file(f"Có {len(parsed)} cơ sở y tế gần bạn trong bán kính {radius_km} km.")
                        if audio_file:
                            with open(audio_file, 'rb') as f:
                                st.audio(f.read(), format='audio/mpeg')
                            try:
                                import os
                                os.unlink(audio_file)
                            except Exception:
                                pass



