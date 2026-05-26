import streamlit as st
import pandas as pd
import os
import graphviz

# 1. Pengaturan Dasar Halaman
st.set_page_config(page_title="Knapsack 0/1 Optimizer", page_icon="🎒", layout="wide")
st.title("🎒 Knapsack 0/1 Backtracking Optimizer")

# ==========================================
# FITUR 9: INPUT FORM (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Pengaturan Knapsack")
# Input kapasitas W
kapasitas_w = st.sidebar.number_input("Kapasitas Maksimal (W)", min_value=1, value=10, step=1)

st.sidebar.markdown("---")
st.sidebar.info("Mesin algoritma sedang dikembangkan oleh Jayden & Ko Calvin. Saat ini menggunakan mode Dummy.")

# ==========================================
# FITUR 10: MEMBACA & MENAMPILKAN TABEL INPUT
# ==========================================
# Mengambil path relatif ke data/test.csv
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "../../data/test.csv")

# Membaca data CSV dengan Pandas
try:
    df_barang = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"File CSV tidak ditemukan di: {csv_path}")
    df_barang = pd.DataFrame()

# Membagi layar utama menjadi 2 kolom (Kiri untuk Tabel, Kanan untuk Hasil & Pohon)
col1, col2 = st.columns([1, 2])

# ------ KOLOM KIRI (Tabel) ------
with col1:
    st.subheader("📦 Tabel Barang Input")
    if not df_barang.empty:
        st.markdown("💡 *Kamu bisa mengedit, menambah, atau menghapus baris.*")
        
        # MENGGUNAKAN DATA EDITOR (Tabel Interaktif)
        edited_df = st.data_editor(
            df_barang,
            width="stretch",
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "label": st.column_config.TextColumn("Nama Barang (ID)", required=True),
                "weight": st.column_config.NumberColumn("Berat (W)", min_value=0.1, step=0.1, format="%.2f"),
                "profit": st.column_config.NumberColumn("Profit (P)", min_value=0.1, step=0.1, format="$%.2f")
            }
        )
        st.caption(f"Total barang siap diproses: {len(edited_df)} item")

# ------ KOLOM KANAN (Pohon & Statistik) ------
with col2:
    # ==========================================
    # FITUR 11: VISUALISASI POHON GRAPHVIZ (DINAMIS)
    # ==========================================
    st.subheader("🌳 Visualisasi Pohon Pencarian")
    
    # Simulasi data "Log Node" dari mesin backend (Dummy)
    dummy_nodes = [
        {"id": "Root", "label": "Kapasitas: 10\nProfit: 0", "color": "lightblue", "shape": "box"},
        {"id": "A", "label": "Ambil Apple\nProfit: 3.50", "color": "lightgreen", "shape": "box"},
        {"id": "B", "label": "Skip Apple\nProfit: 0.00", "color": "lightblue", "shape": "box"},
        {"id": "C", "label": "Ambil Banana\nProfit: 5.60", "color": "lightgreen", "shape": "box"},
        {"id": "D", "label": "Pruned!\nOverweight", "color": "lightpink", "shape": "ellipse"}
    ]

    dummy_edges = [
        {"from": "Root", "to": "A", "label": " Masuk tas"},
        {"from": "Root", "to": "B", "label": " Lewati"},
        {"from": "A", "to": "C", "label": " Masuk tas"},
        {"from": "B", "to": "D", "label": " Heuristik jelek", "style": "dashed", "color": "red"}
    ]

    # Membuat kanvas Graphviz secara dinamis menggunakan Python
    pohon_dfs = graphviz.Digraph()
    pohon_dfs.attr(rankdir='TB')

    for node in dummy_nodes:
        pohon_dfs.node(node["id"], node["label"], shape=node["shape"], style="filled", fillcolor=node["color"], fontname="Arial")

    for edge in dummy_edges:
        style_garis = edge.get("style", "solid")
        warna_garis = edge.get("color", "black")
        pohon_dfs.edge(edge["from"], edge["to"], label=edge["label"], style=style_garis, color=warna_garis, fontname="Arial", fontsize="10")

    # Merender grafik ke layar web
    st.graphviz_chart(pohon_dfs)
    
    st.markdown("---")

    # ==========================================
    # FITUR 12: PANEL SOLUSI & METRIK (DUMMY)
    # ==========================================
    st.subheader("📊 Statistik Performa")
    # Menggunakan komponen Metric dari Streamlit
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Profit Optimal", value="25.40") # Angka dummy
    m2.metric(label="Waktu Eksekusi", value="12 ms")      # Angka dummy
    m3.metric(label="Node Dikunjungi", value="45 Node")   # Angka dummy