# AI-Enhanced Car Recommender Setup Guide

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements_ai.txt
```

### 2. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with sk-...)

### 3. Set API Key (Choose one method)

**Method A: Environment Variable (Recommended)**
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Mac/Linux
export OPENAI_API_KEY=your_api_key_here
```

**Method B: Enter in App**
- Run the app and enter the key in the sidebar

### 4. Run the AI-Enhanced App
```bash
streamlit run main_ai_enhanced.py
```

## 🤖 How the AI Integration Works

### 1. **Conversational Understanding**
- Users chat naturally about their car needs
- AI extracts subjective preferences and concerns
- No rigid forms - just natural conversation

### 2. **Intelligent Analysis**
- AI analyzes conversation for hidden insights
- Determines user personality and priorities
- Considers emotional and lifestyle factors

### 3. **Enhanced Scoring**
- Combines rule-based scoring with AI judgment
- AI weighs subjective factors (brand perception, lifestyle fit)
- Provides personalized explanations for each recommendation

### 4. **Subjective Insights**
- "This car feels right for your practical family lifestyle"
- "The brand reputation aligns with your reliability concerns"
- "Perfect for weekend adventures but practical for daily use"

## 💡 Benefits Over Traditional Systems

1. **Subjective Understanding**: Understands "feel" and lifestyle fit
2. **Discovery**: Helps users discover what they actually want
3. **Personality Matching**: Matches cars to user personality types
4. **Contextual Reasoning**: Considers real-world scenarios
5. **Natural Interaction**: No complex forms or technical jargon

## 🔧 Customization Options

### Modify AI Behavior
Edit `chatgpt_integration.py` to:
- Change conversation style
- Adjust scoring weights
- Add new subjective factors
- Customize personality analysis

### Add More Data
Enhance `cars_dataset.csv` with:
- Brand personality attributes
- Lifestyle suitability scores
- Emotional appeal ratings
- Community reviews/sentiments

## 📊 Cost Considerations

- GPT-4 API costs ~$0.03 per 1K tokens
- Typical conversation: 2,000-5,000 tokens
- Cost per user: $0.06-$0.15
- For high traffic, consider GPT-3.5-turbo (cheaper)

## 🚀 Next Steps

1. Test the AI chat functionality
2. Gather user feedback on subjective insights
3. Refine conversation prompts
4. Add more sophisticated scoring factors
5. Consider voice integration for even more natural interaction
