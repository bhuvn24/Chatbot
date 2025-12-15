
import sys
import os
import traceback

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.retrievers import load_vector_dbs
from src.core.rag_chain import create_rag_chain
from src.core.memory import get_memory
from src.models.llm import get_llm
from src.models.slm import get_slm

def main():
    print("Starting verification...")
    
    # 1. Test Memory Initialization
    print("1. Testing Memory...")
    try:
        memory = get_memory()
        print(f"Memory initialized: keys={memory.memory_variables}")
    except Exception:
        traceback.print_exc()
        return

    # 2. Test Model Initialization
    print("2. Testing Models...")
    try:
        llm = get_llm()
        slm = get_slm()
        print(f"LLM initialized: {llm.model_name}")
        print(f"SLM initialized: {slm.model_name}")
    except Exception:
        traceback.print_exc()
        return

    # 3. Test Vector DB Loading (Partial or Full)
    print("3. Loading Vector DBs (this might take a moment)...")
    try:
        # We need to run this to get the retrievers
        retrievers = load_vector_dbs()
        print("Vector DBs loaded.")
    except Exception:
        traceback.print_exc()
        return

    # 4. Test Chain Creation and Invocation
    print("4. Testing RAG Chain Invocation...")
    try:
        # Test with 'all' retriever and LLM
        chain = create_rag_chain(llm, retrievers["all"], memory)
        
        query = "What is investing?"
        print(f"Invoking chain with query: '{query}'")
        
        # Invoke check
        response = chain.invoke({"question": query})
        
        if "answer" in response:
            print("SUCCESS: Chain returned an answer.")
            print(f"Answer snippet: {response['answer'][:100]}...")
        else:
            print("FAILURE: No answer in response.")
            print(f"Response keys: {response.keys()}")
            
    except Exception:
        print("FAILURE: Chain invocation crashed.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
