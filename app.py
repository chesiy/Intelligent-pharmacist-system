from flask import Flask,render_template
from flask import request,redirect,url_for
from flask_wtf import FlaskForm
from my_neo import get_drug,get_drug_from_product,get_drug_from_symptom
from wtforms import StringField,SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

class symptomForm(FlaskForm):
    sympt_name=StringField('病症:',validators=[DataRequired()])
    submit1=SubmitField('提交')

class scriptForm(FlaskForm):
    sympt_name2=StringField('病症：',validators=[DataRequired()])
    people_age = SelectField('年龄段', choices=[(1,'成人'), (2,'儿童')], validators=[DataRequired('请选择年龄段')])
    specific_people=SelectField('特殊人群',choices=[(1,'哺乳期妇女'),(2,'过敏患者'),(3,'妊娠期妇女'),(4,'老年人'),(5,'未成年人'),(6,'未成熟儿'),(7,'新生儿'),(8,'孕妇'),(9,'早产儿')])
    diseases = StringField('基础疾病')
    product1_name=StringField('药品1:',validators=[DataRequired()])
    product2_name=StringField('药品2:')
    product3_name = StringField('药品3:')
    frequency1 = IntegerField('一日',render_kw={'size':"2"})
    frequency2 = IntegerField('一日',render_kw={'size':"2"})
    frequency3 = IntegerField('一日',render_kw={'size':"2"})
    fre1=IntegerField('每几小时一次',render_kw={'size':"2"})
    fre2 = IntegerField('每几小时一次',render_kw={'size':"2"})
    fre3 = IntegerField('每几小时一次',render_kw={'size':"2"})
    amount1=IntegerField('一次',render_kw={'size':"2"})
    amount2=IntegerField('一次',render_kw={'size':"2"})
    amount3 = IntegerField('一次',render_kw={'size':"2"})
    usage1=SelectField('用法',choices=[(1,'口服'),(2,'注射')],validators=[DataRequired('请选择用法')])
    usage2=SelectField('用法',choices=[(1,'口服'),(2,'注射')])
    usage3 = SelectField('用法',choices=[(1,'口服'),(2,'注射')])

    submit2=SubmitField('提交处方')

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
        product_name=[]
        product_use=[]
        product_name.append(script_form.product1_name.data)
        product_name.append(script_form.product2_name.data)
        product_name.append(script_form.product3_name.data)
        product_use.append(script_form.product1_useage.data)
        product_use.append(script_form.product2_useage.data)
        product_use.append(script_form.product3_useage.data)

        product_num=0
        for onename in product_name:
            if onename!='':
                product_num= product_num+1

        SuitableDrugs=get_drug_from_symptom(symp2_name)

        cnt=0
        for oneproductname in product_name:
            for onedrug in get_drug_from_product(oneproductname):
                if onedrug in SuitableDrugs:
                    cnt=cnt+1

        if cnt==product_num:
            return 'success'
        return 'fail'

    return render_template('Check_script.html',scri_form=script_form)

@app.route('/drugs/?<string:symp_name>')
def getdrug(symp_name):
    drug_result,product_result = get_drug(symp_name)
    return render_template('suitable_drugs.html', drug_result=drug_result,product_result=product_result)

if __name__  ==  '__main__':
    app.run()
