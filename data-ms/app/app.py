from flask import Flask
import atexit
import scrapper.job.APICronJob as api_job

app = Flask(__name__)

cron_job = api_job.APICronJob()
cron_job.start_api_job()

atexit.register(lambda: cron_job._scheduler.shutdown(wait=False))

@app.route("/")
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run()
