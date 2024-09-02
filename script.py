# %%
import pandas as pd
import numpy as np
import langid
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, accuracy_score, recall_score, precision_score, f1_score, confusion_matrix

# %% [markdown]
# # Data Loading

# %%
review_url = 'https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/review-Alaska.json.gz'
metadata_url = 'https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/meta-Alaska.json.gz'

# %%
review = pd.read_json('alaska dataset/review-Alaska.json', lines=True)
meta = pd.read_json('alaska dataset/meta-Alaska.json', lines=True)

# %% [markdown]
# # Data Understanding

# %% [markdown]
# ## Exploratory Data Analysis

# %%
review.head()

# %%
review.info()

# %% [markdown]
# Pada data review ini, kita hanya menggunakan user_id, rating, dan gmap_id untuk model sistem rekomendasi kita. Data-data tersebut memiliki nilai null pada user_id dan rating

# %%
review[review['user_id'].isna()]

# %% [markdown]
# Setelah melakukan analisis, sepertinya ada kesalahan dalam input data. Terlihat kita memiliki nomor berformat user_id pada kolom pertama dan untuk namanya kemungkinan besar review ini berasal dari third party app untuk memberikan review kepada google local

# %%
review[review['rating'].isna()]

# %% [markdown]
# Selanjutnya mengalisis pada rating. Terlihat rating tidak memiliki nilai, tetapi kita memiliki kolom text review yang dapat digunakan untuk menganalisis sentimen dari text tersebut. Namun kita juga memilik tantangan lain yaitu selain bahasa inggris kita juga memiliki bahasa jerman.

# %% [markdown]
# Namun, jika diperhatikan kedua output dari kode pengecekan data user_id dan dan rating yang memiliki nilai null mengembalikan jumlah data yang sama selanjutnya kita akan memeriksa apakah kedua dataframe tersebut sama

# %%
review[review['user_id'].isna()].equals(review[review['rating'].isna()])

# %% [markdown]
# Terlihat dari output bahwa kedua dataframe tersebut sama

# %% [markdown]
# Dari hasil analisis ini kita memiliki kesimpulan kalau kolom text memiliki informasi yang penting oleh karena itu kita harus mengecek apakah kita memiliki text yang memiliki nilai null

# %%
review[review['user_id'].isna()]['text'].isna().sum()

# %% [markdown]
# Setelah dilakukan analisis, kolom text tidak memiliki nilai null

# %%
meta.head()

# %%
meta.info()

# %% [markdown]
# Pada data meta ini, kita hanya menggunakan name, gmap_id, category, dan avg_rating untuk model sistem rekomendasi kita. Data-data tersebut sudah bersih dari Null kecuali data category

# %% [markdown]
# Namun, setelah melakukan analisis terhadap avg_rating, kita melihat kolom num_of_review. Tentu menjadi sangat tidak adil jika mengurutkan tempat terbaik dari avg_rating saja tanpa ada bobot num_of_review

# %% [markdown]
# # Data Preparation

# %% [markdown]
# ## Dataframe Review

# %%
# masukkan user_id yang null pada varibel website_reviewer ke csv untuk memudahkan persiapan pada data
website_reviewer = review[review['user_id'].isna()]
website_reviewer.to_csv('website_reviewer.csv')

# %% [markdown]
# Selanjutnya kita hanya perlu memperbaiki csv yang memiliki kesalahan input dengan menghapus koma di depan dan menambahkan koma setelah user_id dan ubah nama filenya menjadi _website_reviewer.csv

# %%
# memasukkan data csv ke variabel website_reviewer
website_reviewer = pd.read_csv('_website_reviewer.csv')
website_reviewer

# %% [markdown]
# Terdapat kolom baru yaitu Unnamed: 1, kita dapat menghapusnya

# %%
# menghapus kolom Unnamed: 1
website_reviewer = website_reviewer.drop(columns=['Unnamed: 1'])
website_reviewer

# %%
# fungsi untuk mengklasifikasikan bahasa
def classify_language(text):
    lang, _ = langid.classify(text)
    return lang

# %% [markdown]
# Kita dapat menggunakan model atau library yang telah dibuat, pada kasus ini kita menggunakan langid untuk mengklasifikasikan bahasa

# %%
# menerapkan fungsi pada kolom 'text' dan simpan hasilnya di kolom baru 'language'
website_reviewer['language'] = website_reviewer['text'].apply(classify_language)

# %%
website_reviewer

# %% [markdown]
# Dataframe telah memiliki kolom baru yaitu bahasa sebagai klasifikasinya, tahap selanjutnya yaitu membuang data selain yang berbahasa inggris

# %%
# drop data selain bahasa inggris
website_reviewer = website_reviewer[website_reviewer['language'] == 'en']

# %%
website_reviewer

# %% [markdown]
# Selanjutnya kita akan mengklasifikasikan sentimen dari text dan konversi sentimen tersebut menjadi sebuah rating dengan ketentuan positif 5.0, netral 3.0, dan negatif 1.0

# %%
# inisiasi analyzer untuk analisis sentimen
analyzer = SentimentIntensityAnalyzer()

