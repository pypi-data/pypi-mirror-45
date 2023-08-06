# coding: utf-8
# 因素空间模块

import os
import numpy as np
import itertools

#####################################

#阶乘函数
def func(n):
    if n == 0 or n == 1:
        return 1
    else:
        return (n * func(n - 1))

#####################################

#读取UCI数据集
def load_uci(filename,start_index=2):

    #判断文件不存在
    if not os.path.exists(filename):  
        print("ERROR: file not exit: %s" % (filename))  
        return None  

    #判断不是文件
    if not os.path.isfile(filename):  
        print("ERROR: %s not a filename." % (filename))  
        return None  

    #定义变量  
    data = []
    label = []
    file = open(filename)
    si=start_index-1

    #生成数据集
    for line in file:
        line = line.strip('\n')
        line = line.replace(',?',',nan')
        split_data = line.split(',')
        data_len=len(split_data)-start_index+1
        data.append(list(map(float,split_data[si:data_len])))
        label.append(float(split_data[-1]))

    #返回数据集
    file.close()  
    data = np.array(data)
    label = np.array(label)
    return data,label

#####################################

#精度
def accuracy(rules_set,test_data,test_label,none_value=-1,reverse=False,number=False):

    #定义变量
    correct=0
    total=0

    #遍历测试数据
    for i in range(len(test_data)):

        #进行规则推理
        if predict(rules_set,test_data[i],none_value=none_value,reverse=reverse)==test_label[i]:
            correct+=1
        total+=1

    #判断返回正确数量    
    if number==True:
        return correct

    #返回精度
    return correct/total

    

#####################################

#规则推理
def predict(rules_set,data,none_value=-1,reverse=False):

    #定义临时变量
    np_data=np.asarray(data)    
    count=len(rules_set)
    
    #判断反向规则集推理
    if reverse==True:
        reverse_count=count

        #遍历规则集
        for i in range(count):
            reverse_count-=1
            rule=np.asarray(rules_set[reverse_count])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[reverse_count][-1]    
    else:

        #遍历规则集
        for i in range(count):
            rule=np.asarray(rules_set[i])
            rule=np.delete(rule,-1)

            #返回匹配结果
            if np.sum(np_data==rule)==np.sum(rule!=none_value):
                return rules_set[i][-1]
    

#####################################

#整理数据集
def clean_data(train_data,train_label,data_num=-1):

    #数据集去重
    train_data=np.array(train_data)
    train_label=np.array(train_label)
    train_data,indexes=np.unique(train_data,axis=0,return_index=True)
    train_label=train_label[indexes]

    #返回数据集
    if data_num<=0:
        return train_data,train_label

    #随机返回部分数据集
    if data_num<=len(train_data):
        batch_mask = np.random.choice(len(train_data), data_num, replace=False)
        train_data = train_data[batch_mask]
        train_label = train_label[batch_mask]
        return train_data,train_label

    #随机返回重复数据集
    if data_num>len(train_data):
        batch_mask = np.random.choice(len(train_data), data_num, replace=True)
        train_data = train_data[batch_mask]
        train_label = train_label[batch_mask]
        return train_data,train_label
        
        

#####################################

