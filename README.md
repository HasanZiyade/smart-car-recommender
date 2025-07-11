# 🚗 Smart Used Car Recommender

A web application that provides personalized used car recommendations based on subjective criteria typically not available on regular car listing websites.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🌟 Features

- **Intelligent Questionnaire**: Comprehensive form analyzing user preferences and needs
- **Smart Recommendations**: Heuristic-based scoring algorithm that feels AI-powered
- **Real-life Criteria**: Considers reliability, insurance costs, maintenance costs, and user suitability
- **Interactive Interface**: Clean, modern Streamlit web interface
- **Educational Focus**: Perfect for class demonstrations and learning

## 🎯 How It Works

The recommendation engine uses a sophisticated scoring system:
- **Budget Fit (30%)**: How well the car price matches your budget
- **Priority Factor (40%)**: Alignment with your most important criterion
- **User Type Suitability (30%)**: How well the car matches your driver profile

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/smart-car-recommender.git
   cd smart-car-recommender
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

4. Open your browser to `http://localhost:8501`

## 📊 Dataset

The application includes a comprehensive dataset of 100+ vehicles with:
- **Diverse Brands**: Toyota, Honda, BMW, Tesla, Ford, Chevrolet, and more
- **Multiple Categories**: Sedans, SUVs, Trucks, Hatchbacks, Coupes, Wagons
- **Fuel Types**: Petrol, Hybrid, Electric
- **Price Range**: $4,000 to $50,000
- **Various Years**: 2004-2019 models

### Dataset Columns
- `brand`: Car manufacturer
- `model`: Car model name
- `year`: Manufacturing year
- `price`: Price in USD
- `fuel`: Fuel type (Petrol/Hybrid/Electric)
- `type`: Vehicle type
- `reliability`: Reliability rating (High/Medium/Low)
- `insurance_cost`: Insurance cost category (Low/Medium/High)
- `maintenance_cost`: Maintenance cost category (Low/Medium/High)
- `suitable_driver_type`: Target user types

## 🎓 Educational Use

This project is designed for educational demonstrations, showcasing:
- Data-driven decision making
- User preference analysis
- Recommendation algorithms
- Web application development
- Deployment strategies

## 🌐 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy with one click

### Other Platforms
The app is ready for deployment on:
- Render
- Heroku
- Railway
- Any platform supporting Python web apps

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud ready

## 📁 Project Structure

```
smart-car-recommender/
├── main.py                 # Main Streamlit application
├── cars_dataset.csv        # Car dataset
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── .streamlit/           # Streamlit configuration
│   └── config.toml
└── render_config.txt     # Deployment instructions
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:
- Add more cars to the dataset
- Improve the recommendation algorithm
- Enhance the user interface
- Add new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Demo

Try the live demo: [Smart Car Recommender](https://your-app-url.streamlit.app)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for educational purposes**
