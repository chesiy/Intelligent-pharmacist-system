from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_wtf import FlaskForm
from my_neo import get_drug, get_drug_from_product, get_drug_from_symptom, get_usage_from_product
from wtforms import StringField, SubmitField, SelectField, IntegerField,FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


class symptomForm(FlaskForm):
    sympt_name = StringField('病症:', validators=[DataRequired()])
    submit1 = SubmitField('提交')


class scriptForm(FlaskForm):
    sympt_name2 = StringField('病症：', validators=[DataRequired()])
    product_num = IntegerField('药品数量', render_kw={'size': "2"})
    people_age = SelectField('年龄段', choices=[(1, '成人'), (2, '儿童')], validators=[DataRequired('请选择年龄段')])
    specific_people = SelectField('特殊人群',
                                  choices=[(0, '否'), (1, '哺乳期妇女'), (2, '过敏患者'), (3, '妊娠期妇女'), (4, '老年人'), (5, '未成年人'),
                                           (6, '未成熟儿'), (7, '新生儿'), (8, '孕妇'), (9, '早产儿')])
    diseases = StringField('基础疾病')

    product1_name = StringField('药品1:')
    frequency1 = IntegerField('一日', render_kw={'size': "2"})
    fre1 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount11 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount21 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage1 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    product2_name = StringField('药品2:')
    frequency2 = IntegerField('一日', render_kw={'size': "2"})
    fre2 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount12 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount22 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage2 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    product3_name = StringField('药品3:')
    frequency3 = IntegerField('一日', render_kw={'size': "2"})
    fre3 = IntegerField('每几小时一次', render_kw={'size': "2"})
    amount13 = FloatField('一次', render_kw={'size': "2"})  # 一日几次的
    amount23 = FloatField('一次', render_kw={'size': "2"})  # 每几小时一次的
    usage3 = SelectField('用法',
                         choices=[(1, '口服'), (2, '注射'), (3, '静脉注射'), (4, '静脉滴注'), (5, '快速静脉注射'), (6, '吸入'), (7, '喷雾'),
                                  (8, '外用')])

    submit2 = SubmitField('提交处方')


@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('home.html')


@app.route('/SearchDrug', methods=['POST', 'GET'])
def searchDrug():
    symptom_form = symptomForm()
    if request.method == 'POST':
        symp_name = symptom_form.sympt_name.data
        return redirect(url_for('getdrug', symp_name=symp_name))
    return render_template('Search_drug.html', symp_form=symptom_form)


