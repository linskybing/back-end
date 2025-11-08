"""
Migration script to add daily quest tracking columns to Pet table
Run this after the models have been updated
"""
from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL
import os

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        # Add daily quest columns to pets table
        try:
            conn.execute(text("""
                ALTER TABLE pets 
                ADD COLUMN IF NOT EXISTS daily_quest_1_completed BOOLEAN DEFAULT FALSE
            """))
            print("✓ Added daily_quest_1_completed column to pets table")
        except Exception as e:
            print(f"Note: daily_quest_1_completed column might already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE pets 
                ADD COLUMN IF NOT EXISTS daily_quest_2_completed BOOLEAN DEFAULT FALSE
            """))
            print("✓ Added daily_quest_2_completed column to pets table")
        except Exception as e:
            print(f"Note: daily_quest_2_completed column might already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE pets 
                ADD COLUMN IF NOT EXISTS daily_quest_3_completed BOOLEAN DEFAULT FALSE
            """))
            print("✓ Added daily_quest_3_completed column to pets table")
        except Exception as e:
            print(f"Note: daily_quest_3_completed column might already exist: {e}")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
