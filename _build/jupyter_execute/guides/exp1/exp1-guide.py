# Guide to Experiment 1: RC filters

Métodos da Físcia Experimental I: (F540 2s2020)

* Texto base: Daniel Ugarte, Antônio Riul Junior, Varlei Rodrigues
* Adaptação Jupyter: Gustavo Wiederhecker

import sys
print(sys.executable)
print(sys.version)

#-----------------------------
#Pacote para manipular vetores e matrizes
import numpy as np
#-----------------------------
#Pacotes para lidar com unidades
from astropy import units as un
from astropy import constants as cte
#-----------------------------
#pacote para gráficos
import matplotlib.pyplot as plt
import matplotlib
#Comandos opcionais para formatar gráfico
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 12}	
lines = {'linewidth' : 3.0}
figure = {'figsize' : [6.0, 6/1.6]}
matplotlib.rc('font', **font)
matplotlib.rc('lines', **lines)
matplotlib.rc('figure', **figure)
#-----------------------------
#pacote para desenhar circuitos
import SchemDraw as schem
import SchemDraw.elements as e
d = schem.Drawing(unit=2.5) # unit=2.5 determina o tamanho dos componentes

Neste experimento serão investigados circuitos contento um capacitor e
um resistor. Estes circuitos nos permitem medir a corrente elétrica
(resistor) ou a carga elétrica (capacitor) que fluem nos circuitos. A
amplitude e a fase da corrente ou carga elétrica dependem da frequência. Esta dependência é que
motiva e denominação desses circuitos como filtros de frequência, pois eles modificam como cada frequência é transmitida pelo mesmo. dos
tipos passa-baixas ou passa-altas.

Para compreender este comportamento é fundamental revisar o conceito de
resposta em frequência, ou seja, como a resposta de um dado sistema
linear se comporta como função da frequência de excitação, portanto, é
recomendado que o aluno revise o assunto no livro de sua preferência. O
capítulo 2 do livro do Brophy (Eletrônica básica)  é uma boa
opção, ou mesmo um livro sobre equações diferenciais ordinárias.
{cite}`eggleston2011basic`

```{note}
Objetivos:
-   Compreender as relações entre tensões e correntes senoidais em
    circuitos contendo resistores, capacitores e indutores.

-   Compreender como estes circuitos podem ser utilizados como filtros
    de sinais elétricos.

-   Determinar a resposta em frequência da amplitude e fase de filtros
    RC, RL e RLC; passa-baixas, passa-altas, passa-bandas,
    rejeita-bandas.

-   Descrever o comportamento de filtros através de gráficos de
    transmitância e fase em escala logarítmica (diagramas de Bode).
```



## Frequency response of filters

Considere o diagrama do seguinte circuito elétrico:
```{sidebar} Nota lateral

```

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

No laboratório, uma possível implementação desse circuito tem o aspecto da {ref}`foto_filtro_pa`:

```{figure} figs/foto_passa_altas.jpg
---
width: 450px
name: foto_filtro_pa
---
Filtro passa-baixas montado em uma protoboard.
```

Na tela do osciloscópio, teríamos algo como a figura {ref}`highpass_scope`

```{figure} figs/sweep_freq_pa_000.png
---
width: 450px
name: highpass_scope
---
Here is my figure caption!
```

## Amplitude and phase-shifts (amplitude e deslocamento de fase)

Todo circuito elétrico cuja resposta depende da frequência introduz uma defasagem no sinal de saída em relação ao sinal de entrada. Os filtros passa-baixa e passa-alta estudados são dois exemplos típicos. A figura abaixo ilustra o sinal de entrada ($V_{in}$) e saída ($V_{out}$) de um filtro passa-alta atuando em um sinal de baixa frequência. Notem que os sinais não estão em fase. O valor da defasagem $\phi$ pode ser obtido medindo-se a diferença de tempo $\Delta t$ entre os instantes que elas cruzam 0 Volts ou entre dois máximos das funções senoidais de entrada e saída e o período $T$.

$$ 
\phi = 2\ \pi\ \cfrac{\Delta t}{T}
$$ (eq:fase)


