# 🚗 Smart Used Car Marketplace

An AI-powered web application that provides personalized used car recommendations from real marketplace listings using advanced AI analysis.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🌟 Features

- **AI-Powered Analysis**: Uses GPT-4o-mini to analyze 441 real used car listings
- **Dual Scoring System**: Match Score + Pricing Score for comprehensive evaluation
- **AI Car Consultant**: Built-in chatbot for car buying advice
- **Performance Optimized**: Batch processing for 90% speed improvement
- **Comprehensive Dataset**: Real marketplace data with mileage, pricing, and specifications
- **Modern Interface**: Clean, responsive Streamlit web interface

## 🤖 AI Capabilities

The marketplace uses advanced AI to:
- **Analyze User Preferences**: Understands complex requirements and priorities
- **Score All Cars**: No filtering - pure AI decision making
- **Provide Explanations**: Clear reasoning for each recommendation
- **Offer Consultation**: Expert advice on buying, financing, and maintenance

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- OpenAI API key

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/HasanZiyade/smart-car-recommender.git
   cd smart-car-recommender
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

5. Open your browser to `http://localhost:8501`

### Streamlit Cloud Deployment

1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `OPENAI_API_KEY` in the app secrets
4. Deploy with `streamlit_app.py` as entry point

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
