# Healthcare Dashboard - Streamlit Demo

A comprehensive healthcare institutional dashboard built with Streamlit, featuring financial performance, operational metrics, and quality indicators for NCH Healthcare System, Inc.

## Features

- **Executive KPI Dashboard**: Safety grade, operating margin, cash on hand, and payor dependency
- **Financial Performance**: Historical financial trends with interactive charts
- **Payor Mix Analysis**: Visual breakdown of revenue sources
- **Operational Metrics**: Admissions, patient days, and emergency visits trends
- **Quality & Safety**: Performance comparison against national averages
- **Governance Information**: Executive compensation and board metrics

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd /Users/dev/Downloads/projects/streamlit_demo
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open in your default browser
   - If it doesn't, navigate to `http://localhost:8501`

3. **Stop the application:**
   - Press `Ctrl+C` in the terminal to stop the server

## Project Structure

```
streamlit_demo/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive data visualization

## Data Source

The dashboard displays sample healthcare data for NCH Healthcare System, Inc., including:
- Financial performance metrics (2020-2024)
- Payor mix distribution (FY 2024)
- Operational utilization trends (2023-2024)
- Quality and safety performance indicators
- Governance and leadership information (FY 2022)

## Customization

To modify the dashboard:
1. Edit the `data` dictionary in `app.py` to update the healthcare metrics
2. Modify the chart configurations in the Plotly sections
3. Adjust the layout by changing the column configurations

## Troubleshooting

- **Port already in use**: If port 8501 is busy, Streamlit will automatically use the next available port
- **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Browser doesn't open**: Manually navigate to the URL shown in the terminal output
