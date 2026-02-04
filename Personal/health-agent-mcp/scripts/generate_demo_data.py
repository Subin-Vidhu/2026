#!/usr/bin/env python3
"""
Generate demo health data for testing the Personal Health Agent.
Creates 3 demo users with realistic health data spanning 90 days.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db, SessionLocal, User, WearableData, MedicalRecord, HealthGoal
from datetime import datetime, timedelta
import random
import numpy as np
import json

def generate_demo_data():
    """Generate comprehensive demo data."""
    print("🏥 Personal Health Agent - Demo Data Generator")
    print("=" * 60)
    
    # Initialize database
    print("\n📊 Initializing database...")
    init_db()
    print("✓ Database initialized")
    
    db = SessionLocal()
    
    try:
        # Clear existing demo data
        print("\n🗑️  Clearing existing demo data...")
        db.query(Conversation).delete()
        db.query(HealthGoal).delete()
        db.query(MedicalRecord).delete()
        db.query(WearableData).delete()
        db.query(User).delete()
        db.commit()
        print("✓ Existing data cleared")
        
        # Create demo users
        print("\n👥 Creating demo users...")
        users_data = [
            {
                "name": "Active Alice",
                "age": 32,
                "gender": "female",
                "profile": "athletic",
                "telegram_id": None
            },
            {
                "name": "Busy Bob",
                "age": 45,
                "gender": "male",
                "profile": "sedentary",
                "telegram_id": None
            },
            {
                "name": "Senior Sarah",
                "age": 68,
                "gender": "female",
                "profile": "senior",
                "telegram_id": None
            }
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                name=user_data["name"],
                age=user_data["age"],
                gender=user_data["gender"]
            )
            db.add(user)
            users.append((user, user_data["profile"]))
        
        db.commit()
        print(f"✓ Created {len(users)} demo users")
        
        # Generate wearable data for each user
        print("\n⌚ Generating wearable data (90 days per user)...")
        days_to_generate = 90
        
        for user, profile in users:
            print(f"  • {user.name} ({profile} profile)...")
            
            # Profile-specific baselines
            if profile == "athletic":
                hr_base, hr_trend = 58, -0.05  # Improving
                steps_base, steps_var = 9500, 1500
                sleep_base, sleep_var = 7.5, 0.8
                hrv_base, hrv_trend = 65, 0.08
            elif profile == "sedentary":
                hr_base, hr_trend = 75, 0.02  # Slightly worsening
                steps_base, steps_var = 5500, 1200
                sleep_base, sleep_var = 6.5, 1.2
                hrv_base, hrv_trend = 45, -0.02
            else:  # senior
                hr_base, hr_trend = 70, 0
                steps_base, steps_var = 6000, 800
                sleep_base, sleep_var = 7.0, 1.0
                hrv_base, hrv_trend = 50, 0
            
            # Generate 90 days of data
            for day in range(days_to_generate):
                date = datetime.now() - timedelta(days=days_to_generate - day)
                
                # Add realistic trends and variations
                hr = int(hr_base + hr_trend * day + random.gauss(0, 5))
                steps = int(max(0, steps_base + random.gauss(0, steps_var)))
                sleep = round(max(4, min(10, sleep_base + random.gauss(0, sleep_var))), 1)
                hrv = int(max(20, hrv_base + hrv_trend * day + random.gauss(0, 8)))
                calories = int(1800 + (steps / 10) + random.gauss(0, 200))
                active_minutes = int(max(0, (steps / 100) + random.gauss(0, 20)))
                
                # Add some missing data (realistic)
                if random.random() < 0.10:  # 10% missing data
                    continue
                
                wearable = WearableData(
                    user_id=user.id,
                    date=date,
                    heart_rate=hr,
                    steps=steps,
                    sleep_hours=sleep,
                    hrv=hrv,
                    calories=calories,
                    active_minutes=active_minutes
                )
                db.add(wearable)
            
            db.commit()
        
        print(f"✓ Generated wearable data for all users")
        
        # Add medical records
        print("\n🩺 Creating medical records...")
        
        # Alice - Athletic, healthy
        alice = users[0][0]
        db.add(MedicalRecord(
            user_id=alice.id,
            record_type="blood_work",
            date=datetime.now() - timedelta(days=60),
            data={
                "cholesterol": 185,
                "hdl": 62,
                "ldl": 105,
                "triglycerides": 90,
                "glucose": 88
            },
            notes="Annual checkup - all values normal"
        ))
        
        # Bob - Sedentary, borderline issues
        bob = users[1][0]
        db.add(MedicalRecord(
            user_id=bob.id,
            record_type="blood_work",
            date=datetime.now() - timedelta(days=45),
            data={
                "cholesterol": 215,
                "hdl": 45,
                "ldl": 145,
                "triglycerides": 180,
                "glucose": 105
            },
            notes="Borderline high cholesterol and glucose - lifestyle modifications recommended"
        ))
        
        db.add(MedicalRecord(
            user_id=bob.id,
            record_type="medication",
            date=datetime.now() - timedelta(days=30),
            data={
                "medications": [
                    {"name": "Vitamin D", "dosage": "2000 IU", "frequency": "daily"},
                    {"name": "Fish Oil", "dosage": "1000mg", "frequency": "daily"}
                ]
            },
            notes="Started supplements to support cardiovascular health"
        ))
        
        # Sarah - Senior, managed conditions
        sarah = users[2][0]
        db.add(MedicalRecord(
            user_id=sarah.id,
            record_type="diagnosis",
            date=datetime.now() - timedelta(days=365),
            data={
                "conditions": [
                    "Pre-diabetes (managed)",
                    "Hypertension (controlled with medication)"
                ]
            },
            notes="Stable with current management plan"
        ))
        
        db.add(MedicalRecord(
            user_id=sarah.id,
            record_type="medication",
            date=datetime.now() - timedelta(days=365),
            data={
                "medications": [
                    {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"},
                    {"name": "Lisinopril", "dosage": "10mg", "frequency": "once daily"},
                    {"name": "Aspirin", "dosage": "81mg", "frequency": "once daily"}
                ]
            },
            notes="Current medication regimen for diabetes and blood pressure management"
        ))
        
        db.commit()
        print("✓ Created medical records")
        
        # Create health goals
        print("\n🎯 Creating health goals...")
        
        # Alice - Wants to improve cardio fitness
        db.add(HealthGoal(
            user_id=alice.id,
            goal_type="exercise",
            description="Increase average daily steps to 12,000",
            target_value=12000,
            current_value=9500,
            timeline_days=60,
            status="active"
        ))
        
        # Bob - Wants better sleep
        db.add(HealthGoal(
            user_id=bob.id,
            goal_type="sleep",
            description="Achieve 7.5 hours of sleep per night",
            target_value=7.5,
            current_value=6.5,
            timeline_days=30,
            status="active"
        ))
        
        # Sarah - Maintain mobility
        db.add(HealthGoal(
            user_id=sarah.id,
            goal_type="exercise",
            description="Maintain 6,000 daily steps",
            target_value=6000,
            current_value=5800,
            timeline_days=90,
            status="active"
        ))
        
        db.commit()
        print("✓ Created health goals")
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ Demo data generation complete!")
        print("\n📋 Summary:")
        print(f"   • Users created: 3")
        print(f"   • Wearable data entries: {db.query(WearableData).count()}")
        print(f"   • Medical records: {db.query(MedicalRecord).count()}")
        print(f"   • Health goals: {db.query(HealthGoal).count()}")
        
        print("\n👥 Demo Users:")
        for user, profile in users:
            print(f"   • User ID {user.id}: {user.name} ({profile})")
            print(f"     Age: {user.age}, Gender: {user.gender}")
        
        print("\n🎮 Test Queries:")
        print("   • \"Has my sleep improved this month?\"")
        print("   • \"What does my resting heart rate mean?\"")
        print("   • \"Help me improve my activity levels\"")
        print("   • \"Show me my weekly health summary\"")
        
        print("\n💡 Next Steps:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Telegram bot token to .env")
        print("   3. Run: python run.py")
        print("   4. Start chatting in Telegram or use the API!")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error generating demo data: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    # Import Conversation here to avoid circular import
    from app.database.models import Conversation
    generate_demo_data()