# %%
# fungsi untuk mengklasifikasi sentimen
def sentiment_analysis(text):
    vs = analyzer.polarity_scores(text)
    score = vs['compound']
    
    if score >= 0.05:
        return 5.0
    elif -0.05 < score < 0.05:
        return 3.0
    else:
        return 1.0

# %%
# menerapkan fungsi pada kolom 'text' dan simpan hasilnya di kolom 'rating'
website_reviewer['rating'] = website_reviewer['text'].apply(sentiment_analysis)

# %%
website_reviewer = website_reviewer.drop(columns=['language'])

# %%
website_reviewer

# %%
website_reviewer.rating.unique()

# %% [markdown]
# Sekarang, kita telah memiliki rating dan user_id pada data yang sebelumnya hilang

# %% [markdown]
# Kita berhasil mempertahankan 93.7% data dari seluruh informasi data yang hilang, teknik ini lebih baik dibanding kita melakukan drop pada semua data yang hilang

# %% [markdown]
# Tahap selanjutnya yaitu melakukan penggabungan data ini pada data review

# %%
# menghapus dataframe review yang tidak memiliki nilai
review = review.dropna(subset=['user_id'])

# %%
# menambahkan dataframe yang sebelumnya sudah dipersiapkan
review = pd.concat([review, website_reviewer], ignore_index=True)

# %%
review.info()

# %%
# Mengubah user_id menjadi list tanpa nilai yang sama
user_ids = review['user_id'].unique().tolist()

# %%
# Melakukan encoding userID
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}

# %%
# Melakukan proses encoding angka ke ke userID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}

# %% [markdown]
# Selanjutnya, lakukan hal yang sama pada kolom gmap_id

# %%
# Mengubah gmap_id menjadi list tanpa nilai yang sama
place_ids = review['gmap_id'].unique().tolist()
 
# Melakukan proses encoding gmap_id
gmap_to_gmap_encoded = {x: i for i, x in enumerate(place_ids)}
 
# Melakukan proses encoding angka ke gmap_id
gmap_encoded_to_gmap = {i: x for i, x in enumerate(place_ids)}

# %%
# Mapping userID ke dataframe user
review['user'] = review['user_id'].map(user_to_user_encoded)
 
# Mapping place ke dataframe place
review['gmap'] = review['gmap_id'].map(gmap_to_gmap_encoded)

# %%
# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)
 
# Mendapatkan jumlah places
num_places = len(gmap_encoded_to_gmap)
print(num_places)
 
# Mengubah rating menjadi nilai float
review['rating'] = review['rating'].values.astype(np.float32)
 
# Nilai minimum rating
min_rating = min(review['rating'])
 
# Nilai maksimal rating
max_rating = max(review['rating'])
 
print('Number of User: {}, Number of places: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_places, min_rating, max_rating
))


# %%
review = review.sample(frac=1, random_state=42)
review

# %%
# Membuat variabel x untuk mencocokkan data user dan gmap menjadi satu value
x = review[['user', 'gmap']].values
 
