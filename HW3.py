# HW3
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):
        # YOUR CODE STARTS HERE
        return len(self)==0 # If the length of the stack is 0, it is empty

    def __len__(self): 
        # YOUR CODE STARTS HERE
        curr=self.top      # Keeps track of current node in stack
        length=0 
        while curr!=None:  # Stops when end of stack reached
            length+=1 
            curr=curr.next # Current node is now next node in stack
        return length 

    def push(self,value):
        # YOUR CODE STARTS HERE
        if self.isEmpty(): self.top=Node(value) # If stack is empty, place new node as top of stack
        else:
            new=Node(value) 
            new.next=self.top                   # Points new node's next as rest as stack
            self.top=new                        # Sets new node as the top of stack

    def pop(self):
        # YOUR CODE STARTS HERE
        if self.isEmpty(): return None # If stack is empty theres nothing to pop
        value=self.top.value           # Value of top of stack
        self.top=self.top.next         # Makes the top of stack the node after top (deletes top from stack)
        return value

    def peek(self):
        # YOUR CODE STARTS HERE
        if self.isEmpty(): return None # If stack is empty, nothing to peek
        return self.top.value          # Only need to return value of node
    

#=============================================== Part II ==============================================

class Calculator:
    PRECEDENCE={"+":1,"-":1,"*":2,"/":2,"^":3}
    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        # YOUR CODE STARTS HERE
        try:
            float(txt)
            return True
        except: return False

    # Custom split method
    def _equationSpliter(self,txt):
        result=[]
        txt=txt.replace("-"," -")
        i=0
        length=len(txt)
        while i<length:
            if self._isNumber(txt[i])or((txt[i]=='.'or txt[i]=="-")and i+1<length and self._isNumber(txt[i+1])):
                start=i
                while i<length and(self._isNumber(txt[i])or txt[i]=='.'or txt[i]=="-"):i+=1
                result.append(txt[start:i])
            else:
                while i<length and txt[i].isspace():i+=1
                if i>=length:return result
                if self._isNumber(txt[i])or(txt[i]=='.'or txt[i]=="-"and i+1<length and self._isNumber(txt[i+1])):
                    start=i
                    while i<length and(self._isNumber(txt[i])or txt[i]=='.'or txt[i]=="-"):i+=1
                    result.append(txt[start:i])
                elif i<length:
                    if txt[i]=='(':
                        if not result and txt[-1]in self.PRECEDENCE:return None # Found implied multiplication
                    result.append(txt[i])
                    i+=1
        return result

    
    # Helper method to ensure expression is valid to convert to postfix
    def _isValidExpr(self,txt):
        operands=set(self.PRECEDENCE.keys()) # Makes a set of operands
        operands.add("(")
        operands.add(")")
        stack=Stack() # Stack for future use
        expr=self._equationSpliter(txt) # Expression we will be validating
        if expr==None:return False # Implied multiplication found when making expression 
        if len(expr)==1:return expr
        if not operands.intersection(set(expr)):return False # If the intersection is empty, there are no operators
        for i in range(len(expr)):
            if expr[i] == "(":stack.push("(")
            elif expr[i] == ")":
                if stack.isEmpty():return False  # Unbalanced parentheses
                stack.pop()
            elif self._isNumber(expr[i]):
                if i<len(expr)-1 and self._isNumber(expr[i+1]):return None 
            elif expr[i]in self.PRECEDENCE:
                if i == 0 or i==len(expr)-1 or expr[i-1]in self.PRECEDENCE or(expr[i+1]in self.PRECEDENCE and not"-"): return False  # Consecutive operators or missing operands
            elif self._isNumber(expr[i])or expr[i]=='.':
                while i+1<len(expr)and(self._isNumber(expr[i+1])or expr[i+1]=='.'):i+=1
            elif expr[i]!=' ': return False  # Unsupported characters
        return stack.isEmpty()

    def _isGreater(self,stack,operand):
        try:
            curr=self.PRECEDENCE[operand]
            top=self.PRECEDENCE[stack.peek()]
            return curr<=top
        except KeyError:return False

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +' 
            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3) ^ 2 + (1 +4 ))))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
        '''
        # YOUR CODE STARTS HERE
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        if not self._isValidExpr(txt):return None
        equation=self._equationSpliter(txt)
        result=[]
        for i in range(len(equation)):
            curr=equation[i]
            if self._isNumber(curr):result.append(str(float(curr)))
            elif curr=="(":postfixStack.push(curr)
            elif curr==")":
                while not postfixStack.isEmpty()and postfixStack.peek()!="(":result.append(postfixStack.pop())
                postfixStack.pop()
            else:
                if curr!="^":
                    while not postfixStack.isEmpty()and self._isGreater(postfixStack,curr):result.append(postfixStack.pop())
                postfixStack.push(curr)
        while not postfixStack.isEmpty():result.append(postfixStack.pop())
        return " ".join(result)
    
    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr(' 4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr(' 8 / 4 * (3 - 2.45 * ( 4 - 2 ^ 3 ) ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 + 2 * ( 5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778

            # In invalid expressions, you might print an error message, but code
            must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2")
            >>> x.calculate
            >>> x.setExpr("4 3 +2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('( 3.5 ) ( 15 )')
            >>> x.calculate
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)')
            >>> x.calculate
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))")
            >>> x.calculate
        '''
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        calcStack = Stack()   # method must use calcStack to compute the  expression
        # YOUR CODE STARTS HERE
        postfix=self._getPostfix(self.__expr)
        if postfix==None: return None
        eq=postfix.split(" ")
        for i in range(len(eq)):
            curr=eq[i]
            if not self._isNumber(curr):
                second_num=float(calcStack.pop())
                first_num=float(calcStack.pop())
                if curr=="+":calcStack.push(first_num+second_num)
                elif curr=="-":calcStack.push(first_num-second_num)
                elif curr=="*":calcStack.push(first_num*second_num)
                elif curr=="/":calcStack.push(first_num/second_num)
                elif curr=="^":calcStack.push(first_num**second_num)
            else: calcStack.push(curr)
        return float(calcStack.pop())


#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        # YOUR CODE STARTS HERE
        if word=="" or not word[0].isalpha():return False
        for char in word:
            if not char.isalpha()and not char.isalnum():return False
        return True

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        # YOUR CODE STARTS HERE
        if ";"in expr:equation=expr.split(";")
        else:equation=expr.split(" ")
        for i in range(len(equation)):
            curr=equation[i]
            if self._isVariable(curr)and curr not in self.states:return None
            if curr in self.states:equation[i]=str(self.states[curr])
        return " ".join(equation)
    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        # YOUR CODE STARTS HERE
        result={}
        split=self.expressions.split(";")
        for expr in split:
            equal=expr.split("=")
            if "return " in expr:
                calcObj.setExpr(self._replaceVariables(expr[7:]))
                result["_return_"]=calcObj.calculate
                return result
            i=0
            while i<len(equal):
                equal[i]=equal[i].strip()
                i+=1
            if self._replaceVariables(equal[1])==None:
                self.states={}
                return None
            calcObj.setExpr(self._replaceVariables(equal[1]))
            self.states[equal[0]]=calcObj.calculate
            result[expr]=self.states.copy()


def run_tests():
    import doctest

    # Run tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    doctest.run_docstring_examples(AdvancedCalculator, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    run_tests()