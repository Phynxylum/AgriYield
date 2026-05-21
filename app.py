import streamlit as st
import pandas as pd
import plotly.express as px

# ── DATA ──────────────────────────────────────────────
DATA_TANAMAN = {
    "Jagung": {
        "varietas": {
            "Hibrida":  {"base": 7.0,  "pupuk_opt": 300},
            "Unggul":   {"base": 5.94, "pupuk_opt": 250},
            "Lokal":    {"base": 4.0,  "pupuk_opt": 200},
        },
        "suhu_opt": (20, 30),
        "satuan": "ton/ha",
        "icon": "🌽"
    },
    "Padi": {
        "varietas": {
            "Unggul":  {"base": 6.5,  "pupuk_opt": 250},
            "Lokal":   {"base": 5.29, "pupuk_opt": 200},
            "Hibrida": {"base": 8.0,  "pupuk_opt": 280},
        },
        "suhu_opt": (24, 32),
        "satuan": "ton GKP/ha",
        "icon": "🌾"
    },
    "Kedelai": {
        "varietas": {
            "Unggul":  {"base": 2.2,  "pupuk_opt": 100},
            "Lokal":   {"base": 1.62, "pupuk_opt": 80},
            "Hibrida": {"base": 2.8,  "pupuk_opt": 120},
        },
        "suhu_opt": (22, 32),
        "satuan": "ton/ha",
        "icon": "🫘"
    },
    "Singkong": {
        "varietas": {
            "Unggul":  {"base": 26.17, "pupuk_opt": 200},
            "Lokal":   {"base": 17.0,  "pupuk_opt": 150},
            "Hibrida": {"base": 30.0,  "pupuk_opt": 220},
        },
        "suhu_opt": (25, 35),
        "satuan": "ton/ha",
        "icon": "🌿"
    },
    "Cabai": {
        "varietas": {
            "Unggul":  {"base": 8.77, "pupuk_opt": 150},
            "Lokal":   {"base": 5.0,  "pupuk_opt": 100},
            "Hibrida": {"base": 11.0, "pupuk_opt": 180},
        },
        "suhu_opt": (25, 32),
        "satuan": "ton/ha",
        "icon": "🌶️"
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

# ── FUNGSI ────────────────────────────────────────────
def hitung_estimasi(tanaman, varietas, luas, ph, irigasi,
                    musim, suhu, pupuk, jarak_mod, kedalaman_mod):
    base      = DATA_TANAMAN[tanaman]["varietas"][varietas]["base"]
    pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
    suhu_opt  = DATA_TANAMAN[tanaman]["suhu_opt"]

    if 6.0 <= ph <= 7.0:
        f_ph, ket_ph = 1.0, "Optimal"
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        f_ph, ket_ph = 0.88, "Kurang ideal"
    else:
        f_ph, ket_ph = 0.72, "Tidak ideal"

    f_ir = {"Teknis / pompa": 1.0, "Setengah teknis": 0.88, "Tadah hujan": 0.72}[irigasi]
    f_ms = {"Musim hujan": 1.0, "Transisi": 0.90, "Musim kemarau": 0.78}[musim]
    mn, mx = suhu_opt
    f_su = 1.0 if mn <= suhu <= mx else (0.75 if suhu < mn-5 or suhu > mx+5 else 0.88)
    rasio = pupuk / pupuk_opt
    f_pu = 1.0 if 0.8 <= rasio <= 1.2 else (0.75 if rasio < 0.5 else 0.92)

    produktivitas = base * f_ph * f_ir * f_ms * f_su * f_pu * jarak_mod * kedalaman_mod
    total         = produktivitas * luas
    persen        = (produktivitas / base) * 100

    faktor = {
        "pH Tanah":        round(f_ph * 100),
        "Irigasi":         round(f_ir * 100),
        "Musim Tanam":     round(f_ms * 100),
        "Suhu Udara":      round(f_su * 100),
        "Pemupukan":       round(f_pu * 100),
        "Jarak Tanam":     round(jarak_mod * 100),
        "Kedalaman Tanam": round(kedalaman_mod * 100),
    }

    return round(produktivitas, 2), round(total, 2), round(persen, 1), faktor, ket_ph

# ── CONFIG & CSS ──────────────────────────────────────
st.set_page_config(page_title="AgriYield", page_icon="🌾", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background utama */
.stApp {
    background-color: #0d1f0f;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a1a0c !important;
    border-right: 1px solid #1e3d20;
}
[data-testid="stSidebar"] * {
    color: #c8e6c9 !important;
}

/* Tombol toggle sidebar - SELALU tampil */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible !important; background: transparent !important; }
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    background-color: #1b4d1e !important;
    border-radius: 0 8px 8px 0 !important;
    color: #81c784 !important;
    z-index: 999 !important;
}
[data-testid="stSidebarCollapseButton"] button {
    color: #81c784 !important;
    background: transparent !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem !important;
}

/* Logo */
.logo-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0 1.5rem;
}
.logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #4caf50, #8bc34a);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.logo-text { font-size: 20px; font-weight: 700; color: #e8f5e9 !important; }
.logo-text span { color: #8bc34a !important; }

/* Menu aktif */
.menu-item {
    background: linear-gradient(90deg, #1b4d1e, #0d2e10);
    border-left: 3px solid #4caf50;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 14px; font-weight: 600;
    color: #a5d6a7 !important;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}

/* Label section */
.sidebar-section {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.1em;
    color: #4a7a4c !important;
    text-transform: uppercase;
    margin: 16px 0 8px;
}

/* Input fields */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div {
    background-color: #132815 !important;
    border: 1px solid #1e3d20 !important;
    border-radius: 8px !important;
    color: #c8e6c9 !important;
}
[data-testid="stSidebar"] label {
    color: #81c784 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #4caf50 !important;
}

/* Tombol hitung */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #2e7d32, #4caf50) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 15px rgba(76,175,80,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    box-shadow: 0 4px 20px rgba(76,175,80,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #0d2e10 0%, #1b4d1e 50%, #0a3d0c 100%);
    border: 1px solid #1e3d20;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.5rem;
    position: relative; overflow: hidden; min-height: 120px;
}
.hero-banner::before {
    content: '';
    position: absolute; right: -20px; bottom: -20px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(76,175,80,0.15) 0%, transparent 70%);
}
.hero-icon-wrap {
    width: 64px; height: 64px;
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; flex-shrink: 0;
    box-shadow: 0 8px 24px rgba(76,175,80,0.3);
}
.hero-title { font-size: 30px; font-weight: 700; color: #e8f5e9; margin: 0 0 6px; }
.hero-sub   { font-size: 14px; color: #66bb6a; margin: 0; }

/* Info box */
.info-box {
    background: linear-gradient(135deg, #0d2e10, #132815);
    border: 1px solid #1e3d20; border-radius: 12px;
    padding: 1.5rem 2rem;
    display: flex; align-items: center; gap: 1rem;
}
.info-icon {
    width: 48px; height: 48px; background: #1b4d1e;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
}
.info-text { font-size: 15px; color: #81c784; margin: 0; line-height: 1.8; }
.info-text span { color: #4caf50; font-weight: 600; }

/* Metric cards */
.metric-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 1.5rem;
}
.metric-card {
    background: linear-gradient(135deg, #0d2e10, #132815);
    border: 1px solid #1e3d20; border-radius: 14px;
    padding: 1.25rem 1.5rem;
}
.metric-label {
    font-size: 11px; color: #4a7a4c; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px;
}
.metric-value { font-size: 28px; font-weight: 700; color: #e8f5e9; margin: 0 0 8px; }
.metric-unit  { font-size: 13px; color: #4a7a4c; }
.metric-badge {
    display: inline-block; font-size: 12px;
    padding: 3px 10px; border-radius: 20px; font-weight: 500;
}
.badge-good   { background: rgba(76,175,80,0.2);  color: #81c784; }
.badge-medium { background: rgba(255,183,77,0.2); color: #ffb74d; }
.badge-low    { background: rgba(239,83,80,0.2);  color: #ef9a9a; }

/* Section title */
.section-title {
    font-size: 13px; font-weight: 600; color: #4a7a4c;
    text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 1rem;
}

/* Rekomendasi */
.rekom-card {
    background: #0d2e10; border: 1px solid #1e3d20;
    border-radius: 12px; padding: 1.25rem; height: 100%;
}
.rekom-item {
    display: flex; gap: 10px; margin-bottom: 12px;
    font-size: 13px; color: #a5d6a7; align-items: flex-start; line-height: 1.6;
}
.rekom-dot {
    width: 6px; height: 6px; background: #4caf50;
    border-radius: 50%; margin-top: 6px; flex-shrink: 0;
}

/* Divider & footer */
.divider { border: none; border-top: 1px solid #1e3d20; margin: 1.5rem 0; }
.footer-caption { font-size: 12px; color: #2d5a2f; margin-top: 1rem; text-align: center; }

/* Block container */
.block-container { padding-top: 1.5rem !important; }
[data-testid="stSidebar"] .stDivider { border-color: #1e3d20 !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-icon">🌾</div>
        <div class="logo-text">Agri<span>Yield</span></div>
    </div>
    <div class="menu-item">📊 &nbsp; Estimasi Panen</div>
    <div class="sidebar-section">Data Input</div>
    """, unsafe_allow_html=True)

    tanaman  = st.selectbox("🌱 Jenis Tanaman", list(DATA_TANAMAN.keys()))
    varietas = st.selectbox("🔬 Varietas", list(DATA_TANAMAN[tanaman]["varietas"].keys()))
    luas     = st.number_input("📐 Luas Lahan (ha)", 0.1, 100.0, 1.0, step=0.1)

    st.markdown('<div class="sidebar-section">Kondisi Lahan</div>', unsafe_allow_html=True)
    ph      = st.slider("🧪 pH Tanah", 4.0, 9.0, 6.5, 0.1)
    irigasi = st.selectbox("💧 Sistem Irigasi", ["Teknis / pompa", "Setengah teknis", "Tadah hujan"])
    musim   = st.selectbox("🌤 Musim Tanam", ["Musim hujan", "Transisi", "Musim kemarau"])
    suhu    = st.slider("🌡 Suhu Rata-rata (°C)", 15, 40, 28)
    pupuk   = st.number_input("🌿 Dosis Pupuk (kg/ha)", 0, 500,
                DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"])

    jarak_mod     = 1.0
    kedalaman_mod = 1.0
    if tanaman == "Jagung":
        st.markdown('<div class="sidebar-section">🌽 Khusus Jagung</div>', unsafe_allow_html=True)
        jarak_mod     = JARAK_TANAM[st.selectbox("📏 Jarak Tanam", list(JARAK_TANAM.keys()))]
        kedalaman_mod = KEDALAMAN_TANAM[st.selectbox("📍 Kedalaman Tanam", list(KEDALAMAN_TANAM.keys()))]

    st.markdown("<br>", unsafe_allow_html=True)
    hitung = st.button("🔍 Hitung Estimasi", use_container_width=True, type="primary")

# ── MAIN ──────────────────────────────────────────────
icon = DATA_TANAMAN[tanaman]["icon"]

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-icon-wrap">{icon}</div>
    <div>
        <p class="hero-title">Aplikasi Estimasi Hasil Panen</p>
        <p class="hero-sub">Pertanian Presisi — Sumber data: BPS (2024) & Holidah, Rahmatiyah (2025)</p>
    </div>
</div>
""", unsafe_allow_html=True)

if not hitung:
    st.markdown("""
    <div class="info-box">
        <div class="info-icon">🧮</div>
        <p class="info-text">Isi data di sidebar kiri,<br>lalu klik <span>Hitung Estimasi</span></p>
    </div>
    """, unsafe_allow_html=True)
else:
    prod, total, persen, faktor, ket_ph = hitung_estimasi(
        tanaman, varietas, luas, ph, irigasi,
        musim, suhu, pupuk, jarak_mod, kedalaman_mod
    )
    satuan = DATA_TANAMAN[tanaman]["satuan"]

    if persen >= 85:
        badge_class, badge_text = "badge-good",   "🟢 Sangat Baik"
    elif persen >= 65:
        badge_class, badge_text = "badge-medium", "🟡 Cukup Baik"
    else:
        badge_class, badge_text = "badge-low",    "🔴 Perlu Perbaikan"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Produktivitas</p>
            <p class="metric-value">{prod} <span class="metric-unit">{satuan}</span></p>
            <span class="metric-badge badge-good">Per Hektar</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Total Produksi</p>
            <p class="metric-value">{total} <span class="metric-unit">ton</span></p>
            <span class="metric-badge badge-good">{luas} ha lahan</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Capaian Potensi</p>
            <p class="metric-value">{persen}<span class="metric-unit">%</span></p>
            <span class="metric-badge {badge_class}">{badge_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<p class="section-title">📊 Analisis Faktor</p>', unsafe_allow_html=True)
        df  = pd.DataFrame({"Faktor": list(faktor.keys()), "Skor (%)": list(faktor.values())})
        fig = px.bar(df, x="Skor (%)", y="Faktor", orientation="h",
                     color="Skor (%)",
                     color_continuous_scale=[[0,"#1b4d1e"],[0.5,"#388e3c"],[1,"#81c784"]],
                     range_x=[0, 100])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#81c784", family="Plus Jakarta Sans"),
            coloraxis_showscale=False, height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#1e3d20", tickfont=dict(color="#4a7a4c")),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#a5d6a7"))
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">💡 Rekomendasi</p>', unsafe_allow_html=True)
        pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
        rekoms = []
        if ket_ph != "Optimal":
            rekoms.append("pH tanah belum optimal. Lakukan pengapuran (pH < 6) atau pengasaman (pH > 7).")
        if pupuk < pupuk_opt * 0.8:
            rekoms.append(f"Dosis pupuk kurang dari optimal. Rekomendasi: {pupuk_opt} kg/ha.")
        if irigasi == "Tadah hujan":
            rekoms.append("Pertimbangkan irigasi teknis untuk stabilitas pasokan air.")
        if musim == "Musim kemarau":
            rekoms.append("Tanam kemarau berisiko. Pastikan pasokan air tercukupi.")
        if tanaman == "Jagung" and jarak_mod < 1.0:
            rekoms.append("Gunakan jarak 75×50 cm dan kedalaman 5 cm untuk hasil optimal.")
        if not rekoms:
            rekoms.append("Kondisi lahan sudah optimal. Pertahankan manajemen saat ini!")

        items_html = "".join([
            f'<div class="rekom-item"><div class="rekom-dot"></div><span>{r}</span></div>'
            for r in rekoms
        ])
        st.markdown(f'<div class="rekom-card">{items_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <p class="footer-caption">
        📚 Referensi: BPS (2024) Survei Ubinan &nbsp;|&nbsp;
        Holidah & Rahmatiyah (2025), Botani Vol.2 No.1 &nbsp;|&nbsp;
        DOI: 10.62951/botani.v2i1.162
    </p>
    """, unsafe_allow_html=True)