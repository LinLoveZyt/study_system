# run.py
import uvicorn
import os

if __name__ == "__main__":
    # 确保 data 目录存在
    os.makedirs("app/data/user_profiles", exist_ok=True)
    os.makedirs("app/data/learning_materials", exist_ok=True)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)