Notem que a {eq}`eq:fase` permite-nos relacionar a medida no osciloscópio (diferença de tempo) com a diferença de fase.

t = np.linspace(0,2e-3,100) # vetor de tempo
f,ϕ1,ϕ2 = 1e3,0,np.pi/3 # frequencia e fase
v01,v02 = 1,0.8 # amplitudes
#----
v1 = v01*np.cos(2*np.pi*f*t+ϕ1) # sinal v1(t)
v2 = v02*np.cos(2*np.pi*f*t+ϕ2) # sinal v2(t)
plt.plot(t*1e3, v1, label =r'$V_1(t)$')
plt.plot(t*1e3, v2, label =r'$V_2(t)$')
#----
ϕ = ϕ2-ϕ1 # defasagem
T = 1/f # periodo dos sinais
dt = T*ϕ/(2*np.pi) # atraso temporal entre os sinais
#linhas verticais
plt.axvline(T*1e3,color='k',linestyle='--',linewidth=2.0)
plt.axvline((T-dt)*1e3,color='k',linestyle='--',linewidth=2.0)
#--------
#formatação do gráfico
plt.grid(True) # ativa grades
plt.legend(loc='best')
plt.xlabel('Tempo (ms)')
plt.ylabel('Amplitude (V)')
plt.title('Dois sinais com mesma  frequência (1 kHz) e \n defasagem de $\phi={:1g}^\circ$'.format(180*ϕ/np.pi));
#plt.savefig('sinais_defasados.pdf')

t = np.linspace(0,1e-3,100) # vetor de tempo
f,ϕ1,ϕ2 = 2e3,0, np.pi/2+ np.pi/3*np.random.randn()  # frequencia e fase
v01,v02 = 1,0.8 # amplitudes
#----
v1 = v01*np.cos(2*np.pi*f*t+ϕ1) # sinal v1(t)
v2 = v02*np.cos(2*np.pi*f*t+ϕ2) # sinal v2(t)
plt.plot(t*1e3, v1, label =r'$V_1(t)$')
plt.plot(t*1e3, v2, label =r'$V_2(t)$')
#----
ϕ = ϕ2-ϕ1 # defasagem
T = 1/f # periodo dos sinais
dt = T*ϕ/(2*np.pi) # atraso temporal entre os sinais
#linhas verticais
plt.axvline(T*1e3,color='k',linestyle='--',linewidth=2.0)
# plt.axvline((T-dt)*1e3,color='k',linestyle='--',linewidth=2.0)
#--------
#formatação do gráfico
plt.grid(True) # ativa grades
plt.legend(loc='best')
plt.xlabel('Tempo (ms)')
plt.ylabel('Amplitude (V)')
# plt.title('Dois sinais com mesma defasagem de $\phi$'.format(180*ϕ/np.pi));
plt.tight_layout()
plt.savefig('figs/ex_delta_fase.png', bbox_inches='tight')
#plt.savefig('sinais_defasados.pdf')

````{exercise} Diferença de fase entre sinais
:label: ex:fase_delta1

Considere a figura a seguir e determine:

```{image} figs/ex_delta_fase.png
:alt: circuit picture
:width: 400px
:align: center
```
* a frequência dos sinais
* a diferença de fase entre os sinais
```` 

````{solution} ex:fase_delta1
:label: exs:fase_delta1

Para resolver esse resolver este exercício, primeiro calcule a diferente de tempo entre as ondas, depois utilize a equação {eq}`eq:fase` encontrar a diferença de fase.

````

````{exercise} Diferença de fase entres sinais no osciloscópio
:label: ex:fase_delta2

Considerando  a tela do osciloscópio que foi capturada utilizando um circuito RC:

```{image} figs/sweep_freq_PA_000.png
:alt: oscilloscope traces
:width: 400px
:align: center
```
* A amplitude $v_j\pm\delta v_j$([V]) de cada sinal;
* A frequência $f$ [1/s] (e $\omega$ [rad/s])  dos sinais ;
* A diferença de fase entre os sinais, $\phi=\phi_2-\phi_1$, considere o sinal da fase!
* Com base na fase calculada, trata-se de um filtro passa-baixas ou passa-altas? Justifique.
```` 

