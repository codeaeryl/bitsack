import streamlit as st
import pandas as pd
import os
import graphviz
import time
import glob
import sys

# Tambahkan root directory ke sys.path agar bisa import module 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.setrecursionlimit(150000)

import importlib
import src.core.dfs
import src.optimize.dfs
importlib.reload(src.core.dfs)
importlib.reload(src.optimize.dfs)
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
data_dir = os.path.join(current_dir, "../../data")
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
file_names = [os.path.basename(f) for f in csv_files]

selected_file = st.sidebar.selectbox("📂 Pilih Dataset", file_names)

st.sidebar.markdown("### 🚀 Eksekusi Algoritma")
jalankan_core_btn = st.sidebar.button("Jalankan Algoritma (Core)", use_container_width=True)
jalankan_opt_btn = st.sidebar.button("Jalankan Algoritma (Versi Optimize)", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Gunakan tombol di atas untuk membandingkan performa antara algoritma dasar dan algoritma teroptimasi (Iterative + Multiprocessing).")

# ==========================================
# FITUR 10: MEMBACA & MENAMPILKAN TABEL INPUT
# ==========================================
if selected_file:
    csv_path = os.path.join(data_dir, selected_file)
    try:
        df_barang = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"File CSV tidak ditemukan di: {csv_path}")
        df_barang = pd.DataFrame()
else:
    df_barang = pd.DataFrame()

# Membagi layar utama menjadi 2 kolom (Kiri untuk Tabel, Kanan untuk Hasil & Pohon)
col1, col2 = st.columns([1, 2])

# ------ KOLOM KIRI (Tabel) ------
with col1:
    st.subheader("📦 Tabel Barang Input")
    if not df_barang.empty:
        st.markdown("💡 *Kamu bisa mengedit, menambah, atau menghapus baris sebelum dijalankan.*")
        
        # MENGGUNAKAN DATA EDITOR (Tabel Interaktif)
        edited_df = st.data_editor(
            df_barang,
            width="stretch",
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "label": st.column_config.TextColumn("Nama Barang (ID)", required=True),
                "weight": st.column_config.NumberColumn("Berat (W)", min_value=0.1, step=0.1, format="%.2f"),
                "profit": st.column_config.NumberColumn("Profit (P)", min_value=0.1, step=0.1, format="%.2f")
            }
        )
        st.caption(f"Total barang siap diproses: {len(edited_df)} item")

# ------ KOLOM KANAN (Pohon & Statistik) ------
with col2:
    if jalankan_core_btn or jalankan_opt_btn:
        mesin_aktif = "Core" if jalankan_core_btn else "Versi Optimize"
        fungsi_dfs = dfs_core if jalankan_core_btn else dfs_optimize
        
        with st.spinner(f"Mesin {mesin_aktif} sedang bekerja memproses {len(edited_df)} data..."):
            # Konversi data editor ke list of dicts
            data_list = edited_df.to_dict(orient='records')
            
            # Eksekusi Algoritma
            start_time = time.time()
            hasil = fungsi_dfs(data_list, kapasitas_w=kapasitas_w)
            end_time = time.time()
            
            waktu_eksekusi = (end_time - start_time) * 1000
            
            # ==========================================
            # FITUR 11: VISUALISASI POHON GRAPHVIZ (DINAMIS)
            # ==========================================
            st.subheader("🌳 Visualisasi Pohon Pencarian")
            
            if len(edited_df) <= 20:
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
                
                # Membangun pohon dari log eksplorasi (hanya jika data kecil)
                for log in hasil['exploration_log']:
                    node_id = str(log['node'])
                    status = log['status']
                    item_name = log.get('current_item', f"Item-? (Node {log['node']})")
                    depth = depth_map.get(item_name, 0)
                    
                    label_text = f"Node {node_id}\n{item_name}\nProfit: {log['profit']}\nBerat: {log['weight']}"
                    
                    # Logika warna node berdasarkan status
                    if "PRUNED" in status:
                        color = "lightpink" # Merah muda untuk cabang yang dipotong
                    elif item_name == "LEAF":
                        color = "lightgreen" # Hijau untuk daun/ujung
                    else:
                        color = "lightblue" # Biru untuk eksplorasi normal
                        
                    pohon_dfs.node(node_id, label_text, shape="box", style="filled", fillcolor=color, fontname="Arial", fontsize="10")
                    
                    # Rekonstruksi Garis (Edge) secara matematis tanpa parameter parent_node
                    if depth > 0:
                        parent_log = last_seen_at_depth.get(depth - 1)
                        if parent_log is not None:
                            parent_id = str(parent_log['node'])
                            
                            # Tentukan apakah cabang ini "Ambil" (x=1) atau "Skip" (x=0) berdasarkan jumlah barang di dalam tas
                            if len(log['chosen']) > len(parent_log['chosen']):
                                edge_label = " x=1"
                                edge_color = "darkgreen"
                            else:
                                edge_label = " x=0"
                                edge_color = "black"
                                
                            edge_style = "dashed" if "PRUNED" in status else "solid"
                            if "PRUNED" in status: edge_color = "red"
                            
                            pohon_dfs.edge(parent_id, node_id, label=edge_label, style=edge_style, color=edge_color, fontname="Arial", fontsize="9")
                            
                    last_seen_at_depth[depth] = log
                        
                st.graphviz_chart(pohon_dfs)
            else:
                st.warning(f"⚠️ Fitur Visualisasi Pohon Graphviz dinonaktifkan karena dataset masif ({len(edited_df)} barang). Maksimal n=20 untuk mencegah browser crash.")
                st.info("Algoritma tetap sukses memproses ratusan ribu data di belakang layar. Silakan cek hasil akhirnya di bawah!")
                
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
                st.success(f"✅ Kombinasi barang terbaik ditemukan! Total Bobot: {total_w_solusi:.2f} / {kapasitas_w}")
                st.dataframe(solusi_df, hide_index=True, use_container_width=True)
            else:
                st.error("Tidak ada barang yang muat di dalam kapasitas tas tersebut.")
                
            st.markdown("---")
    else:
        st.info("👈 Tekan salah satu tombol **Jalankan Algoritma** di menu samping untuk memproses data.")