# Membuat variabel y untuk membuat rating dari hasil 
y = review['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
 
# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * review.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)
 
print(x, y)

# %%
x_train.shape

# %% [markdown]
# Sekarang, data review sudah siap digunakan! selanjutnya kita akan menyiapkan data meta

# %% [markdown]
# ## Dataframe Metadata

# %%
# Mengganti NaN dengan list kosong
meta['category'] = meta['category'].apply(lambda x: x if isinstance(x, list) else [])

# %% [markdown]
# Pada data category di Meta, kita mengganti data yang kosong menjadi list [] yang artinya tidak memiliki kategori apapun

# %%
mlb = MultiLabelBinarizer()
categories_encoded = mlb.fit_transform(meta['category'])

# %%
categories_df = pd.DataFrame(categories_encoded, columns=mlb.classes_)

# %% [markdown]
# Melakukan vektorisasi data category terhadap dataframe meta dengan Multi Label Binarizer dan menyimpannya di categories_df

# %%
categories_df

# %%
meta = meta.join(categories_df)

# %% [markdown]
# menggabungkan categories_df ke dataframe meta dan melakukan drop kolom category

# %%
# similiarity matrix category dengan cosine similiarity
similarity_matrix = cosine_similarity(categories_df)
print(similarity_matrix)

# %% [markdown]
# melakukan similiarity matrix dengan cosine similiarity

# %% [markdown]
# # Model Development

# %% [markdown]
# ## Non-Personalized User

# %%
def wilson_score_interval(avg_rating, num_of_reviews):
    p = avg_rating / 5.0
    n = num_of_reviews
    z = 1.96  # Z-score for 95% confidence interval
    denominator = 1 + (z ** 2) / n
    centre_adjusted_probability = p + (z ** 2) / (2 * n)
    adjusted_probability = centre_adjusted_probability / denominator
    return  adjusted_probability

# %% [markdown]
# Kita dapat menggunakan Wilson Score Interval untuk memberikan bobot pada rating supaya lebih adil

# %%
# Hitung batas atas interval Wilson Score dan tambahkan ke dataframe
meta['wilson_score'] = meta.apply(lambda row: wilson_score_interval(row['avg_rating'], row['num_of_reviews']), axis=1)

# %%
meta.head()

# %% [markdown]
# Dengan begini, dataframe meta telah memiliki skor wilson untuk memberikan rekomendasi tempat terbaik berdasarkan rating kepada Non-personalized user

# %%
# menampilkan tempat terbaik berdasarkan rating
best_places = meta.sort_values(by='wilson_score', ascending=False).head(10)
best_places

# %% [markdown]
# Tampilan rekomendasi tempat terbaik untuk Non-personalized user sebanyak 10

# %% [markdown]
# ## Content-Based Filter

# %%
# fungsi untuk mendapatkan rekomendasi content-based
def get_content_based(gmap_id, similarity_matrix, data, top_n=10):
    item_index = data[data['gmap_id'] == gmap_id].index[0]
    
    similarity_scores = list(enumerate(similarity_matrix[item_index]))
    
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    
    top_items = data.iloc[top_indices][['gmap_id', 'name', 'category']]
    
    return top_items

# %%
# Contoh mendapatkan rekomendasi
recommendations = get_content_based('0x56b646ed2220b77f:0xd8975e316de80952', data=meta, similarity_matrix=similarity_matrix)
recommendations

# %% [markdown]
# ## Colaborative-Based Filter

# %%
# membuat model KNN
knn = KNeighborsRegressor(n_neighbors=5)

# %%
# melatih model
knn.fit(x_train, y_train)

# %%
def get_collaborative_based(user_id, review, meta, knn, gmap_to_gmap_encoded, user_to_user_encoded, gmap_encoded_to_gmap):
    # Mendapatkan tempat yang sudah dikunjungi oleh pengguna
    place_visited_by_user = review[review.user_id == user_id]

    # Menemukan tempat yang belum dikunjungi oleh pengguna
    place_not_visited = meta[~meta['gmap_id'].isin(place_visited_by_user.gmap_id.values)]['gmap_id'] 
    place_not_visited = list(
        set(place_not_visited)
        .intersection(set(gmap_to_gmap_encoded.keys()))
    )
    place_not_visited = [[gmap_to_gmap_encoded.get(x)] for x in place_not_visited]

    # Encode pengguna dan buat array untuk prediksi
    user_encoder = user_to_user_encoded.get(user_id)
    user_place_array = np.hstack(
        ([[user_encoder]] * len(place_not_visited), place_not_visited)
    )

    # Mendapatkan rating prediksi untuk data tempat pengguna
    ratings = knn.predict(user_place_array).flatten()

    # Mendapatkan indeks dari 10 rating tertinggi
    top_ratings_indices = ratings.argsort()[-10:][::-1]

    # Mempetakan ID tempat yang direkomendasikan
    recommended_place_ids = [
        gmap_encoded_to_gmap.get(place_not_visited[x][0]) for x in top_ratings_indices
    ]

    # Menampilkan rekomendasi untuk pengguna
    print(f'Showing recommendations for user: {user_id}')

    # Menampilkan tempat yang telah dikunjungi oleh pengguna dengan rating tertinggi
    top_place_user = (
        place_visited_by_user.sort_values(by='rating', ascending=False)
        .head(5)
        .gmap_id.values
    )

    # Filter DataFrame untuk tempat yang telah dikunjungi
    place_df_rows = meta[meta['gmap_id'].isin(top_place_user)]

    # Filter DataFrame untuk tempat yang direkomendasikan
    recommended_place = meta[meta['gmap_id'].isin(recommended_place_ids)]

    # Mengembalikan 10 rekomendasi tempat teratas
    return place_visited_by_user, recommended_place

# %%
user_id = review.user_id.sample(1).iloc[0]
visited, top_10_places = get_collaborative_based(user_id, review, meta, knn, gmap_to_gmap_encoded, user_to_user_encoded, gmap_encoded_to_gmap)

# %%
visited['gmap_id']

# %%
top_10_places[['gmap_id', 'name']]

# %% [markdown]
# # Evaluation

# %%
# mengambil 1 sample gmap_id
sample_gmap_id = meta.gmap_id.sample(1).iloc[0]
sample_user_id = review.user_id.sample(1).iloc[0]

# %% [markdown]
# ## Content-Based Filter

# %%
# input sample
meta[meta['gmap_id'] == sample_gmap_id][['gmap_id', 'name', 'category']]

# %%
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_colwidth', None)

# %%
recommendations_sample_content_based = get_content_based(sample_gmap_id, data=meta, similarity_matrix=similarity_matrix)
recommendations_sample_content_based

# %% [markdown]
# Terlihat bahwa semua data category juga memiliki persamaan dari category yang ada pada input sample

# %% [markdown]
# ## Collaborative-Based Filter

# %%
x_val.shape

# %%
# membuat prediksi
y_pred = knn.predict(x_val)
 
# hitung MSE
mse = np.sqrt(mean_squared_error(y_val, y_pred))
print(f'MSE: {mse}')


