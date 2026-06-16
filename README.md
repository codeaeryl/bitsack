# bitsack
Algorithmic Strategies Final Project

| NRP     | Nama                                |
| :------ | :---------------------------------- |
| 2272017 | Calvin Yohanis                      |
| 2472007 | Richard Vincentius Christian Dinata |
| 2472048 | Jayden Marvel Ethanael              |

## 📂 Project Structure

🔗 **Repository Link:** [https://github.com/codeaeryl/bitsack](https://github.com/codeaeryl/bitsack)

Berikut adalah struktur direktori proyek **bitsack** beserta penjelasan singkat untuk masing-masing *folder* dan *file* yang ada:

```text
bitsack/
├── data/
│   ├── data.csv
│   ├── data_v2.csv
│   ├── dataset_20.csv
│   ├── dataset_1000.csv
│   └── test.csv
└── src/
    ├── app.py
    ├── core/
    │   ├── __init__.py
    │   ├── bound.py
    │   ├── data.py
    │   ├── dfs.py
    │   └── sort.py
    ├── optimize/
    │   ├── __init__.py
    │   ├── bound.py
    │   ├── data.py
    │   ├── dfs.py
    │   └── sort.py
    └── utils/
        └── loader.py
```

### 📁 Penjelasan Direktori & File

#### 1. `data/` (Dataset Folder)
Berisi seluruh file dataset berformat CSV yang digunakan untuk pengujian algoritma Knapsack.
*   `data.csv`: Dataset utama berisi 100.000 barang dengan nilai bobot dan profit bertipe *float*.
*   `data_v2.csv`: Dataset sekunder berisi 100.000 barang dengan nilai bertipe *integer* bulat.
*   `dataset_20.csv`: Dataset berukuran kecil berisi 20 barang.
*   `dataset_1000.csv`: Dataset berukuran menengah berisi 1.000 barang, cocok untuk melihat komputasi transisi algoritma.
*   `test.csv`: Dataset skala sangat kecil (10 barang dengan nama buah) yang digunakan khusus untuk *testing* manual dan *Live Demo* UI dengan graf pohon *Graphviz*.

#### 2. `src/app.py` (Antarmuka Utama Web - Richard)
Titik masuk utama (*entry point*) sekaligus antarmuka *front-end* interaktif berbasis web menggunakan *framework* **Streamlit**. Dijalankan dengan perintah `python -m streamlit run src/app.py`. Fitur meliputi pemilihan dataset (CSV atau input manual), edit tabel dinamis, eksekusi dua versi algoritma, render visualisasi pohon pencarian dengan **Graphviz**, serta panel statistik performa.

#### 3. `src/core/` (Modul Logika Utama - Calvin)
Berisi implementasi asli dari algoritma rekursif standar sesuai konsep fundamental.
*   `dfs.py`: Inti logika algoritma *Depth-First Search* (DFS) rekursif dan strategi pemangkasan (*Branch & Bound*).
*   `bound.py`: Fungsi heuristik (*Bounding Function*) untuk memprediksi *upper bound* dan memangkas (*pruning*) cabang pohon yang tidak menjanjikan.
*   `sort.py`: Modul *pre-processing* untuk mengurutkan daftar barang berdasarkan rasio *Profit/Weight* tertinggi.
*   `data.py`: Modul untuk membaca dan melakukan *parsing* data masukan (CSV).

#### 4. `src/optimize/` (Modul Optimasi - Jayden)
Berisi implementasi level lanjut yang difokuskan pada kecepatan dan efisiensi memori menggunakan struktur data dan algoritma yang lebih efisien.
*   `dfs.py`: Logika DFS **Iteratif** (tanpa rekursi bawaan Python) berbasis *Stack* yang ditenagai oleh optimasi perhitungan **NumPy** array. Kebal terhadap *RecursionError* pada data berskala 1 Juta.
*   `bound.py`: Implementasi *Bounding Function* teroptimasi dengan *prefix-sum* dan *binary search* O(log n).
*   `sort.py`: Modul *pre-processing* berbasis **NumPy** `argsort` untuk pengurutan cepat.
*   `data.py`: Modul persiapan data menggunakan *Struct-of-Arrays* (parallel lists) untuk akses skalar yang lebih cepat di dalam *DFS loop*.

#### 5. `src/utils/` (Utilitas)
*   `loader.py`: *Helper script* fungsional untuk memuat dan mem-*parsing* file CSV secara generik.

## ⚙️ Cara Menjalankan Aplikasi

Aplikasi ini menggunakan antarmuka web interaktif berbasis Streamlit. Berikut langkah-langkah instalasi dan cara menjalankannya:

### Prasyarat
*   Python 3.10 atau lebih baru.
*   *(Opsional tapi disarankan)* **Graphviz** terinstall di sistem operasi Anda untuk kelancaran *render* visualisasi pohon pencarian (Knapsack Tree) secara lokal. Jika tidak terinstall, aplikasi akan memanggil API sekunder *fallback* yang membutuhkan koneksi internet.

### Instalasi Dependensi

1. Buka terminal (atau Command Prompt) di direktori *root* proyek (`bitsack/`).
2. Buat dan aktifkan *Virtual Environment* (Sangat direkomendasikan):
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di macOS/Linux:
   source venv/bin/activate
   ```
3. Install seluruh dependensi yang dibutuhkan dari file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Modul eksternal utama yang diinstall meliputi `streamlit`, `pandas`, `numpy`, dan `graphviz`)*.

### Menjalankan Streamlit

Jalankan perintah berikut di dalam terminal:
```bash
python -m streamlit run src/app.py
```
Aplikasi akan otomatis terbuka di peramban web (*browser*) *default* Anda pada alamat `http://localhost:8501`.

## 🧠 Penjelasan Algoritma

Proyek ini memecahkan kasus **0/1 Knapsack Problem** menggunakan pendekatan eksplorasi ruang keadaan (*State Space Tree*) lengkap dengan analisis pemangkasan.

Dalam Knapsack 0/1, kita dihadapkan pada sejumlah barang, masing-masing dengan berat (*weight*) dan nilai keuntungan (*profit*). Tujuannya adalah memilih *subset* barang agar total *profit* maksimal tercapai tanpa melampaui kapasitas berat maksimum yang tersedia (*W*). Syarat "0/1" berarti setiap barang bersifat *indivisible*, yakni hanya bisa diambil sepenuhnya (1) atau tidak diambil sama sekali (0).

### 1. Modul Core: DFS Rekursif dengan Branch & Bound
Algoritma inti di `src/core/dfs.py` adalah metode fundamental **Depth-First Search (DFS)** berbasis rekursi yang diperkuat dengan teknik pemangkasan **Branch and Bound**.
*   **Pre-processing (Sort):** Seluruh daftar barang wajib diurutkan terlebih dahulu berdasarkan rasio $\frac{Profit}{Weight}$ secara menurun (*descending*). Urutan ini mutlak diperlukan agar kalkulasi *Bounding Function* dapat bertindak serakah (*greedy*) dengan mengasumsikan barang paling berharga selalu diutamakan.
*   **Eksplorasi DFS:** Menelusuri seluruh kemungkinan permutasi keadaan (ambil barang $x_i=1$ cabang kiri, atau tidak ambil $x_i=0$ cabang kanan).
*   **Bounding Function:** Di setiap pemberhentian (node), program menghitung estimasi batas atas (*upper bound*) dari potensi *profit* tertinggi jika cabang yang sedang ditelusuri dilanjutkan. Estimasi dihitung dengan teknik Knapsack Fraksional (barang sisanya boleh dipotong proporsional). Jika nilai *upper bound* ini ternyata **lebih kecil atau sama dengan** dari *profit* riil terbaik yang sudah digenggam sejauh ini (`best_profit`), maka percabangan tersebut langsung **dipangkas** (*pruned*) guna menghemat waktu karena dijamin tidak mungkin melampaui rekor.

### 2. Modul Optimize: Pendekatan Iteratif & NumPy Stack
Modul optimasi di `src/optimize/dfs.py` adalah *pipeline* eksekusi tingkat lanjut (*advanced*) yang didesain secara khusus untuk dataset kolosal (hingga jutaan baris) di mana rekursif DFS biasa akan otomatis tersandung limit komputasi tumpukan bawaan sistem operasi (*Recursion Depth Exceeded*).
*   **Iterasi Berbasis Stack:** Menggantikan limitasi rekursi semu (manipulasi `sys.setrecursionlimit`) dengan mendirikan struktur data **Stack** (LIFO) otonom yang dibungkus dalam blok `while`. Arsitektur ini sukses memindahkan beban berat dari sempitnya tumpukan eksekusi (*call stack*) ke ranah memori proses (Heap) sistem yang jauh lebih luas.
*   **Akselerasi Numerik (NumPy):**
    *   Pengurutan dinamis (*Sorting*) menggunakan rutinitas *native C* `numpy.argsort()`.
*   **Lapis Ganda Strategi Pemangkasan (Aggressive Bounding):**
    *   **Penyemaian *Greedy Heuristic*:** Menginisialisasi `best_profit` di awal pencarian menggunakan pendekatan *greedy*. Hal ini memicu *pruning* agresif sejak node pertama tanpa harus menunggu DFS secara alami menyentuh dasar pohon (*leaf*).
    *   **Fraksional Bounding O(log N):** Memadukan *Prefix Sum Array* (akumulasi berat dan profit) dengan Pencarian Biner (`bisect` / `numpy.searchsorted`) untuk melompat (*skip index*) ke barang terakhir yang muat. Perhitungan *Upper Bound* menjadi instan dalam hitungan **O(log N)** tanpa perulangan konvensional.
    *   **Sufficiency Pruning O(1):** Jika sisa kapasitas tas ternyata masih muat menampung total berat **seluruh** sisa barang (dikalkulasi secara O(1) melalui selisih *Prefix Sum*), maka sisa cabang otomatis diakhiri dan semua barang sisanya diambil seketika.
    *   **Capacity Pruning O(1):** Menggunakan *Suffix Minimum Weight Array* (pencatatan berat barang teringan yang tersisa). Jika sisa kapasitas tas sudah lebih kecil dari barang teringan sekalipun, mustahil ada barang yang muat. Cabang langsung dimatikan (*pruned*).