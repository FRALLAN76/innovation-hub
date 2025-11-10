#!/usr/bin/env python3
"""
Reset database script
Use this to manually reset the database when needed
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from innovation_hub.database import get_db
from innovation_hub.tests import create_seed_data, reset_database

def main():
    """Reset database and recreate seed data"""
    print("⚠️  WARNING: This will delete ALL data in the database!")
    print("=" * 60)

    # Ask for confirmation
    response = input("Are you sure you want to reset the database? (yes/no): ")

    if response.lower() != 'yes':
        print("❌ Database reset cancelled")
        return

    db = next(get_db())
    try:
        print("\n🔄 Resetting database...")
        reset_database(db)

        print("🔄 Creating seed data...")
        create_seed_data(db)

        print("\n✅ Database has been reset successfully!")
        print("📊 Seed data includes:")
        print("   - Test users")
        print("   - Categories")
        print("   - Sample ideas")

    except Exception as e:
        print(f"\n❌ Database reset failed: {e}")
        return False
    finally:
        db.close()

    return True

if __name__ == "__main__":
    main()
