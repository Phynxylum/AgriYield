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
        "suhu_opt": (20, 30), "satuan": "ton/ha", "icon": "🌽"
    },
    "Padi": {
        "varietas": {
            "Unggul":  {"base": 6.5,  "pupuk_opt": 250},
            "Lokal":   {"base": 5.29, "pupuk_opt": 200},
            "Hibrida": {"base": 8.0,  "pupuk_opt": 280},
        },
        "suhu_opt": (24, 32), "satuan": "ton GKP/ha", "icon": "🌾"
    },
    "Kedelai": {
        "varietas": {
            "Unggul":  {"base": 2.2,  "pupuk_opt": 100},
            "Lokal":   {"base": 1.62, "pupuk_opt": 80},
            "Hibrida": {"base": 2.8,  "pupuk_opt": 120},
        },
        "suhu_opt": (22, 32), "satuan": "ton/ha", "icon": "🫘"
    },
    "Singkong": {
        "varietas": {
            "Unggul":  {"base": 26.17, "pupuk_opt": 200},
            "Lokal":   {"base": 17.0,  "pupuk_opt": 150},
            "Hibrida": {"base": 30.0,  "pupuk_opt": 220},
        },
        "suhu_opt": (25, 35), "satuan": "ton/ha", "icon": "🌿"
    },
    "Cabai": {
        "varietas": {
            "Unggul":  {"base": 8.77, "pupuk_opt": 150},
            "Lokal":   {"base": 5.0,  "pupuk_opt": 100},
            "Hibrida": {"base": 11.0, "pupuk_opt": 180},
        },
        "suhu_opt": (25, 32), "satuan": "ton/ha", "icon": "🌶️"
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp { background-color: #0E1210; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0B0F0D !important;
    border-right: 1px solid #1E2B22;
}
[data-testid="stSidebar"] * { color: #E8EDE8 !important; }

/* Toggle sidebar */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible !important; background: transparent !important; }
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    background-color: #161E16 !important;
    border-radius: 0 8px 8px 0 !important;
    color: #8FBC8F !important;
    z-index: 999 !important;
}
[data-testid="stSidebarCollapseButton"] button {
    color: #8FBC8F !important;
    background: transparent !important;
}
section[data-testid="stSidebar"] > div:first-child { padding-top: 1rem !important; }

