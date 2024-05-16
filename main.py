if __name__ == "__main__":
    import uvicorn
    uvicorn.run("settings:app", host="0.0.0.0", port=8000)