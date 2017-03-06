# -*- coding:utf-8 -*-
"""
TREE STRUCTURE:

                    left   (NodeInt or NodeBinaryOp)
                 /
        operator 
                 \   
                    right  (NodeInt)

""" 



#tokenizes the string to obtain a list of nodes
def tokenize(string):
    buffer = Buffer(string)
    tk_int = TokenInt()
    tk_op = TokenOperator()
    tokens = []
    
    while buffer.peek():
        token = None
        #tries with every type of token
        for tk in (tk_int, tk_op):
            token = tk.consume(buffer)
            if token:
                tokens.append(token)
                break
        #if there is no token, means there is no input
        if not token:
            raise ValueError("Error in syntax")
    
    return tokens


def parse(tokens):
    if tokens[0][0] != 'int':
        raise ValueError("Must start with an int")
    #now tokens[0] is an int
    node = NodeInt(tokens[0][1])    #saves the first token value
    nbo = None
    last = tokens[0][0]             #saves the first token type
    #starts with the second token
    for token in tokens[1:]:
        if token[0] == last:
            raise ValueError("Error in syntax")
        last = token[0]
        #if it's an operator, saves it at nbo, and the last int at nbo.left
        if token[0] == 'ope':
            nbo = NodeBinaryOp(token[1])
            nbo.left = node    
        #if it's an int, saves it at nbo.right
        if token[0] == 'int':
            nbo.right = NodeInt(token[1])
            node = nbo
    
    return node
    
def calculate(nbo):    
    #if it's a Binary Operator Node calculates the result of its operation
    if isinstance(nbo.left, NodeBinaryOp):
        leftval = calculate(nbo.left)
    else:
        leftval = nbo.left.value
    #calculates the result of the operation    
    if nbo.kind == '-':
        return leftval - nbo.right.value
    elif nbo.kind == '+':
        return leftval + nbo.right.value
    else:
        raise ValueError("Wrong operator")

def evaluate(node):
    #if it's only an int without operators
    if isinstance(node, NodeInt):
        return node.value
    else:
        return calculate(node)
    

def operate(string):
    #tokenizes the input string
    tokens = tokenize(string)
    #parses the token list to a tree
    node = parse(tokens)
    
    return evaluate(node)
    
        
#defines Node classes to create the tree
class Node(object):
    pass
#defines Int Node with a value (int)     
class NodeInt(Node):
    def __init__(self, value):
        self.value = value
#定义二叉树
class NodeBinaryOp(Node):
    def __init__(self, kind):
        self.kind = kind
        self.left = None    #左端点
        self.right = None   #右端点
    
#define Token classes    
class Token(object):
    def consume(self, buffer):
        pass
#tokenizer for int
class TokenInt(Token):
    #reads the buffer while char are numbers
    def consume(self, buffer):
        accum = ""
        while True:
            ch = buffer.peek()
            if ch is None or ch not in "0123456789":
                break
            else:
                accum += ch
                buffer.advance()

        if accum != "":
            return ("int", int(accum))
        else:
            return None 

class TokenOperator(Token):
    #读取buffer里的操作符并返回值和类型
    def consume(self, buffer):
        ch = buffer.peek()
        if ch is not None and ch in "+-":
            buffer.advance()
            return ("ope", ch)
        return None
        
#定义存储input的buffer
class Buffer(object):
    #输入字符
    def __init__(self, data):
        self.data = data
        self.offset = 0
    #返回在输入字符的偏移位置
    def peek(self):
        if self.offset >= len(self.data):
            return None
        return self.data[self.offset]
    def advance(self):
        self.offset += 1
        

if __name__ == '__main__':

    inputs = raw_input("INPUT : ")
    tokens = tokenize(inputs)
    node = parse(tokens)
    print("Result : "+ str(evaluate(node)))