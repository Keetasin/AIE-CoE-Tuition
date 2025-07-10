# 241-353 AI ECOSYSTEM MODULE

## 🎓 Thai University Tuition Fee Dashboard (Computer & AI Engineering)

### 📖 Project Overview

This project presents a **Dash web application** designed to visualize tuition fee data of Computer Engineering and Artificial Intelligence Engineering programs offered by Thai universities. The data is collected from [MyTCAS.com](https://course.mytcas.com), then cleaned, processed, and displayed using interactive dashboards. The system aims to assist high school students and parents in comparing tuition costs and exploring academic programs more easily.

---

### 🛠️ Data Extraction & Processing

The project includes an automated pipeline to:

1. **Scrape course data** (university, faculty, program, type, and tuition) using [Playwright](https://playwright.dev/) from [MyTCAS.com](https://course.mytcas.com).
2. **Clean and deduplicate** the dataset.
3. **Filter** only programs related to Computer and AI Engineering.
4. **Extract and normalize tuition fee** (convert to per-semester if listed as total).
5. **Categorize** course types and split faculty > major.
6. **Assign regions** (North, Central, South, etc.) based on university names.
7. **Geocode** university names to retrieve latitude and longitude for mapping.

Final data is exported to `data/university_fee_with_latlon1.xlsx` for visualization.

---

### 📊 Dashboard Pages

1. **Overview**
   - Summary statistics of tuition fees
   - Histogram and Box Plot visualizations
   - Filters by program type, region, and keywords

2. **Map**
   - Interactive map showing university locations with average tuition
   - Hover to view details of each university and its programs

3. **Search**
   - Advanced search and filtering system
   - Sortable data table showing all programs and tuition details

---


### Setup & Installation

Ensure that you have Python installed on your system before proceeding.

1. Clone the repository:
   ```bash
   git clone <repo-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-folder>
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

### Running and Viewing the Application

1. Ensure you are inside the project directory.
2. Run the application:
   ```bash
   tuition_dashboard.py
   ```
3. Open your browser and go to:
   ```
   http://127.0.0.1:8050/
   ```