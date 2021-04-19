# Guide to Experiment 3a: Transistor characterization

Métodos da Físcia Experimental I: (F540 2s2020)

* JupyterBook: Gustavo Wiederhecker, Varlei Rodrigues
* Contributions: Daniel Ugarte, Antônio Riul Junior, Varlei Rodrigues

#-----------------------------
#Pacote para manipular vetores e matrizes
import numpy as np
import os
import pandas as pd
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
from myst_nb import glue
#pacote para desenhar circuitos
import SchemDraw as schem
import SchemDraw.elements as e
d = schem.Drawing(unit=2.5) # unit=2.5 determina o tamanho dos componentes
# %config InlineBackend.figure_format = 'svg'

In this experiment, the basic properties of a bipolar junctio transistor will be explored.

The name transistor ([a combination of transfer + resistor](https://web.archive.org/web/20080528164454/http://users.arczip.com/rmcgarra2/namememo.gif))originates from this device capabiblity of transferring electric signals. It is an *active device* that amplifies the voltage or current of an input signal, therefore, it is necessary to use a power supply. The transistor is a sandwich of two *pn* junctions, facing each other, forming a sequence of $ npn $ or $ pnp $ junctions. Each of these parts is called the collector, base and emitter, and the information to be transferred and / or used as a control signal is applied to the base of the transistor.

To fully appreciate this device, it is desirable that you read an introductory  text on the semiconductors properties and circuit treatment of transistors (Sections 4.1 to 4.3 in {cite}`eggleston2011basic`).

:::{admonition} Goals
:class: tip
- 	Measure the characteristic curve of a bipolar junction transistor (BJT).
-   Measure the value of the current gain $ (\beta) $ of the BJT transistor.
:::

:::{admonition} Items to include in your lab report
:class: warning
1. From the experimental data, reconstruct the transistor collector curves ($I_C(V_{CE})$). You must generate the graphs, based on the data provided in {ref}`sec:dataset_transistor_3a`.
    * Try to add the different traces to a single figure, instead of adding multiple repetitive plots to your report. Consider distinct line colors for each trace.
    * Be carefull to properly convert the voltage measurements into currents using the appropriate values for the resistors.
2. Include a graph of $I_C(I_B)$ and determine the transistor gain.
    * Make sure to include the linear fitting you used  to determine $\beta$
4. Provide hyperlinks to your TinkerCAD simulation and upload your QUCS file.
:::


## Characteristic curves (I-V curve)
presents characteristic curves for the bipolar junction transistor BD 135, being similar for other junction transistors. For each current value of the base there is a current in the collector, for which the equation below is satisfied:

$$ I_\text{collector} = \beta \times I_\text{base}, $$ (eq:transitor_ic_ib)


In general, for {eq}`eq:transitor_ic_ib` to be valid, if ($V_{CE}$) is  higher than the $V_{BE}$ , which is required  to polarize the transistor into the active region. Play around with the background theory notebook ( {doc}`aula_transistor_interativo`) to get an insight into the the transistor behavior. An example of the *IV* curves generated at this notebook are shown in {numref}`fig:transistor_gif`:
```{figure} figs/transistor.gif
---
width: 650px
name: "fig:transistor_gif"
---
Solving the transistor using the load line method for varying values of the base current.
```


Characteristics curves are often presented in transistor datasheets, such as the example in {numref}`fig:bjt_sheet`
```{figure} figs/ic_vce_curve.png
---
width: 350px
name: "fig:bjt_sheet"
align: center
---
Example [datasheet from manufacturer](https://github.com/gwiederhecker/F540_jbook/blob/2021_1s/guides/exp3a/figs/BD135_datasheet.pdf?raw=true) showing transistor gain characterization
```

## Transistor  gain $\beta$
The gain of a transistor depends on its construction, current range and the frequency of operation of the circuit assembly. For the transistor BD 135, the characteristic curves as a function of the current $ I_B $ are illustrated in {numref}`fig:ic_ib_bjt`

```{figure} figs/curva2.png
---
width: 350px
name: "fig:ic_ib_bjt"
align: center
---
Example dateset of transistor gain characterization
```

An approximate value of the $ (\beta) $ gain can be obtained on a linear graph of $ I_c $ as a function of $ I_B $, the gain being given by the slope of the line, as in the example of {numref}`fig:ic_ib_bjt`.

## Measuring characterisitic curves
The characteristic curve of a transistor is the graph of $ I_C $ for $ V_ {CE} $. The proposed assembly for this measure is illustrated in the figure below.
Note that the assembly is formed by a voltage divider (resistors $ R2 $ and $ R3 $) that feeds the base of the transistor through the resistor $ R1 $, imposing a fixed $ (approximately) $ current of $ I_B $ at the base. After the transistor is polarized, the current in the collector will be given by the golden rule: $ I_ {collector} = \beta \times I_ {base} $.

To obtain the value of $ I_B $, it is necessary to measure the potential drop in the resistance of the base $ (R1) $. The potential on the transistor, between the collector and the emitter $ (V_{CE}) $, is measured directly with a voltmeter or with the oscilloscope. 

Only the $ I_C $ measure is missing. Since the power supply is fixed at $ 15 V $, from the measurement of $ V_ {CE} $ and the resistance value of decades it is possible to calculate the current in the collector, $ I_C $. Therefore, it is enough to vary the resistance of decades to obtain each curve. Try to obtain a larger number of points in the region where the variation of $ V_ {CE} $ is more abrupt (lower values of voltage $ V_ {CE} $). 3 $ I_C $ curves must be measured by $ V_ {CE} $, with $ R_1 $ = 10 k $ \Omega $, 15 k $ \Omega $ and 18 k $ \Omega $.

```{figure} figs/medida_caracteristica.png
---
width: 400px
name: "fig:bjt_setup1"
align: center
---
Circuit schematic used in the transistor characterization
```

## Measuring transistor Gain 
The gain of the $ (\beta) $ transistor can be obtained simply by the ratio between the current in the collector and the current in the emitter, as previously shown. In a variation of the previous assembly, we can measure the gain of the transistor. We will use the a linear voltage ramp to vary the base voltage and, consequently, the current at the base of the transistor. 

The current $ I_C $ is measured through the resistance $ RC $, while $ I_B $ is measured against the resistance $R_B$.
 By controlling either the base voltage ($V_{BB}$), or the base resistace $R_B$, it is possible to control $ I_B $.
```{figure} figs/esquema_medida_beta.png
---
width: 400px
name: "fig:bjt_setup2"
align: center
---
Circuit schematic used in the transistor gain characterization. The internal resistance of the base voltage source is 50 Ohms.
```

### Videos of the experiments
**You must login with you @m.unicamp.br account to view these videos!**

#### Characteristic curves
This first video illustrate the experimental procedure and data acquisition associated with the characteristic curves.

<iframe width="640" height="360" src="https://web.microsoftstream.com/embed/video/b5122894-1a3c-4a64-92c5-203a3a189128?autoplay=false&amp;showinfo=true" allowfullscreen style="border:none;"></iframe>

#### Transistor gain
This second video illustrate the experimental procedure and data acquisition associated with the transistor gain.

<iframe width="640" height="360" src="https://web.microsoftstream.com/embed/video/1de87b4e-eed9-4e2a-895f-fbfedb97feea?autoplay=false&amp;showinfo=true" allowfullscreen style="border:none;"></iframe>

#Loading dataset with "tab" as separator
path='dados'
filename = 'dados_Vce_Vcc_15p5.csv'
filepath = os.path.join(path,filename)
df1 = pd.read_csv(filepath) #DataFrame
glue("df_pandas_ic_vce", df1.head())
#---
filename = 'dados_Ic_vs_Ib_Vbb_Vcc_15p5V.csv'
filepath = os.path.join(path,filename)
df2 = pd.read_csv(filepath) #DataFrame
glue("df_pandas_beta", df2.head())

(sec:dataset_transistor_3a)=
### Downloadable dataset
* One (.zip) file: [Transistor characterization](https://github.com/gwiederhecker/F540_jbook/blob/2021_1s/guides/exp3a/dados/dados_transistor_3a?raw=true)
    * `.zip` file contains:
        * `dados_Vce_Vcc_15p5.csv` file corresponding to the characteristic curves (see {numref}`tbl:pandas_ic_vce`)
        * `dados_Ic_vs_Ib_Vbb_Vcc_15p5V.csv` file corresponding to the $I_C$ versus $I_B$ curve. (see {numref}`tbl:pandas_ic_vce`)
    * Images of the protoboard assembly. 


````{tabbed} Characteristic curves
```{glue:figure} df_pandas_ic_vce
:figwidth: 600px
:name: "tbl:pandas_ic_vce"
:align: center

Structure of the `dados_Vce_Vcc_15p5.csv` data file, corresponding to the decade resistance  indicated at the column label; the separator between entries is a **comma (,)**.
```
````
````{tabbed} Gain characterization
```{glue:figure} df_pandas_beta
:figwidth: 600px
:name: "tbl:pandas_beta"
:align: center

Structure of the `dados_Ic_vs_Ib_Vbb_Vcc_15p5V.csv` data file, corresponding to the osciloscope traces measured at distinct point in the circuit; the separator between entries is a **comma (,)**.
```
````