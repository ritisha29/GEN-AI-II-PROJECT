import os
import sys
import pandas as pd

# Add the parent directory to sys.path to allow importing from the app package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.vector_store import vector_store

def build_index(csv_path: str):
    """
    Reads a CSV file containing reviews and indexes them into ChromaDB.
    """
    print(f"Loading data from {csv_path}...")
    if not os.path.exists(csv_path):
        print(f"Error: Could not find file {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Check for required columns
    required_columns = ["review_id", "product_id", "rating", "review_text"]
    for col in required_columns:
        if col not in df.columns:
            print(f"Error: Missing required column '{col}' in CSV.")
            return

    # Prepare data for Vector Store
    documents = []
    metadatas = []
    ids = []

    print("Processing and generating embeddings...")
    for index, row in df.iterrows():
        documents.append(str(row["review_text"]))
        
        # Ensure metadata values are basic types (string, int, float, bool)
        metadatas.append({
            "review_id": str(row["review_id"]),
            "product_id": str(row["product_id"]),
            "rating": int(row["rating"])
        })
        
        # ID must be unique
        ids.append(f"doc_{row['review_id']}")

    # Insert into ChromaDB
    print(f"Inserting {len(documents)} documents into Vector Database...")
    try:
        vector_store.add_documents(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Successfully built the index!")
    except Exception as e:
        print(f"Error inserting documents: {e}")

if __name__ == "__main__":
    # Determine path to the default reviews.csv
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_csv_path = os.path.join(base_dir, "data", "reviews.csv")
    
    # You could also take the path from sys.argv if provided
    csv_file = sys.argv[1] if len(sys.argv) > 1 else default_csv_path
    
    build_index(csv_file)
