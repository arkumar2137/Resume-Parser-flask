from flask import Flask, render_template,jsonify, request
from flask_restful import Resource,Api
from flask_cors import CORS

import pandas as pd
import Extract_data
import itertools
#import csv
import rank

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def uploads():
    user = request.form
    docfile = request.files['resume_file']
    filename = secure_filename(docfile.filename)
    print(user)
    print('================================')
    print(filename)
    return render_template('uploadMessage.html')

@app.route('/candidates')
def candidates():
    d = [{      
            "Company Name": "Scaledge", 
            "Experience": "3 years", 
            "Qualification": "M.Tech", 
            "Skills": "Python,ML,DL,NLP",
            "Candidates Name" : "Ashish"
        },
        {      
            "Company Name": "Scaledge", 
            "Experience": "3 years", 
            "Qualification": "M.Tech", 
            "Skills": "Python,ML,DL,NLP",
            "Candidates Name" : "Ashish"
        }]
    return jsonify(d)
    #context = {"name": "Ashish"}
    #return render_template('candidates.html', context=context)

"""
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/resume_checker')
def resume_checker():
    return render_template('resume.html')
"""
# Fetch data
class extract_R(Resource):
    def get(self):
        userDetils = request.form
        filename= userDetils['resume_file']
        final_data = Extract_data.main(filename)
        df = pd.DataFrame.from_dict(final_data,orient = 'index')
        output = []
        result = {}
        for index, row in df.iterrows():
            output.append(dict(row))
        return output
        #return render_template('candidates.html', context=output)


class extract_JD(Resource):
    def get(self):
        filename = "Sheetal_Sahu.pdf"
        final_data = Extract_data.main(filename)
        df = pd.DataFrame.from_dict(final_data,orient = 'index')
        output = []
        result = {}
        for index, row in df.iterrows():
            output.append(dict(row))
        return output
        #return render_template('jobs.html')


       

class ranking(Resource):
    def get(self):
        # Resume data and create dataframe
        resume_data = [{'NAME': 'Ankur Krishna', 'SKILLS': 'JAVA TECHNOLOGIES DISTRIBUTED TECHNOLOGIES Java, JDBC SOAP Webservices, RESTful services FRAMEWORKS DATABASE Spring Boot, Hibernate & JPA PostgreSQL, Oracle IDE OPERATING SYSTEMS Eclipse, STS Microsoft Windows,python, Linux WEB/APP SERVERS TOOLS Tomcat Maven, GIT, Log4J, JUnit, JIRA, Putty I hereby declare that all of the details furnished above are true on the best of my knowledge and belief. (Ankur Krishna Shrivastava) Experience Organization: Revian Soft Technologies Pvt. Ltd. (Nov 2019-till date) Designation: Software Engineer Project Handled: #1 Title: Greencart e-commerce Duration: March 2021 To Till Date. Functional Domain: E-commerce Environment : Java, J2EE, Angular, SpringBoot, Spring Data, REST/SOAP Services, Microservices, Eureka Server, Zuul Gateway, PostgreSQL. Team Size :','EXPERIENCE':'2+ years'},
        {'NAME': 'Sheetal Sahu', 'SKILLS': 'Python, Machine Learning, Tableau Domain: Telecomm| Tech Stack: Python,NLP Domain: Entertainment| Tech Stack: Python Domain: Ecommerce| Tech Stack: SQL Tech Stack: Machine Learning Tools/Languages: Python, SQL,python,machine learning','EXPERIENCE':'3+ Years'},
        {'NAME':'A','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'2+ year'},
        {'NAME':'B','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'4+ year'},
        {'NAME':'c','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'6+ year'}]
        resume_df = pd.DataFrame.from_dict(resume_data)
       
        # JOb Description data and create dataframe
        jd_data = [{"SKILLS":'JAVA,Machine Learning,Python,GIT,JIRA,JUNIT','EXPERIENCE':'1+ year'}]
        jd_df = pd.DataFrame.from_dict(jd_data,orient = 'columns') 
        final_data = rank.main(resume_df,jd_df)
        output = []
        result = {}
        for index, row in final_data.iterrows():
            output.append(dict(row))
        return jsonify(output)
        #return render_template('resume.html')

@app.route('/faker')
def faker():
    return "String coming from faker endpoint"



api.add_resource(extract_R,'/upload') 
api.add_resource(extract_JD,'/jobs') 
api.add_resource(ranking,'/resume_checker')

if __name__ == '__main__':
    app.run(debug=True) 