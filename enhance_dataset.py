import pandas as pd
import numpy as np
import random

# Read the current dataset
df = pd.read_csv('cars_dataset.csv')

# Add mileage column to existing cars
def calculate_realistic_mileage(year, car_type, reliability):
    """Calculate realistic mileage based on car age and characteristics"""
    current_year = 2025
    age = current_year - year
    
    # Base mileage per year (varies by car type and usage)
    if car_type in ['SUV', 'Truck']:
        base_miles_per_year = random.randint(12000, 18000)
    elif car_type in ['Sedan', 'Hatchback']:
        base_miles_per_year = random.randint(10000, 15000)
    elif car_type == 'Coupe':
        base_miles_per_year = random.randint(8000, 12000)  # Often weekend cars
    else:
        base_miles_per_year = random.randint(10000, 14000)
    
    # Reliability affects how well-maintained (lower mileage if high reliability)
    if reliability == 'High':
        multiplier = random.uniform(0.85, 1.1)
    elif reliability == 'Medium':
        multiplier = random.uniform(0.9, 1.2)
    else:
        multiplier = random.uniform(1.0, 1.4)
    
    # Calculate total mileage with some randomness
    total_mileage = int(age * base_miles_per_year * multiplier)
    
    # Add some randomness and ensure reasonable bounds
    variation = random.randint(-5000, 10000)
    total_mileage = max(500, total_mileage + variation)
    
    # Ensure very new cars don't have excessive mileage
    if age <= 1:
        total_mileage = min(total_mileage, 15000)
    elif age <= 2:
        total_mileage = min(total_mileage, 30000)
    
    return total_mileage

# Add mileage to existing cars
df['mileage'] = df.apply(lambda row: calculate_realistic_mileage(row['year'], row['type'], row['reliability']), axis=1)

