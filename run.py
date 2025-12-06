import uvicorn

if __name__ == "__main__":
    # uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    print("Server is running on http://127.0.0.1:8000")