@app.route('/CheckScript', methods=['POST', 'GET'])
def checkScript():
    script_form = scriptForm()
    if request.method == 'POST':
        symp2_name = script_form.sympt_name2.data
        true_product_num = script_form.product_num.data
        product_name = []
        product_use = []  # 口服/注射
        product_frequency = []
        product_amount1 = []
        product_fre = []
        product_amount2 = []
        product_name.append(script_form.product1_name.data)
        product_name.append(script_form.product2_name.data)
        product_name.append(script_form.product3_name.data)
        str = ['口服', '注射', '静脉注射', '静脉滴注', '快速静脉注射', '吸入', '喷雾', '外用']
        product_use.append(str[int(script_form.usage1.data) - 1])
        product_use.append(str[int(script_form.usage2.data) - 1])
        product_use.append(str[int(script_form.usage3.data) - 1])
        product_frequency.append(script_form.frequency1.data)
        product_frequency.append(script_form.frequency2.data)
        product_frequency.append(script_form.frequency3.data)
        product_amount1.append(script_form.amount11.data)
        product_amount1.append(script_form.amount12.data)
        product_amount1.append(script_form.amount13.data)
        product_fre.append(script_form.fre1.data)
        product_fre.append(script_form.fre2.data)
        product_fre.append(script_form.fre3.data)
        product_amount2.append(script_form.amount21.data)
        product_amount2.append(script_form.amount22.data)
        product_amount2.append(script_form.amount23.data)

        product_num = 0
        for onename in product_name:
            if onename != '':
                product_num = product_num + 1
        if product_num != true_product_num:
            return '验证失败，填写的处方中药品数目与实际提交的药品数目不符'

        SuitableDrugs = get_drug_from_symptom(symp2_name)

        cnt = 0
        for oneproductname in product_name:
            if not ((product_amount1 != '' and product_frequency != '') or (
                    product_amount2 != '' and product_fre != '')):
                return '验证失败，用量信息未填写完整'
            for onedrug in get_drug_from_product(oneproductname):  # 验证药品与疾病是否对应
                if onedrug in SuitableDrugs:
                    cnt = cnt + 1
        if cnt != product_num:
            return '验证失败，处方中的药品不应被用于治疗该疾病'

        for oneproductname in product_name:  # 验证用法用量是否正确
            if (oneproductname != ''):
                Usage = get_usage_from_product(oneproductname)
                if Usage['usage'] == product_use[product_name.index(oneproductname)]:  # 用法

                    if Usage['frequency'] != None and Usage['frequency'][0] == '一':
                        index1 = Usage['frequency'].find('日')
                        index2 = Usage['frequency'].find('次')
                        result = Usage['frequency'][index1 + 1:index2]
                        index3 = -1
                        if Usage['frequency'].find('-') != -1:  # 解决有些是~，有些是-
                            index3 = Usage['frequency'].find('-')
                        elif Usage['frequency'].find('～') != -1:
                            index3 = Usage['frequency'].find('～')
                        if index3 == -1:  # 一个数字的情况  #频率
                            if int(result) != product_frequency[product_name.index(oneproductname)]:
                                return '验证失败，处方中药品的用药频率有误'
                            else:
                                print('pass frequency1')
                        elif not (int(result[0:index3]) <= product_frequency[product_name.index(oneproductname)] <= int(
                                result[index3 + 1:])):  # a-b的情况
                            return '验证失败，处方中药品的用药频率有误'
                        else:
                            print('pass frequency2')

                        if Usage['consumption'] != None and Usage['consumption'][0] != '':  # 用量
                            index = Usage['consumption'].find('/')
                            index_1 = -1
                            if Usage['consumption'].find('-') != -1: #这里的-需改为中文！！！！！！！！
                                index_1 = Usage['consumption'].find('-')
                            elif Usage['consumption'].find('～') != -1:
                                index_1 = Usage['consumption'].find('～')
                            if index == -1:  # 没有/kg/日
                                mg_index = Usage['consumption'].find('mg')
                                if mg_index != -1:  # 单位为mg
                                    result = Usage['consumption'][0:mg_index]
                                    if index_1 == -1 and float(result) != product_amount1[
                                        product_name.index(oneproductname)]:
                                        return '验证失败，处方中药品的用量有误'
                                    elif index_1 != -1 and not (float(result[0:index_1]) <= product_amount1[
                                        product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                        return '验证失败，处方中药品的用量有误'
                                else:
                                    g_index = Usage['consumption'].find('g')  # 单位为g
                                    if g_index != -1:
                                        result = Usage['consumption'][0:g_index]
                                        if index_1 == -1 and float(result) * 1000 != product_amount1[
                                            product_name.index(oneproductname)]:
                                            return '验证失败，处方中药品的用量有误'
                                        elif index_1 != -1 and not (float(result[0:index_1]) * 1000 <= product_amount1[
                                            product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                            return '验证失败，处方中药品的用量有误'

                    elif Usage['frequency'] != None and Usage['frequency'][0] == '每':
                        index1 = Usage['frequency'].find('每')
                        index2 = Usage['frequency'].find('小')
                        result = Usage['frequency'][index1 + 1:index2]
                        index3 = -1
                        if Usage['frequency'].find('-') != -1:  # 解决有些是~，有些是-
                            index3 = Usage['frequency'].find('-')
                        elif Usage['frequency'].find('～') != -1:
                            index3 = Usage['frequency'].find('～')
                        if index3 == -1:  # 一个数字的情况  #频率
                            if int(result) != product_fre[product_name.index(oneproductname)]:
                                return '验证失败，处方中药品的用药频率有误'
                            else:
                                print('pass fre1')
                        elif not (int(result[0:index3]) <= product_fre[product_name.index(oneproductname)] <= int(
                                result[index3 + 1:])):  # a-b的情况
                            return '验证失败，处方中药品的用药频率有误'
                        else:
                            print('pass fre2')

                        if Usage['consumption'] != None and Usage['consumption'][0] != '':  # 用量
                            index = Usage['consumption'].find('/')
                            index_1 = -1
                            if Usage['consumption'].find('-') != -1:  # 这里的-需改为中文！！！！！！！！
                                index_1 = Usage['consumption'].find('-')
                            elif Usage['consumption'].find('～') != -1:
                                index_1 = Usage['consumption'].find('～')

                            if index == -1:  # 没有/kg/日
                                mg_index = Usage['consumption'].find('mg')
                                if mg_index != -1:  # 单位为mg
                                    result = Usage['consumption'][0:mg_index]
                                    if index_1 == -1 and float(result) != product_amount2[
                                        product_name.index(oneproductname)]:
                                        return '验证失败，处方中药品的用量有误'
                                    elif index_1 != -1 and not (float(result[0:index_1]) <= product_amount2[
                                        product_name.index(oneproductname)] <= float(result[index_1 + 1:])):
                                        return '验证失败，处方中药品的用量有误'
                                else:
                                    g_index = Usage['consumption'].find('g')  # 单位为g
                                    if g_index != -1:
                                        result = Usage['consumption'][0:g_index]
                                        if index_1 == -1 and float(result) * 1000 != product_amount2[
                                            product_name.index(oneproductname)]:
                                            return '验证失败，处方中药品的用量有误'
                                        elif index_1 != -1 and not (float(result[0:index_1]) * 1000 <= product_amount2[
                                            product_name.index((oneproductname))] <= float(result[index_1 + 1:])):
                                            return '验证失败，处方中药品的用量有误'
                else:
                    return '验证失败，用法错误'
        return '验证成功'
    return render_template('Check_script.html', scri_form=script_form)


@app.route('/drugs/?<string:symp_name>')
def getdrug(symp_name):
    drug_result, product_result = get_drug(symp_name)
    return render_template('suitable_drugs.html', drug_result=drug_result, product_result=product_result)


if __name__ == '__main__':
    app.run(debug=True)
