from typing import Dict


def format_tonase(ton):
    return f"{ton:.2f} ton"


def estimasi_hasil(
    area_ha: float,
    potensi_varietas: float,
    jarak_tanam_cm: float,
    kedalaman_cm: float,
    efisiensi: float = 0.85,
) -> Dict[str, float]:
    """Estimasi produksi jagung berdasarkan luas, varietas, jarak tanam, dan kedalaman."""
    spacing_m = jarak_tanam_cm / 100
    density_per_ha = 10000 / (spacing_m ** 2)
    standar_density = 65000
    density_factor = min(1.0, density_per_ha / standar_density)

    if 3.0 <= kedalaman_cm <= 5.0:
        depth_factor = 1.0
    elif 2.0 <= kedalaman_cm < 3.0 or 5.0 < kedalaman_cm <= 6.0:
        depth_factor = 0.95
    else:
        depth_factor = 0.8

    ton_per_ha = potensi_varietas * density_factor * depth_factor * efisiensi
    ton_total = ton_per_ha * area_ha

    return {
        "area_ha": area_ha,
        "density_per_ha": density_per_ha,
        "ton_total": ton_total,
        "ton_per_ha": ton_per_ha,
    }


def peringatan_hasil(ton_per_ha: float, potensi_varietas: float) -> str:
    if ton_per_ha < potensi_varietas * 0.6:
        return "Hasil tergolong rendah; tinjau kesuburan tanah, air, dan pemeliharaan."
    if ton_per_ha < potensi_varietas * 0.9:
        return "Hasil sedang; tingkatkan irigasi dan pemupukan untuk mendekati potensi."
    return "Hasil baik; pertahankan praktik budidaya yang sama."