## Filtros passa-altas (PA) e passa-baixas (PB)

d = schem.Drawing(unit=2.5)
#fonte
source_color='blue' # cor da fonte
d.add(e.GND,color=source_color) # terra
d.add(e.SOURCE_SIN, label='$V_{Th}$', color=source_color) # fonte
d.add(e.RES, d='right',label='$R_{Th}$', color=source_color)
d.add(e.DOT_OPEN, color=source_color)
#circuito
diode1 =d.add(e.RES, d='right',label='$R$') #capacitor
d.add(e.CAP, d='down',label='$C$') # resistor de saída
d.add(e.GND)
#output
d.add(e.LINE, d='right', xy=diode1.end, l=1)
d.add(e.DOT_OPEN)
#---
d.draw()
d.save('figs/filtro_pb_esquema.png')

O circuito abaixo ilustra um caso de filtro onde os sinais de baixa frequência têm suas amplitudes atenuadas, enquanto sinais de alta frequência são transmitidos quase sem atenuação. Monte o filtro passa-alta usando R = 300 $\Omega$, C = 470 nF. 
```{figure} figs/filtro_pb_esquema.png
---
width: 300px
name: fig:filtro_pb_esquema
---
Esquemático de um filtro passa-baixas.
```

A função de transferência $H(\omega)$ ou ganho do circuito $G(\omega)$ são definidos como,

$$
G(\omega)=H(\omega)=\cfrac{V_{out}}{V_{in}}
$$ (eq:ganho)

Experimentalmente, as quantidades $V_{out}$ e $V_{in}$ possuem amplitude e fase, que são medidas separadamente como no exercício {ref}`ex:fase_delta2`.

### Preparação para o experimento


````{exercise} Preparação para experimento
:label: ex:prep_exp1

* Demonstre a função de transferência (Ganho de tensão) para este circuito. Utilize as impedâncias complexas para isto.
* Qual a frequência de corte do circuito?.
* Como ele se comporta (impedância total e tensão de saída).
* Com o mínimo de matemática, tente visualizar como a fase do sinal $V_{out}$ se altera em relação à $V_{in}$.
* Qual efeito de $R_{Th}$ na resposta do circuito? Ele altera a medida de $V_{out}(f)$, $V_{in}(f)$ e $V_{out}(f)/V_{in}(f)$ ?

Simulação do circuito:
* Utilize o TinkerCAD para montar o circuito da figura {ref}`fig:filtro_pb_esquema`, investigue seu comportamento. 
* Utilize o QUCS para explorar o comportamento.

```` 

### Adquirindo os dados experimentais


Utilize o gerador de sinais para analisar o comportamento de e da fase $\phi$ para a frequência de corte, a frequência uma década abaixo da frequência de corte e a frequência uma década acima da frequência de corte. 
* Utilizando o pylab adquira os valores de $V_{in}$, frequência, $V_{out}$ e $\phi$ para uma faixa de valores de frequência. Use $V_{in}$ = 2 V ($V_{in}^{pp}=1 $ V) para a amplitude do sinal de entrada. 

```{note}
* No programa devem ser definidos os valores:
    * frequência inicial= 10 Hz
    * frequência final = 100 kHz
    * pontos = 30
* Antes de utilizar 30 pontos, faça uma varredura com 10 pontos para certificar que está tudo correto.
```


import pandas as pd
data = pd.read_csv('figs/dados_sweep.csv')
from myst_nb import glue
glue("df_pandas_exemplo", data.head())

### Dados disponibilizados
teste de link, [Circuito passa-baixas](dados/passa-baixas.zip)
* Os dados disponibilizados no Teams foram obtidos seguindos os parâmetros acima.
* Dois arquivos: 
    * [Circuito passa-baixas](dados/passa-baixas.zip)
    * [Circuito passa-altas](dados/passa-altas.zip)
