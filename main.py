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
    # Determine user type based on responses with more sophisticated logic
    user_type = "Commuter"  # Default
    
    # Age and usage pattern analysis
    if responses['age'] in ["18-25", "26-35"]:
        if responses['usage'] in ["Daily commuting to school", "Weekend trips"]:
            user_type = "Student"
        elif responses['performance'] == "Very important" or responses['brand'] == "Performance and luxury brands":
            user_type = "Enthusiast"
        elif responses['budget_priority'] == "The cheapest option possible":
            user_type = "Budget"
    
    # Family size consideration
    if responses['family_size'] in ["3-4 people", "5+ people"]:
        user_type = "Family"
    elif responses['usage'] == "Daily commuting to work":
        user_type = "Commuter"
    elif responses['performance'] == "Very important" or responses['brand'] == "Performance and luxury brands":
        user_type = "Enthusiast"
    elif responses['budget_priority'] == "The cheapest option possible" and responses['age'] in ["18-25"]:
        user_type = "Budget"
    
    # Determine priorities with weighted system
    priorities = {}
    
    # Budget priority scoring
    if responses['budget_priority'] == "Low insurance costs":
        priorities["insurance"] = 0.4
        priorities["budget"] = 0.3
    elif responses['budget_priority'] == "Low maintenance costs":
        priorities["maintenance"] = 0.4
        priorities["budget"] = 0.3
    elif responses['budget_priority'] == "The cheapest option possible":
        priorities["budget"] = 0.5
        priorities["insurance"] = 0.2
        priorities["maintenance"] = 0.2
    elif responses['budget_priority'] == "Good resale value":
        priorities["reliability"] = 0.3
        priorities["brand"] = 0.3
    
    # Reliability importance
    if responses['reliability'] == "Extremely important":
        priorities["reliability"] = priorities.get("reliability", 0) + 0.4
    elif responses['reliability'] == "Very important":
        priorities["reliability"] = priorities.get("reliability", 0) + 0.3
    
    # Performance importance
    if responses['performance'] == "Very important":
        priorities["performance"] = 0.3
    elif responses['performance'] == "Important":
        priorities["performance"] = 0.2
    
    # Fuel efficiency
    if responses['fuel_preference'] == "Fuel efficiency is important":
        priorities["fuel_efficiency"] = 0.3
    elif responses['fuel_preference'] == "Interested in hybrid/electric":
        priorities["fuel_efficiency"] = 0.4
        priorities["environmental"] = 0.2
    
    # Safety (based on family size and age)
    if responses['family_size'] in ["3-4 people", "5+ people"] or "Safety features" in responses.get('features', []):
        priorities["safety"] = 0.3
    
    return user_type, priorities

