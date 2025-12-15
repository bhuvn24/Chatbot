
import sys
import os
# Add the project root to proper path to allow absolute imports of 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.retrievers import load_vector_dbs
import traceback

def main():
    print("Attempting to load vector DBs...")
    try:
        dbs = load_vector_dbs()
        print("Successfully loaded vector DBs.")
        for key in dbs:
            print(f" - {key}: {dbs[key]}")
    except Exception as e:
        print("Failed to load vector DBs.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
