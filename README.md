###### if you're a absolute beginner to vscode and building projects in it, go through the below video
link:


# 📊 PhonePe Pulse Data Visualization & Exploration Dashboard

## 📌 Project Overview

This project involves the extraction, transformation, and visualization of PhonePe Pulse data to analyze transaction dynamics, insurance growth, user engagement, and device dominance across Indian states and districts. The dashboard provides interactive insights using **Streamlit**, **Plotly**, and **MySQL**.

## 🎯 Problem Statement

PhonePe, a leading digital payments platform, aims to derive actionable insights from user and transaction data across India to:

- Understand regional trends in digital payments.
- Explore user behavior segmented by device brands and app opens.
- Analyze insurance transaction growth and penetration.
- Identify top-performing states, districts, and pincodes.

---

## 🏗️ Project Structure

phonepe_data_dashboard/
│
├── data/ # Contains extracted structured JSON data from PhonePe Pulse GitHub
│ ├── aggregated/
│ ├── map/
│ └── top/
│
├── scripts/
│ └── extract_and_load.py # Parses JSON and inserts cleaned data into MySQL
│
├── streamlit_app/
│ └── dashboard.py # Streamlit dashboard app using Plotly visualizations
│
├── .env # Contains environment variables for DB connection
├── requirements.txt # Project dependencies
└── README.md # Project documentation (this file)




---

## 🔧 Technologies Used

| Component         | Description                                   |
|-------------------|-----------------------------------------------|
| **Python**        | Core language for scripting and backend logic |
| **Streamlit**     | Web app framework to build interactive dashboards |
| **MySQL**         | Relational database to store cleaned data     |
| **Plotly**        | Interactive charting and graphing             |
| **pandas**        | Data analysis and manipulation                |
| **JSON**          | Source format for raw data                    |

---

#                                        Functional Workflow                                           #

### 1. Data Extraction
- Extracted structured JSON data from the PhonePe Pulse dataset folders (`aggregated`, `map`, `top`).
- Parsed using Python and normalized into structured pandas DataFrames.

### 2. Data Transformation
- Cleaned and renamed columns to match consistent formats across datasets.
- Prepared multiple tables: 
  - `aggregated_transaction`, `aggregated_user`
  - `map_transaction`, `map_user`, `map_insurance`
  - `top_transaction`, `top_user`, `top_insurance`
  - `aggregated_insurance`

### 3. Data Loading
- Used MySQL Connector to insert structured data into MySQL tables via `extract_and_load.py`.
- Connected securely using credentials stored in `.env`.

### 4. Data Visualization
- Built a dynamic and interactive Streamlit dashboard.
- Used Plotly to build bar charts, line graphs, and geo-based visualizations.

---

##                                           📈 Key Dashboard Features                                  #

Each module visualizes critical business insights:

1. **Transaction Dynamics**  
   → View growth/decline across states, categories, quarters.

2. **Device Dominance**  
   → Analyze user preferences across different device brands.

3. **Insurance Growth**  
   → Track state-wise adoption of PhonePe’s insurance offerings.

4. **Market Expansion**  
   → Identify regions with the highest transaction volumes.

5. **User Engagement**  
   → See which regions show high app opens vs registrations.

6. **Top Performing Locations**  
   → Districts and pincodes leading in users/transactions.

7. **Insurance Engagement**  
   → District-wise visualization of insurance counts.

8. **User Registration Trends**  
   → Spot state/district/pincode trends for user signups.

9. **Insurance Transaction Insights**  
   → See where most insurance payments occur.

---

## 🧪 How to Run the Project

### Step 1: Clone the Repo & Set Up Virtual Environment

```bash
git clone <repo-url>
cd phonepe_data_dashboard
python -m venv venv
venv\Scripts\activate  # for Windows



Step 2: Install Dependencies------>pip install -r requirements.txt

Step 3: Set Up Environment Variables
        Create a .env file in the root directory:
                                                DB_HOST=localhost
                                                DB_USER=root
                                                DB_PASSWORD=P@rimi18
                                                DB_NAME=phonepe_pulse

Step 4: Load Data to MySQL---->cd scripts
                               python extract_and_load.py

Step 5: Run the Streamlit Dashboard--->
                                       cd ../streamlit_app
                                       streamlit run dashboard.py


📬 Contact
For suggestions or queries:
📧 parimibharathkumar@gmail.com
📍 India



