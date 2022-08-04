from flask import Flask, render_template,jsonify, request
from flask_restful import Resource,Api
from flask_cors import CORS

import pandas as pd
import Extract_data
import itertools
#import csv
import rank
import os
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

# Config the folder for uploaded resume and Job description
app.config['UPLOAD_FOLDER'] = 'Upload-Resume'
app.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
app.config['result'] = 'result'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    #userDetils = request.form
    #filename= request.files['resume_file']
    filelist = [ f for f in os.listdir(app.config['UPLOAD_FOLDER']) ]  
    x = os.listdir(app.config['UPLOAD_FOLDER'])
    for f in request.files.getlist('resume_file'):
        if f.filename in x:
            Error = "All Ready "+f.filename +" Existed"
        else:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))   
        x = os.listdir(app.config['UPLOAD_FOLDER'])
    
    count = 0
    for file in x:
        final_data = Extract_data.main(app.config['UPLOAD_FOLDER']+"/"+file)
        print(type(final_data))
        if count == 0:
            df = pd.DataFrame.from_dict(final_data,orient = 'index')
            count += 1
        else:
            df1 = pd.DataFrame.from_dict(final_data,orient = 'index')
            df = df.append(df1)
            
            
    print(df)     
    output = []
    result = {}
    df_final = df.fillna("")
    for index, row in df_final.iterrows():
        print(dict(row))
        output.append(dict(row))
    
    #return Response(df.to_json(orient="records"), mimetype='application/json')
    return jsonify(output)
    #return render_template('uploadMessage.html')

@app.route('/candidates')
def candidates():
    return render_template('candidates.html')

# Fetch data
class extract_R(Resource):
    def post(self):
        Error = " "
        files_list = os.listdir(app.config['UPLOAD_FOLDER'])

        # Save file in local file system
        for f in request.files.getlist('resume_file'):
            if f.filename in files_list:
                Error = "All Ready " + f.filename + " Existed"
            else:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))  # save resume
                Extract_resume_data = Extract_data.main(app.config['UPLOAD_FOLDER'] + "/" + f.filename)  # Extracted data
                FinalDf = pd.DataFrame.from_dict(Extract_resume_data, orient='index')  # Create dataframe
                listObj = []

                # create json file and save the data
                if os.path.exists(os.path.join(app.config['result'], "user_data.json")):
                    with open(os.path.join(app.config['result'], "user_data.json")) as fp:
                        listObj = json.load(fp)
                        for _, row in FinalDf.iterrows():
                            dict_final = dict(row)
                            listObj.append(dict_final)
                    with open(os.path.join(app.config['result'], "user_data.json"), 'w') as json_file:
                        json.dump(listObj, json_file, indent=4, separators=(',', ': '), default=str)
                else:
                    with open(os.path.join(app.config['result'], "user_data.json"), 'w') as fp:
                        for _, row in FinalDf.iterrows():
                            dict_final = dict(row)
                            listObj.append(dict_final)
                            json.dump(listObj, fp, default=str)
                return jsonify(listObj)
            return Error


# for extracting Job description
class extract_JD(Resource):
    def post(self):
        Error = " "
        files_list = os.listdir(app.config['UPLOAD_JD_FOLDER'])

        # Save file in local file system
        for f in request.files.getlist('jd_file'):
            if f.filename in files_list:
                Error = "All Ready " + f.filename + " Existed"
            else:
                f.save(os.path.join(app.config['UPLOAD_JD_FOLDER'], f.filename))  # save job description
                Extract_job_description_data = Extract_data.main(app.config['UPLOAD_JD_FOLDER'] + "/" + f.filename)  # Extracted data
                FinalDf = pd.DataFrame.from_dict(Extract_job_description_data, orient='index')  # Create dataframe
                listObj = []

                # create json file and save the data
                if os.path.exists(os.path.join(app.config['result'], "job_description_data.json")):
                    with open(os.path.join(app.config['result'], "job_description_data.json")) as fp:
                        listObj = json.load(fp)
                        for _, row in FinalDf.iterrows():
                            dict_final = dict(row)
                            listObj.append(dict_final)
                    with open(os.path.join(app.config['result'], "job_description_data.json"), 'w') as json_file:
                        json.dump(listObj, json_file, indent=4, separators=(',', ': '), default=str)
                else:
                    with open(os.path.join(app.config['result'], "job_description_data.json"), 'w') as fp:
                        for _, row in FinalDf.iterrows():
                            dict_final = dict(row)
                            listObj.append(dict_final)
                            json.dump(listObj, fp, default=str)
                return jsonify(listObj)
            return Error


