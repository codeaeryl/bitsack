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
│   └── test.csv
└── src/
    ├── core/
    │   ├── bound.py
    │   ├── data.py
    │   ├── dfs.py
    │   └── sort.py
    ├── optimize/
    │   └── dfs.py
    ├── mp_optimize/
    │   ├── __init__.py
    │   └── dfs.py
    ├── utils/
    │   ├── app.py
    │   ├── cli.py
    │   ├── cli_optimize.py
    │   └── loader.py
    └── main.py

### 📁 Penjelasan Direktori & File

#### 1. `data/` (Dataset Folder)
Berisi seluruh file dataset berformat CSV yang digunakan untuk pengujian algoritma Knapsack.
*   `data.csv`: Dataset utama berisi 100.000 barang dengan nilai bobot dan profit bertipe *float*.
*   `data_v2.csv`: Dataset sekunder berisi 100.000 barang dengan nilai bertipe *integer* bulat.
*   `test.csv`: Dataset skala kecil (10 barang dengan nama buah) yang digunakan khusus untuk *testing* ringan dan *Live Demo* UI.

#### 2. `src/core/` (Modul Logika Utama - Calvin)
Berisi implementasi asli dari algoritma rekursif standar sesuai konsep fundamental.
*   `dfs.py`: Inti logika algoritma *Depth-First Search* (DFS) rekursif dan strategi pemangkasan (*Branch & Bound*).
*   `bound.py`: Fungsi heuristik (*Bounding Function*) untuk memprediksi *upper bound* dan memangkas (*pruning*) cabang pohon yang tidak menjanjikan.
*   `sort.py`: Modul *pre-processing* untuk mengurutkan daftar barang berdasarkan rasio *Profit/Weight* tertinggi.
*   `data.py`: Modul untuk membaca dan melakukan *parsing* data masukan (CSV).

#### 3. `src/optimize/` (Modul Optimasi - Jayden)
Berisi implementasi level lanjut yang difokuskan pada kecepatan dan efisiensi memori.
*   `dfs.py`: Logika DFS **Iteratif** (tanpa rekursi bawaan Python) berbasis *Stack* yang ditenagai oleh optimasi perhitungan **NumPy** array. Modul ini kebal terhadap isu *RecursionError* pada data berskala 1 Juta.

#### 4. `src/mp_optimize/` (Modul Eksperimen Multiprocessing)
*   `dfs.py`: Area *sandbox* uji coba pemrosesan *Multithreading/Multiprocessing* (saat ini ditangguhkan/dievaluasi karena limitasi memori RAM lokal pada *dataset* masif).
*   `__init__.py`: Penanda direktori modul Python.

#### 5. `src/utils/` (Antarmuka & Utilitas)
Berisi script penghubung (*interface*) antara pengguna dan logika mesin (CLI dan UI).
*   `app.py` **(Web UI - Richard)**: Antarmuka *front-end* interaktif berbasis web menggunakan *framework* **Streamlit**, lengkap dengan fitur edit tabel dinamis dan render visualisasi pohon pencarian dengan **Graphviz**.
*   `cli.py`: *Command Line Interface* (CLI) *sandbox* standar untuk menguji logika inti modul `core` (Calvin) lengkap dengan riwayat log eksplorasi node.
*   `cli_optimize.py`: CLI khusus *benchmarking* untuk mengukur performa komputasi dan pemakaian puncak memori (*Peak Memory Profiler*) dari modul `optimize` (Jayden).
*   `loader.py`: *Helper script* fungsional untuk menginisialisasi atau memuat *module* secara dinamis.

#### 6. Root Level
*   `src/main.py`: Titik masuk utama (*Entry point*) untuk memicu berjalannya keseluruhan ekosistem aplikasi ini.