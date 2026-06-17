import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# --- STYLE CSS CUSTOM (BACKGROUND MOLEKUL & CARD ELEGAN) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 50%, #ffffff 100%) !important;
        background-attachment: fixed !important;
        color: #1e293b;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; opacity: 0.06; z-index: 0;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230f766e' stroke-width='3'%3E%3Cpath d='M80 650 L140 650 L120 530 L100 530 Z' /%3E%3Cpath d='M100 560 L140 560 M105 590 L135 590 M110 620 L130 620' /%3E%3Ccircle cx='190' cy='520' r='12' /%3E%3Ccircle cx='250' cy='490' r='18' /%3E%3Ccircle cx='290' cy='540' r='10' /%3E%3Cline x1='190' y1='520' x2='235' y2='495' /%3E%3Cline x1='250' y1='490' x2='290' y2='530' /%3E%3C/g%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230f766e' stroke-width='2.5'%3E%3Cpath d='M680 150 L680 190 L630 300 L730 300 L680 190' /%3E%3Cpath d='M645 270 L715 270 M655 240 L705 240' /%3E%3Cpolygon points='600,100 640,80 680,100 680,140 640,160 600,140' /%3E%3Cpolygon points='560,140 600,160 600,200 560,220 520,200 520,140' /%3E%3C/g%3E%3C/svg%3E");
        background-position: left bottom, right top; background-repeat: no-repeat; background-size: 350px, 350px;
    }
    div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid #e2e8f0;
    }
    h1, h2, h3 { color: #0f766e !important; font-weight: 700; }
    .identitas-box {
        background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 12px;
        border-left: 5px solid #0f766e; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 10px; margin-bottom: 25px;
    }
    .feature-card {
        background-color: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 8px;
        border: 1px solid #e2e8f0; border-left: 4px solid #0f766e; margin-bottom: 5px;
    }
    .feature-title { color: #0f766e; font-weight: bold; font-size: 1.05rem; margin-bottom: 5px; }
    .feature-desc { color: #334155; font-size: 0.92rem; line-height: 1.5; }
    
    /* Box Petunjuk Navigasi Baru */
    .nav-instruction-box {
        background-color: #e0f2fe; color: #0369a1; padding: 15px; border-radius: 8px;
        border: 1px solid #bae6fd; margin-top: 25px; font-size: 0.95rem; font-weight: 500;
        display: flex; align-items: center; gap: 10px;
    }
    
    .stButton>button {
        background-color: #0f766e !important; color: white !important;
        border-radius: 8px !important; font-weight: bold !important; border: none !important;
        width: 100%; padding: 10px 0px; box-shadow: 0 2px 4px rgba(15, 118, 110, 0.2);
    }
    .stButton>button:hover { background-color: #0d9488 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK ---
AR_PERIODIK = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'Ag': 107.87, 'I': 126.90, 'Ba': 137.33, 'Pb': 207.2
}

# --- FUNGSI FORMAT ANGKA ---
def format_4_angka(nilai): return f"{nilai:.4f}".replace('.', ',')
def format_2_angka(nilai): return f"{nilai:.2f}".replace('.', ',')
def format_dinamis(nilai):
    return f"{round(nilai, 2):,}".replace('.', 'X').replace(',', '.').replace('X', ',')

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
            rincian.append(f"({jumlah} × Ar {unsur} [{format_4_angka(ar_unsur)}])")
        else: unsur_tidak_dikenal.append(unsur)
    return total_bm, unsur_tidak_dikenal, " + ".join(rincian)

# ==========================================
# SIDEBAR NAVIGASI (BERSIH)
# ==========================================
st.sidebar.title("🧪 Kalkulator Kimia")
st.sidebar.markdown("---")
menu_pilih = st.sidebar.radio(
    "", 
    ["🏠 Home", "🔬 Bobot Molekul", "🔄 Konversi Satuan", "💧 Faktor Pengenceran"]
)

# ==========================================
# LOGIKA STRUKTUR HALAMAN UTAMA
# ==========================================

if menu_pilih == "🏠 Home":
    st.title("🧪 Kalkulator Kimia")
    st.markdown("### Perhitungan Bobot Molekul, Konversi Satuan, dan Faktor Pengenceran")
    st.markdown("---")
    
    # BOX INFORMASI MAKALAH
    st.markdown("""
    <div class="identitas-box">
        <div style="color: #0f766e; font-weight: bold; font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; margin-bottom: 10px;">
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

    st.markdown("<h2>📚 Panduan Fitur Aplikasi</h2>", unsafe_allow_html=True)
    st.write("Klik masing-masing panel di bawah ini untuk melihat detail kegunaan menu:")

    with st.expander("🔬 FITUR 1: Perhitungan Bobot Molekul (BM / Mr)"):
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Deskripsi Fungsi Bobot Molekul</div>
            <div class="feature-desc">
                Menghitung massa molekul relatif berdasarkan rumus kimia yang dimasukkan analis dengan menjabarkan runtutan nilai atom relatif (Ar).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔄 FITUR 2: Konversi Hubungan Satuan Kimia"):
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Deskripsi Fungsi Konversi Satuan</div>
            <div class="feature-desc">
                Mengonversi kadar antar-satuan parameter kimia seperti Molaritas, Normalitas, Massa (gram), %b/b, ppm, dan Mol secara komprehensif.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("💧 FITUR 3: Perhitungan Faktor Pengenceran"):
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Deskripsi Fungsi Faktor Pengenceran</div>
            <div class="feature-desc">
                Mencari tahu volume larutan induk pekat asal yang harus dipipet sebelum diencerkan menggunakan hitungan stoikiometri akurat.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- BOX PETUNJUK NAVIGASI DI BAGIAN BAWAH ---
    st.markdown("""
    <div class="nav-instruction-box">
        💡 <b>Petunjuk Penggunaan:</b> Seluruh fitur perhitungan di atas dapat diakses langsung melalui 
        <b>Menu Navigasi di Sebelah Kiri Atas Layar</b>. Jika menu tidak terlihat, silakan klik tanda panah 
        &nbsp;<b>&gt;</b>&nbsp; di pojok kiri atas untuk membuka panel navigasi halaman.
    </div>
    """, unsafe_allow_html=True)

elif menu_pilih == "🔬 Bobot Molekul":
    st.title("🔬 Perhitungan Bobot Molekul")
    st.markdown("---")
    input_senyawa = st.text_input("Masukkan Rumus Kimia Senyawa (Contoh: H2SO4, Ca(OH)2, NaCl):", "H2SO4")
    
    if st.button("Hitung BM / Mr"):
        if input_senyawa:
            bm, error_unsur, cara_teks = hitung_bm_dari_teks(input_senyawa)
            if error_unsur: 
                st.error(f"Unsur tidak dikenal: {', '.join(error_unsur)}. Gunakan huruf besar di awal unsur (Contoh: 'NaOH' bukan 'naoh').")
            else:
                st.success(f"Bobot Molekul (BM) dari {input_senyawa} adalah: {format_4_angka(bm)} g/mol")
                st.info(f"**Proses Perhitungan:**\n\n$$\\text{{Mr }} {input_senyawa} = {cara_teks} = {format_4_angka(bm)}\\text{{ g/mol}}$$")
        else: 
            st.warning("Silakan isi rumus kimia terlebih dahulu.")

elif menu_pilih == "🔄 Konversi Satuan":
    st.title("🔄 Konversi Hubungan Satuan Kimia")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        mr_input = st.number_input("Massa Molar / Mr Zat (g/mol):", min_value=0.1, value=98.0000, format="%.4f")
        val_input = st.number_input("Valensi Zat / Ekivalen (n):", min_value=1, value=2, step=1)
    with col2:
        vol_input = st.number_input("Volume Larutan (mL):", min_value=0.1, value=1000.0000, format="%.4f")
        rho_input = st.number_input("Massa Jenis Larutan / ρ (g/mL):", min_value=0.01, value=1.0000, format="%.4f")

    st.markdown("### Parameter Konversi")
    satuan_asal = st.selectbox("Pilih Satuan Asal yang Diketahui:", ["Molaritas (M)", "Normalitas (N)", "Massa (gram)", "% b/b", "ppm (mg/L)", "Mol (n)"])
    nilai_asal = st.number_input(f"Masukkan Nilai dari {satuan_asal}:", min_value=0.0, value=1.0000, format="%.4f")
    
    st.markdown("---")
    if st.button("Proses Perhitungan Konversi"):
        v_liter = vol_input / 1000.0
        massa_larutan = vol_input * rho_input
        
        if satuan_asal == "Molaritas (M)":
            molaritas = nilai_asal
        elif satuan_asal == "Normalitas (N)":
            molaritas = nilai_asal / val_input
        elif satuan_asal == "Massa (gram)":
            molaritas = (nilai_asal / mr_input) / v_liter
        elif satuan_asal == "% b/b":
            molaritas = (nilai_asal * 10 * rho_input) / mr_input
        elif satuan_asal == "ppm (mg/L)":
            molaritas = (nilai_asal / 1000.0) / mr_input
        elif satuan_asal == "Mol (n)":
            molaritas = nilai_asal / v_liter

        # Hitung seluruh parameter keluaran
        res_m = molaritas
        res_n = molaritas * val_input
        res_gr = molaritas * mr_input * v_liter
        res_pct = (molaritas * mr_input) / (10 * rho_input)
        res_ppm = molaritas * mr_input * 1000.0
        res_mol = molaritas * v_liter

        st.success("✨ Hasil Konversi Hubungan Parameter Satuan:")
        
        st.markdown(f"""
        | Parameter Satuan Kimia | Nilai Hasil Analisis |
        | :--- | :--- |
        | **Molaritas (M)** | {format_4_angka(res_m)} M |
        | **Normalitas (N)** | {format_4_angka(res_n)} N |
        | **Massa Zat Terlarut** | {format_dinamis(res_gr)} gram |
        | **Kadar Senyawa (% b/b)** | {format_dinamis(res_pct)} % |
        | **Konsentrasi Trace (ppm)** | {format_dinamis(res_ppm)} ppm |
        | **Jumlah Zat (Mol)** | {format_dinamis(res_mol)} mol |
        """)

        st.info(f"**Proses Alur Perhitungan Matematis (Jembatan Konversi Molaritas Utama):**\n\n"
                f"1. Didapatkan nilai **Molaritas Dasar** = ${format_4_angka(res_m)}\\text{{ M}}$\n"
                f"2. Penentuan Normalitas: $$N = M \\times n = {format_4_angka(res_m)} \\times {val_input} = {format_4_angka(res_n)}\\text{{ N}}$$\n"
                f"3. Penentuan Massa: $$g = M \\times Mr \\times V_{{(L)}} = {format_4_angka(res_m)} \\times {format_4_angka(mr_input)} \\times {format_4_angka(v_liter)} = {format_dinamis(res_gr)}\\text{{ gram}}$$\n"
                f"4. Penentuan Kadar %b/b: $$\\% = \\frac{{M \\times Mr}}{{10 \\times \\rho}} = {format_dinamis(res_pct)}\\%$$\n"
                f"5. Penentuan ppm: $$\\text{{ppm}} = M \\times Mr \\times 1000 = {format_dinamis(res_ppm)}\\text{{ ppm}}$$\n"
                f"6. Penentuan Mol: $$\\text{{mol}} = M \\times V_{{(L)}} = {format_dinamis(res_mol)}\\text{{ mol}}$$")

elif menu_pilih == "💧 Faktor Pengenceran":
    st.title("🧪 Perhitungan Pengenceran Larutan")
    st.markdown("---")
    
    m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat (M1 / N1):", min_value=0.01, value=12.00, format="%.2f")
    m2 = st.number_input("Masukkan Konsentrasi Larutan Encer (M2 / N2):", min_value=0.01, value=0.50, format="%.2f")
    v2 = st.number_input("Masukkan Volume Larutan Encer Target (V2) dalam mL:", min_value=0.1, value=500.00, format="%.2f")
    
    if st.button("Hitung Kebutuhan Volume Pekat (V1)"):
        if m1 >= m2:
            v1 = (m2 * v2) / m1
            st.success(f"Hasil: Ambil {format_2_angka(v1)} mL larutan pekat, lalu encerkan hingga {format_2_angka(v2)} mL.")
            
            st.info(f"**Proses Perhitungan:**\n\n"
                    f"Menggunakan Asas Hukum Pengenceran Larutan Analitis:\n"
                    f"$$C_1 \\times V_1 = C_2 \\times V_2$$\n\n"
                    f"Maka rumus mencari volume awal pekat ($V_1$) adalah:\n"
                    f"$$V_1 = \\frac{{C_2 \\times V_2}}{{C_1}}$$\n\n"
                    f"$$V_1 = \\frac{{{format_2_angka(m2)} \\times {format_2_angka(v2)}}}{{{format_2_angka(m1)}}}$$\n\n"
                    f"$$V_1 = \\frac{{{format_2_angka(m2 * v2)}}}{{{format_2_angka(m1)}}}$$\n\n"
                    f"$$V_1 = {format_2_angka(v1)}\\text{{ mL}}$$")
        else: 
            st.error("Gagal: Konsentrasi awal (M1/N1) wajib lebih besar daripada konsentrasi akhir (M2/N2)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelompok 7 | © 2026")