def calculate_recommendation_score(car, budget, priorities, user_type, responses):
    """
    Calculate a comprehensive recommendation score for a car based on user preferences.
    Uses a sophisticated weighted scoring system for realistic recommendations.
    """
    score = 0
    max_score = 100
    
    # 1. Budget fit (25% of total score)
    price = car['price']
    budget_score = 0
    if price <= budget * 0.7:  # Great value
        budget_score = 25
    elif price <= budget * 0.85:  # Good value
        budget_score = 20
    elif price <= budget:  # Within budget
        budget_score = 15
    elif price <= budget * 1.05:  # Slightly over budget
        budget_score = 8
    elif price <= budget * 1.1:  # 10% over budget
        budget_score = 3
    else:  # Over budget
        budget_score = 0
    
    score += budget_score
    
    # 2. Priority-based scoring (40% of total score)
    priority_score = 0
    
    # Reliability scoring
    if priorities.get("reliability", 0) > 0:
        reliability_weight = priorities["reliability"]
        if car['reliability'] == 'High':
            priority_score += 25 * reliability_weight
        elif car['reliability'] == 'Medium':
            priority_score += 15 * reliability_weight
        else:
            priority_score += 5 * reliability_weight
    
    # Insurance cost scoring
    if priorities.get("insurance", 0) > 0:
        insurance_weight = priorities["insurance"]
        if car['insurance_cost'] == 'Low':
            priority_score += 20 * insurance_weight
        elif car['insurance_cost'] == 'Medium':
            priority_score += 12 * insurance_weight
        else:
            priority_score += 3 * insurance_weight
    
    # Maintenance cost scoring
    if priorities.get("maintenance", 0) > 0:
        maintenance_weight = priorities["maintenance"]
        if car['maintenance_cost'] == 'Low':
            priority_score += 20 * maintenance_weight
        elif car['maintenance_cost'] == 'Medium':
            priority_score += 12 * maintenance_weight
        else:
            priority_score += 3 * maintenance_weight
    
    # Fuel efficiency scoring
    if priorities.get("fuel_efficiency", 0) > 0:
        fuel_weight = priorities["fuel_efficiency"]
        mpg_combined = (car['mpg_city'] + car['mpg_highway']) / 2
        if mpg_combined >= 40:
            priority_score += 25 * fuel_weight
        elif mpg_combined >= 30:
            priority_score += 20 * fuel_weight
        elif mpg_combined >= 25:
            priority_score += 15 * fuel_weight
        elif mpg_combined >= 20:
            priority_score += 10 * fuel_weight
        else:
            priority_score += 5 * fuel_weight
    
    # Environmental scoring (for electric/hybrid preference)
    if priorities.get("environmental", 0) > 0:
        env_weight = priorities["environmental"]
        if car['fuel'] == 'Electric':
            priority_score += 25 * env_weight
        elif car['fuel'] == 'Hybrid':
            priority_score += 20 * env_weight
        else:
            priority_score += 5 * env_weight
    
    # Safety scoring
    if priorities.get("safety", 0) > 0:
        safety_weight = priorities["safety"]
        if car['safety_rating'] == 5:
            priority_score += 20 * safety_weight
        elif car['safety_rating'] == 4:
            priority_score += 15 * safety_weight
        elif car['safety_rating'] == 3:
            priority_score += 10 * safety_weight
        else:
            priority_score += 5 * safety_weight
    
    score += min(priority_score, 40)
    
    # 3. User type suitability (20% of total score)
    suitable_types = car['suitable_driver_type'].split(';')
    type_score = 0
    if user_type in suitable_types:
        type_score = 20
    elif any(user_type.lower() in stype.lower() for stype in suitable_types):
        type_score = 15
    else:
        type_score = 5
    
    score += type_score
    
    # 4. Personal preferences (15% of total score)
    preference_score = 0
    
    # Size preference
    if responses['size_preference'] != "No preference":
        if responses['size_preference'] == "Compact/Small" and car['type'] in ['Hatchback', 'Sedan']:
            preference_score += 5
        elif responses['size_preference'] == "Mid-size" and car['type'] in ['Sedan', 'SUV']:
            preference_score += 5
        elif responses['size_preference'] == "Large" and car['type'] in ['SUV', 'Truck', 'Van']:
            preference_score += 5
    
    # Fuel type preference matching
    if responses['fuel_preference'] == "Interested in hybrid/electric":
        if car['fuel'] in ['Electric', 'Hybrid']:
            preference_score += 5
    elif responses['fuel_preference'] == "Performance over efficiency":
        if car['type'] in ['Coupe', 'Sedan'] and car['fuel'] == 'Petrol':
            preference_score += 3
    
    # Brand preference
    brand_preferences = {
        "Japanese brands (Toyota, Honda, etc.)": ['Toyota', 'Honda', 'Mazda', 'Subaru', 'Nissan', 'Mitsubishi', 'Lexus', 'Acura', 'Infiniti'],
        "American brands (Ford, Chevrolet, etc.)": ['Ford', 'Chevrolet', 'Dodge', 'Jeep', 'Cadillac', 'Buick', 'GMC', 'Lincoln', 'Ram'],
        "European brands (BMW, Audi, etc.)": ['BMW', 'Audi', 'Mercedes', 'Volkswagen', 'Volvo', 'Mini', 'Jaguar', 'Land Rover'],
        "Performance and luxury brands": ['BMW', 'Audi', 'Mercedes', 'Lexus', 'Cadillac', 'Lincoln', 'Porsche', 'Jaguar', 'Maserati'],
        "Budget-friendly brands": ['Hyundai', 'Kia', 'Nissan', 'Mitsubishi', 'Chevrolet', 'Ford']
    }
    
    if responses['brand'] in brand_preferences:
        if car['brand'] in brand_preferences[responses['brand']]:
            preference_score += 3
    
    # Color preference bonus
    if responses.get('color_preference') and responses['color_preference'] != "No preference":
        if car['color'].lower() == responses['color_preference'].lower():
            preference_score += 2
    
    score += min(preference_score, 15)
    
    # Age penalty for very old cars
    current_year = 2025
    car_age = current_year - car['year']
    if car_age > 8:
        score -= 5
    elif car_age > 5:
        score -= 2
    
    return min(max(score, 0), max_score)

