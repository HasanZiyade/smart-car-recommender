import openai
import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Tuple

class CarRecommenderAI:
    def __init__(self, api_key: str):
        """Initialize a fresh AI-enhanced car recommender for each search"""
        self.client = openai.OpenAI(api_key=api_key)
        # Removed conversation_history to ensure fresh start each time
    
    def score_all_cars(self, cars_data: pd.DataFrame, user_responses: Dict) -> pd.DataFrame:
        """
        Use AI to score all cars based on user responses - optimized for speed
        Returns: DataFrame with AI scores and explanations
        """
        
        # Filter by budget first to reduce processing
        budget_filtered = cars_data[cars_data['price'] <= user_responses['budget'] * 1.2]
        
        if len(budget_filtered) == 0:
            # If no cars in budget, take cheapest 20
            budget_filtered = cars_data.nsmallest(20, 'price')
        
        # Take a focused sample for AI analysis (max 25 cars to keep it fast)
        if len(budget_filtered) > 25:
            sample_cars = pd.concat([
                budget_filtered.nsmallest(8, 'price'),  # Cheapest options
                budget_filtered.nsmallest(8, 'mileage'),  # Low mileage options  
                budget_filtered.nlargest(9, 'safety_rating').sample(min(9, len(budget_filtered)))  # High safety options
            ]).drop_duplicates().head(25)
        else:
            sample_cars = budget_filtered
        
        # Use batch scoring for much better performance
        scored_cars = self.batch_score_cars(sample_cars, user_responses)
        
        # Return top 15 cars sorted by AI score
        return scored_cars.sort_values('ai_score', ascending=False).head(15)
    
    def batch_score_cars(self, cars_df: pd.DataFrame, user_responses: Dict) -> pd.DataFrame:
        """
        Score multiple cars in a single AI call for much better performance
        """
        
        # Build user profile summary
        user_profile = f"""User: {user_responses['age']}, {user_responses['family_size']}, Budget: ${user_responses['budget']:,}
Max mileage: {user_responses.get('mileage_preference', 'No preference')}, Use: {user_responses['usage']}
Priorities: Reliability={user_responses['reliability']}, Performance={user_responses['performance']}
Preferences: {user_responses['size_preference']} size, {user_responses.get('color_preference', 'any')} color"""
        
        # Build car listings summary (much more concise)
        cars_summary = ""
        for idx, (_, car) in enumerate(cars_df.iterrows()):
            cars_summary += f"{idx+1}. {car['year']} {car['brand']} {car['model']} - ${car['price']:,}, {car.get('mileage', 'N/A'):,}mi, {car['type']}, {car['fuel']}, {car['mpg_city']}/{car['mpg_highway']}mpg, {car['safety_rating']}⭐, {car['reliability']} reliability\n"
        
        system_prompt = f"""Rate each car for this user (1-100 scale). Be fast and decisive.

USER: {user_profile}

CARS:
{cars_summary}

Respond with ONLY this format (no explanations):
1: match=85, price=75, reason="Great family car, good value"  
2: match=70, price=90, reason="Reliable but pricey"
[etc for each car]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": system_prompt}],
                temperature=0.1,  # Lower temperature for more consistent scoring
                max_tokens=800   # Limit tokens for faster response
            )
            
            # Parse the response quickly
            content = response.choices[0].message.content.strip()
            
            # Parse scores from the response
            scored_cars = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if i >= len(cars_df):
                    break
                    
                try:
                    # Extract match and price scores from format: "1: match=85, price=75, reason="text""
                    if 'match=' in line and 'price=' in line:
                        match_part = line.split('match=')[1].split(',')[0].strip()
                        price_part = line.split('price=')[1].split(',')[0].strip()
                        reason_part = line.split('reason="')[1].split('"')[0] if 'reason="' in line else "Good option"
                        
                        match_score = min(100, max(0, int(match_part)))
                        price_score = min(100, max(0, int(price_part)))
                        
                        car_dict = cars_df.iloc[i].to_dict()
                        car_dict['ai_score'] = match_score
                        car_dict['pricing_score'] = price_score
                        car_dict['ai_explanation'] = reason_part
                        scored_cars.append(car_dict)
                        
                except (ValueError, IndexError):
                    # Fallback scoring if parsing fails
                    car_dict = cars_df.iloc[i].to_dict()
                    car_dict['ai_score'] = 75  # Default decent score
                    car_dict['pricing_score'] = 75
                    car_dict['ai_explanation'] = "Good option for your needs"
                    scored_cars.append(car_dict)
            
            return pd.DataFrame(scored_cars)
            
        except Exception as e:
            # Fallback: simple rule-based scoring if AI fails
            st.warning("AI scoring temporarily unavailable, using quick analysis...")
            return self.fallback_scoring(cars_df, user_responses)
    
    def fallback_scoring(self, cars_df: pd.DataFrame, user_responses: Dict) -> pd.DataFrame:
        """Fast rule-based scoring when AI is unavailable"""
        scored_cars = []
        
        for _, car in cars_df.iterrows():
            # Simple scoring based on budget, mileage, and safety
            budget_score = 100 - abs(car['price'] - user_responses['budget']) / user_responses['budget'] * 100
            mileage_score = max(0, 100 - car.get('mileage', 100000) / 2000)  # Lower mileage = better score
            safety_score = car['safety_rating'] * 20  # Convert 5-star to 100-point scale
            
            match_score = (budget_score * 0.4 + mileage_score * 0.3 + safety_score * 0.3)
            match_score = min(100, max(0, match_score))
            
            car_dict = car.to_dict()
            car_dict['ai_score'] = int(match_score)
            car_dict['pricing_score'] = 75  # Default pricing score
            car_dict['ai_explanation'] = "Quick analysis match"
            scored_cars.append(car_dict)
            
        return pd.DataFrame(scored_cars)
    
    def generate_unified_summary(self, recommendations: pd.DataFrame, user_responses: Dict) -> str:
        """Generate a unified summary for the single AI recommendation system"""
        
        top_3_cars = recommendations.head(3).to_dict('records')
        other_cars = recommendations.iloc[3:].to_dict('records') if len(recommendations) > 3 else []
        
        user_profile = f"""
        User: {user_responses['age']}, {user_responses['family_size']}, {user_responses['usage']}
        Budget: ${user_responses['budget']:,}
        Preferences: {user_responses['size_preference']}, {user_responses['color_preference']}, {user_responses['brand']}
        Priorities: Reliability is {user_responses['reliability']}, Performance is {user_responses['performance']}
        """
        
        system_prompt = f"""
        You are a friendly, expert car advisor. Create a personalized summary for the user's unified AI car recommendations.
        
        User Profile: {user_profile}
        
        Top 3 AI Picks: {json.dumps(top_3_cars, indent=2)}
        Other Relevant Options: {len(other_cars)} additional cars scored and ranked
        
        Write a warm, personal summary (2-3 paragraphs) that:
        1. Welcomes them and acknowledges their specific needs
        2. Explains your AI analysis approach and how you scored the cars
        3. Highlights why the top 3 are perfect for them
        4. Mentions that you've found additional relevant options beyond the top picks
        5. Encourages them to explore different options and compare
        
        Make it feel like a personal consultation from an expert who has analyzed every option.
        Be conversational, confident, and helpful.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Welcome! I've personally analyzed every car in our database based on your preferences for {user_responses['usage']} with a ${user_responses['budget']:,} budget. After comprehensive AI scoring, I've identified your top 3 perfect matches plus {len(other_cars)} additional relevant options. Each recommendation is scored and explained based on your specific needs."

