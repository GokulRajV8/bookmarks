from . import app
from . import bm_service

if __name__ == "__main__":
    # starting server
    app.run()

    # closing resources
    bm_service.close()
