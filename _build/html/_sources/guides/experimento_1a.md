[\[sec:filtros\]]{#sec:filtros label="sec:filtros"} Experimento I - Filtros
===========================================================================

Filtros RC passa-alta e passa-baixa
-----------------------------------

Neste experimento serão investigados circuitos contento um capacitor e
um resistor. Estes circuitos nos permitem medir a corrente elétrica
(resistor) ou a carga elétrica (capacitor) que fluem nos circuitos. A
amplitude e a fase da corrente ou carga elétrica, em relação a tensão de
excitação do circuito, dependem da frequência e esta dependência é que
motiva e denominação desses circuitos como filtros de frequência dos
tipos passa-baixas ou passa-altas.

Para compreender este comportamento é fundamental revisar o conceito de
resposta em frequência, ou seja, como a resposta de um dado sistema
linear se comporta como função da frequência de excitação, portanto, é
recomendado que o aluno revise o assunto no livro de sua preferência. O
capítulo 2 do livro do Brophy (Eletrônica básica) [@Bro90] é uma boa
opção, ou mesmo um livro sobre equações diferenciais ordinárias
[@BoyDiP09].

### Objetivos

-   Compreender as relações entre tensões e correntes senoidais em
    circuitos contendo resistores, capacitores e indutores.

-   Compreender como estes circuitos podem ser utilizados como filtros
    de sinais elétricos.

-   Determinar a resposta em frequência da amplitude e fase de filtros
    RC, RL e RLC; passa-baixas, passa-altas, passa-bandas,
    rejeita-bandas.

-   Descrever o comportamento de filtros através de gráficos de
    transmitância e fase em escala logarítmica (diagramas de Bode).

### Teoria

#### Divisor de tensão

Seguindo o teorema de Thevenin [@Bro90], podemos representar todos os
componentes internos do nosso gerador de corrente alternada (AC) por uma
fonte ideal associada a uma resistência (ou impedância) equivalente,
como na b. Podemos tratar o circuito da b da mesma forma que trataríamos
um circuito de corrente contínua. Para o circuito mostrado na , podemos
escrever a Lei das malhas de Kirchoff:

$$\begin{aligned}
\label{eq:exp0_1}\epsilon-R_g i -R_1 i - R_2 i=0\text{ (em relação à tensão de circuito aberto $\epsilon$),}\\
\label{eq:exp0_2}V_1-R_1 i - R_2 i=0\text{ (em relação à tensão medida $V_1$).}\end{aligned}$$

Com a Eq. [\[eq:exp0_2\]](#eq:exp0_2){reference-type="ref"
reference="eq:exp0_2"} concluímos que a corrente é dada por
$i=\epsilon/(R_g+R_1+R_2)=V_1/(R_1+R_2)$. Pela lei de Ohm, sabemos que
$V=Ri$, portanto, $V_2=V_1 R/(R_1+R_2)$. Logo, a resposta do divisor de
tensão é dada por,
$$\label{eq:exp0_4}\boxed{H\equiv \frac{\text{Tensão de saída}}{\text{Tensão de entrada}}=\frac{V_2}{V_1}=\frac{R_2}{R_1+R_2},}$$
e não depende da frequência, ou seja o **divisor de tensão** é um
**filtro passa-todas**, e.g., todas as frequências são transmitidas (da
entrada para a saída) sem sofrer qualquer distorção. Note também que a
função de transferência $H$ não depende da resistência interna do
gerador, ela é uma propriedade do circuito!

Definindo $x=V_1/V_2$, obtemos a seguinte expressão,
$$\label{eq:exp0_3}\boxed{R_1=R_2(x-1)}$$ O comportamento da relação
dada pela é mostrado na . Note que quando $R_2=R_1$, a tensão é dividida
simetricamente entre os dois resistores, i.e., $V_2/V_1=0.5$.

#### Filtros contendo apenas um componente reativo

A resposta em frequência dos filtros RC e RL é exatamente análoga à
resposta do divisor de tensão, no caso dos filtros mostrados na Fig.
[\[fig:rc\]](#fig:rc){reference-type="ref" reference="fig:rc"} a função
de transferência é dada por [^1], $$H(\omega)=\frac{Z_2}{Z_1+Z_2}
\label{eq:h_rc};$$ sendo que $Z_{2}$ é a impedância complexa do
componente que esta conectado à saída do circuito; $Z_1+Z_2$ é a
impedância complexa total do circuito. No caso da Fig.
[\[fig:rc\]](#fig:rc){reference-type="ref" reference="fig:rc"}(b) o
numerador da Eq. [\[eq:h_rc\]](#eq:h_rc){reference-type="ref"
reference="eq:h_rc"}. seria $Z_R$, enquanto que no caso da o numerador
seria $Z_C$. É fácil mostrar que $Z_R=R$ e $Z_C=-j/(\omega C)$,
portanto, a fase e a amplitude de $H(\omega)$ dependem da frequência, em
contraste com o divisor de tensão formado apenas por resistores.
Definimos a transmitância (ou ganho) do filtro a partir de $H(\omega)$,
$$\label{eq:t_Rc}\boxed{T=|H(\omega)|^2}.$$ É mais comum utilizar a
versão logarítmica (em decibels - dB) desta quantidade, que é definida
da seguinte forma,
$$\label{eq:tdb_Rc}\boxed{T_{dB}=10\log_{10}T=20\log_{10}|H(\omega)|}.$$

##### Passa-altas.

Para o filtro passa-altas a tensão de saída é medida no resistor, como
mostrado na [\[fig:rc\]](#fig:rc){reference-type="ref"
reference="fig:rc"}, portanto, a função de transferência é
$H(\omega)=j \omega R C/(1+j\omega R C)$. A transmitância e a fase serão
dadas por,
$$\label{eq:h_t_rc}\boxed{T=\frac{\omega^2 R^2 C^2}{1+\omega^2 R^2 C^2}}$$
$$\label{eq:h_fase_rc}\boxed{\phi=\arg H(\omega)=\arctan\left(\frac{1}{\omega R C}\right)}$$
Os comportamentos da transmitância e da fase do circuito passa-altas,
como função da frequência, são ilustrados na
[1.1](#fig:rc_bode){reference-type="ref" reference="fig:rc_bode"}(a,b).
Estes dois gráficos representam o **diagrama de Bode** do circuito da
[\[fig:rc\]](#fig:rc){reference-type="ref" reference="fig:rc"}(a). É de
extrema importância entender como as funções dadas pelas
[\[eq:h_t\_rc,eq:h_fase_rc\]](#eq:h_t_rc,eq:h_fase_rc){reference-type="ref"
reference="eq:h_t_rc,eq:h_fase_rc"} comportam-se como nas
[1.1](#fig:rc_bode){reference-type="ref" reference="fig:rc_bode"}(a,b).
Para compreender isto basta tomar o logarítmo da
[\[eq:h_t\_rc\]](#eq:h_t_rc){reference-type="ref"
reference="eq:h_t_rc"}, $$\begin{aligned}
    T_{dB}\equiv 10\log(T) & =10\log (\omega^2 R^2 C^2) -10 \log (1+\omega^2 R^2 C^2),\\
    T_{dB} &=20\log (\omega/\omega_c) -10 \log (1+\omega^2/\omega_c^2),\end{aligned}$$
sendo que $\omega_c=1/RC$. Se $\omega\gg\omega_c$ ou [^2] podemos
aproximar assintoticamente a expressão anterior, $$\begin{aligned}
    T_{dB}(\omega\gg \omega_c)&\approx 10\log (\omega^2 R^2 C^2) -10 \log (\omega^2 R^2 C^2)=0,\\
    T_{dB}(\omega\ll \omega_c)&\approx 20\log (\omega/\omega_c) -10 \log (1)=20\log (\omega/\omega_c).\end{aligned}$$
Note que as expansões acima nos revelam que, para frequências pequenas,
a transmitância (em dB) cresce linearmente com derivada 20 como função
do logarítmo da freqûencia. Ou seja, a cada vez que $\omega/\omega_c$
cresce por um fator 10 (o logarítmo cresce de uma unidade), a
transmitância aumenta em 20 decibels. A maneira compacta de dizer isto é
que o a transmitância aumenta em 20 dB/dec nesta faixa de frequência
($\omega\ll\omega_c$). Já na faixa de frequências altas
($\omega\gg\omega_c$) a transmitância tem o valor assintótico constante
de 0 dB. O significado disto é que a transmitância (linear) é
$T\approx1$. Nesta faixa de frequências o sinal de saída do filtro tem,
aproximadamente, a mesma amplitude do sinal de entrada e a fase da
saída, em relação à entrada, também se aproxima de 0 grau. Fica óbvia a
denominação deste filtro como **passa-altas**, ou seja, os sinal de alta
frequência ($\omega\gg\omega_c$) são transmitidos integralmente pelo
filtro, com a mesma amplitude e fase da entrada. **Repita esta
demonstração para o circuito da
[\[fig:rc\]](#fig:rc){reference-type="ref" reference="fig:rc"}(b) e se
convença de que tal filtro é o passa-baixas.**

![[\[fig:rc_bode\]]{#fig:rc_bode label="fig:rc_bode"}Resposta em
frequência de um filtro RC passa-altas. (a,b) Diagrama de Bode do
filtro, em (a) é mostrada a transmitância, em (b) a resposta de fase.
(c) Formas de onda dos canais 1 (entrada) 2 (saída) correspondentes aos
pontos vermelhos marcados em (a,b), $f=f_c$. (d) Representação de
fasores dos canais 1 e 2 nas mesmas condições de (c). Em todas as curvas
o canal 2 é representado em vermelho, o canal 1 em
azul.](rc.pdf){#fig:rc_bode width="\\textwidth"}

Para visualizar o significado do diagrama de Bode, note os pontos
vermelhos nas Figs. [1.1](#fig:rc_bode){reference-type="ref"
reference="fig:rc_bode"}(a,b) que indicam a denominada frequência de
corte do circuito, $\omega_c=2\pi f_c =1/(RC)$. As formas de onda
medidas na entrada ($V_1$) e saída ($V_2$) do circuito passa-altas são
mostradas na [1.1](#fig:rc_bode){reference-type="ref"
reference="fig:rc_bode"}(c) (exatamente na frequência de corte). Note
que como a fase é positiva neste ponto ($\phi=45^{\circ}$), a tensão no
canal 2 (saída) está adiantada em relação ao canal 1 (entrada). A Fig.
[1.1](#fig:rc_bode){reference-type="ref" reference="fig:rc_bode"}(d)
indica a representação das duas ondas no plano complexo. Nesta
representação escolhemos como referência a onda de entrada (azul) que é
alinhada ao longo do eixo real, enquanto a onda de saída (vermelha) está
adiantada de ($\phi=45^{\circ}$); a amplitude das ondas corresponde ao
módulo dos vetores indicados.

[^1]: Demonstre esta relação partindo da Lei de Kirchoff e utilizando a
    impedância complexa dos componentes do circuito.

[^2]: Quando escrevemos o símbolo $\gg(\ll)$, poder ser algo como
    $20\sim50\times$ maior(menor).
