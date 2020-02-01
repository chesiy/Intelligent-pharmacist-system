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
    product_num=IntegerField('药品数量',render_kw={'size':"2"})
    people_age = SelectField('年龄段', choices=[(1,'成人'), (2,'儿童')], validators=[DataRequired('请选择年龄段')])
    specific_people=SelectField('特殊人群',choices=[(0,'否'),(1,'哺乳期妇女'),(2,'过敏患者'),(3,'妊娠期妇女'),(4,'老年人'),(5,'未成年人'),(6,'未成熟儿'),(7,'新生儿'),(8,'孕妇'),(9,'早产儿')])
    diseases = StringField('基础疾病')
    product_name=[StringField('药品:')]*5
    frequency=[IntegerField('一日',render_kw={'size':"2"})]*5
    fre=[IntegerField('每几小时一次',render_kw={'size':"2"})]*5
    amount1=[IntegerField('一次',render_kw={'size':"2"})]*5 #一日几次的
    amount2 = [IntegerField('一次', render_kw={'size': "2"})] * 5  #每几小时一次的
    usage=[SelectField('用法',choices=[(1,'口服'),(2,'注射')])]*5

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
        true_product_num=script_form.product_num
        product_name=[]
        product_use=[] #口服/注射
        product_name.append(script_form.product1_name.data)
        product_name.append(script_form.product2_name.data)
        product_name.append(script_form.product3_name.data)
        product_use.append(script_form.usage1.data)
        product_use.append(script_form.usage2.data)
        product_use.append(script_form.usage3.data)
        print('@@@@@@@@@@@@@@@@@@@@@@@')
        print(product_use)
        product_num=0
        for onename in product_name:
            if onename!='':
                product_num= product_num+1
        if product_num!=true_product_num:
            return '验证失败，填写的处方中药品数目与实际提交的药品数目不符'

        SuitableDrugs=get_drug_from_symptom(symp2_name)

        cnt=0
        for oneproductname in product_name:
            if product_use[oneproductname.index()]== 1:#口服
                product_frequency=script_form.frequency1
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
    app.run(debug=True)
