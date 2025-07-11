import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Smart Car Recommender",
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

def analyze_questionnaire_responses(responses):
    """
    Analyze questionnaire responses to determine user profile and priorities
    """
    # Determine user type based on responses
    user_type = "Commuter"  # Default
    
    if responses['age'] == "18-25" and responses['usage'] in ["Daily commuting to school", "Weekend trips"]:
        user_type = "Student"
    elif responses['family_size'] in ["3-4 people", "5+ people"]:
        user_type = "Family"
    elif responses['usage'] == "Daily commuting to work":
        user_type = "Commuter"
    elif responses['performance'] == "Very important" or responses['brand'] == "Performance and luxury brands":
        user_type = "Enthusiast"
    elif responses['budget_priority'] == "The cheapest option possible":
        user_type = "Budget"
    
    # Determine priority based on responses
    priority = "Reliability"  # Default
    
    if responses['budget_priority'] == "Low insurance costs":
        priority = "Low Insurance Cost"
    elif responses['budget_priority'] == "Low maintenance costs":
        priority = "Low Maintenance Cost"
    elif responses['reliability'] == "Extremely important":
        priority = "Reliability"
    
    return user_type, priority

def calculate_recommendation_score(car, budget, priority, user_type):
    """
    Calculate a recommendation score for a car based on user preferences.
    This uses heuristic-based logic to simulate intelligent recommendations.
    """
    score = 0
    max_score = 100
    
    # Budget fit (30% of total score)
    price = car['price']
    if price <= budget * 0.8:  # Well within budget
        score += 30
    elif price <= budget:  # Within budget
        score += 20
    elif price <= budget * 1.1:  # Slightly over budget
        score += 10
    else:  # Over budget
        score += 0
    
    # Priority factor (40% of total score)
    if priority == "Reliability":
        if car['reliability'] == 'High':
            score += 40
        elif car['reliability'] == 'Medium':
            score += 25
        else:
            score += 10
    
    elif priority == "Low Insurance Cost":
        if car['insurance_cost'] == 'Low':
            score += 40
        elif car['insurance_cost'] == 'Medium':
            score += 25
        else:
            score += 10
    
    elif priority == "Low Maintenance Cost":
        if car['maintenance_cost'] == 'Low':
            score += 40
        elif car['maintenance_cost'] == 'Medium':
            score += 25
        else:
            score += 10
    
    # User type suitability (30% of total score)
    suitable_types = car['suitable_driver_type'].split(';')
    if user_type in suitable_types:
        score += 30
    elif any(user_type.lower() in stype.lower() for stype in suitable_types):
        score += 20
    else:
        score += 5
    
    return min(score, max_score)

def get_recommendations(df, budget, priority, user_type, max_results=10):
    """Get car recommendations based on user preferences"""
    
    # Calculate scores for all cars
    df['recommendation_score'] = df.apply(
        lambda car: calculate_recommendation_score(car, budget, priority, user_type),
        axis=1
    )
    
    # Sort by score and filter by budget (allow 10% over budget)
    recommendations = df[df['price'] <= budget * 1.1].sort_values(
        'recommendation_score', ascending=False
    ).head(max_results)
    
    return recommendations

def format_car_display(car):
    """Format car information for display"""
    return f"""
    **{car['year']} {car['brand']} {car['model']}**
    - **Price:** ${car['price']:,}
    - **Type:** {car['type']} ({car['fuel']})
    - **Reliability:** {car['reliability']}
    - **Insurance Cost:** {car['insurance_cost']}
    - **Maintenance Cost:** {car['maintenance_cost']}
    - **Suitable for:** {car['suitable_driver_type'].replace(';', ', ')}
    - **Match Score:** {car['recommendation_score']:.0f}/100
    """

