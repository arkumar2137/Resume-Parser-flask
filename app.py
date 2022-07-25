from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidates')
def candidates():
    context = {
        "name": "Ashish"
    }
    return render_template('candidates.html', context=context)

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/resume_checker')
def resume_checker():
    return render_template('resume.html')

if __name__ == '__main__':
    app.run(debug=True) 