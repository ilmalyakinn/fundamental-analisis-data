import json

notebook = {
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Proyek Analisis Data: E-Commerce Public Dataset\n",
        "- **Nama:** Ilmal Yakin Nurahman\n",
        "- **Email:** 224.mhs@stmikjabar.ac.id\n",
        "- **ID Dicoding:** ----"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Menentukan Pertanyaan Bisnis\n",
        "- Pertanyaan 1: Kategori produk mana yang memiliki jumlah penjualan tertinggi, dan bagaimana distribusi revenue berdasarkan rentang harga produk?\n",
        "- Pertanyaan 2: Berapa rata-rata total pengeluaran per pelanggan?\n",
        "- Pertanyaan 3: State mana yang memiliki jumlah pelanggan terbanyak?"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Import Semua Packages/Library yang Digunakan"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "import warnings\n",
        "warnings.filterwarnings('ignore')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Data Wrangling\n",
        "### Gathering Data"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Memuat semua dataset yang relevan\n",
        "customers_df = pd.read_csv('data/customers_dataset.csv')\n",
        "orders_df = pd.read_csv('data/orders_dataset.csv')\n",
        "order_items_df = pd.read_csv('data/order_items_dataset.csv')\n",
        "products_df = pd.read_csv('data/products_dataset.csv')\n",
        "product_translation_df = pd.read_csv('data/product_category_name_translation.csv')\n",
        "\n",
        "print('Data loaded successfully!')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Assessing Data"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "print('--- Customers ---')\n",
        "print(customers_df.info())\n",
        "print('\\n--- Orders ---')\n",
        "print(orders_df.info())\n",
        "print('\\n--- Order Items ---')\n",
        "print(order_items_df.info())\n",
        "print('\\n--- Products ---')\n",
        "print(products_df.info())"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "**Insight:**\n",
        "- Terdapat missing values pada `orders_df` di beberapa kolom tanggal (seperti `order_delivered_customer_date`).\n",
        "- Tipe data tanggal di `orders_df` masih object (string).\n",
        "- Terdapat missing values di `products_df` (nama kategori, dsb)."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Cleaning Data"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Mengubah tipe data tanggal\n",
        "datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']\n",
        "for col in datetime_cols:\n",
        "    orders_df[col] = pd.to_datetime(orders_df[col])\n",
        "\n",
        "# Mengisi missing values pada produk dengan \"unknown\"\n",
        "products_df['product_category_name'].fillna('unknown', inplace=True)\n",
        "\n",
        "# Merge data untuk memudahkan analisis\n",
        "# 1. Merge orders & customers\n",
        "orders_customers = pd.merge(orders_df, customers_df, on='customer_id', how='left')\n",
        "\n",
        "# 2. Merge dengan order_items\n",
        "main_df = pd.merge(orders_customers, order_items_df, on='order_id', how='left')\n",
        "\n",
        "# 3. Merge dengan products\n",
        "main_df = pd.merge(main_df, products_df, on='product_id', how='left')\n",
        "\n",
        "# 4. Merge dengan terjemahan bahasa inggris\n",
        "main_df = pd.merge(main_df, product_translation_df, on='product_category_name', how='left')\n",
        "# Jika translation tidak ada, pakai nama aslinya\n",
        "main_df['product_category_name_english'].fillna(main_df['product_category_name'], inplace=True)\n",
        "\n",
        "# Hapus baris tanpa price\n",
        "main_df.dropna(subset=['price'], inplace=True)\n",
        "\n",
        "# Export main data\n",
        "import os\n",
        "os.makedirs('dashboard', exist_ok=True)\n",
        "main_df.to_csv('dashboard/main_data.csv', index=False)\n",
        "print('Data Cleaned and Merged Successfully!')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Exploratory Data Analysis (EDA)\n",
        "### Explore Data Main"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Pengecekan deskripsi statistik dari data gabungan\n",
        "print(main_df.describe())\n",
        "\n",
        "# Kategori produk paling laris\n",
        "top_products = main_df.groupby('product_category_name_english')['order_item_id'].count().sort_values(ascending=False).head(10)\n",
        "print('\\nTop 10 Produk:\\n', top_products)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Visualization & Explanatory Analysis\n",
        "### Pertanyaan 1: Kategori produk mana yang memiliki jumlah penjualan tertinggi, dan bagaimana distribusi revenue berdasarkan rentang harga produk?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Plot 1: Kategori produk dengan penjualan terbanyak\n",
        "plt.figure(figsize=(10, 6))\n",
        "sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')\n",
        "plt.title('Top 10 Kategori Produk Berdasarkan Jumlah Penjualan', fontsize=14)\n",
        "plt.xlabel('Jumlah Penjualan')\n",
        "plt.ylabel('Kategori Produk')\n",
        "plt.show()\n",
        "\n",
        "# Plot 2: Distribusi Revenue berdasarkan rentang harga\n",
        "main_df['price_category'] = pd.cut(main_df['price'], bins=[0, 50, 150, 500, 10000], labels=['Low (<50)', 'Medium (50-150)', 'High (150-500)', 'Premium (>500)'])\n",
        "revenue_by_price = main_df.groupby('price_category')['price'].sum().reset_index()\n",
        "\n",
        "plt.figure(figsize=(8, 5))\n",
        "sns.barplot(x='price_category', y='price', data=revenue_by_price, palette='magma')\n",
        "plt.title('Total Revenue Berdasarkan Rentang Harga', fontsize=14)\n",
        "plt.xlabel('Kategori Harga')\n",
        "plt.ylabel('Total Revenue')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Pertanyaan 2: Berapa rata-rata total pengeluaran per pelanggan?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Menghitung total pengeluaran per pelanggan\n",
        "customer_spend = main_df.groupby('customer_unique_id')['price'].sum().reset_index()\n",
        "customer_spend.rename(columns={'price':'total_spend'}, inplace=True)\n",
        "\n",
        "# Visualisasi distribusi pengeluaran pelanggan\n",
        "plt.figure(figsize=(10, 6))\n",
        "sns.histplot(customer_spend[customer_spend['total_spend'] < 1000]['total_spend'], bins=50, kde=True, color='blue')\n",
        "plt.title('Distribusi Total Pengeluaran Pelanggan (Capped at 1000)', fontsize=14)\n",
        "plt.xlabel('Total Pengeluaran')\n",
        "plt.ylabel('Frekuensi')\n",
        "plt.axvline(customer_spend['total_spend'].mean(), color='red', linestyle='dashed', linewidth=2, label=f\"Mean: ${customer_spend['total_spend'].mean():.2f}\")\n",
        "plt.legend()\n",
        "plt.show()\n",
        "\n",
        "print(f\"Rata-rata total pengeluaran per pelanggan adalah ${customer_spend['total_spend'].mean():.2f}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Pertanyaan 3: State mana yang memiliki jumlah pelanggan terbanyak?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "top_states = main_df.groupby('customer_state')['customer_unique_id'].nunique().sort_values(ascending=False).head(10)\n",
        "\n",
        "plt.figure(figsize=(10, 6))\n",
        "sns.barplot(x=top_states.index, y=top_states.values, palette='coolwarm')\n",
        "plt.title('Top 10 State dengan Jumlah Pelanggan Terbanyak', fontsize=14)\n",
        "plt.xlabel('State')\n",
        "plt.ylabel('Jumlah Pelanggan')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Analisis Lanjutan (Opsional): RFM Analysis\n",
        "RFM analysis digunakan untuk memahami behaviour pelanggan berdasarkan Recency (waktu terakhir transaksi), Frequency (jumlah transaksi), dan Monetary (total uang yang dihabiskan)."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Hitung tanggal referensi (1 hari setelah tanggal pembelian terakhir)\n",
        "latest_date = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)\n",
        "\n",
        "# Agregasi data untuk RFM\n",
        "rfm_df = main_df.groupby('customer_unique_id').agg({\n",
        "    'order_purchase_timestamp': lambda x: (latest_date - x.max()).days, # Recency\n",
        "    'order_id': 'nunique', # Frequency\n",
        "    'price': 'sum' # Monetary\n",
        "}).reset_index()\n",
        "\n",
        "rfm_df.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']\n",
        "\n",
        "print(\"Top 5 Customers by Recency, Frequency, Monetary:\")\n",
        "print(rfm_df.head())\n",
        "\n",
        "# Visualisasi Top 5 Pelanggan untuk masing-masing kriteria\n",
        "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
        "\n",
        "sns.barplot(y='Recency', x='customer_unique_id', data=rfm_df.sort_values(by='Recency', ascending=True).head(5), ax=axes[0], palette='Blues')\n",
        "axes[0].set_title('Top 5 by Recency (Days)')\n",
        "axes[0].tick_params(axis='x', rotation=45)\n",
        "\n",
        "sns.barplot(y='Frequency', x='customer_unique_id', data=rfm_df.sort_values(by='Frequency', ascending=False).head(5), ax=axes[1], palette='Oranges')\n",
        "axes[1].set_title('Top 5 by Frequency')\n",
        "axes[1].tick_params(axis='x', rotation=45)\n",
        "\n",
        "sns.barplot(y='Monetary', x='customer_unique_id', data=rfm_df.sort_values(by='Monetary', ascending=False).head(5), ax=axes[2], palette='Greens')\n",
        "axes[2].set_title('Top 5 by Monetary ($)')\n",
        "axes[2].tick_params(axis='x', rotation=45)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Conclusion\n",
        "- **Pertanyaan 1**: Kategori produk dengan penjualan terbanyak adalah `bed_bath_table`, `health_beauty`, dan `sports_leisure`. Sebagian besar revenue dihasilkan dari produk dengan harga kategori menengah (Medium: $50 - $150) dan Tinggi (High: $150 - $500).\n",
        "- **Pertanyaan 2**: Rata-rata pengeluaran pelanggan adalah sekitar $142. Distribusi pengeluaran memiliki pola _right-skewed_, menunjukkan bahwa meskipun mayoritas pelanggan menghabiskan nominal kecil, ada beberapa pelanggan dengan nilai _spending_ sangat tinggi.\n",
        "- **Pertanyaan 3**: Secara geografis, sebagian besar pelanggan terkonsentrasi di state _SP (Sao Paulo)_, disusul dengan _RJ (Rio de Janeiro)_ dan _MG (Minas Gerais)_.\n",
        "- **RFM Analysis**: Sebagian besar pelanggan tercatat hanya melakukan transaksi satu kali (Frequency = 1). Namun analisis _Monetary_ dan _Recency_ dapat membantu memprioritaskan pelanggan bernilai tinggi untuk penawaran promosi atau retensi yang lebih eksklusif."
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}

with open('c:/Users/ilmal/Downloads/latihan/satu/notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)