def show_questionnaire():
    """Display the questionnaire form"""
    st.title("🚗 Smart Used Car Recommender")
    st.markdown("""
    ### Tell us about yourself and your car needs
    Please answer the following questions to get personalized car recommendations.
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
        
        st.subheader("⭐ Priorities")
        col3, col4 = st.columns(2)
        
        with col3:
            reliability = st.selectbox(
                "How important is reliability to you?",
                ["Somewhat important", "Important", "Very important", "Extremely important"]
            )
            
            budget_priority = st.selectbox(
                "Which is most important for your budget?",
                ["The cheapest option possible", "Low insurance costs", 
                 "Low maintenance costs", "Good resale value"]
            )
            
            performance = st.selectbox(
                "How important is performance/fun driving?",
                ["Not important", "Somewhat important", "Important", "Very important"]
            )
        
        with col4:
            brand = st.selectbox(
                "Do you have brand preferences?",
                ["No preference", "Japanese brands (Toyota, Honda, etc.)", 
                 "American brands (Ford, Chevrolet, etc.)", "European brands (BMW, Audi, etc.)",
                 "Performance and luxury brands", "Budget-friendly brands"]
            )
            
            features = st.multiselect(
                "Which features are most important to you?",
                ["Safety features", "Technology/Infotainment", "Fuel efficiency", 
                 "Cargo space", "Comfort", "Style/Appearance"]
            )
            
            timeline = st.selectbox(
                "When do you need the car?",
                ["Immediately", "Within a month", "Within 3 months", "Just browsing"]
            )
        
        # Submit button
        submitted = st.form_submit_button("🔍 Find My Perfect Car", type="primary")
        
        if submitted:
            # Store responses in session state
            st.session_state.questionnaire_responses = {
                'age': age,
                'family_size': family_size,
                'experience': experience,
                'location': location,
                'budget': budget,
                'usage': usage,
                'fuel_preference': fuel_preference,
                'size_preference': size_preference,
                'reliability': reliability,
                'budget_priority': budget_priority,
                'performance': performance,
                'brand': brand,
                'features': features,
                'timeline': timeline
            }
            st.session_state.show_results = True
            st.rerun()

def show_results(df, responses):
    """Display the recommendation results"""
    # Analyze responses to get user type and priority
    user_type, priority = analyze_questionnaire_responses(responses)
    
    st.title("🎯 Your Personalized Car Recommendations")
    
    # Show user profile
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Your Profile:** {user_type}")
    with col2:
        st.info(f"**Your Priority:** {priority}")
    with col3:
        st.info(f"**Your Budget:** ${responses['budget']:,}")
    
    # Get recommendations
    recommendations = get_recommendations(df, responses['budget'], priority, user_type)
    
    if len(recommendations) == 0:
        st.warning("No cars found matching your criteria. Try adjusting your budget or preferences.")
        if st.button("🔄 Retake Questionnaire"):
            st.session_state.show_results = False
            st.rerun()
    else:
        st.success(f"Found {len(recommendations)} cars that match your profile!")
        
        # Display recommendations in a clean grid
        for idx, (_, car) in enumerate(recommendations.iterrows()):
            if idx % 2 == 0:
                cols = st.columns(2)
            
            col = cols[idx % 2]
            
            with col:
                with st.container():
                    # Score-based styling
                    score = car['recommendation_score']
                    if score >= 80:
                        st.success("🌟 **Excellent Match**")
                    elif score >= 60:
                        st.info("👍 **Good Match**")
                    else:
                        st.warning("🤔 **Possible Match**")
                    
                    st.markdown(format_car_display(car))
                    st.markdown("---")
        
        # Show detailed insights
        st.subheader("📊 Your Recommendation Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_price = recommendations['price'].mean()
            st.metric("Average Price", f"${avg_price:,.0f}")
        
        with col2:
            high_reliability = len(recommendations[recommendations['reliability'] == 'High'])
            st.metric("High Reliability Cars", f"{high_reliability}/{len(recommendations)}")
        
        with col3:
            low_insurance = len(recommendations[recommendations['insurance_cost'] == 'Low'])
            st.metric("Low Insurance Cars", f"{low_insurance}/{len(recommendations)}")
        
        with col4:
            avg_score = recommendations['recommendation_score'].mean()
            st.metric("Average Match Score", f"{avg_score:.0f}/100")
        
        # Explanation based on user profile
        st.subheader("🧠 Why These Recommendations?")
        explanation = f"""
        Based on your questionnaire responses, we identified you as a **{user_type}** driver with **{priority}** as your top priority.
        
        **Your Profile Analysis:**
        - Age: {responses['age']} 
        - Family size: {responses['family_size']}
        - Primary use: {responses['usage']}
        - Budget: ${responses['budget']:,}
        
        **Matching Logic:**
        - Cars are scored based on budget fit (30%), your priority factor (40%), and suitability for your driver type (30%)
        - We included cars up to 10% over your budget for flexibility
        - Higher scores indicate better matches for your specific needs
        """
        st.markdown(explanation)
        
        # Option to retake questionnaire
        if st.button("🔄 Retake Questionnaire"):
            st.session_state.show_results = False
            st.rerun()

def main():
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Show questionnaire or results based on state
    if not hasattr(st.session_state, 'show_results') or not st.session_state.show_results:
        show_questionnaire()
    else:
        show_results(df, st.session_state.questionnaire_responses)
    
    # Show dataset in expander (always available)
    with st.expander("📋 View Complete Dataset"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()