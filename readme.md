# Laporan Proyek Machine Learning - Arda Ardiyansyah

## Project Overview

Google Maps memiliki lebih dari 1 miliar pengguna aktif bulanan dan telah memetakan lebih dari 220 negara dan wilayah di seluruh dunia. Layanan ini tersedia dalam lebih dari 40 bahasa dan memperbarui 25 juta mil jalan setiap hari. Platform ini digunakan oleh 67% pengguna smartphone dan telah menangkap lebih dari 36 juta mil persegi citra satelit. Selain itu, lebih dari 5 juta aplikasi dan situs web mengintegrasikan API Google Maps, dengan penggunaan seluler menyumbang lebih dari 67% dari total lalu lintasnya. Google Maps adalah aplikasi navigasi teratas di antara pemilik smartphone di AS dan telah terintegrasi dengan layanan ride-sharing seperti Uber dan Lyft. Pengguna menyumbang lebih dari 20 juta data setiap hari, dan fitur Street View-nya mencakup lebih dari 10 juta mil jalan, dengan lebih dari 1 miliar kilometer citra yang ditangkap secara global. Dengan lebih dari 150 juta bisnis lokal terdaftar, Google Maps menangani lebih dari 5 miliar pencarian setiap hari.

Proyek ini penting untuk diselesaikan karena sistem rekomendasi dapat secara signifikan meningkatkan kepuasan dan keterlibatan pengguna dengan menyediakan saran yang relevan dan dipersonalisasi. Maka dari itu, proyek ini bertujuan untuk menerapkan sistem rekomendasi yang dapat membantu pengguna menemukan tempat yang sesuai dengan preferensi mereka. Sistem ini akan menggunakan data aktivitas pengguna dan rating yang diberikan untuk memprediksi dan merekomendasikan tempat-tempat yang paling relevan, membantu pengguna menemukan lokasi yang mungkin tidak mereka sadari sebelumnya namun sesuai dengan kebutuhan atau preferensi mereka.

## Business Understanding

Bagian laporan ini mencakup:

### Problem Statements

- **Rekomendasi kepada user baru yang belum memiliki preferensi**
<br>
User baru yang belum pernah berinteraksi dengan aplikasi sering kali tidak memiliki preferensi yang jelas, sehingga sulit untuk memberikan rekomendasi yang relevan. Sistem rekomendasi harus mampu mengatasi tantangan ini dengan memanfaatkan data rating yang adil untuk memberikan saran awal yang berguna.

- **Kesalahan input kepada data**
<br>
Kesalahan atau ketidaktepatan dalam data, seperti rating atau kategori yang hilang, dapat menyebabkan rekomendasi yang tidak tepat. Oleh karena itu, diperlukan metode untuk menangani dan memperbaiki data yang salah sebelum digunakan dalam sistem rekomendasi.

- **Kebutuhan relevansi rekomendasi**
<br>
Dalam lingkungan yang sangat kompetitif seperti aplikasi Google Maps, di mana pengguna mengandalkan rekomendasi untuk menemukan tempat atau layanan yang sesuai dengan kebutuhan mereka, relevansi dari rekomendasi sangat penting. Sistem harus mampu memahami preferensi pengguna berdasarkan aktivitas sebelumnya dengan mengandalkan kategori dari data tempat yang pernah dikunjunginya, memastikan bahwa setiap rekomendasi tidak hanya relevan tetapi juga meningkatkan pengalaman pengguna secara keseluruhan.

### Goals

- Memberikan rekomendasi kepada user baru yang belum memiliki preferensi
- Merapihkan data yang sebelumnya memiliki kesalahan
- Memberikan rekomendasi yang relevan terhadap preferensi user

### Solution Statements

- Memberikan rekomendasi kepada user yang belum memiliki preferensi dengan pendekatan Wilson Score Interval untuk mengurutkan rating terbaik, Wilson Score Interval juga diimplementasikan oleh database terkenal yaitu Elasticsearch. [1]
- Melakukan pendekatan Machine Learning dengan kasus analisis sentimen dan language classificaton terhadap data yang hilang
- Melakukan pendekatan 2 sistem rekomendasi yaitu Content-Based dan Collaborative-Based dengan KNN

Semua poin di atas harus diuraikan dengan jelas. Anda bebas menuliskan berapa pernyataan masalah dan juga goals yang diinginkan.

## Data Understanding

### Overview

Dataset ini berisi informasi ulasan tentang Google Maps (penilaian, teks, gambar, dll.), metadata bisnis (alamat, informasi geografis, deskripsi, kategori informasi, harga, jam buka, dan informasi MISC), serta tautan (bisnis terkait) hingga September 2021 di Amerika Serikat. Namun pada kasus ini kita hanya menggunakan Negara Bagian Alaska.

Dataset ini terdiri dari 2 bagian, yaitu data review dan metadata. Pada data review kita memiliki 1,051,246 data sedangkan metadata memiliki 12,774 data.

Variabel-variabel pada data review adalah sebagai berikut:

- user_id: ID dari penulis ulasan.
- name: Nama dari penulis ulasan.
- time: Waktu ulasan (dalam format waktu Unix).
- rating: Penilaian terhadap tempat.
- text: Teks ulasan.
- pics: Gambar yang menyertai ulasan.
- resp: Tanggapan tempat terhadap ulasan, termasuk waktu Unix dan teks tanggapan.
- gmap_id: ID dari tempat.

Variabel-variabel pada metadata adalah sebagai berikut:

