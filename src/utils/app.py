import streamlit as st
import pandas as pd
import os

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

with col1:
    st.subheader("📦 Tabel Barang Input")
    if not df_barang.empty:
        # Menampilkan dataframe interaktif
        st.dataframe(df_barang, use_container_width=True)
        st.caption(f"Total barang: {len(df_barang)} item")

# ==========================================
# FITUR 12: PANEL SOLUSI & METRIK (DUMMY)
# ==========================================
with col2:
    st.subheader("📊 Statistik Performa")
    # Menggunakan komponen Metric dari Streamlit
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Profit Optimal", value="25.40") # Angka dummy
    m2.metric(label="Waktu Eksekusi", value="12 ms")      # Angka dummy
    m3.metric(label="Node Dikunjungi", value="45 Node")   # Angka dummy

    st.markdown("---")

    # ==========================================
    # FITUR 11: VISUALISASI POHON GRAPHVIZ (DUMMY)
    # ==========================================
    st.subheader("🌳 Visualisasi Pohon Pencarian")
    # Contoh graf pohon statis sebelum disuntik data dari backend
    st.graphviz_chart('''
        digraph {
            node [fontname="Arial", shape="box", style="rounded,filled", fillcolor="lightblue"]
            edge [fontname="Arial", fontsize=10]
            
            "Root" -> "Ambil Apple" [label="  Masuk tas"]
            "Root" -> "Skip Apple" [label="  Lewati"]
            
            "Ambil Apple" -> "Ambil Banana" [color="green", penwidth=2]
            "Ambil Apple" -> "Skip Banana"
            
            "Skip Apple" -> "Pruned!" [color="red", style="dashed", label=" Heuristik jelek"]
            "Pruned!" [fillcolor="lightpink", shape="ellipse"]
        }
    ''')