#!/usr/bin/env python3
"""Script to check votes in database"""

from innovation_hub.database import get_db
from innovation_hub.database.models import Idea, Vote
from sqlalchemy import func

def main():
    db = next(get_db())

    print("📊 Vote Statistics")
    print("=" * 50)

    # Count total votes
    total_votes = db.query(Vote).count()
    print(f"Total votes in database: {total_votes}")

    # Count unique voters
    unique_voters = db.query(func.count(func.distinct(Vote.user_id))).scalar()
    print(f"Unique voters: {unique_voters}")

    # Ideas with votes
    ideas_with_votes = db.query(Idea).filter(Idea.vote_count > 0).all()
    print(f"\nIdeas with votes: {len(ideas_with_votes)}")

    if ideas_with_votes:
        print("\n📋 Ideas ranked by votes:")
        for idea in sorted(ideas_with_votes, key=lambda x: x.vote_count, reverse=True):
            print(f"  • {idea.title[:50]}: {idea.vote_count} votes")

    # Show all votes
    all_votes = db.query(Vote).all()
    if all_votes:
        print(f"\n🗳️ All votes:")
        for vote in all_votes:
            idea = db.query(Idea).filter(Idea.id == vote.idea_id).first()
            print(f"  • User {vote.user_id} voted for: {idea.title[:40]} (ID: {vote.idea_id})")
            print(f"    Voted at: {vote.created_at}")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
