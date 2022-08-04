# Import Libraries
import spacy
import pandas as pd
import fitz
import re
from datetime import date


#Check Email ID
def Emailcheck(email):
    Emailregex = '\S+@\S+'
    Email_address = re.findall(Emailregex, email)
    return Email_address

# Check Phone Number
def PhoneNumbercheck(phonenumber):
    PhoneRegrex = '\d{10}'
    Phone_number = re.findall(PhoneRegrex, phonenumber)
    return Phone_number

# Load Model
def LoadModel(modelName):
    NlpModel = spacy.load(modelName)
    return NlpModel


# Prediction Model
def prediction(nlp_model, resume_path):
    fname = resume_path
    doc = fitz.open(fname)
    text = ""
    for page in doc:
        text = text + str(page.get_text())
    tx = " ".join(text.split("\n"))
    string = tx.strip('\t')
    doc = nlp_model(tx)
    cols = []
    data = []
    for ent in doc.ents:
        # print(f"{ent.label_.upper():{30}}-{ent.text}")
        cols.append(ent.label_.upper())
        data.append(ent.text)

    # Email and phone number extraction
    Email = Emailcheck(string)
    PhoneNumber = PhoneNumbercheck(string)
    if len(Email) >= 1:
        cols.append("Email Address")
        data.append(Email[0])
    if len(PhoneNumber) >= 1:
        cols.append("Contact Number")
        data.append(PhoneNumber[0])

    # add current date
    current_date = date.today()
    cols.append("date")
    data.append(current_date)

    # Create data frame and save the data in dataframe
    em_df = pd.DataFrame(data, index=cols)

    return em_df.to_dict()


# Main Model
def main(Predtext):
    # path = "train_data.pkl"
    ModelPath = "train_model"
    NlpModel = LoadModel(ModelPath)
    FinalData = prediction(NlpModel, Predtext)
    return FinalData
