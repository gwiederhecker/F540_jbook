# Solving Kirchhoff's law ordinary differential equation

Import packages...

from sympy import *
#pacote para desenhar circuitos
import SchemDraw as schem
import SchemDraw.elements as e

d = schem.Drawing(unit=2.5)
d.add(e.DOT_OPEN, label ='$V_{in}$')
comp1 =d.add(e.RES, d='right',label='$R$') #capacitor
d.add(e.CAP, d='down',label='$C$') # resistor de saída
d.add(e.GND)
#output
d.add(e.LINE, d='right', xy=comp1.end, l=1)
d.add(e.DOT_OPEN,label ='$V_{out}$')
#---
d.draw()

Escrevendo a lei de Kirchhoff para o circuito da figura acima,
$$
\frac{dq}{dt}+\frac{1}{\tau}q=\frac{v_{in}(t)}{R}.
$$ (eq:kvl)

Exploraremos o pacote ```sympy``` para nos ajudar a resolver esta equação diferencial ordinária.

## Defining **symbols** and equation to be solved

A solução tentantiva será na forma,
$$ q(t)=A \cos(\omega t)+B*\sin(\omega t)
$$ (eq:trial)

A,B,omega,t, tau = symbols('A B omega t tau')
qtrial= A*cos(omega*t)+B*sin(omega*t)

lhs = diff(qtrial,t)+1/tau*qtrial 

v0, R = symbols('v0 R')
rhs = v0/R*cos(omega*t)

eq = lhs-rhs
simplify(lhs)

terms = [sin(omega*t),cos(omega*t)]
eqlhs=collect(simplify(eq),terms)


coefs = [eqlhs.coeff(term) for term in terms]
coefs

eq2 = [Eq(coef,0) for coef in coefs]
solution, = linsolve(eq2,(A,B))

sol = solution[0]*terms[0] + solution[1]*terms[1]
simplify(sol)

print_latex(simplify(sol))

Therefore, the solution is:
$$q(t) = \frac{\tau v_{0} \left(\omega \tau \cos{\left(\omega t \right)} + \sin{\left(\omega t \right)}\right)}{R \left(\omega^{2} \tau^{2} + 1\right)}
$$

#Another form....
Equivalently we could solve directly for the electric current $i=dq/dt$, $$\frac{di}{dt}+\frac{1}{\tau}i=\frac{1}{R}\frac{d v_{in}(t)}{dt}$$

A,B,omega,t, tau = symbols('A B omega t tau')
itrial= A*cos(omega*t)+B*sin(omega*t)

lhs = diff(itrial,t)+1/tau*itrial

v0, R = symbols('v0 R')
rhs = diff(v0/R*cos(omega*t),t)

eq = lhs-rhs
simplify(lhs)

terms = [sin(omega*t),cos(omega*t)]
eqlhs=collect(simplify(eq),terms)


coefs = [eqlhs.coeff(term) for term in terms]
coefs

eq2 = [Eq(coef,0) for coef in coefs]
solution, = linsolve(eq2,(A,B))

sol = solution[0]*terms[0] + solution[1]*terms[1]
simplify(sol)

print_latex(simplify(sol))

