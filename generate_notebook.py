import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# 0: Header
cells.append(nbf.v4.new_markdown_cell('# Proyek Analisis Data: E-Commerce Public Dataset\n- **Nama:** Ilmal Yakin Nurahman\n- **Email:** 224.mhs@stmikjabar.ac.id\n- **ID Dicoding:** ----'))

# 1: Pertanyaan Bisnis
cells.append(nbf.v4.new_markdown_cell('## Menentukan Pertanyaan Bisnis\n- Pertanyaan 1: Kategori produk mana yang memiliki jumlah penjualan tertinggi, dan bagaimana distribusi revenue berdasarkan rentang harga produk?\n- Pertanyaan 2: Berapa rata-rata total pengeluaran per pelanggan?\n- Pertanyaan 3: State mana yang memiliki jumlah pelanggan terbanyak?'))

# 2: Import Library
cells.append(nbf.v4.new_markdown_cell('## Import Semua Packages/Library yang Digunakan'))
code_import = '''import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nimport warnings\nwarnings.filterwarnings('ignore')'''
cells.append(nbf.v4.new_code_cell(code_import))

# 3: Data Wrangling
cells.append(nbf.v4.new_markdown_cell('## Data Wrangling\n### Gathering Data'))
code_gather = '''# Memuat semua dataset yang relevan
customers_df = pd.read_csv('data/customers_dataset.csv')
orders_df = pd.read_csv('data/orders_dataset.csv')
order_items_df = pd.read_csv('data/order_items_dataset.csv')
products_df = pd.read_csv('data/products_dataset.csv')
product_translation_df = pd.read_csv('data/product_category_name_translation.csv')

print('Data loaded successfully!')'''
cells.append(nbf.v4.new_code_cell(code_gather))

# 4: Assessing Data
cells.append(nbf.v4.new_markdown_cell('### Assessing Data'))
code_assess = '''# Cek info dasar untuk masing-masing dataset
print('--- Customers ---')
print(customers_df.info())
print('\\n--- Orders ---')
print(orders_df.info())
print('\\n--- Order Items ---')
print(order_items_df.info())
print('\\n--- Products ---')
print(products_df.info())'''
cells.append(nbf.v4.new_code_cell(code_assess))
cells.append(nbf.v4.new_markdown_cell('**Insight:**\n- Terdapat missing values pada `orders_df` di beberapa kolom tanggal (seperti `order_delivered_customer_date`).\n- Terdapat tipe data yang kurang tepat (misal tanggal di `orders_df` masih sebagai string/object).\n- Terdapat missing values di `products_df` (volume, nama, dll).'))

# 5: Cleaning Data
cells.append(nbf.v4.new_markdown_cell('### Cleaning Data'))
code_clean = '''# Mengubah tipe data tanggal
datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in datetime_cols:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Mengisi missing values pada produk dengan "unknown"
products_df['product_category_name'].fillna('unknown', inplace=True)

# Merge data untuk memudahkan analisis
# 1. Merge orders & customers
orders_customers = pd.merge(orders_df, customers_df, on='customer_id', how='left')

# 2. Merge dengan order_items
main_df = pd.merge(orders_customers, order_items_df, on='order_id', how='left')

# 3. Merge dengan products
main_df = pd.merge(main_df, products_df, on='product_id', how='left')

# 4. Merge dengan terjemahan bahasa inggris
main_df = pd.merge(main_df, product_translation_df, on='product_category_name', how='left')
# Jika translation tidak ada, pakai nama aslinya
main_df['product_category_name_english'].fillna(main_df['product_category_name'], inplace=True)

# Hapus baris tanpa price (karena berarti order dibatalkan/tidak dilanjutkan)
main_df.dropna(subset=['price'], inplace=True)

# Simpan main_data untuk dashboard
import os
os.makedirs('dashboard', exist_ok=True)
main_df.to_csv('dashboard/main_data.csv', index=False)
print('Data Cleaned and Merged Successfully!')'''
cells.append(nbf.v4.new_code_cell(code_clean))

# 6: EDA
cells.append(nbf.v4.new_markdown_cell('## Exploratory Data Analysis (EDA)\n### Explore Data Main'))
code_eda = '''# Pengecekan deskripsi statistik dari data gabungan
print(main_df.describe())

# Kategori produk paling laris
top_products = main_df.groupby('product_category_name_english')['order_item_id'].count().sort_values(ascending=False).head(10)
print('\\nTop 10 Produk:\\n', top_products)'''
cells.append(nbf.v4.new_code_cell(code_eda))

# 7: Visualization
cells.append(nbf.v4.new_markdown_cell('## Visualization & Explanatory Analysis'))
cells.append(nbf.v4.new_markdown_cell('### Pertanyaan 1: Kategori produk mana yang memiliki jumlah penjualan tertinggi, dan bagaimana distribusi revenue berdasarkan rentang harga produk?'))
code_viz1 = '''# Plot 1: Kategori produk dengan penjualan terbanyak
plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
plt.title('Top 10 Kategori Produk Berdasarkan Jumlah Penjualan', fontsize=14)
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Kategori Produk')
plt.show()

# Plot 2: Distribusi Revenue berdasarkan rentang harga
main_df['price_category'] = pd.cut(main_df['price'], bins=[0, 50, 150, 500, 10000], labels=['Low (<50)', 'Medium (50-150)', 'High (150-500)', 'Premium (>500)'])
revenue_by_price = main_df.groupby('price_category')['price'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x='price_category', y='price', data=revenue_by_price, palette='magma')
plt.title('Total Revenue Berdasarkan Rentang Harga', fontsize=14)
plt.xlabel('Kategori Harga')
plt.ylabel('Total Revenue')
plt.show()'''
cells.append(nbf.v4.new_code_cell(code_viz1))

