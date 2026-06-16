import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# --- STYLE CSS (GRADASI & ELEMEN KIMIA) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #ffffff 50%, #fef9c3 100%) !important;
        background-attachment: fixed !important;
        color: #1e293b;
    }
    div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-right: 1px solid #e2e8f0;
    }
    h1, h2, h3 { color: #0369a1 !important; font-weight: 700; }
    .identitas-box {
        background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 12px;
        border-left: 5px solid #0ea5e9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 10px; margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #0ea5e9 !important; color: white !important;
        border-radius: 8px !important; font-weight: bold !important; border: none !important;
        width: 100%; padding: 10px 0px;
    }
    .stButton>button:hover { background-color: #0284c7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK ---
AR_PERIODIK = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'Ag': 107.87, 'I': 126.90, 'Ba': 137.33, 'Pb': 207.2
}

def format_koma(nilai): return f"{nilai:.4f}".rstrip('0').rstrip('.').replace('.', ',')
def format_koma_v(nilai): return f"{nilai:.2f}".replace('.', ',')

def hitung_bm_dari_teks(rumus):
    def parse_formula(f):
        reg = r'([A-Z][a-z]*)(\d*)'
        res = re.findall(reg, f)
        return {element: int(count) if count else 1 for element, count in res}
    while '(' in rumus:
        match = re.search(r'\(([^()]+)\)(\d*)', rumus)
        if match:
            sub_formula, sub_count = match.groups()
            sub_count = int(sub_count) if sub_count else 1
            sub_dict = parse_formula(sub_formula)
            expanded = "".join([f"{el}{num * sub_count}" for el, num in sub_dict.items()])
            rumus = rumus.replace(match.group(), expanded)
    komponen = parse_formula(rumus)
    total_bm = 0.0
    unsur_tidak_dikenal = []
    rincian = []
    for unsur, jumlah in komponen.items():
        if unsur in AR_PERIODIK:
            ar_unsur = AR_PERIODIK[unsur]
            total_bm += ar_unsur * jumlah
            rincian.append(f"({jumlah} x Ar {unsur} [{format_koma(ar_unsur)}])")
        else: unsur_tidak_dikenal.append(unsur)
    return total_bm, unsur_tidak_dikenal, " + ".join(rincian)

# ==========================================
# SIDEBAR NAVIGASI
# ==========================================
st.sidebar.title("🧪 Navigation")
menu_pilih = st.sidebar.radio("Pilih Menu:", ["Home", "Bobot Molekul", "Konversi", "Pengenceran"])

# ==========================================
# LOGIKA HALAMAN UTAMA (STRUKTUR DIPERBAIKI)
# ==========================================

if menu_pilih == "Home":
    # Judul utama dan deskripsi diletakkan di dalam sini agar hanya muncul di Home
    st.title("🧪 Kalkulator Kimia")
    st.markdown("### Perhitungan Bobot Molekul, Konversi Satuan, dan Faktor Pengenceran")
    st.markdown("---")
    
    # BOX INFORMASI MAKALAH (Hanya muncul saat menu Home aktif)
    st.markdown("""
    <div class="identitas-box">
        <div style="color: #0369a1; font-weight: bold; font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; margin-bottom: 10px;">
            📄 INFORMASI PROJECT MAKALAH
        </div>
        <table style="width:100%; border:none; color:#334155; font-size:0.95rem; line-height: 1.6;">
            <tr><td style="width: 25%; font-weight: bold;">Mata Kuliah</td><td>: Logika Pemrograman dan Komputer</td></tr>
            <tr><td style="font-weight: bold;">Kelompok</td><td>: Kelompok 7</td></tr>
            <tr><td style="vertical-align: top; font-weight: bold;">Anggota</td><td>: 
                <table style="width:100%; margin-top:-2px; border:none; color:#334155;">
                    <tr><td>• 2560556 - AFFAN IHSANUL FATAH</td><td>• 2560618 - ELVIA ELVARITTA</td></tr>
                    <tr><td>• 2560765 - MUHAMMAD AQIL</td><td>• 2560739 - RAFI ALIFIA SHARIATI</td></tr>
                    <tr><td>• 2560796 - TIARA APRILIANTI</td><td></td></tr>
                </table>
            </td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## Selamat Datang
    Aplikasi **Kalkulator Kimia** ini dibuat untuk membantu melakukan perhitungan kimia dengan cepat, mudah, dan akurat.
    ### Fitur
    - 🧪 Perhitungan Bobot Molekul (BM/Mr)
    - 🔄 Konversi Satuan Kimia
    - 💧 Perhitungan Faktor Pengenceran
    """)

elif menu_pilih == "Bobot Molekul":
    # Ketika menu ini dipilih, bagian atas langsung bersih dan menampilkan elemen ini
    st.title("🔬 Perhitungan Bobot Molekul")
    st.markdown("---")
    input_senyawa = st.text_input("Masukkan Rumus Kimia Senyawa (Contoh: H2SO4, NaOH):", "H2SO4")
    if st.button("Hitung BM / Mr"):
        if input_senyawa:
            bm, error_unsur, cara_teks = hitung_bm_dari_teks(input_senyawa)
            if error_unsur: st.error(f"Unsur tidak dikenal: {', '.join(error_unsur)}.")
            else:
                st.success(f"Bobot Molekul (BM) dari {input_senyawa} adalah: {format_koma(bm)} g/mol")
                st.info(f"**Proses Hitung:** Mr = {cara_teks}")
        else: st.warning("Silakan isi rumus kimia.")

elif menu_pilih == "Konversi":
    st.title("🔄 Konversi Hubungan Satuan Kimia")
    st.markdown("---")
    mr_val = st.number_input("Massa Molar / Mr Senyawa (g/mol):", min_value=0.1, value=98.0)
    val_val = st.number_input("Valensi / Ekivalen Zat (n):", min_value=1, value=2)
    rho_val = st.number_input("Massa Jenis Larutan / ρ (g/mL):", min_value=0.01, value=1.0)
    
    satuan_asal = st.selectbox("Pilih Satuan Asal:", ["Molaritas (M)", "Normalitas (N)"])
    satuan_tujuan = st.selectbox("Pilih Satuan Tujuan:", ["Normalitas (N)", "Molaritas (M)"])
    nilai_asal = st.number_input(f"Masukkan Nilai {satuan_asal}:", min_value=0.0, value=1.0)
    
    if st.button("Proses Konversi"):
        if satuan_asal == "Molaritas (M)" and satuan_tujuan == "Normalitas (N)":
            hasil = nilai_asal * val_val
            st.success(f"Hasil: {format_koma(hasil)} N")
        elif satuan_asal == "Normalitas (N)" and satuan_tujuan == "Molaritas (M)":
            hasil = nilai_asal / val_val
            st.success(f"Hasil: {format_koma(hasil)} M")

elif menu_pilih == "Pengenceran":
    st.title("🧪 Perhitungan Pengenceran Larutan")
    st.markdown("---")
    m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat (M1):", min_value=0.01, value=12.0)
    m2 = st.number_input("Masukkan Konsentrasi Larutan Encer (M2):", min_value=0.01, value=0.5)
    v2 = st.number_input("Masukkan Volume Larutan Encer (V2) dalam mL:", min_value=0.01, value=500.0)
    if st.button("Hitung V1"):
        if m1 >= m2:
            v1 = (m2 * v2) / m1
            st.success(f"Ambil {format_koma(v1)} mL larutan pekat, encerkan hingga {format_koma_v(v2)} mL.")
        else: st.error("M1 harus lebih besar dari M2!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelompok 7 | © 2026")