/* Logo */
.logo-wrap {
    display: flex; align-items: center; gap: 10px;
    padding: 0.5rem 0 1.5rem;
    border-bottom: 1px solid #1E2B22;
    margin-bottom: 1rem;
}
.logo-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #2D4A2D, #8FBC8F);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(143,188,143,0.25);
}
.logo-text { font-size: 20px; font-weight: 700; color: #E8EDE8 !important; }
.logo-text span { color: #8FBC8F !important; }

/* Menu */
.menu-item {
    background: linear-gradient(90deg, #161E16, #0E1210);
    border-left: 2px solid #8FBC8F;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 13px; font-weight: 600;
    color: #8FBC8F !important;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
    letter-spacing: 0.02em;
}

/* Section label */
.sidebar-section {
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.15em; color: #3D5C3D !important;
    text-transform: uppercase; margin: 16px 0 8px;
}

/* Inputs */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div {
    background-color: #111A12 !important;
    border: 1px solid #1E2B22 !important;
    border-radius: 8px !important;
    color: #E8EDE8 !important;
}
[data-testid="stSidebar"] label {
    color: #6B9B6B !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* Slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #8FBC8F !important;
    border: 2px solid #E8EDE8 !important;
    box-shadow: 0 0 8px rgba(143,188,143,0.4) !important;
}

/* Button */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #2D4A2D, #8FBC8F) !important;
    color: #0E1210 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 1rem !important;
    width: 100% !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 15px rgba(143,188,143,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    box-shadow: 0 6px 25px rgba(143,188,143,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #0B0F0D 0%, #111A12 60%, #0B0F0D 100%);
    border: 1px solid #1E2B22;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.5rem;
    position: relative; overflow: hidden; min-height: 120px;
}
.hero-banner::after {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, transparent, #8FBC8F, transparent);
}
.hero-banner::before {
    content: '';
    position: absolute; right: 0; top: 0; bottom: 0; width: 40%;
    background: radial-gradient(ellipse at right, rgba(143,188,143,0.06) 0%, transparent 70%);
}
.hero-icon-wrap {
    width: 68px; height: 68px;
    background: linear-gradient(135deg, #1E3A1E, #8FBC8F);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; flex-shrink: 0;
    box-shadow: 0 8px 24px rgba(143,188,143,0.25);
}
.hero-title {
    font-size: 30px; font-weight: 700;
    color: #E8EDE8; margin: 0 0 6px; letter-spacing: -0.01em;
}
.hero-sub { font-size: 12px; color: #4A6B4A; margin: 0; letter-spacing: 0.06em; }

/* Info box */
.info-box {
    background: #0B0F0D; border: 1px solid #1E2B22;
    border-radius: 12px; padding: 1.75rem 2rem;
    display: flex; align-items: center; gap: 1.25rem;
}
.info-icon {
    width: 52px; height: 52px;
    background: #161E16; border: 1px solid #2A3D2A;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
}
.info-text { font-size: 15px; color: #6B9B6B; margin: 0; line-height: 1.8; }
.info-text span { color: #8FBC8F; font-weight: 600; }

/* Metric cards */
.metric-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 1.5rem;
}
.metric-card {
    background: #0B0F0D; border: 1px solid #1E2B22;
    border-radius: 14px; padding: 1.4rem 1.6rem;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #8FBC8F, transparent);
}
.metric-label {
    font-size: 10px; color: #3D5C3D; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.12em; margin: 0 0 10px;
}
/* ANGKA METRIC — lebih besar dan jelas */
.metric-value {
    font-size: 300px; font-weight: 700;
    color: #E8EDE8; margin: 0 0 10px;
    line-height: 1;
}
.metric-unit { font-size: 44px; color: #4A6B4A; font-weight: 400; }
.metric-badge {
    display: inline-block; font-size: 12px;
    padding: 4px 12px; border-radius: 20px; font-weight: 500;
}
.badge-good   { background: rgba(143,188,143,0.15); color: #A8D5A8; border: 1px solid rgba(143,188,143,0.3); }
.badge-medium { background: rgba(255,183,77,0.12);  color: #FFD080; border: 1px solid rgba(255,183,77,0.25); }
.badge-low    { background: rgba(239,100,100,0.12); color: #F5A0A0; border: 1px solid rgba(239,100,100,0.25); }

/* Section title */
.section-title {
    font-size: 11px; font-weight: 600; color: #4A6B4A;
    text-transform: uppercase; letter-spacing: 0.15em; margin: 0 0 1rem;
}

/* Rekomendasi */
.rekom-card {
    background: #0B0F0D; border: 1px solid #1E2B22;
    border-radius: 12px; padding: 1.4rem;
}
/* TEKS REKOMENDASI — lebih terang dan jelas */
.rekom-item {
    display: flex; gap: 12px; margin-bottom: 14px;
    align-items: flex-start; line-height: 1.7;
}
.rekom-dot {
    width: 6px; height: 6px; background: #8FBC8F;
    border-radius: 50%; margin-top: 8px; flex-shrink: 0;
    box-shadow: 0 0 6px rgba(143,188,143,0.5);
}
.rekom-text {
    font-size: 16px; font-weight: 400;
    color: #C8D8C8;  /* lebih terang dari sebelumnya */
    line-height: 1.7;
}

/* Divider & footer */
.divider { border: none; border-top: 1px solid #1E2B22; margin: 1.5rem 0; }
.footer-caption {
    font-size: 11px; color: #2A3D2A; margin-top: 1rem;
    text-align: center; letter-spacing: 0.05em;
}

.block-container { padding-top: 1.5rem !important; }
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
    varietas = st.selectbox("◈ Varietas", list(DATA_TANAMAN[tanaman]["varietas"].keys()))
    luas     = st.number_input("▣ Luas Lahan (ha)", 0.1, 100.0, 1.0, step=0.1)

    st.markdown('<div class="sidebar-section">Kondisi Lahan</div>', unsafe_allow_html=True)
    ph      = st.slider("◉ pH Tanah", 4.0, 9.0, 6.5, 0.1)
    irigasi = st.selectbox("◈ Sistem Irigasi", ["Teknis / pompa", "Setengah teknis", "Tadah hujan"])
    musim   = st.selectbox("◈ Musim Tanam", ["Musim hujan", "Transisi", "Musim kemarau"])
    suhu    = st.slider("◉ Suhu Rata-rata (°C)", 15, 40, 28)
    pupuk   = st.number_input("▣ Dosis Pupuk (kg/ha)", 0, 500,
                DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"])

    jarak_mod     = 1.0
    kedalaman_mod = 1.0
    if tanaman == "Jagung":
        st.markdown('<div class="sidebar-section">Khusus Jagung</div>', unsafe_allow_html=True)
        jarak_mod     = JARAK_TANAM[st.selectbox("◈ Jarak Tanam", list(JARAK_TANAM.keys()))]
        kedalaman_mod = KEDALAMAN_TANAM[st.selectbox("◈ Kedalaman Tanam", list(KEDALAMAN_TANAM.keys()))]

    st.markdown("<br>", unsafe_allow_html=True)
    hitung = st.button("🌿  Hitung Estimasi", use_container_width=True, type="primary")

# ── MAIN ──────────────────────────────────────────────
icon = DATA_TANAMAN[tanaman]["icon"]

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-icon-wrap">{icon}</div>
    <div>
        <p class="hero-title">Aplikasi Estimasi Hasil Panen</p>
        <p class="hero-sub">PERTANIAN PRESISI — SUMBER DATA: BPS (2024) & HOLIDAH, RAHMATIYAH (2025)</p>
    </div>
</div>
""", unsafe_allow_html=True)

if not hitung:
    st.markdown("""
    <div class="info-box">
        <div class="info-icon">🧮</div>
        <p class="info-text">Isi data di sidebar kiri,<br>lalu klik <span>🌿 Hitung Estimasi</span></p>
    </div>
    """, unsafe_allow_html=True)
else:
    prod, total, persen, faktor, ket_ph = hitung_estimasi(
        tanaman, varietas, luas, ph, irigasi,
        musim, suhu, pupuk, jarak_mod, kedalaman_mod
    )
    satuan = DATA_TANAMAN[tanaman]["satuan"]

    if persen >= 85:
        badge_class, badge_text = "badge-good",   "✓ Sangat Baik"
    elif persen >= 65:
        badge_class, badge_text = "badge-medium", "◈ Cukup Baik"
    else:
        badge_class, badge_text = "badge-low",    "▲ Perlu Perbaikan"

    st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <p class="metric-label">Produktivitas</p>
        <p style="margin:0 0 10px"><span style="font-size:48px;font-weight:700;color:#E8EDE8;line-height:1">{prod}</span> <span style="font-size:15px;color:#6B9B6B">{satuan}</span></p>
        <span class="metric-badge badge-good">Per Hektar</span>
    </div>
    <div class="metric-card">
        <p class="metric-label">Total Produksi</p>
        <p style="margin:0 0 10px"><span style="font-size:48px;font-weight:700;color:#E8EDE8;line-height:1">{total}</span> <span style="font-size:15px;color:#6B9B6B">ton</span></p>
        <span class="metric-badge badge-good">{luas} ha lahan</span>
    </div>
    <div class="metric-card">
        <p class="metric-label">Capaian Potensi</p>
        <p style="margin:0 0 10px"><span style="font-size:48px;font-weight:700;color:#E8EDE8;line-height:1">{persen}</span><span style="font-size:15px;color:#6B9B6B">%</span></p>
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
                     color_continuous_scale=[[0,"#161E16"],[0.5,"#2D4A2D"],[1,"#8FBC8F"]],
                     range_x=[0, 100])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#6B9B6B", family="Inter"),
            coloraxis_showscale=False, height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#1E2B22", tickfont=dict(color="#3D5C3D", size=12)),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#C8D8C8", size=13))
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
            rekoms.append("Kondisi lahan sudah optimal. Pertahankan manajemen saat ini.")

        items_html = "".join([
            f'<div class="rekom-item"><div class="rekom-dot"></div><span class="rekom-text">{r}</span></div>'
            for r in rekoms
        ])
        st.markdown(f'<div class="rekom-card">{items_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <p class="footer-caption">
        BPS (2024) Survei Ubinan &nbsp; · &nbsp;
        Holidah & Rahmatiyah (2025), Botani Vol.2 No.1 &nbsp; · &nbsp;
        DOI: 10.62951/botani.v2i1.162
    </p>
    """, unsafe_allow_html=True)