#最大规则算法
def max_rules(train_data,train_label,none_value=-1,train_times=10000,used_factors=False,full_rules=False,strict=False,expand=False,rules_sort=False):

    #初始化变量
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    trained_factors=np.array([])
    used_factor_set=np.array([])
    delete_list=[]
    rule=[none_value]*(factor_num+1)
    rules_set=[]
    decide_data=np.full(data.shape,none_value)
    decide_label=np.full(label.shape,none_value)

    #判断不启用全规则算法
    if full_rules==False:
        
        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            decide_data=np.full(data.shape,none_value)
            decide_label=np.full(label.shape,none_value)
            final_count=len(used_factor_set)
            
            #生成因素分类构建决定表    
            for j in range(factor_num):
                factor_classes=[]

                #按照一个因素分类
                for k in np.unique(data[:,j]):
                    factor_classes.append(np.where(data[:,j]==k))

                #遍历一个因素的每个类
                for k in range(len(factor_classes)):

                    #判断一个类是决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #构建收敛表和决定表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])
                            decide_data[factor_classes[k][0][l]][j]=data[factor_classes[k][0][l]][j]
                            decide_label[factor_classes[k][0][l]]=label[factor_classes[k][0][l]]

            #遍历全部因素组合数量
            for j in range(1,factor_num+1):
                rules=[]

                #遍历决定表
                for k in range(len(decide_data)):
                    data_factor_use=np.where(decide_data[k]!=none_value)[0]
                    decide_num=len(data_factor_use)

                    #判断无生成规则
                    if decide_num==0:
                        continue

                    #构建当前数据所有组合                    
                    combinations=list(itertools.combinations(data_factor_use,j))
                    
                    #遍历所有组合
                    for l in combinations:
                        factor_count=len(l)
                        rule=[none_value]*(factor_num+1)

                        #判断严格规则集
                        if strict==False:
                        
                        #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]
                                trained_factors=np.append(trained_factors,l[m])
                                trained_factors=np.unique(trained_factors)

                            #加入生成规则    
                            rules.append(rule.copy())

                        else:

                            #停止扩大规则集
                            expand=False
                            
                            #生成之前因素规则
                            for m in range(final_count):
                                rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                            #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]
                                trained_factors=np.append(trained_factors,l[m])
                                trained_factors=np.unique(trained_factors)

                            #加入生成规则    
                            rules.append(rule.copy())
                            

                        #判断扩大规则集
                        if expand==True:

                            #生成之前因素规则
                            for m in range(final_count):
                                rule[int(used_factor_set[m])] = data[k][int(used_factor_set[m])]

                            #生成当前因素规则
                            for m in range(factor_count):
                                rule[l[m]]=decide_data[k][l[m]]
                                rule[-1]=decide_label[k]

                            #加入生成规则    
                            rules.append(rule.copy())

                #判断无规则生成        
                if len(rules)==0:
                    break

                #构建规则集
                rules=(np.unique(rules,axis=0)).tolist()
                rules_set+=rules                    
                    
            #构建约简因素集和收敛数据    
            used_factor_set=np.append(used_factor_set,trained_factors)
            used_factor_set=np.unique(used_factor_set)
            data=np.delete(data,delete_list,axis=0)
            label=np.delete(label,delete_list,axis=0)

            #判断收敛完成
            if len(data)==0:
                break

            #判断无法收敛改用全规则算法
            if len(data)==last_data_num:
                print('use full rules instead')
                data=np.array(train_data)
                label=np.array(train_label)
                rules_set=[]
                full_rules=True
                break

                   

        

    #判断使用全规则算法
    if full_rules==True:
        
        #遍历每一个因素
        for i in range(factor_num):
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,i+1))

            #构建每一种因素组合
            for j in combinations:
                factor_classes=[]
                factor_count=len(j)
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,j[k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #生成推理规则
                        for l in range(factor_count):
                            rule[j[l]]=data[factor_classes[k][0][0]][j[l]]
                            rule[-1]=label[factor_classes[k][0][0]]

                        #构建推理规则集    
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])

        #生成约简因素集
        used_factor_set=factor_index

    #判断规则库排序
    if rules_sort==True:
        rules_set=np.array(rules_set)
        rules_set=np.unique(rules_set,axis=0)
        order_index=[0]*len(rules_set)

        #生成排序索引
        for i in range(len(order_index)):
            order_index[i]=np.sum(rules_set[i]!=none_value)

        #生成排序规则库
        rules_set=rules_set[np.argsort(order_index)].tolist()
    
    
    #判断返回约简因素集
    if(used_factors==True):
        return rules_set,used_factor_set
   
    #返回规则集
    return rules_set

#####################################

