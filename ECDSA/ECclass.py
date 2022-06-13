class PrimeField:  
    
    ### 생성자 
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num {} not in field range 0 to {}'.format(num, prime - 1)
            # 0 <= num <= p-1 이 아닌 ValueError를 반환하며 함수 동작 중단 (예외처리 구문)
            raise ValueError(error)
        self.num = num
        self.prime = prime
        
        
    ### 객체 표현 메서드 (객체명 실행 시 출력 정보 재정의)
    def __repr__(self):
        return '{} in Z_{}'.format(self.num, self.prime)
    
    
    ### 두 소수체 원소가 서로 같은지, 다른지 판단 메서드 (==, != 연산자 재정의)
    def __eq__(self, other):
        # 비교 소수체 원소가 비어있는 객체이면 자명하게 거짓 반환
        if other is None:
            return False
        # 값도 같고, 소수체를 정의하는 소수도 같은 경우 참 반환
        return self.num == other.num and self.prime == other.prime
    
    
    def __ne__(self, other):
        # 두 객체가 다르면 참 반환, 다르면 거짓 반환
        return not (self == other)
    
    
    ### 덧셈 메서드 (+ 연산자 재정의)
    # 두 소수체 객체 self와 other에 대해 self.num + other.num (mop p) 계산하기
    def __add__(self, other):
        # 두 소수체가 같은 prime 에서 정의된 것인지 판단하여 거짓이면 error 발생
        # 같은 소수체에서 정의된 것이면 self.num + other.num (mop p) 값 계산
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + other.num) % self.prime
        # 계산 결과를 현재 객체의 클래스 type(PrimeField)에 맞추어 반환
        return self.__class__(num, self.prime)
     
        
    ### 뺄셈 메서드 (- 연산자 재정의)
    # 두 소수체 객체 self와 other에 대해 self.num - other.num (mop p) 계산하기
    def __sub__(self, other):
        # 두 소수체가 같은 prime 에서 정의된 것인지 판단하여 거짓이면 error 발생
        # 같은 소수체에서 정의된 것이면 self.num - other.num (mop p) 값 계산
        if self.prime != other.prime:  
            raise TypeError('Cannot subtract two numbers in different Fields')
        num = (self.num - other.num) % self.prime
        # 계산 결과를 현재 객체의 클래스 type(PrimeField)에 맞추어 반환
        return self.__class__(num, self.prime)
    
    
    ### 곱셈 메서드 (* 연산자 재정의)
    # 두 소수체 객체 self와 other에 대해 self.num * other.num (mop p) 계산하기
    def __mul__(self, other):
        # 두 소수체가 같은 prime 에서 정의된 것인지 판단하여 거짓이면 error 발생
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        # 같은 소수체에서 정의된 것이면 self.num * other.num (mop p) 반환
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)
    
    
    ### 상수배 메서드 (정수와의 * 연산자 재정의)
    # 소수체 객체 self 와 정수 상수 scalr 에 대해 scalar * self.num (mod p) 반환
    # 위 곱셈 메서드에서 scalar 값이 0 <= scalar <= p-1 이 아니어도 계산할 수 있도록 로직을 수정하면 됨
    def __rmul__(self, scalar):
        num = (self.num * scalar) % self.prime
        return self.__class__(num=num, prime=self.prime)
    
    
    ### 빠른 거듭제곱 메서드 (** 연산자 재정의)
    # 소수체 객체 self 와 정수 상수 scalar 에 대해 self.num 를 scalr 번 mod p로 거듭제곱 계산하기
    def __pow__(self, exponent):
        # 페르마의 작은 정리로 부터 scalar (mod p-1) 만큼 self.num 을 거듭제곱하면 됨
        n = exponent % (self.prime - 1)
        # self.num 을 scalar (mod p-1) 만큼 거듭제곱할 때 pow 함수를 사용하여 효율적으로 계산 (Square & Multiply)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)
    
    
    ### 나눗셈 메서드 (/ 연산자 재정의)
    # 두 소수체 객체 self와 other에 대해 self.num / other.num (mop p) 계산하기
    def __truediv__(self, other):
        # 두 소수체가 같은 prime 에서 정의된 것인지 판단하여 거짓이면 error 발생
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        # other.num == 0 이면 곱셈에 대한 역원이 존재하지 않으므로 error 발생
        if other.num == 0:
            raise TypeError('Does not exist the multiplicative inverse of 0')
        # self.num * 1/other.num (mod p) 반환
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(num, self.prime)  
 
 
class Point:
    
    ### 생성자 메서드
    # 입력 : point 좌표 (x,y) 와 타원곡선 계수 (a,b)
    # 모든 입력값들은 소수체 Z_p의 원소
    # 무한원점 정의 : point 좌표 x 와 y 가 모두 None 인 점
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        ### 정의된 타원곡선 위의 점인지 판단
        # 타원곡선을 정의하는 방정식을 만족하지 않는 경우 곡선 위의 점이 아님을 알리고 error 처리
        # PrimeField 클래스를 import 하였기 때문에 아래 연산은 PrimeField 에서 정의한 연산법칙을 따름
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))
    
    
    ### 객체 표현 메서드
    # 객체명을 실행했들 때 출력 정보 재정의
    def __repr__(self):
        # 무한원점 표현
        if self.x is None:
            return 'Point at Infinity (Pinf)'
        # 일반적인 Point 표현 (Point 좌표와 타원곡선 계수 a & b)
        else:
            return 'Point({},{}) with a = {} and b = {}'.format(self.x, self.y, self.a, self.b)
        
        
    ### 두 점이 서로 같은지 판단하는 메서드 (타원곡선 Group에서 Point에 대한 ==, != 연산자 재정의)
    def __eq__(self, other):
        # 비교 Point (other)가 비어있는 객체이면 자명하게 거짓 반환
        if other is None:
            return False
        # 두 Point self 와 other 의 x 좌표, y 좌표가일치하고, 두 점이 정의된 타원곡선이 같을 때 같다고 판단
        return (self.x == other.x and self.y == other.y) and (self.a == other.a and self.b == other.b)
    
    
     ### 두 점이 서로 다른지 판단하는 메서드 (타원곡선 Group에서 Point에 대한 != 연산자 재정의)
    def __ne__(self, other):
        # 두 Point self 와 other 가 다르면 참 반환, 같으면 거짓 반환
        return not (self == other)
    
    
    ### 타원곡선 위의 점 덧셈 연산 메서드 (타원곡선 Group에서 Point에 대한 + 연산자 재정의)
    def __add__(self, other):
        # Point self 와 Point other 가 같은 타원곡선에서 정의된 경우만 연산 가능함
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))
            
        ### Case 0: 두 point 중 하나가 무한원점인 경우
        # Case 0.0: Point self 가 무한원점 O 인 경우 => Point other 를 return
        if self.x is None:
            return other     
        # Case 0.1: Point other 가 무한원점 O 인 경우 => Point self 를 return
        if other.x is None:
            return self
        
        ### Case 1: self.x ≠ other.x (두 점의 x 좌표가 다른 경우)
        # Formula (x3,y3) == (x1,y1) + (x2,y2)
        # m = (y2 - y1) / (x2 - x1)
        # x3 = m**2 - x1 - x2
        # y3 = m * (x1 - x3) - y1
        if self.x != other.x:
            m = (other.y - self.y) / (other.x - self.x)
            x = m**2 - self.x - other.x
            y = m * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        
        ### Case 2: self.x == other.x, self.y != other.y (두 점의 x 좌표가 같고 y 좌표가 다른 경우) 
        # 두 점을 지나는 직선이 y축과 평행 => 연산결과는 무한원점
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
                
        ### Case 3: self == other (두 점이 같은 경우, 즉, doubling)
        # Case 3.1: self == other,  self.y == 0  => Point self에서 접선이 y축과 평행 => 2self 는 무한원점
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)    
        # Case 3.2: self == other,  self.y !=0 
        # Formula (x3,y3) == (x1,y1) + (x1,y1)
        # m = (3 * x1**2 + a) / (2 * y1)
        # x3 = m**2 - 2 * x1
        # y3 = m * (x1 - x3) - y1
        if self == other:
            m = (3 * self.x**2 + self.a) / (2 * self.y)
            x = m**2 - 2 * self.x
            y = m * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        
        
    ### 타원곡선 위의 점 뻴셈 연산 메서드 (타원곡선 Group에서 Point에 대한 - 연산자 재정의)
    def __sub__(self, other):
        # Point self 와 Point other 가 같은 타원곡선에서 정의된 경우만 연산 가능함
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))
        
        # Case 0: other가 무한원점이 경우 => self - other = self
        if other.x is None:
            return self
        
        # Case 1: other가 무한원점이 아닌 경우 
        # Formula (x3,y3) == (x1,y1) - (x2,y2) == (x1,y1) + (x2,-y2)
        # -y2 = 0 - y2 in Z_p
        y = 0*other.y - other.y
        otherNeg = self.__class__(other.x, y, self.a, self.b)
        return (self + otherNeg)
        
        
    ### 타원곡선 Point 상수배 연산 메서드 (타원곡선 Point에 대해 정수와의 * 연산자 재정의)
    # 빠른 지수승 연산의 덧셈 버전
    # coefficient 가 음수인 경우는 Point self 의 order - coefficient가 되어야 함 (일단 생략)
    def __rmul__(self, coefficient):
        coef = coefficient
        current = self  
        result = self.__class__(None, None, self.a, self.b)  
        while coef:
            if coef & 1:  
                result += current
            current += current  
            coef >>= 1  
        return result