# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:59:07 2020

@author: alexandru.vesa
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.ref = None
        
    def __repr__(self):
        return self.data
        


class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.ref
        nodes.append("None")
        return " -> ".join(nodes)
    
    def easyCreate(self, nodes = None):
        if nodes is not None:
            #take out first element of the list and initialize the node
            node = Node(data = nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.ref = Node(data = elem)
                node = node.ref
                
    #Traverse or iterate through the nodes
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.ref
            
    def insertAtBeggining(self , node):
        node.ref = self.head
        self.head = node
    
    def insertAtFinal(self, node):
        #new_node = Node(node)
        if self.head is None:  #if the first Node is None
            self.head = node   #the first element become the node (we want to add) itself
            return
        n = self.head
        while n.ref is not None:
            n = n.ref
        n.ref =node
        
    def insertAfterSpecificNode(self, targetNode, newNode):
        #check if list is empty
        if not self.head:
            raise Exception ("List is empty")
        
        #go through the list 
        for node in self:
            if node.data == targetNode: #check if the node you want to use as ref exist
                newNode.ref = node.ref
                node.ref = newNode
                return
    
    def insertBeforeSpecificNode(self, targetNode, newNode):
        if not self.head:
            raise Exception("List is empty")
            
        prevNode = self.head
        for node in self:
            if node.data == targetNode:
                prevNode.ref = newNode
                newNode.ref = node
                return
            prevNode = node
        
    def insertAtSpecificIndex(self, index, newNode):
        
        n = self.head
        
        if index == 0 :
            return self.insertAtBeggining(newNode)
        
        while index > 1:
           n = n.ref
           index = index -1
        newNode.ref = n.ref
        n.ref = newNode
        
        #return n
        
        
    def reverse(self, head):
        head =self.head
        if (head ==None):
            return 
        
        self.reverse(head.ref)
            
            
            
        
    
def testLinkedList(node1 :str, node2 : str, node3 : str):
    llista = LinkedList()
    
    firstNode = Node(node1)
    llista.head = firstNode
    secondNode = Node(node2)
    firstNode.ref = secondNode
    thirdNode = Node(node3)
    secondNode.ref = thirdNode
    print(llista)
    
llista = LinkedList()
llista.easyCreate(['a','b','c'])
#node_to_add = Node('o')
#node_to_final = Node('e')
#llista.insertAtBeggining(node_to_add)
#llista.insertAtFinal(node_to_final)
llista.insertAfterSpecificNode("a", Node('aaaaa'))
llista.insertBeforeSpecificNode("b", Node('bbbb'))
llista.insertAtSpecificIndex(2, Node('fuck'))
llista.insertAtSpecificIndex(4, Node('Ion'))