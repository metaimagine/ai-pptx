import uvicorn, logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

if __name__ == '__main__':
    uvicorn.run('applications:app', host='0.0.0.0', port=8080, reload=True)