* Cada arquivos `.zip` contém:
    * arquivo `.jpg` com uma fotografia do circuito
    * arquivo `dados_sweep.csv`: veja exemplo da estrutura desse arquivo a seguir.
        * 4 colunas
        * a fase (coluna `fase (graus)` corresponde a $\phi = \phi_2-\phi_1$) 
    * pasta `traços-temporal-imagens`:
        * arquivos com nome `sweep_freq_xxx.bmp` correspondendo ao traço temporal utilizado para fazer calcular cada um dos parâmetros do arquivo `dados_sweep.csv`. A numeração `xxx` dos arquivos `.bmp` corresponde ao número presente na primeira coluna  do arquivo `dados_sweep.csv`
        * Certifique-se que você consegue "ler" os dados de um dos arquivos `sweep_freq_xxx.bmp` e obter o resultado correspondente registrado no arquivo `dados_sweep.csv`


````{tabbed} Exemplos tabela de dados
```{glue:figure} df_pandas_exemplo
:figwidth: 600px
:name: "tbl:pandas"
:align: center

Estrutura do arquivo de dados `.csv`, o separador entre as colunas é `,`.
```
````
````{tabbed} Exemplos screenshot osciloscópio
```{figure} figs/sweep_freq_pa_000.png
---
width: 450px
name: "fig:highpass_scope_exemplo"
---
Screenshot do osciloscópio para o passa-altas com $f=10$ Hz!
```
````

## Aplicação do filtro passa-alta

Uma aplicação real muito importante de filtrs é eliminar uma componente indesejada de um sinal elétrico. Suponha um sinal que possui apenas duas frequências,

$$v(t) = v_{01} \cos(2\pi f_1 t)+v_{02} \cos(2\pi f_2 t).$$ (eq:soma_tensao)

No domínio do tempo este sinal pode ser visualizado como é mostrado a seguir.

Como veremos, nosso gerador de funções BK-4052 pode gerar este tipo de sinal, porém ele representa as frequências do sinal utilizando o valor médio, $$f_0=(f_1+f_2)/2,$$ e a diferença de frequência,  $$\delta f= f_1-f_2.$$ Por isto, na sequência a seguir estes valores são calculados e mostrados. Faça esta mesma transformação quando quiser gerar seu sinal.

t = np.linspace(0,5e-3,500) # vetor de tempo
f1,f2= 1e3,0.5e3 # frequencia e fase
v01,v02 = 1,1 # amplitudes
print('f1 = {} Hz'.format(f1))
print('f2 = {} Hz'.format(f2))
print('f0 = (f1+f2)/2 = {} Hz'.format(0.5*(f1+f2)))
print('δf = (f1-f2) = {} Hz'.format(np.abs(f1-f2)))
#----
v1 = v01*np.cos(2*np.pi*f1*t) # sinal v1(t)
v2 = v02*np.cos(2*np.pi*f2*t) # sinal v2(t)
plt.plot(t*1e3, v1+v2, label= '$v(t)=v_1(t)+v_2(t)$')
#--------
#formatação do gráfico
plt.grid(True) # ativa grades
plt.legend(loc='best')
plt.xlabel('Tempo (ms)')
plt.ylabel('Amplitude (V)')
plt.title('Sinal composto por duas ondas senoidais. \n $f_1$={:1g} Hz e $f_2$={:1g} Hz'.format(f1,f2));
#plt.savefig('sinais_defasados.pdf')

## Exemplo de uma transformada de Fourier

De acordo com o teorema de Fourier, qualquer função periódica bem comportada pode ser representada por uma somatória de funções harmônicas. Considere uma função dependente do tempo $t$ tal que $F(t) = F(t+T)$, em que $T$ e o período da função. $F(t)$ pode ser escrita como: $$ F(t) = \cfrac{a_0}{2} + \displaystyle\sum_{n=1}^{\infty} \left(a_n \mathrm{cos}(n \omega_0 t) + b_n \mathrm{sen}(n \omega_0 t)\right)$$

