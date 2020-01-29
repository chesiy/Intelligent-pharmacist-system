from flask import Flask,render_template
from flask import request,redirect,url_for
from flask_wtf import FlaskForm
from my_neo import get_drug
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

class symptomForm(FlaskForm):
    sympt_name=StringField('Symptom:',validators=[DataRequired()])
    submit1=SubmitField('SUBMIT SYMPTOM')

class scriptForm(FlaskForm):
    sympt_name2=StringField('Symptom:',validators=[DataRequired()])
    drug1_name=StringField('Drug1:',validators=[DataRequired()])
    drug2_name=StringField('Drug2:',validators=[DataRequired()])
    submit2=SubmitField('SUBMIT SCRIPT')

@app.route('/',methods=['POST','GET'])
def homepage():
    return render_template('home.html')

@app.route('/SearchDrug',methods=['POST','GET'])
def searchDrug():
    symptom_form = symptomForm()
    if request.method == 'POST':
        symp_name = symptom_form.sympt_name.data
        return redirect(url_for('getdrug',symp_name=symp_name))
    return render_template('Search_drug.html',symp_form=symptom_form)

@app.route('/CheckScript',methods=['POST','GET'])
def checkScript():
    script_form = scriptForm()
    if request.method=='POST':
        symp2_name = script_form.sympt_name2.data
        drug1_name =script_form.drug1_name.data
        drug2_name=script_form.drug2_name.data

        SuitableDrugs=get_drug(symp2_name)
        if (drug1_name in SuitableDrugs) and (drug2_name in SuitableDrugs):
            return 'Success'
        else:
            return 'Fail'

    return render_template('Check_script.html',scri_form=script_form)

@app.route('/drugs/?<string:symp_name>')
def getdrug(symp_name):
    drug_result = get_drug(symp_name)
    print('*****************')
    print(drug_result)
    return render_template('suitable_drugs.html', drug_result=drug_result)


if __name__  ==  '__main__':
    app.run()
