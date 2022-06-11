from panels.export import *

if __name__ == '__main__':
    uvicorn.run("__main__:application", host="127.0.0.1", port=8220, reload=True)
