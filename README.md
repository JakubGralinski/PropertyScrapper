# 🌟✨ Deep Seek Crawler & Warsaw Housing Data Analysis 🚀🏙️

Welcome to **Property Scrapper** – your one-stop solution for **scraping** and **analyzing** housing/property data in Warsaw! This project combines advanced web crawling techniques with state-of-the-art data processing and machine learning to uncover trends in the housing market. 💡📊

---

## 📂 Project Structure

.
├── scrapper.ipynb              # Notebook for web scraping with Selenium & async crawling 🤖🌐
├── properties.ipynb            # Notebook for data processing, ML modeling, & visualization 📈🎨
├── config.py                   # Configuration constants (URLs, CSS selectors, etc.) ⚙️
├── models
│   └── property.py             # Pydantic data model for a Property 🏠🔍
├── utils
│   ├── data_utils.py           # Utility functions for processing & saving data 💾🛠️
│   └── scraper_utils.py        # Helper functions for web scraping (driver init, scrolling, etc.) 🔧
├── requirements.txt            # Python package dependencies 📦
├── .env                        # Environment variables (e.g., GROQ_API_KEY) 🔑
├── .gitignore                  # Files & folders to ignore (e.g., .env, CSV outputs) 🚫
└── README.md                   # This awesome README! 📖🎉

---

## 🚀 Installation

### 🔧 Prerequisites

- **Python 3.12** (or a compatible version) 🐍
- **Conda** (highly recommended for environment management) 🌱

### 📥 Setup Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/deep-seek-crawler.git
   cd deep-seek-crawler

	2.	Create and Activate a Conda Environment:

conda create -n deep-seek-crawler python=3.12 -y
conda activate deep-seek-crawler


	3.	Install Dependencies:

pip install -r requirements.txt


	4.	Configure Environment Variables:
Create a .env file in the project root with content like:

GROQ_API_KEY=your_groq_api_key_here

(Your API key is kept secret – 🔒 no worries!)

🛠️ Usage

1. Web Scraping (scrapper.ipynb) 🤖🌐

The web scraper leverages Selenium and BeautifulSoup to:
	•	Navigate to the Otodom.pl listings page for Warsaw 🏙️
	•	Dismiss cookie banners 🍪 and scroll to load lazy content ⏳
	•	Extract property details (title, price, location, URL) using CSS selectors 🎯
	•	Save the extracted data into a CSV file (e.g., listings.csv) 💾

To Run the Scraper:
	•	Open scrapper.ipynb in Jupyter Notebook or JupyterLab.
	•	Run all cells (or execute the scrape_otodom() function).
	•	Check your CSV file for the scraped listings! 🎉

2. Housing Data Analysis & Modeling (properties.ipynb) 📈🎨

This notebook handles:
	•	Data Loading & Cleaning:
Loads housing_warsaw_with_coordinates.csv, cleans price fields (removing symbols, commas, etc.), converts data types, and extracts valid district information. 🧹✨
	•	Exploratory Data Analysis:
Creates histograms, scatter plots, correlation matrices, and even maps using GeoPandas/Contextily (static) and Folium (interactive)! 📊🗺️
	•	Preprocessing Pipeline:
Combines:
	•	A numeric pipeline (missing value imputation, optional feature creation via CombinedAttributesAdder, and scaling) 🔢
	•	A categorical pipeline (missing value imputation and one-hot encoding for District) 🎨
All merged using a ColumnTransformer to create a final feature array.
	•	Model Training & Evaluation:
Trains several models (Linear Regression, Decision Tree, Random Forest, XGBoost) with hyperparameter tuning (using GridSearchCV) and cross-validation (using RMSE as the metric) to predict Price per m². 🔍🤖

To Run the Analysis & Modeling:
	•	Open properties.ipynb in Jupyter Notebook or JupyterLab.
	•	Run cells sequentially to:
	•	Load and preprocess the data.
	•	Train and evaluate different models.
	•	Visualize your results with vibrant maps and charts!

⚙️ Configuration
	•	config.py:
Contains key settings such as:
	•	BASE_URL – The starting URL for property listings 🌐
	•	LISTINGS_CONTAINER_CLASS & LISTING_CLASS – CSS selectors for identifying listings on the page 🏷️
	•	OUTPUT_FILE – The filename for saving scraped data 💾
	•	Scraper Utilities:
Functions in utils/scraper_utils.py handle:
	•	Driver Initialization (with stealth options to bypass bot detection) 🚀
	•	Cookie Banner Dismissal 🍪
	•	Scrolling & Extraction of listings 🔍

🔍 Advanced Topics
	•	Hyperparameter Tuning:
Use GridSearchCV to fine-tune models like Random Forest and XGBoost. Finer grids and possible target transformations (e.g., log transformation) help reduce error variance. 📈🔬
	•	Mapping & Visualization:
Create:
	•	Static Maps: Using GeoPandas and Contextily for publication-quality visualizations. 🖼️
	•	Interactive Maps: Using Folium and branca.colormap for dynamic exploration of housing data. 🌟


## 📚 Libraries Used

- **Selenium** & **BeautifulSoup** 🤖  
  *Purpose:* Used for web scraping—Selenium drives a real browser to handle dynamic content and JavaScript, while BeautifulSoup parses the HTML to extract data.

- **Crawl4AI** 🚀  
  *Purpose:* Enables asynchronous web crawling to efficiently fetch and process multiple pages concurrently.

- **GeoPandas** & **Contextily** 🗺️  
  *Purpose:* GeoPandas makes it easy to work with geospatial data in Python, and Contextily is used to add basemaps (e.g., real-world maps) to static visualizations.

- **Folium** & **branca** 🌐  
  *Purpose:* Folium creates interactive maps for visualizing geospatial data in a web-friendly format, and branca provides color mapping for these visualizations.

- **scikit-learn** 📈  
  *Purpose:* Provides tools for data preprocessing (e.g., imputation, scaling, encoding), model building (Linear Regression, Decision Trees, Random Forests), and evaluation (cross-validation, GridSearchCV).

- **XGBoost** 🔥  
  *Purpose:* Implements gradient boosting algorithms for building powerful predictive models, often outperforming traditional ensemble methods on tabular data.

- **Pydantic** 💻  
  *Purpose:* Used for defining data models with validation (e.g., the Property model) to ensure consistency in the extracted data.

- **requests** 🌐  
  *Purpose:* Facilitates making HTTP requests to fetch web pages when not using a browser-based approach.

- **asyncio** ⏱️  
  *Purpose:* Powers asynchronous programming, allowing for concurrent web crawling and processing of multiple pages.

- **python-dotenv** 🔑  
  *Purpose:* Loads environment variables from a `.env` file (e.g., API keys) to keep sensitive information secure.

- **webdriver_manager** 🚗  
  *Purpose:* Automatically manages the installation and setup of web drivers for Selenium, simplifying browser automation setup.
