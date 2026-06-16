import streamlit as st
import pandas as pd
import os
import graphviz
import time
import glob
import sys

# src/app.py
# Modul ini adalah Antarmuka Web Utama (Front-end) dari proyek Knapsack 0/1.
# Dibangun menggunakan framework Streamlit. Modul ini menghubungkan pengguna dengan
# mesin algoritma (core/dfs.py dan optimize/dfs.py) secara visual dan interaktif.

# Tambahkan root direktori ke system path agar Python bisa membaca folder 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# Meningkatkan batas rekursi untuk mencegah error saat menggunakan algoritma Core pada data besar
sys.setrecursionlimit(150000)

from src.core.dfs import jalankan_dfs_modular as dfs_core
from src.optimize.dfs import jalankan_dfs_modular as dfs_optimize

# 1. Pengaturan Dasar Halaman
st.set_page_config(page_title="Knapsack 0/1 Optimizer", page_icon="🎒", layout="wide")
st.title("🎒 Knapsack 0/1 Backtracking Optimizer")

# ==========================================
# FITUR 9: INPUT FORM (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Pengaturan Knapsack")
# Input kapasitas W
kapasitas_w = st.sidebar.number_input("Kapasitas Maksimal (W)", min_value=1, value=10, step=1)

# Pilihan Sumber Data Dinamis dari Folder 'data'
current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "../data")
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
file_names = ["📝 Input Manual"] + [os.path.basename(f) for f in csv_files]

selected_file = st.sidebar.selectbox("📂 Pilih Dataset", file_names)

st.sidebar.markdown("### 🚀 Eksekusi Algoritma")
jalankan_core_btn = st.sidebar.button("Jalankan Algoritma (Core)", use_container_width=True)
jalankan_opt_btn = st.sidebar.button("Jalankan Algoritma (Versi Optimize)", type="primary", use_container_width=True)

# ==========================================
# FITUR 10: MEMBACA & MENAMPILKAN TABEL INPUT
# ==========================================
if selected_file == "📝 Input Manual":
    df_barang = pd.DataFrame({
        "label": pd.Series(dtype=str),
        "weight": pd.Series(dtype=int),
        "profit": pd.Series(dtype=int)
    })
elif selected_file:
    csv_path = os.path.join(data_dir, selected_file)
    try:
        df_barang = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"File CSV tidak ditemukan di: {csv_path}")
        df_barang = pd.DataFrame({
            "label": pd.Series(dtype=str),
            "weight": pd.Series(dtype=int),
            "profit": pd.Series(dtype=int)
        })
else:
    df_barang = pd.DataFrame({
        "label": pd.Series(dtype=str),
        "weight": pd.Series(dtype=int),
        "profit": pd.Series(dtype=int)
    })

# Convert weight and profit columns to integer to satisfy integer requirement
if not df_barang.empty:
    if 'weight' in df_barang.columns:
        df_barang['weight'] = pd.to_numeric(df_barang['weight'], errors='coerce').fillna(0).astype(int)
    if 'profit' in df_barang.columns:
        df_barang['profit'] = pd.to_numeric(df_barang['profit'], errors='coerce').fillna(0).astype(int)

# Membagi layar utama menjadi 2 kolom (Kiri untuk Tabel, Kanan untuk Hasil & Pohon)
col1, col2 = st.columns([1, 2])

# ------ KOLOM KIRI (Tabel) ------
with col1:
    st.subheader("📦 Tabel Barang Input")
    if df_barang is not None:
        st.markdown("💡 *Kamu bisa mengedit, menambah, atau menghapus baris sebelum dijalankan.*")
        
        # MENGGUNAKAN DATA EDITOR (Tabel Interaktif)
        edited_df = st.data_editor(
            df_barang,
            width="stretch",
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "label": st.column_config.TextColumn("Nama Barang (ID)", required=True),
                "weight": st.column_config.NumberColumn("Berat (W)", min_value=1, step=1, format="%d"),
                "profit": st.column_config.NumberColumn("Profit (P)", min_value=1, step=1, format="%d")
            }
        )
        st.caption(f"Total barang siap diproses: {len(edited_df)} item")

