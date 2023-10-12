import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from collections import Counter
from_class = uic.loadUiType("calculator.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        self.stack = []
        self.operators = "+-*/(."
        self.numbers = "0123456789"
        ac_state = False
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator")
        button_functions = {
            'pushButton_0': self.button_0_clicked,
            'pushButton_1': self.button_1_clicked,
            'pushButton_2': self.button_2_clicked,
            'pushButton_3': self.button_3_clicked,
            'pushButton_4': self.button_4_clicked,
            'pushButton_5': self.button_5_clicked,
            'pushButton_6': self.button_6_clicked,
            'pushButton_7': self.button_7_clicked,
            'pushButton_8': self.button_8_clicked,
            'pushButton_9': self.button_9_clicked,
            'pushButton_point' : self.point,
            'pushButton_back' : self.backspace,
            'pushButton_allclear' : self.allclear,
            'pushButton_plus' : self.plus,
            'pushButton_minus' : self.minus,
            'pushButton_multiply' : self.multiply,
            'pushButton_divide' : self.divide,
            'pushButton_result' : self.calc_result,
            'pushButton_startbracket' : self.start_bracket,
            'pushButton_endbracket' : self.end_bracket,
            'pushButton_pi' : self.pi,
            'pushButton_mod' : self.mod,
            'pushButton_root' : self.root,
            'pushButton_exp' : self.exp
            # 나머지 버튼들에 대해서도 매핑 추가
        }

        self.mode = {
            'pushButton_point' : '.',
            'pushButton_plus' : '+',
            'pushButton_minus' : '-',
            'pushButton_multiply' : '*',
            'pushButton_divide' : '/'
        }

        

        for button_name, button_function in button_functions.items():
            # if button_name in self.mode: 
            #     self.state = button_name
            #     check = 1
            button = getattr(self, button_name)
            if ac_state == True and (button_name == 'pushButton_allclear'):
                ac_state = False
                self.Window.clear()


            if button_name == 'pushButton_allclear':
                ac_state = True
                button.clicked.connect(button_function)
            else:
                ac_state = False
                button.clicked.connect(button_function)
            

                
    def split_expression(self,expression):
        operators = ['+','-','*','/','(',')','^','√']
        result = []
        i = 0

        while i < len(expression):
            if expression[i] == ' ':
                i+=1
                continue
            if expression[i].isdigit():
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                result.append(expression[i:j])
                i = j
            elif expression[i] in operators:
                result.append(expression[i])
                i += 1
            elif expression[i] == '𝝿':
                result[-1] = str(float(result[-1])*3.141592)
                i += 1
            elif expression[i] == 'm':
                result.append('%')
                i += 3
            else:
                raise ValueError("Invalid character in expression: " + expression[i])
        return result 
    

    def isNumeric(self,num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def calc_result(self):
        # document = self.Window.document()
        # # 마지막 줄의 텍스트 가져오기
        # last_block = document.findBlockByLineNumber(document.blockCount())
        # last_line_text = last_block.text()
        last_line_text = self.Window.text()
        tokens = self.split_expression(last_line_text)
        c = Counter(tokens)
        if c['('] != c[')']:
             self.Window_2.setText('에러 : 괄호 갯수 확인.')
             raise Exception("괄호의 갯수가 맞지 않습니다. 확인해주세요.")

        lst = []        # 빈 리스트 생성
        stack = []      # 스택 생성

        prior = {'√': 4,'^':4, '%':3, '*':3, '/':3, '+':2, '-':2, '(':1}     # 우선순위 설정
        for n in range(len(tokens)):    # 토큰의 길이만큼 반복하여
            prior = {'√': 4,'^':4, '%':3, '*':3, '/':3, '+':2, '-':2, '(':1} 
            if self.isNumeric(tokens[n]) : # 만약 숫자이면 바로 lst에 추가
                lst.append(tokens[n])
            elif tokens[n] == '(':  # (이면 바로 stack에 추가
                    stack.append(tokens[n])
            elif tokens[n] == ')':  # )가 나오면 stack에서 (가 나올때까지 pop처리 및 lst에 추가. 
                while stack[-1] != '(':
                    lst.append(stack.pop())
                stack.pop() # (가 나타나면 pop처리
            else:   # 그외에 경우 tokens[n]이 stack[-1]의 우선순위와 같거나 보다 작으면 tokens[n]의 우선순위가 더 커질때까지 pop
                while stack and prior[tokens[n]] <= prior[stack[-1]]:
                    lst.append(stack.pop()) # pop한것들은 lst에 추가 시켜줌   
                stack.append(tokens[n]) # 위의 조건이 완료 되면 stack에 추가

        while len(stack) != 0:  # stack에 남아있는 연산자들 lst에 추가
            lst.append(stack.pop())


        # op_check = ['+','/','*','-']    # 연산자 체크를 위해 미리 생성
        stack =[]   # 피연산자 바로 추가할 리스트 생성
        a1=0   # stack[-1]을 위한 변수 생성
        a2=0  # stack[-2]을 위한 변수 생성
        for l in range(len(lst)):   # 후위표기법으로 저장되 있는 리스트의 수만큼 반복   
            if self.isNumeric(lst[l]):    # 만약 피연산자이면 바로 stack에 추가
                stack.append(float(lst[l]))
            elif lst[l] == '^':
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1**a2)
            elif lst[l] == '√':
                a1 = stack.pop()
                stack.append(pow(a1,1/2))
            
            elif lst[l] == '%':
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1 % a2)
            elif lst[l] == '+': # + 이면 stack에서 2개 피연산자를 pop하여 게산해준뒤 다시 stack에 추가
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1 + a2)
            elif lst[l] == '-': # - 이면 stack에서 2개 피연산자를 pop하여 게산해준뒤 다시 stack에 추가
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1 - a2) 
            elif lst[l] == '*': # * 이면 stack에서 2개 피연산자를 pop하여 게산해준뒤 다시 stack에 추가
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1 * a2)
            elif lst[l] == '/': # / 이면 stack에서 2개 피연산자를 pop하여 게산해준뒤 다시 stack에 추가
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(a1 / a2)

        self.Window_2.setText(str(stack[0]))


    def exp(self):
        self.current_text = self.Window.text()
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '^'
                self.Window.setText(new_text)            

    def root(self):
        self.current_text = self.Window.text()
        # if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
        new_text = self.current_text + ' √'
        self.Window.setText(new_text)          

    def mod(self):
        self.current_text = self.Window.text()
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + ' mod '
                self.Window.setText(new_text)         

    def pi(self):
        self.current_text = self.Window.text()
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '𝝿'
                self.Window.setText(new_text)


    def start_bracket(self):
        self.current_text = self.Window.text()
        # new_text = self.current_text + '('
        # self.noRepeatSym_input(self,new_text)
        if self.current_text[-1] in self.operators:
            new_text = self.current_text + '('
            self.Window.setText(new_text)
   

    def end_bracket(self):
        self.current_text = self.Window.text()
        if self.current_text[-1].isdigit():
                new_text = self.current_text + ')'
                self.Window.setText(new_text)
        
        # self.noRepeatSym_input(self,new_text)
        
        # self.Window.setText(new_text)            

    def point(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        
        if (self.current_text[-1].isdigit() or self.current_text[-1] == ')') :
                new_text = self.current_text + '.'
                self.Window.setText(new_text)
        # if self.current_text[-1].isdigit():
        #     new_text = self.current_text + '.'
        #     self.Window.setText(new_text)

    def plus(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '+'
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '+'
                self.Window.setText(new_text)
        # self.noRepeatSym_input(new_text)
        # self.Window.setText(new_text)
    
    def minus(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '-'
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '-'
                self.Window.setText(new_text)
        # self.noRepeatSym_input(new_text)
        # self.Window.setText(new_text)

    def multiply(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '*'
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '*'
                self.Window.setText(new_text)
        # self.noRepeatSym_input(new_text)
        # self.Window.setText(new_text)

    def divide(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '/'
        if self.current_text[-1].isdigit() or self.current_text[-1] == ')':
                new_text = self.current_text + '/'
                self.Window.setText(new_text)
        # self.noRepeatSym_input(new_text)
        # self.Window.setText(new_text)                

    def allclear(self):
        self.Window.setText('')
        self.Window_2.setText('')

    def backspace(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text[:-1]
        # self.Window.setText(new_text)
        self.Window.setText(new_text)

    def button_0_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '0'
        self.Window.setText(new_text)

    def button_1_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '1'
        self.Window.setText(new_text)   

    def button_2_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '2'
        self.Window.setText(new_text)   

    def button_3_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '3'
        self.Window.setText(new_text)   

    def button_4_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '4'
        self.Window.setText(new_text)   

    def button_5_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '5'
        self.Window.setText(new_text)   

    def button_6_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '6'
        self.Window.setText(new_text)   

    def button_7_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '7'
        self.Window.setText(new_text)   

    def button_8_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '8'
        self.Window.setText(new_text)   

    def button_9_clicked(self):
        # self.current_text = self.Window.toPlainText()
        self.current_text = self.Window.text()
        new_text = self.current_text + '9'
        self.Window.setText(new_text)   

    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