def get_recommendations(df, budget, priorities, user_type, responses, max_results=10):
    """Get car recommendations based on user preferences"""
    
    # Calculate scores for all cars
    df['recommendation_score'] = df.apply(
        lambda car: calculate_recommendation_score(car, budget, priorities, user_type, responses),
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
    **{car['year']} {car['brand']} {car['model']} ({car['color']})**
    - **Price:** ${car['price']:,}
    - **Type:** {car['type']} ({car['fuel']})
    - **MPG:** {car['mpg_city']} city / {car['mpg_highway']} highway
    - **Safety Rating:** {car['safety_rating']}/5 stars
    - **Reliability:** {car['reliability']}
    - **Insurance Cost:** {car['insurance_cost']}
    - **Maintenance Cost:** {car['maintenance_cost']}
    - **Cargo Space:** {car['cargo_space']} cubic feet
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
                'color_preference': color_preference,
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
    # Analyze responses to get user type and priorities
    user_type, priorities = analyze_questionnaire_responses(responses)
    
    st.title("🎯 Your Personalized Car Recommendations")
    
    # Show user profile with more details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Your Profile:** {user_type}")
    with col2:
        # Show top priority
        if priorities:
            top_priority = max(priorities.items(), key=lambda x: x[1])
            priority_names = {
                "reliability": "Reliability",
                "insurance": "Low Insurance Cost", 
                "maintenance": "Low Maintenance Cost",
                "budget": "Budget Value",
                "fuel_efficiency": "Fuel Efficiency",
                "safety": "Safety",
                "performance": "Performance"
            }
            st.info(f"**Top Priority:** {priority_names.get(top_priority[0], top_priority[0].title())}")
        else:
            st.info("**Priority:** Balanced Approach")
    with col3:
        st.info(f"**Your Budget:** ${responses['budget']:,}")
    
    # Get recommendations
    recommendations = get_recommendations(df, responses['budget'], priorities, user_type, responses)
    
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
                    elif score >= 65:
                        st.info("👍 **Very Good Match**")
                    elif score >= 50:
                        st.warning("🤔 **Good Match**")
                    else:
                        st.error("⚠️ **Possible Match**")
                    
                    st.markdown(format_car_display(car))
                    st.markdown("---")
        
        # Show detailed insights with enhanced metrics
        st.subheader("📊 Your Recommendation Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_price = recommendations['price'].mean()
            st.metric("Average Price", f"${avg_price:,.0f}")
        
        with col2:
            avg_mpg = ((recommendations['mpg_city'] + recommendations['mpg_highway']) / 2).mean()
            st.metric("Average MPG", f"{avg_mpg:.1f}")
        
        with col3:
            avg_safety = recommendations['safety_rating'].mean()
            st.metric("Average Safety Rating", f"{avg_safety:.1f}/5")
        
        with col4:
            avg_score = recommendations['recommendation_score'].mean()
            st.metric("Average Match Score", f"{avg_score:.0f}/100")
        
        # Additional insights
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            high_reliability = len(recommendations[recommendations['reliability'] == 'High'])
            st.metric("High Reliability Cars", f"{high_reliability}/{len(recommendations)}")
        
        with col6:
            low_insurance = len(recommendations[recommendations['insurance_cost'] == 'Low'])
            st.metric("Low Insurance Cars", f"{low_insurance}/{len(recommendations)}")
        
        with col7:
            efficient_cars = len(recommendations[(recommendations['mpg_city'] + recommendations['mpg_highway'])/2 >= 30])
            st.metric("Fuel Efficient Cars", f"{efficient_cars}/{len(recommendations)}")
        
        with col8:
            if responses.get('color_preference') and responses['color_preference'] != "No preference":
                color_matches = len(recommendations[recommendations['color'].str.lower() == responses['color_preference'].lower()])
                st.metric(f"{responses['color_preference']} Cars", f"{color_matches}/{len(recommendations)}")
            else:
                high_safety = len(recommendations[recommendations['safety_rating'] >= 4])
                st.metric("High Safety (4+ stars)", f"{high_safety}/{len(recommendations)}")
        
        # Enhanced explanation based on user profile
        st.subheader("🧠 Why These Recommendations?")
        
        # Build dynamic explanation based on priorities
        priority_explanations = []
        if priorities.get("reliability", 0) > 0.2:
            priority_explanations.append(f"**Reliability** (weight: {priorities['reliability']:.1f}) - You value dependable vehicles")
        if priorities.get("fuel_efficiency", 0) > 0.2:
            priority_explanations.append(f"**Fuel Efficiency** (weight: {priorities['fuel_efficiency']:.1f}) - You want to save on gas")
        if priorities.get("safety", 0) > 0.2:
            priority_explanations.append(f"**Safety** (weight: {priorities['safety']:.1f}) - You prioritize protection")
        if priorities.get("budget", 0) > 0.2:
            priority_explanations.append(f"**Budget Value** (weight: {priorities['budget']:.1f}) - You want the best deal")
        if priorities.get("insurance", 0) > 0.2:
            priority_explanations.append(f"**Low Insurance** (weight: {priorities['insurance']:.1f}) - You want lower insurance costs")
        
        explanation = f"""
        Based on your questionnaire responses, we identified you as a **{user_type}** driver.
        
        **Your Profile Analysis:**
        - Age: {responses['age']} 
        - Family size: {responses['family_size']}
        - Primary use: {responses['usage']}
        - Budget: ${responses['budget']:,}
        - Size preference: {responses['size_preference']}
        - Color preference: {responses.get('color_preference', 'No preference')}
        
        **Your Weighted Priorities:**
        {chr(10).join(['• ' + exp for exp in priority_explanations]) if priority_explanations else '• Balanced approach across all factors'}
        
        **Our Scoring System:**
        - **Budget Fit (25%):** How well the price fits your budget
        - **Priority Match (40%):** How well the car matches your specific priorities  
        - **User Type Fit (20%):** How suitable the car is for your driver profile
        - **Personal Preferences (15%):** Color, size, brand, and feature preferences
        
        Cars scoring 80+ are excellent matches, 65+ are very good matches, and 50+ are good options to consider.
        """
        st.markdown(explanation)
        
        # Show distribution of car types recommended
        st.subheader("🚗 Recommended Vehicle Types")
        type_counts = recommendations['type'].value_counts()
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(type_counts)
        
        with col2:
            for car_type, count in type_counts.items():
                st.write(f"**{car_type}:** {count} cars")
        
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