# OKF Synthetic Data Generation

## Overview
This project implements a **manually versioned prompt engineering approach** for generating **synthetic data** in the **Open Knowledge Framework (OKF)**, a supply chain resilience framework. Specifically, it supports generating structured data for:

- **OKW (Open Know Where)**: Focused on **location, facility, and tooling data**.
- **OKH (Open Know How)**: Focused on **manufacturing and production instructions**.

The project leverages **LLMs (Large Language Models) via the Groq API** to generate realistic, structured JSON data that adheres to predefined **JSON schemas**. This approach ensures flexibility in generating domain-specific synthetic data across multiple versions.

---

## Features
- **Versioned Prompt Engineering**: Each version has its own prompt and schema files for controlled updates.
- **Dynamic Schema & Prompt Handling**: Automatically loads the correct schema and prompt for each version.
- **Automated Data Generation**: Generates valid JSON outputs for different products and domains.
- **Multiple Domains Supported**: Generates data for various industries, such as **cooking and manufacturing**.
- **Structured Data Output**: Ensures compliance with OKW and OKH standards.

---

## Project Structure
```bash
OKF_SYNTHETIC_DATA_GENERATION/
│── versions/
│   │── latest/
│   │   ├── okw.schema_latest.json
│   │   ├── okh.schema_latest.json
│   │   ├── prompt_latest.txt
│   │── v1/
│   │   ├── okw.schema_v1.json
│   │   ├── okh.schema_v1.json
│   │   ├── prompt_v1.txt
│   │── v2/
│   │   ├── okw.schema_v2.json
│   │   ├── okh.schema_v2.json
│   │   ├── prompt_v2.txt
│   │── v3/
│   │   ├── okw.schema_v3.json
│   │   ├── okh.schema_v3.json
│   │   ├── prompt_v3.txt
│── main.py
│── requirements.txt
│── VERSIONS.md
│── README.md
```


## Installation & Setup
1. Clone the Repository
```bash
git clone https://github.com/your-repo/OKF_SYNTHETIC_DATA_GENERATION.git
cd OKF_SYNTHETIC_DATA_GENERATION
```
2. Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```
### OR
source venv/bin/activate  # On Mac/Linux
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Set Up Groq API Key
You need a Groq API Key to generate synthetic data. Export it as an environment variable:

```bash
set GROQ_API_KEY=your_api_key  # Windows
```
### OR
export GROQ_API_KEY=your_api_key  # Mac/Linux
Running the Project
Generate Data for a Specific Version
To generate data for a specific version (e.g., v2):

```bash
python main.py --version v2 --api_key "your_api_key"
This will:

Load schemas and prompt from versions/v2/.
Generate structured data.
Save it as generated_data_v2.json inside the v2 folder.

### OR 
Run without specifying a version to run the latest version

Generate Data for Custom Products and Domains
You can generate data for specific products in different domains.

Example 1: Cooking Domain (Oatmeal Cookie, Pancake, Chocolate Cake)
```bash
python main.py --version lastest --domain "cooking" --scenario "A chaotic environment where a baker wants to bake something" --products "Oatmeal Cookie" "Pancake" "Chocolate Cake" --api_key "your_api_key"
```
Example 2: Manufacturing Domain (Custom Engine, Industrial Drill, Robotic Arm)
```bash
python main.py --version latest --domain "manufacturing" --scenario "An automated factory producing high-precision equipment" --products "Custom Engine" "Industrial Drill" "Robotic Arm" --api_key "your_api_key"
```
This will:

Use manufacturing domain context.
Generate data for three specific products.
Store output in versions/latest/generated_data_latest.json

## Versioning Strategy
Each version folder (v1, v2, v3, latest) contains:

Prompt Variations: Refined for better data quality.
Schema Updates: Improved structuring of generated JSON.
Generated Data: Stored for reproducibility.
Refer to VERSIONS.md for detailed change history.
