from app.config import supabase
import random

def generate_food_prices():
    # Main dishes
    nasi_dishes = [
        ("Nasi Goreng Spesial", 25000, 35000),
        ("Nasi Uduk", 12000, 18000),
        ("Nasi Kuning", 15000, 22000),
        ("Nasi Campur", 20000, 30000),
        ("Nasi Ayam", 18000, 28000),
        ("Nasi Bebek", 25000, 35000),
        ("Nasi Pecel", 15000, 22000),
        ("Nasi Gudeg", 20000, 30000),
        ("Nasi Liwet", 18000, 25000),
        ("Nasi Ulam", 17000, 25000),
    ]

    # Soups and stews
    soups = [
        ("Soto Ayam", 15000, 25000),
        ("Soto Betawi", 20000, 30000),
        ("Sop Buntut", 35000, 50000),
        ("Bakso", 12000, 20000),
        ("Mie Bakso", 15000, 25000),
        ("Rawon", 20000, 30000),
        ("Sayur Asem", 12000, 18000),
        ("Sayur Lodeh", 12000, 18000),
        ("Sop Iga", 30000, 45000),
        ("Tongseng", 20000, 30000),
    ]

    # Street food and snacks
    street_food = [
        ("Gado-gado", 12000, 20000),
        ("Ketoprak", 12000, 20000),
        ("Siomay", 10000, 18000),
        ("Batagor", 10000, 18000),
        ("Martabak Telur", 20000, 30000),
        ("Martabak Manis", 25000, 40000),
        ("Pisang Goreng", 8000, 15000),
        ("Tahu Goreng", 5000, 10000),
        ("Tempe Goreng", 5000, 10000),
        ("Gorengan Mix", 10000, 15000),
    ]

    # Traditional snacks
    traditional_snacks = [
        ("Kue Putu", 5000, 10000),
        ("Kue Lumpur", 5000, 10000),
        ("Klepon", 5000, 10000),
        ("Onde-onde", 5000, 10000),
        ("Risoles", 5000, 10000),
        ("Lemper", 5000, 10000),
        ("Pastel", 5000, 10000),
        ("Kue Cucur", 5000, 10000),
        ("Serabi", 8000, 15000),
        ("Nagasari", 5000, 10000),
    ]

    # Meat dishes
    meat_dishes = [
        ("Rendang", 25000, 40000),
        ("Ayam Goreng", 18000, 28000),
        ("Ayam Bakar", 20000, 30000),
        ("Sate Ayam", 15000, 25000),
        ("Sate Kambing", 20000, 30000),
        ("Ikan Bakar", 25000, 35000),
        ("Bebek Goreng", 25000, 35000),
        ("Telur Dadar", 8000, 12000),
        ("Empal Gentong", 25000, 35000),
        ("Gulai Kambing", 25000, 35000),
    ]

    # Seafood dishes
    seafood = [
        ("Ikan Goreng", 20000, 30000),
        ("Cumi Goreng", 25000, 35000),
        ("Udang Goreng", 25000, 35000),
        ("Kepiting Saus Padang", 50000, 80000),
        ("Kerang Saus Tiram", 25000, 35000),
        ("Gurame Asam Manis", 35000, 50000),
        ("Kakap Bakar", 35000, 50000),
        ("Capcay Seafood", 25000, 35000),
        ("Nasi Goreng Seafood", 30000, 40000),
        ("Tom Yam Seafood", 30000, 45000),
    ]

    # Vegetable dishes
    vegetables = [
        ("Urap-urap", 10000, 15000),
        ("Pecel", 12000, 18000),
        ("Cap Cay", 18000, 25000),
        ("Tumis Kangkung", 12000, 18000),
        ("Oseng-oseng", 12000, 18000),
        ("Lalapan", 8000, 12000),
        ("Karedok", 12000, 18000),
        ("Plecing Kangkung", 12000, 18000),
        ("Terong Balado", 12000, 18000),
        ("Sayur Asem", 12000, 18000),
    ]

    # Drinks
    drinks = [
        ("Es Teh Manis", 5000, 8000),
        ("Es Jeruk", 6000, 10000),
        ("Es Campur", 12000, 18000),
        ("Es Cincau", 8000, 12000),
        ("Es Kelapa Muda", 10000, 15000),
        ("Jus Alpukat", 12000, 18000),
        ("Jus Mangga", 10000, 15000),
        ("Es Cendol", 10000, 15000),
        ("Wedang Jahe", 8000, 12000),
        ("Bandrek", 8000, 12000),
    ]

    # Combine all categories
    all_foods = (
        nasi_dishes + soups + street_food + traditional_snacks +
        meat_dishes + seafood + vegetables + drinks
    )

    # Generate food prices data with random prices within ranges
    food_prices_data = []
    for name, min_price, max_price in all_foods:
        price = random.randint(min_price, max_price)
        food_prices_data.append({
            'name': name,
            'price': price,
        })

    return food_prices_data

def seed_food_prices():
    try:
        # Delete existing data
        supabase.table('food_prices').delete().neq('id', 0).execute()
        
        # Generate and insert new food prices
        food_prices = generate_food_prices()
        result = supabase.table('food_prices').insert(food_prices).execute()
        
        print(f"Successfully inserted {len(food_prices)} food items")
        return True
    except Exception as e:
        print(f"Error seeding food prices: {e}")
        return False

if __name__ == "__main__":
    seed_food_prices()

seed_food_prices()