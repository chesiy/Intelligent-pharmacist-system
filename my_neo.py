from py2neo import Node, Graph, Relationship, NodeMatcher, RelationshipMatcher

def get_drug_product(drugname):  #由药物名查询药品
    graph=Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:其产品]->(Product) return Product.name,Product.size'
    print(str)
    result_list = list(graph.run(str).data())
    result_product=[]
    for results in result_list:
        result_product.append('药品名称：'+results['Product.name']+' 制剂规格：'+results['Product.size'])
    return result_product

def get_drug(symptomname):  # 由疾病名称查询对症药物
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    # nodematcher=NodeMatcher(graph)
    # relamatcher=RelationshipMatcher(graph)
    # node=nodematcher.match('symptom',name=symptomname).first()#找到了该疾病
    # relamatcher.match((node,),r_type='适用于')

    str = 'MATCH a=(symptom{name:\'' + symptomname + '\'})-[:可使用]->(drug) return drug.name'
    print(str)
    result_list = list(graph.run(str).data())
    result_drug=[]
    products={}

    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
        products[oneresult['drug.name']]=get_drug_product(oneresult['drug.name'])
    print(products)
    return result_drug,products