- name: Nama dari tempat.
- address: Alamat dari tempat.
- gmap_id: ID dari tempat.
- description: Deskripsi dari tempat.
- latitude: Garis lintang (latitude) dari lokasi tempat.
- longitude: Garis bujur (longitude) dari lokasi tempat.
- category: Kategori dari tempat.
- avg_rating: Rata-rata penilaian dari tempat.
- num_of_reviews: Jumlah ulasan yang diterima oleh tempat.
- price: Rentang harga dari tempat.
- hours: Jam buka dari tempat.
- MISC: Informasi tambahan atau MISC mengenai tempat.
- state: Status terkini dari tempat (misalnya, ditutup permanen).
- relative_results: Tempat-tempat terkait yang direkomendasikan oleh Google.
- url: URL dari tempat.

Dataset : [2] & [3]

Dataset Download : [Google Local Data (2021)](https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/)

### Exploratory Data Analysis

#### Data Review
- Pada data review ini, kita hanya menggunakan user_id, rating, dan gmap_id untuk model sistem rekomendasi kita. Data-data tersebut memiliki nilai null pada user_id dan rating
- Setelah melakukan analisis, sepertinya ada kesalahan dalam input data. Terlihat kita memiliki nomor berformat user_id pada kolom pertama dan untuk namanya kemungkinan besar review ini berasal dari third party app untuk memberikan review kepada google local
- Selanjutnya mengalisis pada rating. Terlihat rating tidak memiliki nilai, tetapi kita memiliki kolom text review yang dapat digunakan untuk menganalisis sentimen dari text tersebut. Namun kita juga memilik tantangan lain yaitu selain bahasa inggris kita juga memiliki bahasa jerman.
- Dari hasil analisis ini kita memiliki kesimpulan kalau kolom text memiliki informasi yang penting Setelah dilakukan analisis, kolom text tidak memiliki nilai null pada data rating yang tidak memiliki nilai
- Terakhir, data user_id dan rating yang hilang merupakan data yang sama

#### Metadata
- Pada metadata ini, kita hanya menggunakan name, gmap_id, category, dan avg_rating untuk model sistem rekomendasi kita. Data-data tersebut sudah bersih dari Null kecuali data category
- Setelah melakukan analisis terhadap avg_rating, kita melihat kolom num_of_review. Tentu menjadi sangat tidak adil jika mengurutkan tempat terbaik dari avg_rating saja tanpa ada bobot num_of_review

## Data Preparation

### Dataframe Review

#### 1. Data Preprocessing

Langkah-langkah:
- Mengidentifikasi Data yang Hilang: 
  - Simpan dataframe review yang memiliki nilai `rating` dan `user_id` yang hilang ke dalam file CSV.
  - Perbaiki CSV dengan menghapus koma di depan dan menambahkan koma setelah `user_id`.
  - Ubah nama file menjadi `_website_reviewer.csv`.
  - Hapus kolom `Unnamed: 1` yang tidak diperlukan.

Tujuan:
- Memastikan bahwa data yang hilang diperlakukan dengan benar untuk meningkatkan kualitas data.

#### 2. Language Classification

Langkah-langkah:
- Klasifikasi Bahasa: 
  - Gunakan library `langid` untuk mengklasifikasikan bahasa dari teks review. [5], [6], [7]
  - Tambahkan kolom baru `bahasa` pada dataframe untuk menyimpan hasil klasifikasi.

Tujuan:
- Mengidentifikasi bahasa yang digunakan dalam setiap review agar hanya data yang relevan (bahasa Inggris) dipertahankan.

#### 3. Language Filtering

Langkah-langkah:
- Memfilter Bahasa: 
  - Buang data review yang tidak menggunakan bahasa Inggris.

Tujuan:
- Mempertahankan hanya review dalam bahasa Inggris untuk konsistensi analisis sentimen dan rating.

#### 4. Sentiment Analysis & Rating Conversion

Langkah-langkah:
- Klasifikasi Sentimen: 
  - Klasifikasikan sentimen teks review sebagai positif, netral, atau negatif dengan model yang telah dibuat yaitu vaderSentiment. 
  - Konversi sentimen ke dalam bentuk rating dengan aturan berikut:
    - Positif: 5.0
    - Netral: 3.0
    - Negatif: 1.0

Tujuan:
- Menghasilkan rating berdasarkan analisis sentimen untuk data yang awalnya memiliki nilai rating yang hilang.

#### 5. Data Merging

Langkah-langkah:
- Penggabungan Data: 
  - Gabungkan data yang telah diproses (dengan rating dan `user_id` yang hilang telah diperbaiki) ke dalam dataframe review utama.

Tujuan:
- Memastikan semua data digabungkan dengan benar setelah proses perbaikan, tanpa kehilangan informasi penting.

#### 6. Feature Engineering

Langkah-langkah:
- Encoding Identifiers: 
  - Encode kolom `user_id` dan `gmap_id` menjadi indeks integer.
  - Pemetaan data `user_id` dan `gmap_id` ke dalam dataframe yang berkaitan.

Tujuan:
- Menyiapkan data agar dapat digunakan dalam model pembelajaran mesin dengan encoding yang sesuai.

#### 7. Data Shuffling and Splitting

Langkah-langkah:
- Pengacakan Data: 
  - Acak data agar distribusinya menjadi acak sebelum pembagian dataset.
- Pembagian Data:
  - Bagi data menjadi set training dan validasi dengan komposisi 80:20.
  - Pemetaan data `user_id` dan `gmap_id` ke dalam satu value terlebih dahulu.
  - Konversikan rating ke skala 0 sampai 1 untuk memudahkan proses training.

Tujuan:
- Memastikan bahwa data terbagi dengan baik untuk training dan validasi, serta siap untuk proses pembelajaran mesin.


