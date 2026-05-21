import streamlit as st
import pandas as pd
import plotly.express as px

# ═════════════════════════════════════════════════════════════════════
# KONFIGURASI & CUSTOM CSS - DARK GREEN NEON UI
# ═════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgriYield - Estimasi Hasil Panen",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(145deg, #0a0f14 0%, #0d1419 50%, #0a0f14 100%);
    font-family: 'Outfit', sans-serif;
}

h1, h2, h3, h4, h5, h6, .stMarkdown {
    font-family: 'Outfit', sans-serif !important;
}

.app-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #00ff87 0%, #00d4aa 50%, #00ff87 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}

.subtitle {
    color: #5eead4 !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    opacity: 0.8;
}

.section-title {
    color: #00ff87 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1218 0%, #0a0f14 100%) !important;
    border-right: 1px solid #1a2a24 !important;
    padding: 1rem !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #00ff87 !important;
}

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 0;
    border-bottom: 1px solid #1a2a24;
    margin-bottom: 1.5rem;
}

.sidebar-brand .emoji {
    font-size: 4rem;
    background: linear-gradient(135deg, #00ff87, #00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 20px rgba(0, 255, 135, 0.3));
}

.sidebar-brand h2 {
    font-family: 'Space Grotesk', sans-serif;
    background: linear-gradient(90deg, #00ff87, #5eead4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0 0 0;
    font-weight: 700;
}

.sidebar-brand p {
    color: #5eead4;
    font-size: 0.75rem;
    margin: 0;
    opacity: 0.7;
}

.stSelectbox > div > div,
.stNumberInput > div > div > div > input {
    background: rgba(10, 20, 16, 0.8) !important;
    border: 1px solid #1a2a24 !important;
    border-radius: 10px !important;
    color: #e0fff4 !important;
    font-family: 'Outfit', sans-serif !important;
}

.stSelectbox > div > div:hover,
.stNumberInput > div > div > div > input:hover {
    border-color: #00ff87 !important;
    box-shadow: 0 0 15px rgba(0, 255, 135, 0.15) !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    color: #5eead4 !important;
    font-size: 0.85rem !important;
}

.stSlider [data-testid="stSliderTrack"] {
    background: #1a2a24 !important;
}

.stSlider [data-testid="stSliderThumb"] {
    background: #00ff87 !important;
    border: 2px solid #00ff87 !important;
    box-shadow: 0 0 10px rgba(0, 255, 135, 0.5) !important;
}

.stSlider > div > label {
    color: #5eead4 !important;
    font-size: 0.85rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00cc6a 0%, #00ff87 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(0, 255, 135, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(0, 255, 135, 0.4) !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(10, 20, 16, 0.9) 0%, rgba(15, 25, 20, 0.9) 100%);
    border: 1px solid #1a2a24;
    border-radius: 16px;
    padding: 1.25rem;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #00ff87;
    box-shadow: 0 0 25px rgba(0, 255, 135, 0.15);
}

[data-testid="stMetricLabel"] {
    color: #5eead4 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    color: #00ff87 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stAlert {
    background: rgba(10, 20, 16, 0.9) !important;
    border: 1px solid #1a2a24 !important;
    border-radius: 10px !important;
}

.stDivider {
    border-color: #1a2a24 !important;
}

[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(10, 20, 16, 0.9) 0%, rgba(15, 25, 20, 0.9) 100%);
    border: 1px solid #1a2a24;
    border-radius: 16px;
    padding: 1rem;
}

.footer-caption {
    color: #5eead4 !important;
    opacity: 0.5;
    font-size: 0.75rem !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #0a0f14;
}
::-webkit-scrollbar-thumb {
    background: #1a2a24;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #00ff87;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# DATA - DATABASE TANAMAN
# ═══════════════════════════════════════════════════════════════════
DATA_TANAMAN = {
    "Jagung": {
        "varietas": {
            "Hibrida":  {"base": 7.0,  "pupuk_opt": 300},
            "Unggul":   {"base": 5.94, "pupuk_opt": 250},
            "Lokal":    {"base": 4.0,  "pupuk_opt": 200},
        },
        "suhu_opt": (20, 30),
        "satuan": "ton/ha",
    },
    "Padi": {
        "varietas": {
            "Unggul":  {"base": 6.5,  "pupuk_opt": 250},
            "Lokal":   {"base": 5.29, "pupuk_opt": 200},
            "Hibrida": {"base": 8.0,  "pupuk_opt": 280},
        },
        "suhu_opt": (24, 32),
        "satuan": "ton GKP/ha",
    },
    "Kedelai": {
        "varietas": {
            "Unggul":  {"base": 2.2,  "pupuk_opt": 100},
            "Lokal":   {"base": 1.62, "pupuk_opt": 80},
            "Hibrida": {"base": 2.8,  "pupuk_opt": 120},
        },
        "suhu_opt": (22, 32),
        "satuan": "ton/ha",
    },
    "Singkong": {
        "varietas": {
            "Unggul":  {"base": 26.17, "pupuk_opt": 200},
            "Lokal":   {"base": 17.0,  "pupuk_opt": 150},
            "Hibrida": {"base": 30.0,  "pupuk_opt": 220},
        },
        "suhu_opt": (25, 35),
        "satuan": "ton/ha",
    },
    "Cabai": {
        "varietas": {
            "Unggul":  {"base": 8.77, "pupuk_opt": 150},
            "Lokal":   {"base": 5.0,   "pupuk_opt": 100},
            "Hibrida": {"base": 11.0, "pupuk_opt": 180},
        },
        "suhu_opt": (25, 32),
        "satuan": "ton/ha",
    },
}

JARAK_TANAM = {
    "75 x 50 cm (optimal)": 1.0,
    "70 x 40 cm":           0.92,
    "70 x 25 cm":           0.82,
}

KEDALAMAN_TANAM = {
    "5 cm (optimal)": 1.0,
    "3 cm":           0.93,
    "7 cm":           0.91,
    "8 cm":           0.87,
}

# ═══════════════════════════════════════════════════════════════════
# FUNGSI PERHITUNGAN
# ═══════════════════════════════════════════════════════════
def hitung_estimasi(tanaman, varietas, luas, ph, irigasi, musim, suhu, pupuk, jarak_mod, kedalaman_mod):
    base = DATA_TANAMAN[tanaman]["varietas"][varietas]["base"]
    pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
    suhu_opt = DATA_TANAMAN[tanaman]["suhu_opt"]
    
    # Faktor pH Tanah
    if 6.0 <= ph <= 7.0:
        f_ph, ket_ph = 1.0, "Optimal"
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        f_ph, ket_ph = 0.88, "Kurang ideal"
    else:
        f_ph, ket_ph = 0.72, "Tidak ideal"
    
    # Faktor Irigasi
    f_ir = {"Teknis / pompa": 1.0, "Setengah teknis": 0.88, "Tadah hujan": 0.72}[irigasi]
    
    # Faktor Musim
    f_ms = {"Musim hujan": 1.0, "Transisi": 0.90, "Musim kemarau": 0.78}[musim]
    
    # Faktor Suhu
    mn, mx = suhu_opt
    if mn <= suhu <= mx:
        f_su = 1.0
    elif suhu < mn-5 or suhu > mx+5:
        f_su = 0.75
    else:
        f_su = 0.88
    
    # Faktor Pupuk
    rasio = pupuk / pupuk_opt
    if 0.8 <= rasio <= 1.2:
        f_pu = 1.0
    elif rasio < 0.5:
        f_pu = 0.75
    else:
        f_pu = 0.92
    
    # Perhitungan Total
    produktivitas = base * f_ph * f_ir * f_ms * f_su * f_pu * jarak_mod * kedalaman_mod
    total = produktivitas * luas
    persen = (produktivitas / base) * 100
    
    faktor = {
        "pH tanah": round(f_ph * 100),
        "Irigasi": round(f_ir * 100),
        "Musim tanam": round(f_ms * 100),
        "Suhu udara": round(f_su * 100),
        "Pemupukan": round(f_pu * 100),
        "Jarak tanam": round(jarak_mod * 100),
        "Kedalaman tanam": round(kedalaman_mod * 100),
    }
    
    return round(produktivitas, 2), round(total, 2), round(persen, 1), faktor, ket_ph

# ═══════════════════════════════════════════════════════════════════
# TAMPILAN UTAMA
# ═══════════════════════════════════════════════════════════════════
st.markdown('<p class="app-title">🌽 AgriYield</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pertanian Presisi Berbasis AI — Estimasi Hasil Panen</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR - AREA INPUT
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="emoji">🌽</div>
            <h2>AgriYield</h2>
            <p>Precision Agriculture</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 **Data Input**")
    
    tanaman = st.selectbox("Jenis Tanaman", list(DATA_TANAMAN.keys()))
    varietas = st.selectbox("Varietas", list(DATA_TANAMAN[tanaman]["varietas"].keys()))
    luas = st.number_input("Luas Lahan (ha)", 0.1, 100.0, 1.0, step=0.1)
    
    st.markdown("---")
    st.markdown("### 🌱 **Kondisi Lahan**")
    
    ph = st.slider("pH Tanah", 4.0, 9.0, 6.5, 0.1)
    irigasi = st.selectbox("Sistem Irigasi", ["Teknis / pompa", "Setengah teknis", "Tadah hujan"])
    musim = st.selectbox("Musim Tanam", ["Musim hujan", "Transisi", "Musim kemarau"])
    suhu = st.slider("Suhu (°C)", 15, 40, 28)
    pupuk = st.number_input("Dosis Pupuk (kg/ha)", 0, 500, DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"])
    
    jarak_mod, kedalaman_mod = 1.0, 1.0
    
    if tanaman == "Jagung":
        st.markdown("---")
        st.markdown("### 🌽 **Pengaturan Khusus Jagung**")
        jarak = st.selectbox("Jarak Tanam", list(JARAK_TANAM.keys()))
        jarak_mod = JARAK_TANAM[jarak]
        kedalaman = st.selectbox("Kedalaman Tanam", list(KEDALAMAN_TANAM.keys()))
        kedalaman_mod = KEDALAMAN_TANAM[kedalaman]
    
    st.markdown("---")
    hitung = st.button("🔍 Hitung Estimasi", use_container_width=True, type="primary")

# ═══════════════════════════════════════════════════════════════════
# AREA HASIL
# ═══════════════════════════════════════════════════════════════════
if hitung:
    prod, total, persen, faktor, ket_ph = hitung_estimasi(
        tanaman, varietas, luas, ph, irigasi, musim, suhu, pupuk, jarak_mod, kedalaman_mod
    )
    satuan = DATA_TANAMAN[tanaman]["satuan"]
    
    st.markdown("### 📊 **Hasil Estimasi Panen**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Produktivitas", f"{prod} {satuan}")
    with col2:
        st.metric("Total Produksi", f"{total} ton")
    with col3:
        kat = "🟢 Sangat baik" if persen >= 85 else ("🟡 Cukup baik" if persen >= 65 else "🔴 Perlu perbaikan")
        st.metric("Capaian Potensi", f"{persen}%", kat)
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 📈 **Analisis Faktor**")
        df = pd.DataFrame({"Faktor": list(faktor.keys()), "Skor (%)": list(faktor.values())})
        fig = px.bar(df, x="Skor (%)", y="Faktor", orientation="h",
                     color="Skor (%)", color_continuous_scale=["#0d2920", "#00ff87"], range_x=[0, 100])
        fig.update_layout(showlegend=False, height=320, margin=dict(l=0, r=0, t=10, b=0),
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         font_color="#5eead4")
        fig.update_traces(marker=dict(line=dict(color="#00ff87", width=1)))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("### 💡 **Rekomendasi**")
        pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
        ada_rek = False
        
        if ket_ph != "Optimal":
            st.warning(f"⚠️ pH tanah {ket_ph}. Lakukan pengapuran (pH<6) atau pengasaman (pH>7).")
            ada_rek = True
        if pupuk < pupuk_opt * 0.8:
            st.warning(f"⚠️ Dosis pupuk kurang. Rekomendasi: {pupuk_opt} kg/ha.")
            ada_rek = True
        if irigasi == "Tadah hujan":
            st.info("💧 Pertimbangkan irigasi teknis untuk hasil lebih stabil.")
            ada_rek = True
        if musim == "Musim kemarau":  # ← FIX: musik → musim
            st.warning("⚠️ Tanam kemarau berisiko. Pastikan pasokan air tercukupi.")
            ada_rek = True
        if tanaman == "Jagung" and jarak_mod < 1.0:
            st.info("💧 Gunakan jarak 75×50 cm dan kedalaman 5 cm untuk hasil optimal.")
            ada_rek = True
        if not ada_rek:
            st.success("✅ Kondisi lahan sudah optimal. Pertahankan manajemen saat ini!")
    
    st.markdown("---")
    st.caption("📚 **Referensi:** BPS (2024); Holidah & Rahmatiyah (2025), Botani Vol.2 No.1")
else:
    st.info("👈 Isi data di sidebar kiri, lalu klik **Hitung Estimasi**")