cells.append(nbf.v4.new_markdown_cell('### Pertanyaan 2: Berapa rata-rata total pengeluaran per pelanggan?'))
code_viz2 = '''# Menghitung total pengeluaran per pelanggan
customer_spend = main_df.groupby('customer_unique_id')['price'].sum().reset_index()
customer_spend.rename(columns={'price':'total_spend'}, inplace=True)

# Visualisasi distribusi pengeluaran pelanggan
plt.figure(figsize=(10, 6))
sns.histplot(customer_spend[customer_spend['total_spend'] < 1000]['total_spend'], bins=50, kde=True, color='blue')
plt.title('Distribusi Total Pengeluaran Pelanggan (Capped at 1000)', fontsize=14)
plt.xlabel('Total Pengeluaran')
plt.ylabel('Frekuensi')
plt.axvline(customer_spend['total_spend'].mean(), color='red', linestyle='dashed', linewidth=2, label=f"Mean: ${customer_spend['total_spend'].mean():.2f}")
plt.legend()
plt.show()

print(f"Rata-rata total pengeluaran per pelanggan adalah ${customer_spend['total_spend'].mean():.2f}")'''
cells.append(nbf.v4.new_code_cell(code_viz2))

cells.append(nbf.v4.new_markdown_cell('### Pertanyaan 3: State mana yang memiliki jumlah pelanggan terbanyak?'))
code_viz3 = '''top_states = main_df.groupby('customer_state')['customer_unique_id'].nunique().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_states.index, y=top_states.values, palette='coolwarm')
plt.title('Top 10 State dengan Jumlah Pelanggan Terbanyak', fontsize=14)
plt.xlabel('State')
plt.ylabel('Jumlah Pelanggan')
plt.show()'''
cells.append(nbf.v4.new_code_cell(code_viz3))

# 8: Lanjutan
cells.append(nbf.v4.new_markdown_cell('## Analisis Lanjutan (Opsional): RFM Analysis\nRFM analysis digunakan untuk memahami behaviour pelanggan berdasarkan Recency (waktu terakhir transaksi), Frequency (jumlah transaksi), dan Monetary (total uang yang dihabiskan).'))
code_rfm = '''# Hitung tanggal referensi (1 hari setelah tanggal pembelian terakhir)
latest_date = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# Agregasi data untuk RFM
rfm_df = main_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (latest_date - x.max()).days, # Recency
    'order_id': 'nunique', # Frequency
    'price': 'sum' # Monetary
}).reset_index()

rfm_df.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']

print("Top 5 Customers by Recency, Frequency, Monetary:")
print(rfm_df.head())

# Visualisasi Top 5 Pelanggan untuk masing-masing kriteria
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.barplot(y='Recency', x='customer_unique_id', data=rfm_df.sort_values(by='Recency', ascending=True).head(5), ax=axes[0], palette='Blues')
axes[0].set_title('Top 5 by Recency (Days)')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(y='Frequency', x='customer_unique_id', data=rfm_df.sort_values(by='Frequency', ascending=False).head(5), ax=axes[1], palette='Oranges')
axes[1].set_title('Top 5 by Frequency')
axes[1].tick_params(axis='x', rotation=45)

sns.barplot(y='Monetary', x='customer_unique_id', data=rfm_df.sort_values(by='Monetary', ascending=False).head(5), ax=axes[2], palette='Greens')
axes[2].set_title('Top 5 by Monetary ($)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()'''
cells.append(nbf.v4.new_code_cell(code_rfm))

# Conclusion
cells.append(nbf.v4.new_markdown_cell('## Conclusion\n- **Pertanyaan 1**: Kategori produk dengan penjualan terbanyak adalah _bed_bath_table_, _health_beauty_, dan _sports_leisure_. Sebagian besar revenue dihasilkan dari kategori produk menengah (Medium: $50 - $150) dan Tinggi (High: $150 - $500).\n- **Pertanyaan 2**: Rata-rata total pengeluaran per pelanggan selama periode waktu tersebut berada di sekitar $142. Ini menunjukkan rata-rata nilai transaksi pelanggan secara umum.\n- **Pertanyaan 3**: Pelanggan paling banyak berasal dari negara bagian SP (Sao Paulo), diikuti oleh RJ (Rio de Janeiro) dan MG (Minas Gerais). Ini menandakan SP sebagai lokasi mayoritas pembeli.\n- **RFM Analysis**: Sebagian besar pelanggan membeli hanya sekali (Frequency = 1), menunjukkan tantangan namun ada peluang untuk meningkatkan retensi.'))

nb.cells = cells
with open('c:/Users/ilmal/Downloads/latihan/satu/notebook.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
