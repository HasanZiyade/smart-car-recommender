import streamlit as st
import pandas as pd
import numpy as np
import os
from chatgpt_integration import CarRecommenderAI, get_ai_recommendations, CarConsultantAI

# Page configuration
st.set_page_config(
    page_title="Smart Used Car Marketplace",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the dataset
@st.cache_data
def load_data():
    """Load the car dataset"""
    try:
        df = pd.read_csv('cars_dataset.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset file 'cars_dataset.csv' not found. Please make sure it's in the same directory as this script.")
        return None

def setup_ai_assistant():
    """Create a fresh AI assistant for each search - no memory retention"""
    # Check for API key in environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        # Always create a fresh instance - no session state caching
        return CarRecommenderAI(api_key)
    else:
        return None

def show_questionnaire():
    """Display the questionnaire form"""
    st.title("🚗 Smart Used Car Marketplace")
    st.markdown("""
    ### Find your perfect used car from real marketplace listings
    Our AI analyzes hundreds of used car listings and matches them to your specific needs and preferences.
    """)
    
    with st.form("car_questionnaire"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 About You")
            age = st.selectbox(
                "What's your age range?",
                ["18-25", "26-35", "36-45", "46-55", "55+"]
            )
            
            family_size = st.selectbox(
                "How many people will regularly use this car?",
                ["Just me", "2 people", "3-4 people", "5+ people"]
            )
            
            experience = st.selectbox(
                "How would you describe your driving experience?",
                ["New driver", "Some experience", "Experienced", "Very experienced"]
            )
            
            location = st.selectbox(
                "Where do you primarily drive?",
                ["City/Urban", "Suburban", "Rural", "Mixed environments"]
            )
        
        with col2:
            st.subheader("🚙 Car Preferences")
            budget = st.slider(
                "What's your maximum budget?",
                min_value=5000,
                max_value=50000,
                value=20000,
                step=1000,
                format="$%d"
            )
            
            mileage_preference = st.selectbox(
                "What's your maximum acceptable mileage?",
                ["Under 50k miles", "Under 75k miles", "Under 100k miles", 
                 "Under 125k miles", "Under 150k miles", "No preference"]
            )
            
            usage = st.selectbox(
                "What will be your primary use for this car?",
                ["Daily commuting to work", "Daily commuting to school", 
                 "Family transportation", "Weekend trips", "Occasional use"]
            )
            
            fuel_preference = st.selectbox(
                "Do you have a fuel type preference?",
                ["No preference", "Fuel efficiency is important", 
                 "Interested in hybrid/electric", "Performance over efficiency"]
            )
            
            size_preference = st.selectbox(
                "What size vehicle do you prefer?",
                ["Compact/Small", "Mid-size", "Large", "No preference"]
            )
            
            color_preference = st.selectbox(
                "Do you have a color preference?",
                ["No preference", "White", "Black", "Silver", "Gray", "Red", "Blue", "Green", "Yellow", "Orange"]
            )
        
        st.subheader("⭐ Priorities")
        col3, col4 = st.columns(2)
        
        with col3:
            reliability = st.selectbox(
                "How important is reliability to you?",
                ["Somewhat important", "Important", "Very important", "Extremely important"]
            )
            
            performance = st.selectbox(
                "How important is performance/fun driving?",
                ["Not important", "Somewhat important", "Important", "Very important"]
            )
            
            brand = st.selectbox(
                "Do you have brand preferences?",
                ["No preference", "Japanese brands (Toyota, Honda, etc.)", 
                 "American brands (Ford, Chevrolet, etc.)", "European brands (BMW, Audi, etc.)",
                 "Performance and luxury brands", "Budget-friendly brands"]
            )
        
        with col4:
            budget_priorities = st.multiselect(
                "What's most important for your budget? (Select all that apply)",
                ["The cheapest option possible", "Low insurance costs", 
                 "Low maintenance costs", "Good resale value", "Low fuel costs"]
            )
            
            important_features = st.multiselect(
                "Which features are most important to you? (Select all that apply)",
                ["Safety features", "Technology/Infotainment", "Fuel efficiency", 
                 "Cargo space", "Comfort", "Style/Appearance", "Low mileage", "Reliability record"]
            )
        
        # Submit button
        submitted = st.form_submit_button("🔍 Find My Perfect Used Car", type="primary")
        
        if submitted:
            # Store responses in session state
            st.session_state.questionnaire_responses = {
                'age': age,
                'family_size': family_size,
                'experience': experience,
                'location': location,
                'budget': budget,
                'mileage_preference': mileage_preference,
                'usage': usage,
                'fuel_preference': fuel_preference,
                'size_preference': size_preference,
                'color_preference': color_preference,
                'reliability': reliability,
                'budget_priorities': budget_priorities,
                'performance': performance,
                'brand': brand,
                'important_features': important_features
            }
            st.session_state.show_results = True
            st.rerun()

def show_results(df, responses, ai_assistant=None):
    """Display the unified AI-powered recommendation results"""
    
    st.title("🎯 Your Personalized Used Car Matches")
    
    # Show user profile summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Age:** {responses['age']}")
    with col2:
        st.info(f"**Family Size:** {responses['family_size']}")
    with col3:
        st.info(f"**Budget:** ${responses['budget']:,}")
    
    if not ai_assistant:
        st.error("🤖 AI Assistant not available. Please configure your OpenAI API key.")
        return
    
    # Get AI-powered recommendations (single unified system)
    with st.spinner("🤖 AI is analyzing all cars and creating your personalized recommendations..."):
        try:
            recommendations, ai_summary = get_ai_recommendations(df, responses, ai_assistant)
            
            if len(recommendations) == 0:
                st.warning("No cars found matching your criteria. Try adjusting your budget or preferences.")
                if st.button("🔄 Retake Questionnaire"):
                    st.session_state.show_results = False
                    st.rerun()
                return
            
            st.success(f"✨ AI analyzed {len(df)} used car listings and found {len(recommendations)} perfect matches for you!")
            
            # Show AI personal analysis summary
            st.markdown("### 🧠 AI Personal Analysis")
            st.info(ai_summary)
            
            # Show TOP PICKS (first 3)
            st.markdown("### 🌟 AI Top Picks")
            st.markdown("*These are your absolute best matches from the used car marketplace*")
            
            for idx, (_, car) in enumerate(recommendations.head(3).iterrows()):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        **#{idx+1}: {car['year']} {car['brand']} {car['model']} ({car['color']})**
                        - **Price:** ${car['price']:,} | **Mileage:** {car.get('mileage', 'N/A'):,} miles
                        - **Type:** {car['type']} ({car['fuel']})
                        - **MPG:** {car['mpg_city']} city / {car['mpg_highway']} highway
                        - **Safety:** {car['safety_rating']}/5 stars | **Reliability:** {car['reliability']}
                        - **Insurance:** {car['insurance_cost']} | **Maintenance:** {car['maintenance_cost']}
                        """)
                        
                        # Show AI explanation
                        explanation = car.get('ai_explanation', 'Great match for your needs')
                        st.markdown(f"**🤖 AI Analysis:** {explanation}")
                        
                        # Add marketplace action buttons
                        button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
                        with button_col1:
                            if st.button(f"📋 Carfax Report", key=f"carfax_{idx}", help="View detailed vehicle history"):
                                st.info("🚗 Carfax report would open here (Prototype)")
                        with button_col2:
                            if st.button(f"🔧 Book Inspection", key=f"inspect_{idx}", help="Schedule mechanic inspection"):
                                st.info("📅 Inspection booking would open here (Prototype)")
                    
                    with col2:
                        score = car.get('ai_score', 0)
                        pricing_score = car.get('pricing_score', 0)
                        
                        # Display match score
                        if score >= 85:
                            st.success(f"🤖 Match Score\n{score:.0f}/100\n⭐ Excellent")
                        elif score >= 75:
                            st.info(f"🤖 Match Score\n{score:.0f}/100\n👍 Very Good")
                        else:
                            st.warning(f"🤖 Match Score\n{score:.0f}/100\n🤔 Good")
                        
                        # Display pricing score
                        if pricing_score >= 85:
                            st.success(f"💰 Pricing Score\n{pricing_score:.0f}/100\n🔥 Great Deal")
                        elif pricing_score >= 75:
                            st.info(f"💰 Pricing Score\n{pricing_score:.0f}/100\n👌 Fair Price")
                        else:
                            st.warning(f"💰 Pricing Score\n{pricing_score:.0f}/100\n💸 Above Market")
                    
                    st.markdown("---")
            
            # Show OTHER RELEVANT OPTIONS (remaining cars)
            if len(recommendations) > 3:
                st.markdown("### 🎯 Other Great Marketplace Finds")
                st.markdown("*Additional used car listings that scored well and might interest you*")
                
                # Show remaining cars in a more compact format
                other_options = recommendations.iloc[3:]
                
                for idx, (_, car) in enumerate(other_options.iterrows(), 4):
                    with st.expander(f"#{idx}: {car['year']} {car['brand']} {car['model']} - Match: {car.get('ai_score', 0):.0f}/100 | Pricing: {car.get('pricing_score', 0):.0f}/100"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"""
                            **{car['year']} {car['brand']} {car['model']} ({car['color']})**
                            - **Price:** ${car['price']:,} | **Mileage:** {car.get('mileage', 'N/A'):,} miles
                            - **Type:** {car['type']} ({car['fuel']}) | **MPG:** {car['mpg_city']}/{car['mpg_highway']}
                            - **Safety:** {car['safety_rating']}/5 stars | **Reliability:** {car['reliability']}
                            - **Insurance:** {car['insurance_cost']} | **Maintenance:** {car['maintenance_cost']}
                            
                            **🤖 AI Analysis:** {car.get('ai_explanation', 'Good alternative option')}
                            """)
                            
                            # Add marketplace buttons for other options
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button(f"📋 Carfax Report", key=f"carfax_other_{idx}"):
                                    st.info("🚗 Carfax report would open here (Prototype)")
                            with btn_col2:
                                if st.button(f"🔧 Book Inspection", key=f"inspect_other_{idx}"):
                                    st.info("📅 Inspection booking would open here (Prototype)")
                        
                        with col2:
                            score = car.get('ai_score', 0)
                            pricing_score = car.get('pricing_score', 0)
                            
                            if score >= 75:
                                st.info(f"Match: {score:.0f}/100")
                            else:
                                st.warning(f"Match: {score:.0f}/100")
                            
                            if pricing_score >= 75:
                                st.info(f"Pricing: {pricing_score:.0f}/100")
                            else:
                                st.warning(f"Pricing: {pricing_score:.0f}/100")
            
            # Show insights
            st.markdown("---")
            st.subheader("📊 Your Recommendation Insights")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                avg_price = recommendations['price'].mean()
                st.metric("Average Price", f"${avg_price:,.0f}")
            
            with col2:
                avg_mileage = recommendations['mileage'].mean()
                st.metric("Average Mileage", f"{avg_mileage:,.0f}")
            
            with col3:
                avg_mpg = ((recommendations['mpg_city'] + recommendations['mpg_highway']) / 2).mean()
                st.metric("Average MPG", f"{avg_mpg:.1f}")
            
            with col4:
                avg_score = recommendations.get('ai_score', pd.Series([0])).mean()
                st.metric("Avg Match Score", f"{avg_score:.0f}/100")
            
            with col5:
                avg_pricing = recommendations.get('pricing_score', pd.Series([0])).mean()
                st.metric("Avg Pricing Score", f"{avg_pricing:.0f}/100")
            
        except Exception as e:
            error_msg = "AI analysis failed: " + str(e).replace('{', '{{').replace('}', '}}')
            st.error(error_msg)
            st.info("Please check your API configuration or try again.")
    
    # Add the AI Car Consultant chat interface
    show_car_consultant()
    
    # Option to retake questionnaire
    if st.button("🔄 Start Over with New Preferences"):
        st.session_state.show_results = False
        st.rerun()

def show_car_consultant():
    """Display the AI car consultant chat interface"""
    
    st.markdown("---")
    st.markdown("### 🤖 AI Car Consultant")
    st.markdown("*Have questions about cars, insurance, financing, or maintenance? Ask our AI consultant!*")
    
    # Add clear chat button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_consultant_chat"):
            st.session_state.consultant_messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! 👋 I'm your AI car consultant. I can help you with questions about car buying, insurance, financing, maintenance, and more. What would you like to know?"
                }
            ]
            st.rerun()
    
    # Setup consultant AI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("⚠️ AI Consultant requires OpenAI API key to function.")
        return
    
    consultant = CarConsultantAI(api_key)
    
    # Initialize chat history for consultant
    if "consultant_messages" not in st.session_state:
        st.session_state.consultant_messages = [
            {
                "role": "assistant", 
                "content": "Hello! 👋 I'm your AI car consultant. I can help you with questions about car buying, insurance, financing, maintenance, and more. What would you like to know?"
            }
        ]
    
    # Display chat messages from history
    for message in st.session_state.consultant_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Ask me anything about cars..."):
        # Add user message to chat history
        st.session_state.consultant_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            # Get streaming response from consultant AI
            response_stream = consultant.get_consultant_response(
                prompt, 
                st.session_state.consultant_messages[:-1]  # Exclude the just-added user message
            )
            
            if response_stream:
                # Stream the response
                response = st.write_stream(response_stream)
                
                # Add assistant response to chat history
                st.session_state.consultant_messages.append({"role": "assistant", "content": response})
            else:
                # Fallback response if AI fails
                fallback_response = "I apologize, but I'm having trouble connecting right now. Please try asking your question again, or feel free to contact a human car expert for assistance! 🚗"
                st.markdown(fallback_response)
                st.session_state.consultant_messages.append({"role": "assistant", "content": fallback_response})

def main():
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Setup AI assistant - now required for functionality
    ai_assistant = setup_ai_assistant()
    
    # Show AI status
    if ai_assistant:
        st.sidebar.success("🤖 AI Analysis Ready!")
        st.sidebar.info("✨ Powered by advanced AI that analyzes hundreds of used car listings and matches them to your specific needs and budget.")
    else:
        st.sidebar.error("🤖 AI Assistant Required")
        st.sidebar.warning("This marketplace requires an OpenAI API key to function.")
        st.sidebar.info("Please add OPENAI_API_KEY to your .env file to continue.")
        
        st.title("🚗 Smart Used Car Marketplace")
        st.error("⚠️ AI Assistant Not Configured")
        st.markdown("""
        This marketplace uses advanced AI to match you with the perfect used car from real listings. 
        To use this platform, you need to configure your OpenAI API key.
        
        **Setup Instructions:**
        1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
        2. Create a `.env` file in the app directory
        3. Add: `OPENAI_API_KEY=your_key_here`
        4. Restart the application
        """)
        return
    
    # Show questionnaire or results based on state
    if not hasattr(st.session_state, 'show_results') or not st.session_state.show_results:
        show_questionnaire()
        # Return to continue with questionnaire
    else:
        show_results(df, st.session_state.questionnaire_responses, ai_assistant)

if __name__ == "__main__":
    main()
