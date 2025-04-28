import sys
import os

# 把web/backend加入系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "")))

from app.services.unemployment_service import get_state_data

if __name__ == "__main__":
    print(get_state_data(2023, 4))