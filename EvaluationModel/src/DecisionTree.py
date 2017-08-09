#coding:utf-8

'''
    决策树构建过程
'''

import MalProbability
from sklearn import tree
from sklearn import cross_validation
import csv
import sys

def build_decision_tree(filename):
    """
        返回训练好的决策树和其准确率
    """
    f=open(sys.argv[1],'r')
    reader=csv.reader(f)
    x=[]
    y=[]
    for line in reader:
        if line[1] in ['1','2','3']:#来自权威检测,且可用于训练
            x.append(line[2:4]+line[5:])
            y.append(line[1])
    x_train,x_test,y_train,y_test=cross_validation.train_test_split(x,y, test_size=0.2, random_state=42)
    clf=tree.DecisionTreeClassifier(max_depth=5)
    clf=clf.fit(x_train,y_train)
    score=clf.score(x_test,y_test)
    print score
    return clf,score

def predict(domain,tree):
    f=MalProbability.get_domain_features(domain)
    return tree.predict([f[0:2]+f[3:]])

def main():
    tree,score=build_decision_tree(sys.argv[1])
    for _ in range(10):
        # print predict("ucoz.org",tree)
        print predict("95533zr.cc",tree)


if __name__=="__main__":
    main()