# Ranking function
class ranking(Resource):
    def get(self):
        jd_data = []
        resume_data = []
        # Job description
        if os.path.exists(os.path.join(app.config['result'], "job_description_data.json")):
            with open(os.path.join(app.config['result'], "job_description_data.json")) as fp:
                jd_data = json.load(fp)
                jd_df = pd.DataFrame.from_dict(jd_data, orient='columns')

        if os.path.exists(os.path.join(app.config['result'], "user_data.json")):
            with open(os.path.join(app.config['result'], "user_data.json")) as fp:
                resume_data = json.load(fp)
                resume_df = pd.DataFrame.from_dict(resume_data)

        # Resume data and create dataframe
        """
        resume_data = [{'NAME': 'Ankur Krishna', 'SKILLS': 'JAVA TECHNOLOGIES DISTRIBUTED TECHNOLOGIES Java, JDBC SOAP Webservices, RESTful services FRAMEWORKS DATABASE Spring Boot, Hibernate & JPA PostgreSQL, Oracle IDE OPERATING SYSTEMS Eclipse, STS Microsoft Windows,python, Linux WEB/APP SERVERS TOOLS Tomcat Maven, GIT, Log4J, JUnit, JIRA, Putty I hereby declare that all of the details furnished above are true on the best of my knowledge and belief. (Ankur Krishna Shrivastava) Experience Organization: Revian Soft Technologies Pvt. Ltd. (Nov 2019-till date) Designation: Software Engineer Project Handled: #1 Title: Greencart e-commerce Duration: March 2021 To Till Date. Functional Domain: E-commerce Environment : Java, J2EE, Angular, SpringBoot, Spring Data, REST/SOAP Services, Microservices, Eureka Server, Zuul Gateway, PostgreSQL. Team Size :','EXPERIENCE':'2+ years'},
        {'NAME': 'Sheetal Sahu', 'SKILLS': 'Python, Machine Learning, Tableau Domain: Telecomm| Tech Stack: Python,NLP Domain: Entertainment| Tech Stack: Python Domain: Ecommerce| Tech Stack: SQL Tech Stack: Machine Learning Tools/Languages: Python, SQL,python,machine learning','EXPERIENCE':'3+ Years'},
        {'NAME':'A','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'2+ year'},
        {'NAME':'B','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'4+ year'},
        {'NAME':'c','SKILLS':'Machine Learning,Python,GIT,JIRA', 'EXPERIENCE':'6+ year'}]
        resume_df = pd.DataFrame.from_dict(resume_data)
       
        # JOb Description data and create dataframe
        jd_data = [{"SKILLS":'JAVA,Machine Learning,Python,GIT,JIRA,JUNIT','EXPERIENCE':'1+ year'}]
        jd_df = pd.DataFrame.from_dict(jd_data,orient = 'columns') 
        """
        final_data = rank.main(resume_df, jd_df)
        output = []
        for index, row in final_data.iterrows():
            output.append(dict(row))
        return jsonify(output)
        #return render_template('resume.html')

api.add_resource(extract_R,'/uploads_resume', methods=['POST']) 
api.add_resource(extract_JD,'/uploads_jd', methods=['POST']) 
api.add_resource(ranking,'/resume_checker')

if __name__ == '__main__':
    app.run(debug=True) 