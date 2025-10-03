# 🌍 Air Quality Monitoring Web App

A Streamlit-based web application to monitor real-time and historical air quality data in Indian cities.  
The app integrates **Supabase** (for storing user data & alerts) and the **WAQI API** (for pollutant readings).

---

## 🚀 Features

- 📊 **Dashboard**  
  - Enter any Indian city and fetch real-time pollutant data (PM2.5, PM10, NO2, SO2, CO, etc.)  
  - Visualize pollutants with **bar, pie, and line charts**  
  - Alerts triggered if pollutant levels exceed safe thresholds  

- 📜 **History**  
  - View **last 7 days of pollutant trends** for a city  
  - Select pollutant and see interactive line charts  

- ⚙️ **User Settings**  
  - Secure login & registration (name, email, phone)  
  - Manage your subscriptions (Email / SMS alerts)  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — Frontend framework  
- [Supabase](https://supabase.com/) — Database & authentication  
- [WAQI API](https://aqicn.org/api/) — Real-time air quality data  
- [Plotly](https://plotly.com/python/) — Interactive charts  

---

## 📂 Project Structure

air-quality-monitoring/
│── .env # API keys & DB credentials (DO NOT COMMIT)
│── requirements.txt # Python dependencies
│── .gitignore # Ignored files
│── .streamlit/config.toml # Streamlit UI settings
└── src/
├── app/ # Streamlit app pages
│ ├── main.py
│ ├── login.py
│ ├── dashboard.py
│ ├── history.py
│ └── settings.py
│
├── dao/ # Database access (Supabase DAOs)
├── services/ # Business logic (API, alerts, users)
├── utils/ # Plotting, thresholds
└── config/ # Supabase & app settings