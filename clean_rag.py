"""
Clean up old files from RAG vector database
"""

import sys
from innovation_hub.ai.rag_service import RAGService

def main():
    print("🧹 Cleaning up RAG database...")
    print("=" * 60)

    # Initialize RAG service
    rag = RAGService()

    # Get current stats
    print("\n📊 Current database stats:")
    stats = rag.get_stats()
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Unique documents: {stats['unique_documents']}")
    print(f"   File types: {stats['file_types']}")

    # Get all documents to see what's there
    print("\n📄 Checking for tmp files...")
    all_docs = rag.get_all_documents()

    tmp_files = set()
    for doc in all_docs:
        filename = doc['metadata'].get('filename', '')
        if 'tmp' in filename.lower() or filename == 'tmp7om2ussc.xls':
            tmp_files.add(filename)

    if tmp_files:
        print(f"\n⚠️  Found {len(tmp_files)} temporary file(s) to delete:")
        for filename in tmp_files:
            print(f"   - {filename}")

        # Delete each tmp file
        print("\n🗑️  Deleting temporary files...")
        for filename in tmp_files:
            result = rag.delete_document(filename)
            if result['status'] == 'success':
                print(f"   ✅ Deleted {result['chunks_deleted']} chunks from {filename}")
            else:
                print(f"   ⚠️  Could not find chunks for {filename}")

        # Show updated stats
        print("\n📊 Updated database stats:")
        stats = rag.get_stats()
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Unique documents: {stats['unique_documents']}")
        print(f"   File types: {stats['file_types']}")

        print("\n✅ Cleanup complete!")
    else:
        print("\n✅ No temporary files found - database is clean!")

    print("=" * 60)

if __name__ == "__main__":
    main()
