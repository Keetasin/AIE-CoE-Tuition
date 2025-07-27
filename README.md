# 241-353 AI ECOSYSTEM MODULE

## Thai University Tuition Fee Dashboard (Computer & AI Engineering)

### Project Overview

This project presents a **Dash web application** designed to visualize tuition fee data of Computer Engineering and Artificial Intelligence Engineering programs offered by Thai universities. The data is collected from [MyTCAS.com](https://course.mytcas.com), then cleaned, processed, and displayed using interactive dashboards. The system aims to assist high school students and parents in comparing tuition costs and exploring academic programs more easily.

---

### Data Extraction & Processing

1. **Scrape course data** (university, faculty, program, type, link and tuition) using [Playwright](https://playwright.dev/) from [MyTCAS.com](https://course.mytcas.com).
2. **Clean and deduplicate** the dataset.
3. **Filter** only programs related to Computer and AI Engineering.
4. **Extract and normalize tuition fee** (convert to per-semester if listed as total).
5. **Categorize** course types and split faculty > major.
6. **Assign regions** (North, Central, South, etc.) based on university names.
7. **Geocode** university names to retrieve latitude and longitude for mapping.

Final data is exported to `data/university_fee_with_latlon.xlsx` for visualization.

---

### Dashboard Pages

1. **Overview**
   - Displays an overall summary of tuition fees across various programs.
   - Users can filter by program type, keyword, or region.
   - Interactive visualizations include a histogram of tuition fee distribution and a boxplot grouped by program type.
   - Summary cards show key statistics such as mean, max, min, median tuition fees, and total number of programs.

2. **Map**
   - Users can select one or multiple universities from a dropdown menu to filter the map and view only the selected universities.
   - An interactive map visualizing the locations of universities.
   - Each point shows tuition-related details and available programs at that university.
   - Colored and sized based on average tuition and number of programs.

3. **Search**
   - Search for programs using filters such as keyword, university, faculty, department, program type, region, and tuition fee range.
   - Display the results in a table where users can select programs of interest and sort by tuition fees (ascending or descending).
   - Users can select and rank their top 10 courses of interest.
   - A button is provided to export the selected top 10 courses to an Excel file.

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
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
      ```bash
      venv\Scripts\activate
      ```
   - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

### Running and Viewing the Application

Ensure you're inside the project directory and the virtual environment is activated.
1. Run the application:
   ```bash
   python .\main.py
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:8050/
   ```