O exemplo abaixo mostra uma função $F(t) = \sin(2\pi {\color{red}{60}} t) + \sin(2\pi {\color{red}{(2\times 10^3)}} t)$, gráfico superior, e a sua transformada de Fourier no gráfico inferior. Note os picos nos valores de $\color{red}{60}$ e $\color{red}{2\times 10^3}$ na transformada de Fourier.

Note que no nosso gerador de funções, é necessário utilizar a função de modulação para gerar os dois sinais simultaneamente:
* Escolha a opção modulação;
* calcule a frequência $f_0,\delta f$ a partir das frequências dos sinais desejados;

A função a seguir foi definida para facilitar nosso cálculo da FFT.

def fft540(time,amp):
    """Função para calcular a FFT de um sinal. 
    Esta função é baseada no comando FFT no Numpy.  
    
    Arguments:
        time {[float]} -- vetor de tempo
        amp {[float]} -- vetor de amplitude
    
    Returns:
        [float] -- vetor de frequências
        [complex float] -- vetor de amplitudes complexas
    """    
    #### fft ####
    timestep = time[1]-time[0] # intervalo de amostragem = dt
    n = len(amp)
    fs = 1/timestep # frequencia de amostragem

    #vetor de frequencias (positivas e negativas)
    freq = np.fft.fftfreq(n, d=timestep)
    #fft
    yfft = np.fft.fft(amp)/n # fft computing and normalization

    return freq, yfft

A seguir construímos os sinais mencionados anteriormente:

t = np.linspace(0,100e-3,int(1e5)) # vetor de tempo
f1,f2= 20,1e3 # frequencia e fase
v01,v02 = 1,1 # amplitudes
#----
v1 = v01*np.cos(2*np.pi*f1*t) # sinal v1(t)
v2 = v02*np.cos(2*np.pi*f2*t) # sinal v2(t)
v = v1+v2 # soma dos dois sinais
#----
print('f1 = {} Hz'.format(f1))
print('f2 = {} Hz'.format(f2))
print('f0 = (f1+f2)/2 = {} Hz'.format(0.5*(f1+f2)))
print('δf = (f1-f2) = {} Hz'.format(np.abs(f1-f2)))
#---- Calculando FFT
freq,Y = fft540(t,v)

### gráfico com 4 eixos###
fig, ax = plt.subplots(2, 2,figsize=[10,7])
#tempo
ax[0,0].plot(1e3*t,v)
ax[0,0].set_xlabel('Tempo (ms)')
ax[0,0].set_ylabel('Amplitude (V)')
#tempo com zoom
ax[1,0].plot(1e3*t,v)
ax[1,0].set_xlabel('Tempo (ms)')
ax[1,0].set_ylabel('Amplitude (V)')
ax[1,0].set_xlim([20,25])
ax[1,0].grid(True)
#fft linear - frequencias negativas e positivas
ax[0,1].plot(freq*1e-3, np.abs(Y),'r*-') # plotting the spectrum
ax[0,1].set_xlabel('Freq (kHz)')
ax[0,1].set_ylabel('|Y(freq)|')
ax[0,1].set_xlim([-5,5])
ax[0,1].grid(True)
#fft semilog - frequencias positivas
mask = range(0,int(len(t)/2)) # máscara para pegar apenas metade do vetor
freq_pos = freq[mask]
Y_pos = Y[mask]
ax[1,1].semilogx(freq_pos*1e-3, np.abs(Y_pos),'r') # plotting the spectrum
ax[1,1].set_xlabel('Freq (kHz)')
ax[1,1].set_ylabel('|Y(freq)|')
ax[1,1].set_xlim([1e-3,1e3])
ax[1,1].grid(True)
#ajustar e mostrar
plt.tight_layout()
plt.show()

## Itens para inlcuir no relatório

### Propriedades do gerador de RF
* Calcule a impedância que o gerador percebe ao se conectar o circuito passa-baixas no mesmo. Mostre em um gráfico como esta impedância varia como função da frequência (utilize ```plt.semilogx```) 
* Com base na tensão medida no canal de entrada ($V_1$) e o circuito Thevenin da nosso gerador, determine a impedância Thevenin do gerador $R_{Th}$

## bibliography

```{bibliography}
:style: unsrt
```

