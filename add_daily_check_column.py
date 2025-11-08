"""
Add last_daily_check column to pets table if it doesn't exist
Run this script if you get errors with daily-check endpoint
"""
from app.database import engine
from sqlalchemy import text

def add_daily_check_column():
    print("Adding last_daily_check column to pets table...")
    
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='pets' AND column_name='last_daily_check'
            """))
            
            if result.rowcount == 0:
                # Column doesn't exist, add it
                conn.execute(text("""
                    ALTER TABLE pets 
                    ADD COLUMN last_daily_check TIMESTAMP WITH TIME ZONE
                """))
                conn.commit()
                print("✓ Column last_daily_check added successfully!")
            else:
                print("✓ Column last_daily_check already exists")
                
    except Exception as e:
        print(f"Error: {e}")
        print("\nIf you see an error, please run: python reset_database.py")

if __name__ == "__main__":
    add_daily_check_column()