# ------ KOLOM KANAN (Pohon & Statistik) ------
with col2:
    # Jalankan algoritma dan simpan hasil ke session_state
    if jalankan_core_btn or jalankan_opt_btn:
        if len(edited_df) < 8:
            st.error("❌ Jumlah barang minimal 8.")
            # Clear previous results from session state if validation fails
            for key in ['hasil', 'waktu_eksekusi', 'mesin_aktif', 'kapasitas_w']:
                if key in st.session_state:
                    del st.session_state[key]
        else:
            mesin_aktif = "Core" if jalankan_core_btn else "Versi Optimize"
            fungsi_dfs = dfs_core if jalankan_core_btn else dfs_optimize
            
            with st.spinner(f"Mesin {mesin_aktif} sedang bekerja memproses {len(edited_df)} data..."):
                # Konversi data editor ke list of dicts dan pastikan bertipe integer
                data_list = []
                for item in edited_df.to_dict(orient='records'):
                    data_list.append({
                        "label": str(item["label"]),
                        "weight": int(float(item["weight"])),
                        "profit": int(float(item["profit"]))
                    })
                
                # Eksekusi Algoritma
                start_time = time.time()
                hasil = fungsi_dfs(data_list, kapasitas_w=kapasitas_w)
                end_time = time.time()
                
                waktu_eksekusi = (end_time - start_time) * 1000
                
                # Simpan hasil ke session_state agar tetap tersedia saat rerun
                st.session_state['hasil'] = hasil
                st.session_state['waktu_eksekusi'] = waktu_eksekusi
                st.session_state['mesin_aktif'] = mesin_aktif
                st.session_state['kapasitas_w'] = kapasitas_w

    # Tampilkan hasil dari session_state (tetap muncul walau tombol download diklik)
    if 'hasil' in st.session_state:
        hasil = st.session_state['hasil']
        waktu_eksekusi = st.session_state['waktu_eksekusi']
        kapasitas_w_hasil = st.session_state['kapasitas_w']

        # ==========================================
        # FITUR 11: VISUALISASI POHON GRAPHVIZ (DINAMIS)
        # ==========================================
        st.subheader("🌳 Visualisasi Pohon Pencarian")
        
        if hasil.get('exploration_log') and len(hasil['exploration_log']) <= 1000:
            pohon_dfs = graphviz.Digraph()
            pohon_dfs.attr(rankdir='TB')
            
            # Mendeduksi urutan depth dari kemunculan pertama item (Murni trik UI/UX)
            depth_map = {}
            current_depth = 0
            for log in hasil['exploration_log']:
                item_name = log.get('current_item', f"Item-? (Node {log['node']})")
                if item_name not in depth_map:
                    depth_map[item_name] = current_depth
                    current_depth += 1

            last_seen_at_depth = {}
            node_map = {log['node']: log for log in hasil['exploration_log']}
            
            # Membangun pohon dari log eksplorasi
            for log in hasil['exploration_log']:
                node_id = str(log['node'])
                status = log['status']
                item_name = log.get('current_item', f"Item-? (Node {log['node']})")
                depth = depth_map.get(item_name, 0)
                
                label_text = f"Node {node_id}\n{item_name}\nProfit: {log['profit']}\nBerat: {log['weight']}"
                
                # Logika warna node berdasarkan jenis pruning / status
                if "PRUNED (Bound" in status:
                    color = "lightpink" # Merah muda untuk Pruning Batas Atas (Bound)
                elif "PRUNED (No item fits)" in status:
                    color = "orange" # Orange untuk Pruning Kapasitas (No Item Fits)
                elif "TAKEN ALL" in status:
                    color = "lightgreen" # Hijau untuk Sufficiency Pruning (Remaining Fit)
                elif item_name == "LEAF":
                    color = "lightgreen" # Hijau untuk daun/ujung normal
                else:
                    color = "lightblue" # Biru untuk eksplorasi normal
                    
                pohon_dfs.node(node_id, label_text, shape="box", style="filled", fillcolor=color, fontname="Arial", fontsize="10")
                
                # Rekonstruksi Garis (Edge) menggunakan parameter parent_node jika tersedia
                parent_id = log.get('parent')
                parent_log = None
                if parent_id is not None:
                    parent_log = node_map.get(parent_id)
                    
                if parent_log is None and depth > 0:
                    # Fallback ke rekonstruksi matematis
                    parent_log = last_seen_at_depth.get(depth - 1)
                    
                if parent_log is not None:
                    parent_id_str = str(parent_log['node'])
                    
                    # Tentukan apakah cabang ini "Ambil" (x=1) atau "Skip" (x=0) berdasarkan jumlah barang di dalam tas
                    if len(log['chosen']) > len(parent_log['chosen']):
                        edge_label = " x=1"
                        edge_color = "darkgreen"
                    else:
                        edge_label = " x=0"
                        edge_color = "black"
                        
                    edge_style = "dashed" if "PRUNED" in status else "solid"
                    if "PRUNED" in status: edge_color = "red"
                    
                    pohon_dfs.edge(parent_id_str, node_id, label=edge_label, style=edge_style, color=edge_color, fontname="Arial", fontsize="9")
                    
                last_seen_at_depth[depth] = log
                    
            st.graphviz_chart(pohon_dfs)
            
            # Legenda Warna (Legend)
            st.markdown("""
            **🎨 Legenda Warna Node:**
            * 🔵 **Biru Muda**: Eksplorasi Normal (Evaluasi keputusan barang saat ini)
            * 🟢 **Hijau Muda**: Solusi Ujung / LEAF / TAKEN ALL (Selesai diproses atau sisa barang otomatis diambil)
            * 🔴 **Merah Muda**: Pruning Batas Atas (Bound) (Cabang dihentikan karena tidak berpotensi melebihi profit terbaik)
            * 🟠 **Jingga (Orange)**: Pruning Kapasitas (Capacity) (Cabang dihentikan karena tidak ada sisa barang yang muat)
            """)
            
            # Fitur Download Gambar Pohon
            st.markdown("##### 💾 Unduh Grafik Pohon")
            
            png_data = None
            try:
                # Coba render secara lokal menggunakan binary Graphviz 'dot'
                png_data = pohon_dfs.pipe(format='png')
            except Exception as e:
                # Fallback ke QuickChart Graphviz API jika binary lokal tidak terinstall
                try:
                    import urllib.parse
                    import urllib.request
                    encoded_dot = urllib.parse.quote(pohon_dfs.source)
                    api_url = f"https://quickchart.io/graphviz?format=png&graph={encoded_dot}"
                    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=5) as response:
                        png_data = response.read()
                except Exception as api_err:
                    png_data = None
            
            if png_data is not None:
                st.download_button(
                    label="🖼️ Unduh sebagai Gambar (PNG)",
                    data=png_data,
                    file_name="pohon_knapsack.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.error("❌ Gagal membuat gambar PNG (offline & Graphviz tidak terinstall).")
        else:
            st.warning(f"⚠️ Fitur Visualisasi Pohon Graphviz dinonaktifkan karena pohon pencarian terlalu besar (> 1000 node) atau dinonaktifkan untuk mencegah browser crash.")
            st.info("Algoritma tetap sukses memproses seluruh data di belakang layar. Silakan cek hasil akhirnya di bawah!")
            
        st.markdown("---")

        # ==========================================
        # FITUR 12: PANEL SOLUSI & METRIK (DINAMIS)
        # ==========================================
        st.subheader("📊 Statistik Performa")
        
        if hasil.get('timeout'):
            st.warning("⚠️ **WAKTU HABIS (TIMEOUT)!** Proses algoritma dihentikan paksa karena melebihi batas waktu (10 detik). Hasil di bawah ini mungkin belum optimal (belum selesai mengeksplorasi seluruh kemungkinan), melainkan hanya kombinasi terbaik yang berhasil ditemukan sejauh ini.")

        m1, m2, m3 = st.columns(3)
        m1.metric(label="Total Profit Optimal", value=f"{hasil['best_profit']}")
        m2.metric(label="Waktu Eksekusi", value=f"{waktu_eksekusi:.2f} ms")
        m3.metric(label="Node Dikunjungi", value=f"{hasil['nodes_visited']} Node")

        st.markdown("#### 🏆 Solusi Optimal (Barang Terpilih)")
        
        if len(hasil['best_combination']) > 0:
            solusi_df = pd.DataFrame(hasil['best_combination'])
            total_w_solusi = solusi_df['weight'].sum()
            st.success(f"✅ Kombinasi barang terbaik ditemukan! Total Bobot: {int(total_w_solusi)} / {kapasitas_w_hasil}")
            st.dataframe(solusi_df, hide_index=True, use_container_width=True)
        else:
            st.error("Tidak ada barang yang muat di dalam kapasitas tas tersebut.")
            
        st.markdown("---")
    else:
        st.info("👈 Tekan salah satu tombol **Jalankan Algoritma** di menu samping untuk memproses data.")