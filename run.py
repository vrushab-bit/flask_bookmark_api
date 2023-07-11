import os
from dotenv import load_dotenv 
load_dotenv()
from src.app import create_app


if __name__ == "__main__":
    
    app = create_app()
    # run app
    app.run()