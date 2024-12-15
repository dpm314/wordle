# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:20:49 2024

@author: DrDave
"""
class Parent(Object):
    def __init__(self, parentName = 'BOB', childName = 'johnny'):
        self.parentName = parentName
        self.childName = childName

class Child(Parent):
    def __init__(self, childName):
        super().__init__()
        self.childName = childName
    def printMe(self):
        #print("I am child: {} \t super().parentName: {}".format(
        #        self.childName, super().parentName             )
        #        )
        print("I am child: {} \t self.parentName: {}".format(
                self.childName, super().parentName             )
                )

#%%
p = Parent(parentName='JEFF')
print(p.parentName)
print(p.childName )
#%%
p.printMe()


#%%
p.parentName = 'GARY'
print(p.parentName)
print(p.childName )
#%%
p.printMe()