# Additional car data to expand the dataset - treating each as a used car ad
additional_cars = [
    # More budget-friendly options
    {'brand': 'Nissan', 'model': 'Versa', 'year': 2015, 'price': 8500, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'Medium', 'insurance_cost': 'Low', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Student;Budget', 'color': 'White', 'mpg_city': 31, 'mpg_highway': 40, 'safety_rating': 4, 'cargo_space': 15},
    {'brand': 'Hyundai', 'model': 'Accent', 'year': 2016, 'price': 9200, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'Medium', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Budget', 'color': 'Red', 'mpg_city': 28, 'mpg_highway': 38, 'safety_rating': 4, 'cargo_space': 13},
    {'brand': 'Kia', 'model': 'Rio', 'year': 2017, 'price': 10500, 'fuel': 'Petrol', 'type': 'Hatchback', 'reliability': 'Medium', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Budget', 'color': 'Blue', 'mpg_city': 32, 'mpg_highway': 40, 'safety_rating': 4, 'cargo_space': 17},
    
    # High mileage deals
    {'brand': 'Toyota', 'model': 'Camry', 'year': 2012, 'price': 11000, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'Medium', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Family;Budget', 'color': 'Silver', 'mpg_city': 25, 'mpg_highway': 35, 'safety_rating': 4, 'cargo_space': 15},
    {'brand': 'Honda', 'model': 'Accord', 'year': 2013, 'price': 12500, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'Medium', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Family;Commuter', 'color': 'Black', 'mpg_city': 27, 'mpg_highway': 36, 'safety_rating': 5, 'cargo_space': 16},
    
    # Low mileage premium finds
    {'brand': 'Lexus', 'model': 'ES', 'year': 2018, 'price': 28000, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'High', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Luxury;Family', 'color': 'White', 'mpg_city': 22, 'mpg_highway': 33, 'safety_rating': 5, 'cargo_space': 16},
    {'brand': 'Acura', 'model': 'TLX', 'year': 2019, 'price': 24000, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'High', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Enthusiast;Family', 'color': 'Gray', 'mpg_city': 23, 'mpg_highway': 33, 'safety_rating': 5, 'cargo_space': 14},
    
    # Compact cars with various mileages
    {'brand': 'Honda', 'model': 'Fit', 'year': 2018, 'price': 13500, 'fuel': 'Petrol', 'type': 'Hatchback', 'reliability': 'High', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Urban', 'color': 'Orange', 'mpg_city': 33, 'mpg_highway': 41, 'safety_rating': 5, 'cargo_space': 16},
    {'brand': 'Toyota', 'model': 'Yaris', 'year': 2019, 'price': 14500, 'fuel': 'Petrol', 'type': 'Hatchback', 'reliability': 'High', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Urban', 'color': 'Blue', 'mpg_city': 32, 'mpg_highway': 40, 'safety_rating': 4, 'cargo_space': 15},
    
    # SUVs with different mileage scenarios
    {'brand': 'Ford', 'model': 'Escape', 'year': 2017, 'price': 16500, 'fuel': 'Petrol', 'type': 'SUV', 'reliability': 'Medium', 'insurance_cost': 'Medium', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Family;Commuter', 'color': 'Red', 'mpg_city': 23, 'mpg_highway': 30, 'safety_rating': 5, 'cargo_space': 34},
    {'brand': 'Chevrolet', 'model': 'Equinox', 'year': 2018, 'price': 18000, 'fuel': 'Petrol', 'type': 'SUV', 'reliability': 'Medium', 'insurance_cost': 'Medium', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Family', 'color': 'White', 'mpg_city': 26, 'mpg_highway': 32, 'safety_rating': 5, 'cargo_space': 30},
    
    # Electric/Hybrid variety
    {'brand': 'Nissan', 'model': 'Leaf', 'year': 2017, 'price': 15000, 'fuel': 'Electric', 'type': 'Hatchback', 'reliability': 'High', 'insurance_cost': 'Medium', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Eco;Urban', 'color': 'White', 'mpg_city': 124, 'mpg_highway': 99, 'safety_rating': 5, 'cargo_space': 24},
    {'brand': 'Toyota', 'model': 'Prius Prime', 'year': 2018, 'price': 19500, 'fuel': 'Plugin Hybrid', 'type': 'Hatchback', 'reliability': 'High', 'insurance_cost': 'Medium', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Eco;Commuter', 'color': 'Silver', 'mpg_city': 54, 'mpg_highway': 50, 'safety_rating': 5, 'cargo_space': 19},
    
    # Luxury options with different mileages
    {'brand': 'BMW', 'model': 'X3', 'year': 2017, 'price': 26000, 'fuel': 'Petrol', 'type': 'SUV', 'reliability': 'Medium', 'insurance_cost': 'High', 'maintenance_cost': 'High', 'suitable_driver_type': 'Luxury;Family', 'color': 'Black', 'mpg_city': 23, 'mpg_highway': 30, 'safety_rating': 5, 'cargo_space': 28},
    {'brand': 'Audi', 'model': 'Q5', 'year': 2018, 'price': 29000, 'fuel': 'Petrol', 'type': 'SUV', 'reliability': 'Medium', 'insurance_cost': 'High', 'maintenance_cost': 'High', 'suitable_driver_type': 'Luxury;Family', 'color': 'Gray', 'mpg_city': 23, 'mpg_highway': 29, 'safety_rating': 5, 'cargo_space': 25},
    
    # Performance cars
    {'brand': 'Ford', 'model': 'Mustang', 'year': 2016, 'price': 19500, 'fuel': 'Petrol', 'type': 'Coupe', 'reliability': 'Medium', 'insurance_cost': 'High', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Enthusiast', 'color': 'Red', 'mpg_city': 21, 'mpg_highway': 31, 'safety_rating': 4, 'cargo_space': 13},
    {'brand': 'Chevrolet', 'model': 'Camaro', 'year': 2017, 'price': 22000, 'fuel': 'Petrol', 'type': 'Coupe', 'reliability': 'Medium', 'insurance_cost': 'High', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Enthusiast', 'color': 'Yellow', 'mpg_city': 20, 'mpg_highway': 30, 'safety_rating': 4, 'cargo_space': 9},
    
    # Trucks
    {'brand': 'Ford', 'model': 'F-150', 'year': 2016, 'price': 24000, 'fuel': 'Petrol', 'type': 'Truck', 'reliability': 'Medium', 'insurance_cost': 'Medium', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Work;Family', 'color': 'Blue', 'mpg_city': 18, 'mpg_highway': 25, 'safety_rating': 5, 'cargo_space': 52},
    {'brand': 'Chevrolet', 'model': 'Silverado', 'year': 2017, 'price': 26000, 'fuel': 'Petrol', 'type': 'Truck', 'reliability': 'Medium', 'insurance_cost': 'Medium', 'maintenance_cost': 'Medium', 'suitable_driver_type': 'Work;Family', 'color': 'White', 'mpg_city': 16, 'mpg_highway': 23, 'safety_rating': 4, 'cargo_space': 53},
    
    # Older reliable cars (higher mileage, lower price)
    {'brand': 'Toyota', 'model': 'Corolla', 'year': 2010, 'price': 8000, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Budget', 'color': 'Silver', 'mpg_city': 26, 'mpg_highway': 34, 'safety_rating': 4, 'cargo_space': 13},
    {'brand': 'Honda', 'model': 'Civic', 'year': 2011, 'price': 9500, 'fuel': 'Petrol', 'type': 'Sedan', 'reliability': 'High', 'insurance_cost': 'Low', 'maintenance_cost': 'Low', 'suitable_driver_type': 'Student;Budget', 'color': 'Blue', 'mpg_city': 28, 'mpg_highway': 36, 'safety_rating': 5, 'cargo_space': 12},
]

# Convert additional cars to DataFrame and add mileage
additional_df = pd.DataFrame(additional_cars)
additional_df['mileage'] = additional_df.apply(lambda row: calculate_realistic_mileage(row['year'], row['type'], row['reliability']), axis=1)

# Combine datasets
enhanced_df = pd.concat([df, additional_df], ignore_index=True)

# Add some variation to existing car mileages and prices to simulate different ads
# Duplicate some popular models with different mileage/price combinations
popular_models = enhanced_df[enhanced_df['brand'].isin(['Toyota', 'Honda', 'Nissan'])].sample(15)

# Create variations of popular models (different mileage/price for same car)
variations = []
for _, car in popular_models.iterrows():
    # Create 2-3 variations per popular model
    for i in range(random.randint(1, 3)):
        variation = car.copy()
        
        # Adjust mileage and price accordingly
        mileage_factor = random.uniform(0.7, 1.8)
        variation['mileage'] = int(variation['mileage'] * mileage_factor)
        
        # Higher mileage = lower price
        if mileage_factor > 1.2:
            variation['price'] = int(variation['price'] * random.uniform(0.75, 0.9))
        elif mileage_factor < 0.9:
            variation['price'] = int(variation['price'] * random.uniform(1.05, 1.2))
        
        # Occasionally change color to simulate different ads
        colors = ['White', 'Black', 'Silver', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Orange']
        if random.random() < 0.3:
            variation['color'] = random.choice(colors)
        
        variations.append(variation)

variations_df = pd.DataFrame(variations)

# Final combined dataset
final_df = pd.concat([enhanced_df, variations_df], ignore_index=True)

# Reorder columns to put mileage after year
columns = ['brand', 'model', 'year', 'mileage', 'price', 'fuel', 'type', 'reliability', 'insurance_cost', 'maintenance_cost', 'suitable_driver_type', 'color', 'mpg_city', 'mpg_highway', 'safety_rating', 'cargo_space']
final_df = final_df[columns]

# Sort by brand and model for better organization
final_df = final_df.sort_values(['brand', 'model', 'year']).reset_index(drop=True)

# Save the enhanced dataset
final_df.to_csv('cars_dataset.csv', index=False)

print(f"Enhanced dataset created with {len(final_df)} car listings!")
print(f"Mileage range: {final_df['mileage'].min():,} - {final_df['mileage'].max():,} miles")
print(f"Price range: ${final_df['price'].min():,} - ${final_df['price'].max():,}")
print("\nSample of new data:")
print(final_df.head(10))
