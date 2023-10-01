import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

bike_day = pd.read_csv('dashboard/day.csv')
bike_hour = pd.read_csv('dashboard/hour.csv')

st.title("Bike Sharing Data Analysis By Imam Waliyuddin Rabbani")
st.subheader("Pertanyaan:")
st.markdown("1. Berapa jumlah total penyewaan sepeda pada tahun 2011 dan 2012?")
st.markdown("2. Berapa rata-rata penyewaan sepeda per jam?")
st.markdown("3. Pada bulan apa penyewaan sepeda paling banyak?")
st.markdown("4. Berapa banyak penyewaan sepeda yang dilakukan oleh pengguna terdaftar dibandingkan dengan pengguna kasual?")
st.markdown("5. Apakah ada korelasi antara suhu dan jumlah penyewaan sepeda?")
st.markdown("6. Berapa banyak hari untuk tiap bulannya dalam dataset di mana lebih dari 1000 sepeda disewa?")

st.header("Exploratory Data Analysis (EDA), Visualization, &  Explanatory Analysis")
st.subheader("Pertanyaan 1")

total_rentals_2011 = bike_day[bike_day['yr'] == 0]['cnt'].sum()
total_rentals_2012 = bike_day[bike_day['yr'] == 1]['cnt'].sum()
years = ['2011', '2012']
total_rentals = [total_rentals_2011, total_rentals_2012]

fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x=years, y=total_rentals, palette='viridis')
plt.title('Total Rentals in 2011 and 2012')
plt.xlabel('Year')
plt.ylabel('Total Rentals')

for i, total in enumerate(total_rentals):
    ax1.text(i, total, f'{total:,}', ha='center', va='bottom', fontsize=12)
plt.ylim(0, 2500000)

st.pyplot(fig1)
st.write("Terlihat bahwa total penyewaan sepeda pada tahun 2011 berjumlah 1.234.103. Sedangkan pada tahun 2012 berjumlah 2.049.576.")

st.subheader("Pertanyaan 2")
average_rentals_per_hour = bike_hour.groupby('hr')['cnt'].mean()
hours = average_rentals_per_hour.index
average_rentals = average_rentals_per_hour.values

fig2, ax2 = plt.subplots(figsize=(20, 8))
sns.barplot(x=hours, y=average_rentals, palette='viridis')
plt.title('Average Rentals per Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Rentals')

for i, avg_rental in enumerate(average_rentals):
    ax2.text(i, avg_rental, f'{avg_rental:.2f}', ha='center', va='bottom', fontsize=10)
plt.ylim(0, 500)
st.pyplot(fig2)
st.write("Terlihat rata-rata penyewaan sepeda tiap jamnya yang dimana penyewaan terdikit pada jam ke 4 dan penyewaan terbanyak pada jam ke 17.")

st.subheader("Pertanyaan 3")
bike_day['date'] = pd.to_datetime(bike_day['dteday'])
bike_day['year_month'] = bike_day['date'].dt.to_period('M')

most_rentals_month_year = bike_day.groupby('year_month')['cnt'].sum()
months = most_rentals_month_year.index.strftime('%Y-%m')
total_rentals = most_rentals_month_year.values

fig3,ax3=plt.subplots(figsize=(20, 6))
sns.barplot(x=months, y=total_rentals, palette='viridis')
plt.title('Total Rentals per Month')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.xticks(rotation=45)  

for i, total in enumerate(total_rentals):
    ax3.text(i, total, f'{total:,}', ha='center', va='bottom', fontsize=10)
plt.ylim(0, 250000)
st.pyplot(fig3)
st.write("Terlihat penyewaan sepeda tiap bulannya yang dimana penyewaan sepeda terbanyak yaitu pada bulan ke 9 tahun 2012 dengan jumlah 218.573.")

st.subheader("Pertanyaan 4")
total_registered_rentals = bike_day['registered'].sum()
total_casual_rentals = bike_day['casual'].sum()
categories = ['Casual', 'Registered']
totals = [total_casual_rentals, total_registered_rentals]

fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.barplot(x=categories, y=totals, palette='viridis')
plt.title('Total Rentals by Category')
plt.xlabel('Category')
plt.ylabel('Total Rentals')

# Menambahkan label di atas setiap batang
for i, total in enumerate(totals):
    ax4.text(i, total, f'{total:,}', ha='center', va='bottom', fontsize=12)
