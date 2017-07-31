from app import app
from config.site import config

@app.context_processor
def site_global_data():
    return dict(**config)