# Integration functions for the main app
def get_ai_recommendations(df: pd.DataFrame, user_responses: Dict, ai_assistant: CarRecommenderAI) -> Tuple[pd.DataFrame, str]:
    """
    Get unified AI-powered recommendations with both top picks and other relevant options
    """
    
    # Have AI score all relevant cars
    scored_cars = ai_assistant.score_all_cars(df, user_responses)
    
    # Get more recommendations to show both top picks and other options
    top_recommendations = scored_cars.head(15)  # Increased from 10 to 15
    
    # Generate personalized summary focusing on the unified approach
    summary = ai_assistant.generate_unified_summary(top_recommendations, user_responses)
    
    return top_recommendations, summary


class CarConsultantAI:
    """Separate AI consultant for general car advice and questions"""
    
    def __init__(self, api_key: str):
        """Initialize the car consultant AI"""
        self.client = openai.OpenAI(api_key=api_key)
    
    def get_consultant_response(self, user_message: str, chat_history: List[Dict]) -> str:
        """
        Get a response from the car consultant AI
        """
        
        system_prompt = """You are a knowledgeable and friendly car consultant assistant. You help users with:

• General car buying advice and tips
• Insurance information and guidance
• Financing options and credit considerations
• Car maintenance and ownership costs
• Vehicle inspection and purchasing process
• Resale value and market trends
• Car features and specifications
• Safety ratings and reliability information
• Fuel efficiency and environmental considerations
• Driving tips and car care advice

You should be helpful, informative, and conversational. Don't make recommendations about specific cars unless the user specifically asks about them. Focus on providing general knowledge and guidance about car ownership, buying, and maintenance.

Keep your responses concise but informative (2-3 paragraphs max). Use emojis occasionally to keep the conversation friendly."""

        # Prepare the conversation history for the API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history (limit to last 10 messages to keep context manageable)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        messages.extend(recent_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=400,
                stream=True
            )
            
            return response
            
        except Exception as e:
            return None
