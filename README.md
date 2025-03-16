-

# **Smart Campus Navigation and Emergency Routing System** 🚑📍

This project is a **Flask-based web application** designed for efficient navigation within a campus and emergency patient transportation from predefined campus locations to the hospital. It integrates **Google Maps API, Folium mapping, live location tracking, and email notifications** to provide an enhanced routing experience.

---

## **🔹 Features**
### 1️⃣ **Campus Navigation**
- Users can **select predefined locations** (such as hostels, library, ground, etc.) to navigate to the hospital.
- **Custom destination input**: Users can enter an address manually.
- **Live location support** for dynamic route calculation.

### 2️⃣ **Route Calculation Using Google Maps API**
- Uses the **Google Directions API** to find the best route.
- Provides **distance and estimated travel time**.
- Supports **driving mode** for navigation.

### 3️⃣ **Interactive Map with Folium** 🗺️
- Displays the **origin, destination, and travel path**.
- **Color-coded routes**:  
  - **Blue:** Outward journey  
  - **Red:** Return journey  
- **Live location tracking** (if enabled by the user).

### 4️⃣ **Return Trip & Email Notification System** 📧
- If a return trip is requested, an **email notification** is sent to alert concerned personnel.
- The email is sent using **SMTP via Gmail**.
- The recipient gets **ETA information** about the returning patient.

### 5️⃣ **Web-based User Interface** 🌐
- Simple HTML & JavaScript frontend.
- A **dynamic map is embedded** using Folium.
- Fully responsive design.

---

## **🛠️ Technologies Used**
| Technology  | Purpose |
|-------------|---------|
| **Python (Flask)** | Backend framework for handling routes and logic. |
| **Google Maps API** | Fetching geolocation, route planning, and directions. |
| **Folium** | Rendering interactive maps. |
| **Requests** | Making API calls to Google Maps API. |
| **SMTP (Gmail)** | Sending automated email notifications. |
| **HTML, JavaScript** | Frontend rendering and handling user input. |

---

## **📌 How It Works**
1. **User selects a destination** from the predefined locations or enters a custom address.
2. **Live location (optional)** can be used for more accurate routing.
3. **Google Maps API** fetches the best route and estimated time.
4. **Folium map** displays the route visually.
5. If a **return trip** is requested:
   - A return route is calculated.
   - An **email notification** is sent to the hospital staff.
6. **User sees distance, estimated time, and the map**.

---

## **🚀 How to Run the Project**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/smart-campus-navigation.git
cd smart-campus-navigation
```
### **2️⃣ Install Dependencies**
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```
### **3️⃣ Set Up API Keys & Credentials**
- Get a **Google Maps API key** from [Google Cloud Console](https://console.cloud.google.com/).
- Enable **Geocoding API** and **Directions API**.
- Export the key:
```bash
export API_KEY="your_google_maps_api_key"
```
- Set up **SMTP credentials** for sending emails:
```bash
export EMAIL_ADDRESS="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
```

### **4️⃣ Run the Application**
```bash
python app.py
```
The application will be available at **http://127.0.0.1:5000/**.

---

## **📂 Project Structure**
```
📦 smart-campus-navigation
 ┣ 📂 templates
 ┃ ┣ 📜 index.html  # Main UI
 ┃ ┣ 📜 map.html    # Interactive Map View
 ┣ 📜 app.py        # Flask backend
 ┣ 📜 requirements.txt  # Required dependencies
 ┣ 📜 README.md     # Project documentation
 ┗ 📜 .gitignore    # Ignore unnecessary files
```

---

## **🔔 Future Enhancements**
- **Real-time traffic updates** for more accurate ETAs.
- **Emergency vehicle tracking** for hospital response coordination.
- **Voice-guided navigation** for accessibility.
- **Mobile app integration** using Flutter.

