
import sys
import os
import traceback

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    print("Testing new langchain imports...")
    
    try:
        from langchain.chains import create_retrieval_chain
        from langchain.chains.combine_documents import create_stuff_documents_chain
        from langchain.chains.history_aware_retriever import create_history_aware_retriever
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        print("All langchain imports successful!")
    except ImportError as e:
        print(f"Import failed: {e}")
        traceback.print_exc()
        return
    
    print("\nTesting rag_chain module import...")
    try:
        from src.core.rag_chain import create_rag_chain
        print("rag_chain import successful!")
    except ImportError as e:
        print(f"rag_chain import failed: {e}")
        traceback.print_exc()
        return
    
    print("\nAll imports successful!")

if __name__ == "__main__":
    main()