#差转算法
def sub_rotate(train_data,train_label,none_value=-1,train_times=10000,used_factors=False,fast=False):

    #初始化变量
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    trained_factors=np.array([])
    used_factor_set=np.array([])
    delete_list=[]
    rule=[none_value]*(factor_num+1)
    rules_set=[]

    #判断不使用快速收敛
    if fast==False:
        comb_num=1
        #comb_total=func(factor_num)/(func(factor_num-comb_num)*func(comb_num))
        #decide_num=[0]*com_total

        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            final_count=len(used_factor_set)            
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,comb_num))
            decide_num=[0]*len(combinations)

            #构建因素组合
            for j in range(len(combinations)):
                delete_list=[]
                factor_classes=[]
                factor_count=len(combinations[j])
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,combinations[j][k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:
                        decide_num[j]+=len(label[factor_classes[k]])

            #定位核因素
            argmax=np.argmax(decide_num)

            #启动多因素组合分类
            if decide_num[argmax]==0:
                comb_num+=1
                print('use more factors')
                continue

            #生成一条规则    
            delete_list=[]
            factor_classes=[]
            factor_count=len(combinations[argmax])
            factor_value=[0.]*len(data)
            factor_value=np.array(factor_value)
            rule=[none_value]*(factor_num+1)
            
            #确定分类值
            for k in range(factor_count):
                factor_value+=data[:,combinations[argmax][k]]**(1/(k+1))

            #构建分类表
            for k in np.unique(factor_value):
                factor_classes.append(np.where(factor_value==k))

            #遍历分类表
            for k in range(len(factor_classes)):

                #判断决定类
                if len(np.unique(label[factor_classes[k]]))==1:

                    #生成推理规则
                    for l in range(factor_count):
                        rule[combinations[argmax][l]]=data[factor_classes[k][0][0]][combinations[argmax][l]]
                        rule[-1]=label[factor_classes[k][0][0]]
                        trained_factors=np.append(trained_factors,combinations[argmax][l])
                        trained_factors=np.unique(trained_factors)

                    #构建推理规则集    
                    rules_set.append(rule.copy())

                    #构建收敛集
                    for l in range(len(factor_classes[k][0])):
                        delete_list.append(factor_classes[k][0][l])

            #收敛数据
            if len(delete_list)!=0:
                used_factor_set=np.append(used_factor_set,trained_factors)
                used_factor_set=np.unique(used_factor_set)
                data=np.delete(data,delete_list,axis=0)
                label=np.delete(label,delete_list,axis=0)
                if comb_num>1:
                    comb_num=1

            #判断收敛完成        
            if len(data)==0:
                break

    #判断使用快速收敛
    if fast==True:
        comb_num=1
        
        #一次数据收敛
        for i in range(train_times):
            delete_list=[]
            trained_factors=np.array([])
            last_data_num=len(data)
            final_count=len(used_factor_set)            
            factor_index=list(range(factor_num))
            combinations=list(itertools.combinations(factor_index,comb_num))

            #构建因素组合
            for j in combinations:
                delete_list=[]
                factor_classes=[]
                factor_count=len(j)
                factor_value=[0.]*len(data)
                factor_value=np.array(factor_value)
                rule=[none_value]*(factor_num+1)

                #确定分类值
                for k in range(factor_count):
                    factor_value+=data[:,j[k]]**(1/(k+1))

                #构建分类表
                for k in np.unique(factor_value):
                    factor_classes.append(np.where(factor_value==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:

                        #生成推理规则
                        for l in range(factor_count):
                            rule[j[l]]=data[factor_classes[k][0][0]][j[l]]
                            rule[-1]=label[factor_classes[k][0][0]]
                            trained_factors=np.append(trained_factors,j[l])
                            trained_factors=np.unique(trained_factors)

                        #构建推理规则集    
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])

                #收敛数据
                if len(delete_list)!=0:
                    used_factor_set=np.append(used_factor_set,trained_factors)
                    used_factor_set=np.unique(used_factor_set)
                    data=np.delete(data,delete_list,axis=0)
                    label=np.delete(label,delete_list,axis=0)
                    if comb_num>1:
                        comb_num=1
                        break

            #启动多因素组合分类
            if last_data_num==len(data):
                comb_num+=1
                print('use more factors')

            #判断收敛完成   
            if len(data)==0:
                break
                
                
    #判断返回约简因素集
    if(used_factors==True):
        return rules_set,used_factor_set
   
    #返回规则集
    return rules_set
                


#####################################

def factor_analy(train_data,train_label,none_value=-1,train_times=10000,used_factors=False):

    #初始化变量
    data=np.array(train_data)
    label=np.array(train_label)
    factor_num=data.shape[1]
    factor_classes=[]
    trained_factors=np.array([])
    used_factor_set=np.array([])
    delete_list=[]
    rule=[none_value]*(factor_num+1)
    rules_set=[]
    class_num=1

    #一次数据收敛
    for i in range(train_times):
        delete_list=[]
        final_count=len(used_factor_set)            
        decide_num=[0]*factor_num

        #判断第一次收敛
        if len(trained_factors)==0:

            #构建因素组合
            for j in range(factor_num):
                delete_list=[]
                factor_classes=[]
                rule=[none_value]*(factor_num+1)

                #构建分类表
                for k in np.unique(data[:,j]):
                    factor_classes.append(np.where(data[:,j]==k))

                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label[factor_classes[k]]))==1:
                        decide_num[j]+=len(label[factor_classes[k]])

            #定位核因素
            argmax=np.argmax(decide_num)
            
            #生成规则        
            delete_list=[]
            factor_classes=[]
            rule=[none_value]*(factor_num+1)

            #构建分类表
            for k in np.unique(data[:,argmax]):
                factor_classes.append(np.where(data[:,argmax]==k))

            #遍历分类表
            for k in range(len(factor_classes)):

                #判断决定类
                if len(np.unique(label[factor_classes[k]]))==1:
                    rule[argmax]=data[factor_classes[k][0][0]][argmax]
                    rule[-1]=label[factor_classes[k][0][0]]
                    trained_factors=np.append(trained_factors,argmax)
                    trained_factors=np.unique(trained_factors)

                    #构建推理规则集    
                    rules_set.append(rule.copy())

                    #构建收敛表
                    for l in range(len(factor_classes[k][0])):
                        delete_list.append(factor_classes[k][0][l])

            #收敛数据
            if len(delete_list)!=0:                
                data=np.delete(data,delete_list,axis=0)
                label=np.delete(label,delete_list,axis=0)

            #生成约简因素集
            used_factor_set=np.append(used_factor_set,trained_factors)
            used_factor_set=np.unique(used_factor_set)
                              
            #判断收敛完成
            if len(data)==0:
                break

        else:

            #定义上一次核因素分类变量
            last_classes=[]
            
            #构建上一次核因素分类
            for j in np.unique(data[:, int(trained_factors[0])]):
                last_classes.append(np.where(data[:,int(trained_factors[0])]==j))

            #定义部分数据集
            class_num=len(last_classes)
            data_part=[0]*class_num
            label_part=[0]*class_num
            
            #创建部分数据集
            for j in range(class_num):
                data_part[j]=data[last_classes[j]]
                label_part[j]=label[last_classes[j]]

            #遍历每一部分数据集
            for j in range(class_num):

                #构建因素组合
                for k in range(factor_num):
                    delete_list=[]
                    factor_classes=[]
                    rule=[none_value]*(factor_num+1)
                    
                    #构建分类表
                    for l in np.unique(data_part[j][:,k]):
                        factor_classes.append(np.where(data_part[j][:,k]==l))
                        
                    #遍历分类表
                    for l in range(len(factor_classes)):

                        #判断决定类
                        if len(np.unique(label_part[j][factor_classes[l]]))==1:
                            decide_num[k]+=len(label_part[j][factor_classes[l]])

            #定位核因素
            argmax=np.argmax(decide_num)
            
            #遍历每一部分数据集
            for j in range(class_num):
                delete_list=[]
                factor_classes=[]
                rule=[none_value]*(factor_num+1)

                #构建分类表
                for k in np.unique(data_part[j][:,argmax]):
                    factor_classes.append(np.where(data_part[j][:,argmax]==k))
                    
                #遍历分类表
                for k in range(len(factor_classes)):

                    #判断决定类
                    if len(np.unique(label_part[j][factor_classes[k]]))==1:
                        
                        #生成之前因素规则
                        for l in range(final_count):
                            rule[int(used_factor_set[l])] = data_part[j][factor_classes[k][0][0]][int(used_factor_set[l])]

                        #生成当前因素规则
                        rule[argmax]=data_part[j][factor_classes[k][0][0]][argmax]
                        rule[-1]=label_part[j][factor_classes[k][0][0]]
                        trained_factors=np.append(trained_factors,argmax)
                        trained_factors=np.unique(trained_factors)

                        #构建推理规则集    
                        rules_set.append(rule.copy())

                        #构建收敛表
                        for l in range(len(factor_classes[k][0])):
                            delete_list.append(factor_classes[k][0][l])
                        
                #收敛数据
                if len(delete_list)!=0:                    
                    data_part[j]=np.delete(data_part[j],delete_list,axis=0)
                    label_part[j]=np.delete(label_part[j],delete_list,axis=0)
                
            #定义初始完整数据
            data=data_part[0]
            label=label_part[0]

            #组合完整数据
            for j in range(1,class_num):
                data=np.append(data,data_part[j],axis=0)
                label=np.append(label,label_part[j],axis=0)

            #生成约简因素集
            used_factor_set=np.append(used_factor_set,trained_factors)
            used_factor_set=np.unique(used_factor_set)            
                    
            #判断收敛完成
            if len(data)==0:
                break       

    #判断返回约简因素集
    if(used_factors==True):
        return rules_set,used_factor_set
   
    #返回规则集
    return rules_set



###############################################################################