plt.ylim(0, 3000000)
st.pyplot(fig4)
st.write("Terlihat bahwa penyewaaan sepeda oleh pengguna terdaftar lebih banyak dibandingkan penyewaan sepeda oleh pengguna kasual, dimana jumlah penyewa oleh pengguna terdaftar sebesar 2.672.662, sedangkan jumlah penyewa oleh pengguna kasual sebesar 620.017.")

st.subheader("Pertanyaan 5")
numeric_columns = bike_day.select_dtypes(include=['int64', 'float64'])
fig5 = plt.figure(figsize = (30,20))
sns.heatmap(numeric_columns.corr(), annot=True, square=True, fmt='.2f')
plt.title('Correlation', fontsize = 20)
st.pyplot(fig5)
st.write("Pda visualisasi yang diberikan, dapat terlihat korelasi antara tiap fitur/kolom. Namun terlihat bahwa terdapat korelasi positif yang cukup tinggi diantara suhu biasa maupun suhu yang dirasakan terhadap jumlah penyewaan, yaitu sebesar 0,63 untuk suhu biasa dan 0,63 untuk suhu yang dirasakan.")

st.subheader("Pertanyaan 6")
bike_day['date'] = pd.to_datetime(bike_day['dteday']).dt.date
days_with_more_than_1000_rentals = bike_day[bike_day['cnt'] > 1000].groupby(['year_month']).size()
months = days_with_more_than_1000_rentals.index.strftime('%Y-%m')
num_of_days = days_with_more_than_1000_rentals.values

fig6,ax6 = plt.subplots(figsize=(20, 6))
sns.barplot(x=months, y=num_of_days, palette='viridis')
plt.title('Number of Days with More than 1000 Rentals per Month')
plt.xlabel('Month')
plt.ylabel('Number of Days')
plt.xticks(rotation=45)  

for i, num_days in enumerate(num_of_days):
    ax6.text(i, num_days, f'{num_days}', ha='center', va='bottom', fontsize=10)
plt.ylim(0, 40)
st.pyplot(fig6)
st.write("Terlihat bahwa jumlah hari yang dimana jumlah penyewaan sepeda lebih dari 1000 untuk tiap bulannya, paling sedikit yaitu pada bulan 1 tahun 2011 yang hanya terdapat 21 hari yang memiliki penyewaan lebih dari 1000. Sedangkan terdapat 8 bulan yang memiliki 31 hari yang terdapat penyewaan lebih dari 1000.")

st.header("Conclusion")
st.subheader("Pertanyaan 1")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 1 bahwa: Total penyewaan sepeda pada tahun 2011 berjumlah 1.234.103. Sedangkan pada tahun 2012 berjumlah 2.049.576.")
st.subheader("Pertanyaan 2")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 2 bahwa: Rata-rata penyewaan sepeda tiap jamnya yang dimana penyewaan terdikit pada jam ke 4 dan penyewaan terbanyak pada jam ke 17.")
st.subheader("Pertanyaan 3")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 3 bahwa: Penyewaan sepeda tiap bulannya yang dimana penyewaan sepeda terbanyak yaitu pada bulan ke 9 tahun 2012 dengan jumlah 218.573.")
st.subheader("Pertanyaan 4")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 4 bahwa: Penyewaaan sepeda oleh pengguna terdaftar lebih banyak dibandingkan penyewaan sepeda oleh pengguna kasual, dimana jumlah penyewa oleh pengguna terdaftar sebesar 2.672.662, sedangkan jumlah penyewa oleh pengguna kasual sebesar 620.017.")
st.subheader("Pertanyaan 5")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 5 bahwa: Terdapat korelasi positif yang cukup tinggi diantara suhu biasa maupun suhu yang dirasakan terhadap jumlah penyewaan, yaitu sebesar 0,63 untuk suhu biasa dan 0,63 untuk suhu yang dirasakan.")
st.subheader("Pertanyaan 6")
st.write("Setelah dilakukan EDA dan visualisasi data, maka dapat dijawab pertanyaan 6 bahwa: Jumlah hari yang dimana jumlah penyewaan sepeda lebih dari 1000 untuk tiap bulannya, paling sedikit yaitu pada bulan 1 tahun 2011 yang hanya terdapat 21 hari yang memiliki penyewaan lebih dari 1000. Sedangkan terdapat 8 bulan yang memiliki 31 hari yang terdapat penyewaan lebih dari 1000.")
