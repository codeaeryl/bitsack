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
# mesin algoritma (core/dfs.py) secara visual dan interaktif.

# Tambahkan root direktori ke system path agar Python bisa membaca folder 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# Meningkatkan batas rekursi untuk mencegah error saat menggunakan algoritma Core pada data besar
sys.setrecursionlimit(150000)

from src.core.dfs import jalankan_dfs_modular as dfs_core
from src.utils.loader import load_csv

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
jalankan_btn = st.sidebar.button("Jalankan Algoritma", type="primary", use_container_width=True)

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
        raw_data = load_csv(csv_path)
        if raw_data and len(raw_data) > 1:
            df_barang = pd.DataFrame(raw_data[1:], columns=raw_data[0])
            # Pastikan tipe data kolom Pandas adalah integer
            if 'weight' in df_barang.columns:
                df_barang['weight'] = df_barang['weight'].astype(int)
            if 'profit' in df_barang.columns:
                df_barang['profit'] = df_barang['profit'].astype(int)
        else:
            df_barang = pd.DataFrame({
                "label": pd.Series(dtype=str),
                "weight": pd.Series(dtype=int),
                "profit": pd.Series(dtype=int)
            })
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
    if jalankan_btn:
        if len(edited_df) < 8:
            st.error("❌ Jumlah barang minimal 8.")
            # Hapus hasil sebelumnya dari session state jika validasi gagal
            for key in ['hasil', 'waktu_eksekusi', 'kapasitas_w']:
                if key in st.session_state:
                    del st.session_state[key]
        else:
            # Periksa jika ada nilai yang kosong atau tidak valid
            has_invalid = False
            for item in edited_df.to_dict(orient='records'):
                label = item.get("label")
                weight = item.get("weight")
                profit = item.get("profit")
                if (not label or pd.isna(label) or 
                    weight is None or pd.isna(weight) or 
                    profit is None or pd.isna(profit) or
                    float(weight) < 1 or float(profit) < 1):
                    has_invalid = True
                    break
            
            if has_invalid:
                st.error("❌ Semua kolom (Label, Berat, Profit) harus diisi dan nilai Berat/Profit minimal 1.")
                for key in ['hasil', 'waktu_eksekusi', 'kapasitas_w']:
                    if key in st.session_state:
                        del st.session_state[key]
            else:
                with st.spinner(f"Algoritma sedang bekerja memproses {len(edited_df)} data..."):
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
                    hasil = dfs_core(data_list, kapasitas_w=kapasitas_w)
                    end_time = time.time()
                    
                    waktu_eksekusi = (end_time - start_time) * 1000
                    
                    # Simpan hasil ke session_state agar tetap tersedia saat rerun
                    st.session_state['hasil'] = hasil
                    st.session_state['waktu_eksekusi'] = waktu_eksekusi
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
        
        if hasil.get('exploration_log'):
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
            best_node_id = hasil.get('best_node_id')
            
            # Membangun pohon dari log eksplorasi
            for log in hasil['exploration_log']:
                node_id = str(log['node'])
                status = log['status']
                item_name = log.get('current_item', f"Item-? (Node {log['node']})")
                depth = depth_map.get(item_name, 0)
                
                label_text = f"Node {node_id}\n{item_name}\nProfit: {log['profit']}\nBerat: {log['weight']}"
                
                # Logika warna node berdasarkan jenis pruning / status
                if log['node'] == best_node_id:
                    color = "#FFD700" # Emas (Gold) untuk solusi terbaik
                    label_text = f"⭐ Node {node_id}\n{item_name}\nProfit: {log['profit']}\nBerat: {log['weight']}\n(SOLUSI TERBAIK)"
                    pohon_dfs.node(node_id, label_text, shape="box", style="filled,bold", fillcolor=color, fontname="Arial", fontsize="10", penwidth="3")
                elif status == "PRUNED":
                    color = "#FFA07A" # Salmon (Light Salmon) untuk Pruning Kapasitas (tidak muat / PRUNED)
                    pohon_dfs.node(node_id, label_text, shape="box", style="filled", fillcolor=color, fontname="Arial", fontsize="10")
                elif status == "LEAF" or item_name == "LEAF":
                    color = "#90EE90" # Hijau (Light Green) untuk daun/ujung normal
                    pohon_dfs.node(node_id, label_text, shape="box", style="filled", fillcolor=color, fontname="Arial", fontsize="10")
                else:
                    color = "#ADD8E6" # Biru (Light Blue) untuk eksplorasi normal
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
                        
                    is_pruned = "PRUNED" in status or status == "Pruned"
                    edge_style = "dashed" if is_pruned else "solid"
                    if is_pruned: edge_color = "red"
                    
                    pohon_dfs.edge(parent_id_str, node_id, label=edge_label, style=edge_style, color=edge_color, fontname="Arial", fontsize="9")
                    
                last_seen_at_depth[depth] = log
                    
            st.graphviz_chart(pohon_dfs)
            
            # Legenda Warna (Legend) - Dinamis berdasarkan status yang muncul
            all_statuses = {log['status'] for log in hasil['exploration_log']}
            has_leaf = any(log.get('current_item') == 'LEAF' or log.get('status') == 'LEAF' for log in hasil['exploration_log'])
            
            legend_lines = ["**🎨 Legenda Warna Node:**"]
            if best_node_id is not None:
                legend_lines.append("* ⭐ **Emas (Gold)**: Solusi Terbaik (Node dengan profit optimal)")
            legend_lines.append("* 🔵 **Biru Muda**: Eksplorasi Normal (Evaluasi keputusan barang saat ini)")
            if has_leaf:
                legend_lines.append("* 🟢 **Hijau Muda**: Solusi Ujung / LEAF (Selesai diproses)")
            if any("PRUNED" in s for s in all_statuses):
                legend_lines.append("* 🟧 **Salmon**: Pruning / PRUNED (Kapasitas tidak muat)")
            
            st.markdown("\n".join(legend_lines))
            
            # Fitur Download Gambar Pohon
            st.markdown("##### 💾 Unduh Grafik Pohon")
            
            png_data = None
            try:
                # Coba render secara lokal menggunakan binary Graphviz 'dot'
                png_data = pohon_dfs.pipe(format='png')
            except Exception as e:
                # Fallback ke QuickChart Graphviz API jika binary lokal tidak terinstall
                try:
                    import urllib.request
                    import json
                    api_url = "https://quickchart.io/graphviz"
                    payload = {"graph": pohon_dfs.source, "format": "png"}
                    data = json.dumps(payload).encode('utf-8')
                    req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10) as response:
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
        st.info("👈 Tekan tombol **Jalankan Algoritma** di menu samping untuk memproses data.")