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
│   ├── dataset_20.csv
│   └── test.csv
├── src/
│   ├── app.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data.py
│   │   └── dfs.py
│   └── utils/
│       ├── cli.py
│       └── loader.py
└── test/
    ├── test_e2e.py
    └── test_loader.py
```

### 📁 Penjelasan Direktori & File

#### 1. `data/` (Dataset Folder)

Berisi seluruh file dataset berformat CSV yang digunakan untuk pengujian algoritma Knapsack.

* `data.csv`: Dataset berisi 8 barang (digunakan untuk demo visualisasi pohon pencarian skala kecil).
* `dataset_20.csv`: Dataset berisi 20 barang (untuk demonstrasi berukuran sedang).
* `test.csv`: Dataset skala kecil (10 barang valid + 5 barang tidak valid) yang digunakan khusus untuk pengujian loader dan pengujian E2E.

#### 2. `src/app.py` (Antarmuka Utama Web - Richard)
Titik masuk utama (*entry point*) sekaligus antarmuka *front-end* interaktif berbasis web menggunakan *framework* **Streamlit**. Dijalankan dengan perintah `python -m streamlit run src/app.py`. Fitur meliputi pemilihan dataset (CSV atau input manual), edit tabel dinamis, eksekusi algoritma, render visualisasi pohon pencarian dengan **Graphviz**, serta panel statistik performa.

#### 3. `src/core/` (Modul Logika Utama - Calvin & Jayden)
Berisi logika utama algoritma Knapsack 0/1 yang diakselerasi dengan NumPy dan Struct-of-Arrays layout.
*   `dfs.py`: Inti logika algoritma *Depth-First Search* (DFS) rekursif dengan lapis ganda strategi pemangkasan (Sufficiency Pruning, Capacity Pruning, dan Overcapacity Pruning).
*   `data.py`: Modul pra-pemrosesan data menggunakan library komputasi matriks C (NumPy) untuk sorting dan penyiapan layout Struct-of-Arrays secara efisien.

#### 4. `src/utils/` (Utilitas)

* `cli.py`: *Command Line Interface* (CLI) *sandbox* standar untuk menguji logika dari mesin Core terakselerasi secara *headless* melalui terminal.
* `loader.py`: *Helper script* fungsional untuk memuat dan mem-*parsing* file CSV secara generik.

#### 5. `test/` (Folder Pengujian)
Berisi berkas unit testing untuk memverifikasi kebenaran logika pemuatan data dan algoritma.
*   `test_loader.py`: Menguji ketahanan fungsi pembersih data pada `src/utils/loader.py` dari baris CSV yang tidak valid.
*   `test_e2e.py`: Melakukan pengujian integrasi ujung-ke-ujung (E2E) pada algoritma Core untuk memastikan profit optimal, batas kapasitas, dan penelusuran pohon pencarian berjalan dengan benar.

## ⚙️ Cara Menjalankan Aplikasi

Aplikasi ini menggunakan antarmuka web interaktif berbasis Streamlit. Berikut langkah-langkah instalasi dan cara menjalankannya:

### Prasyarat

* Python 3.10 atau lebih baru.
* *(Opsional tapi disarankan)* **Graphviz** terinstall di sistem operasi Anda untuk kelancaran *render* visualisasi pohon pencarian (Knapsack Tree) secara lokal. Jika tidak terinstall, aplikasi akan memanggil API sekunder *fallback* yang membutuhkan koneksi internet.

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

## 🗃️ Struktur Format Data (CSV)

Seluruh dataset yang digunakan dalam aplikasi ini harus disimpan dalam format .csv dengan contoh struktur kolom (*header*) baku sebagai berikut:

| label       | weight | profit |
| :---------- | :----: | :----: |
| cherry      |   1   |   5   |
| dragonfruit |   2   |   9   |

* **label**: Nama atau ID dari barang (Teks/String).
* **weight**: Berat dari barang (Bilangan Bulat Positif / *Integer*).
* **profit**: Nilai keuntungan jika barang tersebut diambil (Bilangan Bulat Positif / *Integer*).

*Catatan: Baris data yang mengandung nilai negatif, kosong (blank), atau weight/profit non-integer akan secara otomatis dilewati (diabaikan) oleh sistem pembersihan data saat file dimuat.*

## 🧠 Penjelasan Algoritma

Proyek ini memecahkan kasus **0/1 Knapsack Problem** menggunakan pendekatan eksplorasi ruang keadaan (*State Space Tree*) lengkap dengan analisis pemangkasan.

Dalam Knapsack 0/1, kita dihadapkan pada sejumlah barang, masing-masing dengan berat (*weight*) dan nilai keuntungan (*profit*). Tujuannya adalah memilih *subset* barang agar total *profit* maksimal tercapai tanpa melampaui kapasitas berat maksimum yang tersedia (*W*). Syarat "0/1" berarti setiap barang bersifat *indivisible*, yakni hanya bisa diambil sepenuhnya (1) atau tidak diambil sama sekali (0).

### Modul Core Terakselerasi (DFS Rekursif + NumPy)

Algoritma di `src/core/dfs.py` adalah metode **Depth-First Search (DFS)** rekursif murni yang dioptimasi secara radikal menggunakan **NumPy** dan tata letak **Struct-of-Arrays (SoA)** untuk menangani data skala besar secara instan.

* **Pre-processing Terakselerasi (Sort):** Seluruh daftar barang diurutkan berdasarkan berat secara menurun (*descending*) menggunakan fungsi native-C `numpy.argsort()`. Pengurutan berat menurun ini sangat krusial agar pencarian mengevaluasi barang-barang berat terlebih dahulu, sehingga memicu pemangkasan cabang lebih cepat dan efisien.
* **Struct-of-Arrays (SoA) Layout:** Mengubah struktur data dari array-of-dicts menjadi array NumPy paralel untuk mempercepat akses skalar dan meminimalkan overhead memori selama rekursi DFS.
* **Strategi Pemangkasan (Pruning):**
  *   **Capacity Pruning $O(1)$:** Menggunakan *Suffix Minimum Weight* (`np.minimum.accumulate`). Jika sisa kapasitas tas sudah lebih kecil daripada berat barang teringan yang tersisa, pencarian cabang ini langsung dihentikan karena tidak akan ada barang lain yang muat.
  *   **Overcapacity Pruning / Backtracking:** Percabangan kiri (memasukkan barang) dibatalkan dan dipangkas jika berat total melebihi kapasitas tas ($W$).
