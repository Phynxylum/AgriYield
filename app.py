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
            "Lokal":   {"base": 5.0,  "pupuk_opt": 100},
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

# ── FUNGSI HITUNG ─────────────────────────────────────
def hitung_estimasi(tanaman, varietas, luas, ph, irigasi,
                    musim, suhu, pupuk, jarak_mod, kedalaman_mod):
    base      = DATA_TANAMAN[tanaman]["varietas"][varietas]["base"]
    pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
    suhu_opt  = DATA_TANAMAN[tanaman]["suhu_opt"]

    # Faktor pH
    if 6.0 <= ph <= 7.0:
        f_ph, ket_ph = 1.0, "Optimal"
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        f_ph, ket_ph = 0.88, "Kurang ideal"
    else:
        f_ph, ket_ph = 0.72, "Tidak ideal"

    # Faktor irigasi
    f_ir = {"Teknis / pompa": 1.0, "Setengah teknis": 0.88, "Tadah hujan": 0.72}[irigasi]

    # Faktor musim
    f_ms = {"Musim hujan": 1.0, "Transisi": 0.90, "Musim kemarau": 0.78}[musim]

    # Faktor suhu
    mn, mx = suhu_opt
    f_su = 1.0 if mn <= suhu <= mx else (0.75 if suhu < mn-5 or suhu > mx+5 else 0.88)

    # Faktor pupuk
    rasio = pupuk / pupuk_opt
    f_pu = 1.0 if 0.8 <= rasio <= 1.2 else (0.75 if rasio < 0.5 else 0.92)

    produktivitas = base * f_ph * f_ir * f_ms * f_su * f_pu * jarak_mod * kedalaman_mod
    total         = produktivitas * luas
    persen        = (produktivitas / base) * 100

    faktor = {
        "pH tanah":        round(f_ph * 100),
        "Irigasi":         round(f_ir * 100),
        "Musim tanam":     round(f_ms * 100),
        "Suhu udara":      round(f_su * 100),
        "Pemupukan":       round(f_pu * 100),
        "Jarak tanam":     round(jarak_mod * 100),
        "Kedalaman tanam": round(kedalaman_mod * 100),
    }

    return round(produktivitas, 2), round(total, 2), round(persen, 1), faktor, ket_ph

# ── TAMPILAN STREAMLIT ────────────────────────────────
st.set_page_config(page_title="Estimasi Hasil Panen", page_icon="🌾", layout="wide")

st.title("🌾 Aplikasi Estimasi Hasil Panen")
st.caption("Pertanian Presisi — Sumber data: BPS (2024) & Holidah, Rahmatiyah (2025)")

# Sidebar input
with st.sidebar:
    st.markdown("## 🌾 AgriYield")
    st.markdown("---")
    st.header("📋 Data Input")

    tanaman  = st.selectbox("Jenis tanaman", list(DATA_TANAMAN.keys()))
    varietas = st.selectbox("Varietas", list(DATA_TANAMAN[tanaman]["varietas"].keys()))
    luas     = st.number_input("Luas lahan (ha)", 0.1, 100.0, 1.0, step=0.1)

    st.divider()
    st.subheader("🌱 Kondisi Lahan")
    ph      = st.slider("pH tanah", 4.0, 9.0, 6.5, 0.1)
    irigasi = st.selectbox("Sistem irigasi", ["Teknis / pompa", "Setengah teknis", "Tadah hujan"])
    musim   = st.selectbox("Musim tanam", ["Musim hujan", "Transisi", "Musim kemarau"])
    suhu    = st.slider("Suhu rata-rata (°C)", 15, 40, 28)
    pupuk   = st.number_input("Dosis pupuk (kg/ha)", 0, 500,
                DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"])

    jarak_mod     = 1.0
    kedalaman_mod = 1.0
    if tanaman == "Jagung":
        st.divider()
        st.subheader("🌽 Khusus Jagung")
        st.caption("Holidah & Rahmatiyah (2025)")
        jarak_mod     = JARAK_TANAM[st.selectbox("Jarak tanam", list(JARAK_TANAM.keys()))]
        kedalaman_mod = KEDALAMAN_TANAM[st.selectbox("Kedalaman tanam", list(KEDALAMAN_TANAM.keys()))]

    hitung = st.button("🔍 Hitung Estimasi", use_container_width=True, type="primary")

# Area hasil
if hitung:
    prod, total, persen, faktor, ket_ph = hitung_estimasi(
        tanaman, varietas, luas, ph, irigasi,
        musim, suhu, pupuk, jarak_mod, kedalaman_mod
    )
    satuan = DATA_TANAMAN[tanaman]["satuan"]

    # Metrik utama
    c1, c2, c3 = st.columns(3)
    c1.metric("Produktivitas", f"{prod} {satuan}")
    c2.metric("Total Produksi", f"{total} ton")
    kat = "🟢 Sangat baik" if persen >= 85 else ("🟡 Cukup baik" if persen >= 65 else "🔴 Perlu perbaikan")
    c3.metric("Capaian potensi", f"{persen}%", kat)

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📊 Analisis Faktor")
        df = pd.DataFrame({"Faktor": list(faktor.keys()), "Skor (%)": list(faktor.values())})
        fig = px.bar(df, x="Skor (%)", y="Faktor", orientation="h",
                     color="Skor (%)", color_continuous_scale="Greens", range_x=[0, 100])
        fig.update_layout(showlegend=False, height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("💡 Rekomendasi")
        pupuk_opt = DATA_TANAMAN[tanaman]["varietas"][varietas]["pupuk_opt"]
        ada_rekomendasi = False
        if ket_ph != "Optimal":
            st.warning(f"pH tanah {ket_ph}. Lakukan pengapuran (pH<6) atau pengasaman (pH>7).")
            ada_rekomendasi = True
        if pupuk < pupuk_opt * 0.8:
            st.warning(f"Dosis pupuk kurang. Rekomendasi: {pupuk_opt} kg/ha.")
            ada_rekomendasi = True
        if irigasi == "Tadah hujan":
            st.info("Pertimbangkan irigasi teknis untuk hasil lebih stabil.")
            ada_rekomendasi = True
        if musim == "Musim kemarau":
            st.warning("Tanam kemarau berisiko. Pastikan pasokan air tercukupi.")
            ada_rekomendasi = True
        if tanaman == "Jagung" and jarak_mod < 1.0:
            st.info("Gunakan jarak 75×50 cm dan kedalaman 5 cm untuk hasil optimal.")
            ada_rekomendasi = True
        if not ada_rekomendasi:
            st.success("✅ Kondisi lahan sudah optimal. Pertahankan manajemen saat ini!")

    st.divider()
    st.caption("📚 Referensi: BPS (2024); Holidah & Rahmatiyah (2025), Botani Vol.2 No.1, DOI: 10.62951/botani.v2i1.162")
else:
    st.info("👈 Isi data di sidebar kiri, lalu klik **Hitung Estimasi**")