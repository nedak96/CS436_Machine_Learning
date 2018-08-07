from __future__ import division
import csv
import sys
import numpy as np
import math

# Node object fo the trees
class Node:
    def __init__(self):
        name = None
        left = None
        right = None
        more1s = None

# Safe logarithm function
def log2(x):
    if x == 0:
        return 0
    return math.log(x,2)

# Creates a tree using the Information Gain Heuristic
def cTree(node, data):
    n0s = 0
    n1s = 0
    nds = len(data)-1
    nns = len(data[0])-1
    for i in range(1,nds+1):
        if data[i][nns] == '0':
            n0s += 1
        else:
            n1s += 1
    if n0s == 0:
        node.name = 1
        return
    if n1s == 0:
        node.name = 0
        return
    if nns == 0:
        if n1s > n0s:
            node.name = 1
        else:
            node.name = 0
        return
    n = []
    for i in range(nns):
        i00 = 0
        i01 = 0
        i10 = 0
        i11 = 0
        for j in range(1, nds+1):
            d = data[j]
            if d[i] == '0':
                if d[nns] == '0':
                    i00 += 1
                else:
                    i01 += 1
            else:
                if d[nns] == '0':
                    i10 += 1
                else:
                    i11 += 1
        n.append((n0s/nds)*((i00/n0s)*log2(i00/n0s)+(i01/n0s)*log2(i01/n0s))+(n1s/nds)*((i10/n1s)*log2(i10/n1s)+(i11/n1s)*log2(i11/n1s)))
    ind = np.argmax(n)
    node.name = data[0][ind]
    if i01+i11 > i00+i10:
        node.more1s = True
    else:
         node.more1s = False
    datal = [x[:] for x in data if x[ind]=='0' or x[ind] == node.name]
    datar = [x[:] for x in data if x[ind]=='1' or x[ind] == node.name]
    for d in datal:
        del d[ind]
    for d in datar:
        del d[ind]
    node.left = Node()
    node.right = Node()
    cTree(node.left, datal)
    cTree(node.right, datar)

# Creates a tree using the Variance Impurity Heuristic
def cTree2(node, data):
    n0s = 0
    n1s = 0
    nds = len(data)-1
    nns = len(data[0])-1
    for i in range(1,nds+1):
        if data[i][nns] == '0':
            n0s += 1
        else:
            n1s += 1
    if n0s == 0:
        node.name = 1
        return
    if n1s == 0:
        node.name = 0
        return
    if nns == 0:
        if n1s > n0s:
            node.name = 1
        else:
            node.name = 0
        return
    n = []
    for i in range(nns):
        i00 = 0
        i01 = 0
        i10 = 0
        i11 = 0
        for j in range(1, nds+1):
            d = data[j]
            if d[i] == '0':
                if d[nns] == '0':
                    i00 += 1
                else:
                    i01 += 1
            else:
                if d[nns] == '0':
                    i10 += 1
                else:
                    i11 += 1
        n.append((n0s/nds)*((i00/n0s)*(i01/n0s))+(n1s/nds)*((i10/n1s)*(i11/n1s)))
    ind = np.argmin(n)
    node.name = data[0][ind]
    if i01+i11 > i00+i10:
        node.more1s = True
    else:
         node.more1s = False
    datal = [x[:] for x in data if x[ind]=='0' or x[ind] == node.name]
    datar = [x[:] for x in data if x[ind]=='1' or x[ind] == node.name]
    for d in datal:
        del d[ind]
    for d in datar:
        del d[ind]
    node.left = Node()
    node.right = Node()
    cTree2(node.left, datal)
    cTree2(node.right, datar)

# Function that prints a given tree
def print_tree(node, n):
    for i in range(n):
        print "|",
    print node.name + " = 0 : ",
    if node.left.name == 0 or node.left.name == 1:
        print node.left.name
    else:
        print ""
        print_tree(node.left, n+1)
    for i in range(n):
        print "|",
    print node.name + " = 1 : ",
    if node.right.name == 0 or node.right.name == 1:
        print node.right.name
    else:
        print ""
        print_tree(node.right, n+1)

# Function that returns the accuracy of a given data set
def res(node,data):
    numC = 0
    numD = len(data)-1
    for i in range(1,numD+1):
        d = data[i]
        nodet = node
        while True:
            if nodet.name == 0 or nodet.name == 1:
                break
            ind = data[0].index(nodet.name)
            if d[ind] == '0':
                nodet = nodet.left
            else:
                nodet = nodet.right
        if nodet.name == int(d[len(d)-1]):
            numC += 1
    return numC/numD

# Prune Helper function that returns the maximum accuracy associated with the changed node
def pruneH(root, node, data, n, maxn):
    oName = node.name
    if node.name != 0 and node.name != 1:
        if node.more1s:
            node.name = 1
        else:
            node.name = 0
        n1 = res(root, data)
        if n1 > n:
            n = n1
            maxn = node
        node.name = oName
        n1, maxn1 = pruneH(root, node.left, data, n, maxn)
        if n1 > n:
            n = n1
            maxn = maxn1
        n1, maxn1 = pruneH(root, node.right, data, n, maxn)
        if n1 > n:
            n = n1
            maxn = maxn1
    return n, maxn

# Function that prunes a given tree using the data
def prune(root, data):
    while True:
        orig = res(root, data)
        n, maxn = pruneH(root, root, data, 0, None)
        if n >= orig:
            if maxn.more1s:
                maxn.name = 1
            else:
                maxn.name = 0
        else:
            break

def main():
    f = open(sys.argv[1], 'rb')
    trainf = csv.reader(f)
    data = []
    for row in trainf:
        data.append(row)
    root = Node()
    root2 = Node()
    cTree(root, data)
    cTree2(root2, data)
    f2 = open(sys.argv[2], 'rb')
    trainf2 = csv.reader(f2)
    data2 = []
    for row in trainf2:
        data2.append(row)
    f3 = open(sys.argv[3], 'rb')
    trainf3 = csv.reader(f3)
    data3 = []
    for row in trainf3:
        data3.append(row)
    if sys.argv[5] == "yes":
        prune(root, data2)
        prune(root2, data2)
    print "H1: " + str(res(root, data3))
    print "H2: " + str(res(root2, data3))
    if sys.argv[4] == "yes":
        print "H1 Tree:"
        print_tree(root, 0)
        print "H2 Tree:"
        print_tree(root2, 0)

main()
