# Divar-project
A data analysis pipeline for Divar real estate listings using Python and Pandas. Includes data cleaning, feature extraction (area, price, floor, location), outlier removal, and visualization with Seaborn/Matplotlib. Useful for exploring housing market trends across Tehran neighborhoods.
# 🏢 Divar Real Estate Data Project

This project is a complete pipeline to **scrape**, **clean**, and **analyze** housing advertisement data from [Divar.ir](https://divar.ir), one of Iran’s largest classifieds platforms. The project supports scraping with both **Selenium** and **Requests**, and includes **data cleaning**, **feature extraction**, and **visualization** using Python libraries like Pandas, Matplotlib, and Seaborn.

---

## 🚀 What This Project Does

- ✅ Scrapes over 100,000 real estate listings (apartments) from Divar.
- ✅ Extracts structured information including:
  - Title
  - Posted date
  - Location
  - Price and price per square meter
  - Floor information
  - Amenities (elevator, parking, storage)
  - Listing URL
- ✅ Cleans and preprocesses the data:
  - Converts Persian numerals to English
  - Removes extra text and symbols
  - Handles missing or corrupted values
- ✅ Extracts useful features:
  - Floor number from phrases like `۳ از ۵`
  - Apartment size (e.g., `۵۳ متری`) from titles
  - Encodes locations as numeric values for plotting
- ✅ Visualizes key trends:
  - Price vs. Location
  - Distribution of prices and sizes
  - 3D plots based on price, location, and area

---

## 📁 Example Data Format

```json
{
  "title": "آپارتمان ۵۳ متری /تک واحدی /نوساز/با پارکینگ",
  "posted_date": "۱ روز پیش در تهران",
  "location": "دکتر هوشیار",
  "price": "۵٬۶۰۰٬۰۰۰٬۰۰۰ تومان",
  "price_per_meter": "۱۰۵٬۶۶۰٬۰۰۰ تومان",
  "floor": "۱ از ۴",
  "elevator": true,
  "parking": true,
  "storage": true,
  "url": "https://divar.ir/v/-/AaN89Qqn"
}
