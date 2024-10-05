# 基於 Python 3.12 映像
FROM python:3.12-slim

# 設置工作目錄，對應 FastAPI 應用的目錄
WORKDIR /workspace/project/fastapi

# 複製需求文件到容器中
COPY requirements.txt ./

# 安裝依賴，優化安裝速度
RUN pip install --no-cache-dir -r requirements.txt

# 複製項目相關文件夾到容器中
COPY . .

# 暴露端口
EXPOSE 8000

# 設置啟動命令，確保 FastAPI 應用路徑正確
CMD ["uvicorn", "reports.fastapi.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]