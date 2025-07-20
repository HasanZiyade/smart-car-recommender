# Streamlit Cloud entry point
# This file ensures Streamlit Cloud runs the correct application

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the main application
if __name__ == "__main__":
    from main import main
    main()