Berikut adalah dataframe review final setelah dipersiapkan:
| Index  | User ID          | Name                        | Time          | Rating | Text                                                           | Pics      | Resp                                                                   | GMap ID                                | User | GMap |
|--------|------------------|-----------------------------|---------------|--------|----------------------------------------------------------------|-----------|------------------------------------------------------------------------|----------------------------------------|---------|---------|
| 824236 | 1.086098e+20     | Ramirez Jeep                 | 1533061362453 | 5.0    | None                                                           | [{'url': ['https://lh5.googleusercontent.com/p... | None                                                                   | 0x56c7b612942f1da1:0x42e6f5327929a9ef | 146868  | 12189   |
| 70292  | 1.104279e+20     | Brad Wuerer                 | 1619113654480 | 5.0    | They are amazing. Great customer service and ...               | None      | {'time': 1619200892421, 'text': 'Thank you for...                  | 0x56c89797b9267fab:0xee32c926feb1b48e | 8715    | 3970    |
| 949861 | 1.037296e+20     | ohmyheck31                   | 1542086620517 | 5.0    | The Dog Sled Demo is a must-experience!                        | None      | None                                                                   | 0x56cd209e8e116f63:0xe153a8daf0f05240 | 2804    | 12515   |
| 77559  | 1.115868e+20     | Marissa Wood                 | 1602733667884 | 5.0    | I went into due to a impacted lower wisdom too...               | None      | None                                                                   | 0x51325ab1515b2ca1:0x3c1faae5b3e4ca0a | 12260   | 4286    |
| 825280 | 1.102832e+20     | Lt. Colonel David K. Swendiman | 1598116354646 | 5.0    | Peaceful and beautiful- even though right in t...               | None      | None                                                                   | 0x56c79c7cbc43a02b:0xe0a8e540ac8c61bb | 54051   | 12199   |
| 110268 | 1.070980e+20     | Lewis Sunnyboy              | 1540860599729 | 5.0    | None                                                           | None      | None                                                                   | 0x51325ad73b924d65:0x3dffeb1b71c07b20 | 74274   | 5390    |
| 259178 | 1.032595e+20     | Josh Gogus                  | 1566679702518 | 4.0    | She groomed our yorkie once. She was great wi...               | None      | {'time': 1566679289055, 'text': 'I am so sorry...                  | 0x51324d59f5abb0ed:0xd3778e39d733ff8e | 114072  | 8714    |
| 131932 | 1.085170e+20     | Chelsey M.                   | 1622024063183 | 5.0    | Yummy food                                                     | None      | None                                                                   | 0x56c91db84151adf7:0x483f4c47115c8d6f | 3711    | 6041    |
| 671155 | 1.045853e+20     | chelbie garcia              | 1602384204953 | 5.0    | Food and service were both great. Will definit...              | [{'url': ['https://lh5.googleusercontent.com/p... | {'time': 1602637342860, 'text': 'We strive to ...                  | 0x56c8bd877c06ac0f:0xebf1abe87d2435f5 | 36645   | 11686   |
| 121958 | 1.122489e+20     | zan govan                    | 1581213106974 | 1.0    | None                                                           | None      | None                                                                   | 0x540c2505acd8e65f:0x1f5783762bbb4237 | 44672   | 5745    |


### Dataframe Metadata

#### 1. Handling Missing Data in Category

Langkah-langkah:
- Mengganti Data yang Kosong:
  - Pada kolom `category` di dataframe `meta`, ganti semua nilai yang kosong (NaN) menjadi list kosong `[]`.
  
Tujuan:
- Memastikan bahwa setiap entri dalam kolom `category` memiliki nilai yang terdefinisi dengan baik, bahkan jika tidak ada kategori yang terkait.

#### 2. Vectorizing Category Data

Langkah-langkah:
- Vektorisasi Data Category:
  - Gunakan `MultiLabelBinarizer` untuk melakukan vektorisasi data pada kolom `category` di dataframe `meta`.
  - Simpan hasil vektorisasi dalam dataframe baru, misalnya `categories_df`.

Tujuan:
- Mengubah data kategori menjadi bentuk numerik yang bisa digunakan dalam analisis lebih lanjut, seperti pembentukan similarity matrix.

#### 3. Merging Vectorized Data with Meta

Langkah-langkah:
- Menggabungkan Data:
  - Gabungkan `categories_df` yang berisi data hasil vektorisasi dengan dataframe `meta`.

Tujuan:
- Memastikan bahwa data vektorisasi kategori terintegrasi ke dalam dataframe utama, dan kolom asli yang tidak lagi diperlukan dihapus untuk menjaga kebersihan data.

#### 4. Calculating Similarity Matrix

Langkah-langkah:
- Membuat Similarity Matrix:
  - Gunakan metode `cosine similarity` untuk menghitung similarity matrix berdasarkan kategori yang telah di-vektorisasi.

Tujuan:
- Menghasilkan similarity matrix yang dapat digunakan untuk menghitung seberapa mirip antara berbagai tempat berdasarkan kategori mereka. 

Pembagian ini memberikan struktur yang jelas untuk memahami setiap tahap dalam proses pengolahan dan analisis data, mulai dari penanganan data yang hilang hingga pembentukan similarity matrix yang akan digunakan dalam sistem rekomendasi.

## Modeling

### Non-Personalized User

Sistem rekomendasi Non-Personalized User adalah pendekatan yang memberikan saran kepada pengguna tanpa memperhitungkan preferensi atau riwayat interaksi mereka. Metode ini cocok untuk pengguna baru yang belum memiliki data preferensi atau interaksi dengan item tertentu, seperti tempat.

Wilson Score Interval digunakan untuk mengestimasi probabilitas binomial dengan tingkat keyakinan tertentu. Dalam konteks sistem rekomendasi, metode ini dapat digunakan untuk memperkirakan skor rata-rata item (misalnya, tempat) berdasarkan rating yang tersedia, terutama untuk pengguna baru yang belum memiliki preferensi atau riwayat interaksi. Dengan mempertimbangkan jumlah ulasan dan interval kepercayaan, metode ini membantu dalam memberikan estimasi yang lebih andal, terutama ketika jumlah ulasan rendah, sehingga rating tidak terlalu bias.

Kelebihan:
- Mengatasi Bias: Wilson Score Interval mempertimbangkan ukuran sampel dan tingkat kepercayaan, sehingga lebih handal dibandingkan dengan rata-rata biasa dalam situasi dengan jumlah rating yang sedikit.
- Kegunaan Universal: Cocok untuk diterapkan pada pengguna baru yang belum memberikan rating, sehingga dapat memberikan rekomendasi yang lebih akurat meskipun data terbatas.

Kekurangan:
- Terbatas pada Data Rating: Metode ini hanya fokus pada data rating dan tidak mempertimbangkan fitur atau karakteristik konten lain. Akibatnya, hasil rekomendasi mungkin tidak sepersonal seperti metode lain.
- Kurang Dinamis: Tidak mempertimbangkan kesamaan antara pengguna atau item, sehingga kurang adaptif terhadap preferensi unik pengguna.

Berikut adalah penjelasan dari setiap bagian dalam fungsi:

#### 1. Parameter Masukan:
   - `avg_rating`: Rata-rata rating dari suatu tempat (misalnya 4.2 dari 5).
   - `num_of_reviews`: Jumlah ulasan (reviews) untuk tempat tersebut.

#### 2. Langkah-langkah Perhitungan:

   1. Menghitung Proporsi Rata-rata (p):
      ```python
      p = avg_rating / 5.0
      ```
      - Di sini, `avg_rating` dibagi dengan 5.0 (karena rating maksimum adalah 5) untuk mendapatkan proporsi rata-rata, yaitu `p`.
   
   2. Menetapkan Jumlah Sampel (n):
      ```python
      n = num_of_reviews
      ```
      - Nilai `n` adalah jumlah ulasan yang tersedia.

   3. Menggunakan Z-Score:
      ```python
      z = 1.96
      ```
      - `z` adalah nilai Z-Score untuk interval kepercayaan 95%, yang merupakan standar untuk menghitung interval kepercayaan.

   4. Menghitung Denominator:
      ```python
      denominator = 1 + (z  2) / n
      ```
      - Denominator adalah bagian dari rumus Wilson Score yang menyesuaikan proporsi berdasarkan ukuran sampel (`n`). Ketika `n` kecil, penyesuaian ini menjadi lebih signifikan.

   5. Menghitung Centre-Adjusted Probability:
      ```python
      centre_adjusted_probability = p + (z  2) / (2 * n)
      ```
      - Ini adalah penyesuaian dari proporsi `p` yang memperhitungkan ketidakpastian dengan menambahkan bagian dari kuadrat Z-Score dibagi dengan dua kali jumlah sampel.

   6. Menghitung Adjusted Probability:
      ```python
      adjusted_probability = centre_adjusted_probability / denominator
      ```
      - Nilai ini adalah proporsi yang telah disesuaikan, di mana hasil ini menunjukkan probabilitas yang telah diperbaiki berdasarkan interval kepercayaan.

#### 3. Output:
   ```python
   return adjusted_probability
   ```
   - Fungsi ini mengembalikan `adjusted_probability`, yang merupakan estimasi terbaik dari proporsi rata-rata dengan penyesuaian ketidakpastian.


Menampilkan 10 tempat terbaik berdasarkan rating (Wilson Score Interval) tertinggi:

| Index | Name                                      | Address                                     | GMap ID                                     | Description | Latitude  | Longitude | Category                                     | Avg Rating | Num of Reviews | Price | Hours                                                    | MISC                                                      | State                | Relative Results                                                                                                            | URL                                                        | Wilson Score |
|-------|-------------------------------------------|---------------------------------------------|---------------------------------------------|-------------|-----------|-----------|----------------------------------------------|------------|----------------|-------|----------------------------------------------------------|-----------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|--------------|
| 4097  | A Clean Slate Credit Consultants          | None                                        | 0x88d9b7b7c1662903:0xa5fbc84566909fbb     | None        | 42.756389 | -140.301319 | Credit counseling service, Service establishment | 5.0        | 518            | None  | [[Tuesday, Open 24 hours], [Wednesday, Open 24 hours]] | {'Highlights': ['LGBTQ friendly'], 'Planning': ...}     | Open 24 hours        | [0x88d9b8bcaf5f7ecd:0xedede9a340fa628c, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.996319     |
| 1903  | The Dar Walden Team, Keller Williams Realty | The Dar Walden Team, Keller Williams Realty | 0x56c897c5f9655555:0x965bf44512428041     | None        | 61.194767 | -149.884594 | Real estate agency                           | 5.0        | 467            | None  | [[Friday, 8AM–9PM], [Saturday, 8AM–9PM], [Sunday, Closed]] | {'Accessibility': ['Wheelchair accessible entr...} | Closed ⋅ Opens 8AM   | [0x56c897c5f92dfcd5:0x42d36d11c1c11a29, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.995920     |
| 7682  | 1-800-GOT-JUNK? Anchorage                 | None                                        | 0x56c89797b8875ab3:0xe8b5f4ed9b7d0024     | None        | 60.983961 | -150.057399 | Garbage dump service, Business to business service | 5.0        | 398            | None  | [[Wednesday, 8AM–5PM], [Thursday, 8AM–5PM], [Friday, 8AM–5PM]] | None                                                      | Closed ⋅ Opens 8AM Thu | [0x56c897ae8d53ac7d:0x3be0c3db0d426dc3, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.995220     |
| 5463  | Meridian Dental, LLC                      | Meridian Dental, LLC, 3465 E Meridian Park Loop, Anchorage | 0x56c8e081a93a060b:0x19618d52ec735e72     | None        | 61.592692 | -149.361735 | Dentist, Cosmetic dentist, Dental clinic    | 5.0        | 386            | None  | [[Saturday, 9AM–3PM], [Sunday, Closed], [Monday, 9AM–5PM]] | {'Accessibility': ['Wheelchair accessible entr...} | Open ⋅ Closes 3PM   | [0x56c8e081062dbb17:0xb9efd0c70098eccc, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.995073     |
| 5294  | Allen Rapid Dry Carpet Cleaning (Pet Odor Expert) | Allen Rapid Dry Carpet Cleaning (Pet Odor Expert) | 0x56c8975a317a92b7:0xc71ca09335bc7821     | None        | 61.132375 | -149.788825 | Carpet cleaning service, Upholstery cleaning | 5.0        | 348            | None  | [[Monday, 9AM–5PM], [Tuesday, 9AM–5PM], [Wednesday, 9AM–5PM]] | {'From the business': ['Identifies as veteran-owned', ...} | Closed ⋅ Opens 9AM  | [0x56c897ea0b8b448d:0xa232fad995eddb25, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.994541     |
| 8043  | Muffy's Flowers & Gifts                   | Muffy's Flowers & Gifts, 333 W 4th Ave #218, Anchorage | 0x56c896e5f87d10ed:0xb2e2e0e6354e3a60     | None        | 61.218665 | -149.888525 | Florist, Balloon store, Flower delivery     | 5.0        | 336            | None  | [[Wednesday, 9AM–5PM], [Thursday, 9AM–5PM], [Friday, 9AM–5PM]] | {'From the business': ['Identifies as women-led', ...} | Closed ⋅ Opens 9AM  | [0x56c89704e479c225:0x49dec030cb449be1, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.994348     |
| 9139  | Unity Home Group Alaska - eXp Realty, LLC | Unity Home Group Alaska - eXp Realty, LLC, 725 W 15th Ave, Anchorage | 0x56c897c5f93f0e37:0xcc56a3db4e06fe17     | None        | 61.198689 | -149.869466 | Real estate agency, Real estate agents, Real estate service | 5.0        | 328            | None  | [[Saturday, 8AM–9PM], [Sunday, 8AM–9PM], [Monday, 8AM–9PM]] | {'Service options': ['Online appointments', 'Offers virtual consultations']} | Open ⋅ Closes 9PM   | [0x56c897c5f93f0e37:0xe96447335b4819b4, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.994212     |
| 842   | True Life Chiropractic                    | True Life Chiropractic, 1142 North Muldoon Road, Anchorage | 0x56c897bd92cd5bbd:0x63be17908a90f182     | None        | 61.228746 | -149.742432 | Chiropractor                                | 5.0        | 328            | None  | [[Friday, 9AM–5PM], [Saturday, 10AM–2PM], [Sunday, Closed]] | {'Accessibility': ['Wheelchair accessible entr...} | Closed ⋅ Opens 10AM Sat | [0x4391e3348f045d97:0xf46e3cdd8e8dfda5, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.994212     |
| 2408  | Luff Orthodontics                         | Luff Orthodontics, 3708 Rhone Cir, Anchorage, AK | 0x56c897ba5bb7b90b:0x1cb0a140c127cac2     | None        | 61.187259 | -149.861872 | Dental clinic, Orthodontist                 | 5.0        | 304            | None  | [[Friday, 9AM–5PM], [Saturday, Closed], [Sunday, Closed]] | {'Accessibility': ['Wheelchair accessible entr...} | Closed ⋅ Opens 9AM  | [0x56c899e7bc39631f:0x740e958a4945742c, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.993760     |
| 5404  | Home Inspections Plus+ LLC                | None                                        | 0x56c8eb7a5206ecc7:0xbbad10a0c9c2fb65     | None        | 62.108352 | -149.715168 | Home inspector, Commercial real estate inspector | 5.0        | 265            | None  | [[Saturday, 8AM–6PM], [Sunday, Closed], [Monday, 8AM–6PM]] | None                                                      | Closed ⋅ Opens 8AM Mon | [0x56c8970826002cb5:0x2800ea194fea3b26, ...]                                                          | [Link](https://www.google.com/maps/place//data=!4m2!3...) | 0.992855     |


### Content-Based Filter

Content-Based Filtering membuat rekomendasi berdasarkan kesamaan antara item yang disukai oleh pengguna dengan item lain yang memiliki karakteristik serupa. Misalnya, jika seorang pengguna menyukai tempat dengan pemandangan alam, sistem akan merekomendasikan tempat lain dengan karakteristik serupa.

Kelebihan:
- Personalized: Sangat personal, karena rekomendasi didasarkan pada item yang secara eksplisit disukai oleh pengguna.
- Tidak Membutuhkan Data Pengguna Lain: Tidak perlu bergantung pada data dari pengguna lain, sehingga lebih cepat untuk diimplementasikan pada pengguna baru dengan riwayat preferensi yang jelas.

Kekurangan:
- Overfitting: Cenderung merekomendasikan item yang sangat mirip dengan yang sudah disukai, sehingga bisa mengakibatkan rekomendasi yang terlalu sempit dan kurang bervariasi.

#### 1. Parameter Masukan:
   - `gmap_id`: ID tempat yang digunakan sebagai referensi untuk mencari tempat lain yang mirip.
   - `similarity_matrix`: Matriks yang berisi nilai kesamaan (similarity) antara tempat-tempat yang berbeda, dihitung sebelumnya menggunakan metode seperti cosine similarity.
   - `data`: DataFrame yang berisi informasi tentang tempat, termasuk `gmap_id` dan `name`.
   - `top_n`: Jumlah rekomendasi tempat teratas yang ingin dikembalikan oleh fungsi (default-nya adalah 5).

#### 2. Langkah-langkah Perhitungan:

   1. Menemukan Indeks Item Referensi:
      ```python
      item_index = data[data['gmap_id'] == gmap_id].index[0]
      ```
      - Pertama, fungsi mencari indeks dari `gmap_id` di dalam DataFrame `data`. Indeks ini digunakan untuk mengakses baris yang sesuai di `similarity_matrix`.

   2. Mengambil Skor Kesamaan untuk Item:
      ```python
      similarity_scores = list(enumerate(similarity_matrix[item_index]))
      ```
      - Di sini, fungsi mengambil baris dari `similarity_matrix` yang sesuai dengan `item_index` dan membuat daftar pasangan `(indeks, skor kesamaan)`.

   3. Mengurutkan Skor Kesamaan:
      ```python
      sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
      ```
      - Kemudian, daftar skor kesamaan diurutkan dalam urutan menurun (dari yang paling mirip ke yang paling tidak mirip).

   4. Menemukan Indeks dari Rekomendasi Teratas:
      ```python
      top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
      ```
      - Fungsi kemudian mengambil indeks dari `top_n` tempat teratas, mengabaikan item pertama karena biasanya itu adalah item yang sama (kesamaan dengan dirinya sendiri).

   5. Mengambil Informasi Tempat Teratas:
      ```python
      top_items = data.iloc[top_indices][['gmap_id', 'name']]
      ```
      - Fungsi mengambil informasi `gmap_id` dan `name` dari tempat-tempat teratas yang mirip berdasarkan `top_indices`.

#### 3. Output:
   ```python
   return top_items
   ```
   - Fungsi ini mengembalikan DataFrame `top_items` yang berisi `gmap_id` dan `name` dari tempat-tempat yang direkomendasikan berdasarkan kesamaan konten.

Menampilkan 5 tempat terbaik berdasarkan Content-Based Filtering atau Similiarity Matrix terbesar dengan Skenario pengguna mengklik konten gmap dengan id `0x56b646ed2220b77f:0xd8975e316de80952`, maka:

| Index | GMap ID                                    | Name                            |
|-------|--------------------------------------------|---------------------------------|
| 85    | 0x56b646ed2220b77f:0xd8975e316de80952     | Bear Creek Cabins & RV Park      |
| 3771  | 0x56cedaacb2e94d57:0x7575332e5c393696     | Mat-Su RV Park & Campground      |
| 5466  | 0x56ced6cd63117f0b:0x4b4d20be83e76ed4     | Willow Creek Resort              |
| 5583  | 0x56c6960687b49259:0xa388514405ec2393     | Scenic View RV Park              |
| 5678  | 0x513246fc8f1d16ef:0x8fc0ef9acfa78dbe     | Northern Moosed RV Park & Campground |


### Collaborative-Based Filter

Collaborative Filtering berdasarkan K-Nearest Neighbors (KNN) bekerja dengan mencari pengguna atau item yang serupa dan kemudian merekomendasikan item yang disukai oleh pengguna lain yang mirip tersebut. Dalam implementasi ini, KNN digunakan untuk mengukur kesamaan antara pengguna untuk memberikan rekomendasi.

Kelebihan:
- Adaptif: Mengambil keuntungan dari preferensi pengguna lain yang serupa, sehingga dapat memberikan rekomendasi yang mungkin tidak terdeteksi oleh Content-Based Filtering.
- Mengatasi Masalah Cold Start untuk Item: Jika ada item baru yang belum memiliki banyak interaksi, metode ini bisa tetap merekomendasikannya jika pengguna lain yang serupa menyukainya.
- Menggunakan konsumsi daya yang relatif ringan: Penggunaan sumber daya KNN lebih ringan dan cepat pada tahap training dibanding pendeketan Machine Learning lain maupun Deep Learning

Kekurangan:
- Bergantung pada Data Pengguna Lain: Kualitas rekomendasi sangat bergantung pada seberapa baik preferensi pengguna lain tercatat dalam sistem. Jika data tidak cukup, hasilnya bisa kurang akurat.
- Skalabilitas: KNN bisa menjadi kurang efisien dan lambat jika dataset pengguna dan item sangat besar, karena memerlukan perhitungan jarak untuk banyak pasangan pengguna-item.

#### 1. Parameter Masukan:
   - `user_id`: ID pengguna yang akan diberikan rekomendasi.
   - `review`: DataFrame yang berisi informasi mengenai tempat yang telah dikunjungi pengguna serta rating yang diberikan.
   - `meta`: DataFrame yang berisi informasi metadata tempat, seperti `gmap_id` dan nama tempat.
   - `knn`: Model KNN yang sudah dilatih sebelumnya untuk memprediksi rating berdasarkan hubungan antara pengguna dan tempat.
   - `gmap_to_gmap_encoded`: Pemetaan dari `gmap_id` ke nilai yang sudah di-encode.
   - `user_to_user_encoded`: Pemetaan dari `user_id` ke nilai yang sudah di-encode.
   - `gmap_encoded_to_gmap`: Pemetaan dari nilai yang sudah di-encode kembali ke `gmap_id`.

#### 2. Langkah-langkah dalam Fungsi:

   1. Mendapatkan Tempat yang Sudah Dikunjungi oleh Pengguna:
      ```python
      place_visited_by_user = review[review.user_id == user_id]
      ```
      - Fungsi ini pertama kali mendapatkan tempat-tempat yang sudah dikunjungi oleh pengguna dengan `user_id` yang diberikan.

   2. Menemukan Tempat yang Belum Dikunjungi:
      ```python
      place_not_visited = meta[~meta['gmap_id'].isin(place_visited_by_user.gmap_id.values)]['gmap_id']
      place_not_visited = list(set(place_not_visited).intersection(set(gmap_to_gmap_encoded.keys())))
      place_not_visited = [[gmap_to_gmap_encoded.get(x)] for x in place_not_visited]
      ```
      - Fungsi kemudian menentukan tempat-tempat yang belum dikunjungi oleh pengguna tersebut dengan membandingkan semua tempat di `meta` yang belum ada di `place_visited_by_user`.

   3. Meng-encode Pengguna dan Membuat Array untuk Prediksi:
      ```python
      user_encoder = user_to_user_encoded.get(user_id)
      user_place_array = np.hstack(([[user_encoder]] * len(place_not_visited), place_not_visited))
      ```
      - Pengguna dan tempat yang belum dikunjungi kemudian di-encode menjadi representasi numerik untuk digunakan dalam prediksi KNN.

   4. Memprediksi Rating Tempat yang Belum Dikunjungi:
      ```python
      ratings = knn.predict(user_place_array).flatten()
      ```
      - Model KNN digunakan untuk memprediksi rating untuk setiap tempat yang belum dikunjungi berdasarkan data tempat dan pengguna.

   5. Menemukan 10 Rekomendasi Tempat dengan Rating Tertinggi:
      ```python
      top_ratings_indices = ratings.argsort()[-10:][::-1]
      recommended_place_ids = [gmap_encoded_to_gmap.get(place_not_visited[x][0]) for x in top_ratings_indices]
      ```
      - Setelah memprediksi rating, fungsi menemukan indeks dari 10 tempat dengan rating tertinggi dan memetakannya kembali ke `gmap_id`.

   6. Mengembalikan Tempat yang Telah Dikunjungi dan Rekomendasi:
      ```python
      return place_visited_by_user, recommended_place
      ```
      - Fungsi ini akhirnya mengembalikan DataFrame `place_visited_by_user` yang berisi tempat-tempat yang telah dikunjungi dan `recommended_place`, DataFrame yang berisi 10 tempat teratas yang direkomendasikan untuk pengguna.

#### 3. Output:
   - `place_visited_by_user`: DataFrame yang berisi tempat-tempat yang telah dikunjungi oleh pengguna.
   - `recommended_place`: DataFrame yang berisi 10 rekomendasi tempat teratas untuk pengguna.

Menampilkan 10 tempat terbaik berdasarkan Collaborative-Based Filtering dengan Skenario pengguna telah mengunjungi gmap dengan id `0x56c89427df8203bf:0xd978c612a604bd27`, `0x56c8bcd7fa147091:0xdf45a73cf0e05ac0`, dst (bisa dilihat pada notebook)  maka:

|    | gmap_id                                    | name                                             |
|----|--------------------------------------------|--------------------------------------------------|
| 907| 0x540467a3802bb6b7:0xd895c7f5818a3f51      | Sitka Sound Science Center                       |
| 1387| 0x56c89644557df92b:0x587b142b879b65fd      | Denali Emergency Medicine                        |
| 1642| 0x51348b307278da67:0x58f262dc27fe9fb      | Big Delta Brewing Co.                            |
| 1704| 0x56c12d896cdb6b63:0x6683c0fc7406f043      | Homer Electric Association                        |
| 1744| 0x56c79bc7ed4b4f11:0x39da29a762031829      | Brewed Awakenings                                |
| 1930| 0x56c8966638376403:0x59679d68416a0847      | Gardens at Bragaw                                |
| 1939| 0x540c2523eb5e9503:0x3bbe7f9327611e01      | Misty Fjords Air & Outfitting Inc                |
| 7043| 0x56c8963355e1366d:0xcd9d72bab11a2fa5      | Anchorage RNC Tree Service                       |
| 9445| 0x56c897dbe294c7f1:0x3af6a90b65fd3549      | The Bead Shack                                   |
| 11611| 0x56c89994493f3431:0xaed81c90bd2a135a      | South Anchorage Farmers Market (O'Malley)       |

## Evaluation

### Non-Personalized User
Pada kasus ini, kita tidak dapat mengukurnya karena pada dasarnya Wilson Score Interval merupakan bukan model pembelajaran melainkan hanya kalkulasi semata dengan menambahkan kolom baru untuk mengurutkan rating terbaik

### Content-Based Filter

Pada Content-Based Filter, saya menggunakan precision dengan formula sebagai berikut:

```
Precision = #of recommendation that are relevant/#of item we recommend.
```

Kita tidak dapat menghitung precision menggunakan library seperti scikit-learn karena tidak ada data target/label seperti dalam supervised learning.
Relevansi item dapat diketahui dari kategori item yang direkomendasikan. Apakah kategori item tersebut relevan (mirip) dengan kategori item yang telah dipilih oleh pengguna? Misalnya, jika sistem merekomendasikan 5 item kepada pengguna dan dari 5 item tersebut, 3 item relevan, maka precision-nya adalah 60%.

Pada proyek ini, kita memberi contoh jika input_sample dengan kategori seperti berikut:
|   | gmap_id                               | name            | category                                  |
|---|---------------------------------------|-----------------|-------------------------------------------|
| 7034 | 0x56c661612cd6c8e9:0xab51061bd1fce2c6 | Nick’s Auto Glass | [Auto glass shop, Glass repair service] |

Dengan contoh output seperti berikut:
|    | gmap_id                               | name                   | category                                  |
|----|---------------------------------------|------------------------|-------------------------------------------|
| 5266 | 0x51325a962c628aed:0xd38974136565bde3 | Speedy Glass           | [Auto glass shop, Glass repair service]  |
| 6504 | 0x56c8eb75763e06c5:0x513b63e443562949 | Splashes Autospa       | [Auto glass shop, Glass repair service]  |
| 6784 | 0x56c8eb737157fa45:0x58de944de7fecb91 | Speedy Glass           | [Auto glass shop, Glass repair service]  |
| 7034 | 0x56c661612cd6c8e9:0xab51061bd1fce2c6 | Nick’s Auto Glass      | [Auto glass shop, Glass repair service]  |
| 7260 | 0x56c899d930e5e3f7:0xcf74f00d1e177986 | Novus Glass            | [Auto glass shop, Glass repair service]  |
| 7569 | 0x56c8999ae1910e87:0x233ea2130e9cdd71 | Speedy Glass           | [Auto glass shop, Glass repair service]  |
| 7614 | 0x56c8de7bbab952fd:0xb9a12991f0413b17 | Speedy Glass           | [Auto glass shop, Glass repair service]  |
| 9058 | 0x56c8e094818233c1:0xc4e1cecb77a2944c | Acme Auto Glass        | [Auto glass shop, Glass repair service]  |
| 12547 | 0x56c897da8047ac59:0xf668867469ce395d | Speedy Glass           | [Auto glass shop, Glass repair service]  |
| 1321 | 0x56c91e024450d3c7:0x94dc4cc3493b44f0 | Basin Street Auto Glass| [Auto glass shop]                        |

Kita dapat melihat bahwa semua output mengandung kategori yang sama pada kategori yang terdapat di input_sample, maka dapat disimpulkan precision sebesar 100%

### Collaborative-Based Filter

Pada Collaborative-Based Filter, saya menggunakan metric MSE, didapatkan 0.2945686290028723 dari data validasi sebanyak 210147.

Mean Squared Error (MSE) adalah metrik evaluasi yang digunakan untuk mengukur rata-rata kuadrat dari selisih antara nilai prediksi dan nilai aktual. MSE memberikan gambaran seberapa jauh hasil prediksi dari model dibandingkan dengan nilai yang

- MSE menghitung selisih antara nilai aktual dan nilai prediksi, kemudian mengkuadratkan selisih tersebut untuk memastikan bahwa semua nilai perbedaan adalah positif.
- Hasil akhirnya adalah rata-rata dari semua nilai perbedaan yang dikuadratkan ini.
- Nilai MSE yang lebih rendah menunjukkan bahwa model memiliki kinerja yang lebih baik dalam melakukan prediksi, sedangkan nilai yang lebih tinggi menunjukkan bahwa model tersebut kurang akurat.

Data yang digunakan terdiri dari rating numerik yang diberikan oleh pengguna terhadap berbagai tempat. MSE, yang menghitung perbedaan antara rating yang diprediksi dan rating aktual, memberikan gambaran langsung tentang seberapa akurat model dalam memprediksi preferensi pengguna.

## Kesimpulan
Tujuan dari proyek ini telah tercapai dengan sukses. Sistem rekomendasi yang dikembangkan mampu memberikan rekomendasi yang relevan kepada pengguna baru yang belum memiliki preferensi, berkat penggunaan Wilson Score Interval yang memastikan saran didasarkan pada popularitas tempat di kalangan pengguna lain. Selain itu, data yang sebelumnya memiliki kesalahan telah berhasil dirapikan dengan klasifikasi bahasa dan analisis sentimen dengan keberhasilan mempertahankan 93.7% data dari seluruh informasi data yang hilang (7618 data dari 8130 data yang hilang), teknik ini lebih baik dibanding kita melakukan drop pada semua data yang hilang memungkinkan model untuk bekerja dengan lebih efisien dan menghasilkan prediksi yang lebih akurat. Bagi pengguna yang sudah memiliki preferensi, sistem menggunakan metode Content-Based Filtering dan Collaborative Filtering dengan KNN untuk memberikan rekomendasi yang tepat dan sesuai dengan selera mereka dengan metric yang cukup baik yaitu Sensitivity 100% pada Content-Based Filtering dan MSE di bawah 0.3 Collaborative-Based Filtering. Dengan demikian, proyek ini berhasil mencapai tujuan utamanya yaitu meningkatkan relevansi dan akurasi rekomendasi yang diberikan, baik untuk pengguna baru maupun yang sudah berpengalaman.

## Referensi

[1] [Better than Average: Sort by Best Rating with Elasticsearch](https://www.elastic.co/blog/better-than-average-sort-by-best-rating-with-elasticsearch)
<br>

[2] [J. Li, J. Shang, and J. McAuley, "Unsupervised Contrastive Learning for Phrase Representations and Topic Mining," in Proc. Annual Meeting of the Association for Computational Linguistics (ACL), 2022.](https://aclanthology.org/2022.acl-long.426.pdf)
<br>

[3] [A. Yan, Z. He, J. Li, T. Zhang, and J. McAuley, "Personalized Showcases: Generating Multi-Modal Explanations for Recommendations," in Proc. 46th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR), 2023.](https://arxiv.org/pdf/2207.00422.pdf)
<br>

[4] [Lindner, J. (2024, July 17). Unveiling the secrets of Google Maps: A closer look at the stats that will amaze you. Google Maps Usage Statistics: Over 1 Billion Monthly Active Users.](https://gitnux.org/google-maps-usage-statistics/)
<br>

[5] [Lui, Marco and Timothy Baldwin (2011) Cross-domain Feature Selection for Language Identification, In Proceedings of the Fifth International Joint Conference on Natural Language Processing (IJCNLP 2011), Chiang Mai, Thailand, pp. 553—561.](http://www.aclweb.org/anthology/I11-1062)
<br>

[6] [Lui, Marco and Timothy Baldwin (2012) langid.py: An Off-the-shelf Language Identification Tool, In Proceedings of the 50th Annual Meeting of the Association for Computational Linguistics (ACL 2012), Demo Session, Jeju, Republic of Korea.](http://www.aclweb.org/anthology/P12-3005)
<br>

[7] [Kenneth Heafield and Rohan Kshirsagar and Santiago Barona (2015) Language Identification and Modeling in Specialized Hardware, In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 2: Short Papers).](http://aclweb.org/anthology/P15-2063)
<br>

[8] [Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.](https://doi.org/10.1609/icwsm.v8i1.14550)

**---Ini adalah bagian akhir laporan---**
