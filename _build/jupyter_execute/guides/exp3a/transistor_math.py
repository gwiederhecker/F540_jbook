# Transistor math

import matplotlib.pyplot as plt  # importar a bilioteca pyplot para fazer gráficos
import matplotlib.ticker as plticker
import matplotlib.colors as mcolors
import numpy as np   # importar a biblioteca Numpy para lidar com matrizes
import pandas as pd   # importa bilioteca pandas para  lidar com processamento de dados
import os
from scipy import optimize
import SchemDraw as schem
import SchemDraw.elements as e
import matplotlib.colors as mcolors
from myst_nb import glue

def draw_transistor(unit_size, **kwargs):
    d = schem.Drawing(unit=unit_size,**kwargs)
    VB = d.add(e.DOT_OPEN, label='$V_{BB}$')
    RB = d.add(e.RES, d='right',label='$R_{B}$')
    bjt = d.add(e.BJT_NPN_C, d='right')
    #----
    Rc = d.add(e.RES, d='up', xy=bjt.collector, label='$R_C$')
    Vcc = d.add(e.DOT_OPEN, label='$V_{CC}$')
    #RE = d.add(e.RES, d='down', xy=bjt.emitter, label='$R_E$')
    gnd = d.add(e.GND,xy=bjt.emitter)
    return d
def plot_load_lines_transistor(Vcc=10,Rc=100,Vbb=1,Rb=1000):
    def Ib(Vbe,Ies=3*1e-14):
        β = 39.6 #[1/V]
        return Ies*(np.exp(β*Vbe-1))
    def Ic(Vce,Ies=300*1e-14, VEA = 200):
        β = 39.6 #[1/V]
        #VEA = 40 # Early Voltage 
        βr = 0.0001
        αr = βr/(1+βr)
        Vbc = Vbe - Vce
        return Ies*( np.exp(β*Vbe-1)*(1+(Vbe-Vbc)/VEA) - 1/αr*(np.exp(β*Vbc)-1))
    def Vdiodo(I,Is=1e-13):
        β = 39.6 #[1/V]
        return 1/β*np.log(1+I/Is)
    def KVL(V,Vin,R):
        return Vin-R*Ic(V)-V
    def KVLb(V,Vin,R):
        return Vin-R*Ib(V)-V
    def Vdiodo(Vin,V0,R):
        return optimize.brentq(KVL, -1.1*V0, 1.1*V0, args = (Vin,R))
    def Vdiodob(Vin,V0,R):
        return optimize.brentq(KVLb, -1.1*V0, 1.1*V0, args = (Vin,R))
    #return fixed_point(lambda x: Vin-R*Idiodo(x)-x,0.6,args=(1.0,100))
    npt=50
    Vin = Vcc
    Vb0 = Vbb
    #---
    fig_size = (18,6)
    fig,ax = plt.subplots(1,3,figsize=fig_size)
    #------------------
    ax0 = ax[0]
    draw_transistor(2.5).draw(ax=ax0)
    ax0.set_aspect('equal')
    #DivTensao([e.RES,'R'],[e.DIODE,'D'],fonte = [False,e.SOURCE_V]).draw(ax=ax0)
    ax0.axes.get_xaxis().set_visible(False)
    ax0.axes.get_yaxis().set_visible(False)
    ax0.set_frame_on(False)
    ax0.set_xticklabels(())
    ax0.set_yticklabels(())
    ax0.get_figure().set_size_inches(fig_size[0]*0.7,fig_size[1])
    
    #------------------
    #BASE
    Vin_min, Vin_max = 0,2 # [V]
    I_min, I_max = 0,1500e-6 # [μA]
    I=np.linspace(I_min,I_max,npt)
    V = np.linspace(0,1,npt)
    Vlhs = Vb0-Rb*I # equação LHS
    ax0 = ax[1]
    ax0.plot(Vlhs,I*1e6,label = r'$V_{BB}-R_B I_B-V_{BE}(I_B)=0$')
    ax0.plot(V, Ib(V)*1e6, c='r',lw=2, label = r'$I_B(V_{BE})$',zorder=4)
    #solução para corrente e tensão
    Vd = Vdiodob(Vb0,Vb0,Rb) # equação RHS
    Id = Ib(Vd)
    ax0.axhline(1e6*Id, c='k', ls = '--',zorder=0)
    ax0.axvline(Vd, c='k', ls = '--',zorder=0)
    lab =  r'$I_B$,$V_{BE}$'+'={:2.0f} μA, {:2.0f} mV'.format(1e6*Id,1e3*Vd)
    ax0.scatter(Vd,1e6*Id, c='r', marker='o', s=100, label=lab)
    #---
    #lab = '$V_{aberto}$'+'={} V'.format(Vb0)
    ax0.scatter(Vb0,0, color='b', marker='o', s=70,zorder=3)
    #lab = '$I_{curto}$'+'={:2.1f} mA'.format(1e6*Vin/Rb)
    ax0.scatter(0,Vb0/Rb*1e6, color='b', marker='P', s=70,zorder=3)
    #---
    #eixos x-y
    ax0.axhline(0, color='k', linestyle = '-',lw=2)
    ax0.axvline(0, color='k', linestyle = '-',lw=2)
    #-----------------------
    ax0.set_xlabel('Tensão, $V_{BE}$ (V)')
    ax0.set_ylabel('Corrente, $I_B$ (μA)')
    ax0.set_xlim([Vin_min,Vin_max])
    ax0.set_ylim(np.array([I_min,I_max])*1e6)
    ax0.legend(loc = 'lower center',bbox_to_anchor=[0.5,1.0])
    ax0.grid(True,which='both')
    #------------------
    #COLETOR_EMISSOR
    Vbe = Vd # from previous
    #limites dos eixos
    Vin_min, Vin_max = -1,10 # [V]
    I_min, I_max = -1,100 # [mA]
    #-------------
    V = np.linspace(0,10,npt)
    #I = Idiodo(V)  # equação diodo
    I=np.linspace(I_min,I_max,npt)
    #----------------------
    Vlhs = Vin-Rc*I # equação LHS
    #Vlhs = Vin-R*Id # equação LHS
    #Vrhs = Vdiodo(Vin,Vin,R) # equação RHS
    
    
    ax0 = ax[2]
    ax0.plot(Vlhs,I*1e3, label = r'$V_{CC}-R_C I_C-V_{CE}(I_C)=0$')
    ax0.plot(V, Ic(V)*1e3, c='r',lw=2,label = r'$I_C(V_{CE})$',zorder=4)
    #---
    #eixos x-y
    ax0.axhline(0, color='k', linestyle = '-',lw=2)
    ax0.axvline(0, color='k', linestyle = '-',lw=2)
    #---
    #lab = '$V_{aberto}$'+'={} V'.format(Vin)
    ax0.scatter(Vin,0, color='b', marker='o', s=70,zorder=3)
    #lab = '$I_{curto}$'+'={:2.1f} mA'.format(1e3*Vin/Rc)
    ax0.scatter(0,Vin/Rc*1e3, color='b', marker='P', s=70,zorder=3)
    #solução para corrente e tensão
    Vd = Vdiodo(Vin,Vin,Rc) # equação RHS
    Id = Ic(Vd)
    ax0.axhline(1e3*Id, c='k', ls = '--',zorder=0)
    ax0.axvline(Vd, c='k', ls = '--',zorder=0)
    lab = r'$I_C$,$V_{CE}$'+'={:2.0f} mA, {:2.0f} V'.format(1e3*Id,Vd)
    ax0.scatter(Vd,1e3*Id, c='r', marker='o', s=100, label=lab)
    #-----------------------
    ax0.set_xlabel('Tensão, $V_{CE}$ (V)')
    ax0.set_ylabel('Corrente, $I_C$ (mA)')
    ax0.set_xlim([Vin_min,Vin_max])
    ax0.set_ylim([I_min,I_max])
    ax0.legend(loc = 'lower center',bbox_to_anchor=[0.5,1.0])
    ax0.grid(True,which='both')
    ax0.xaxis.set_major_locator(plticker.MultipleLocator(2))
    ax0.yaxis.set_major_locator(plticker.MultipleLocator(10)) 
    
    #ax0.xaxis.set_major_locator(plticker.MultipleLocator(1))
    #ax0.yaxis.set_major_locator(plticker.MultipleLocator(2)) 
    plt.tight_layout()
    return

def plot_ic_curves_transistor(Vcc=10,Rc=100,Vbb_vec=np.arange(0.6,1.8,0.3),Rb=1000):
    def Ib(Vbe,Ies=3*1e-14):
        β = 39.6 #[1/V]
        return Ies*(np.exp(β*Vbe-1))
    def Ic(Vce,Ies=300*1e-14, VEA = 200):
        β = 39.6 #[1/V]
        #VEA = 40 # Early Voltage 
        βr = 0.0001
        αr = βr/(1+βr)
        Vbc = Vbe - Vce
        return Ies*( np.exp(β*Vbe-1)*(1+(Vbe-Vbc)/VEA) - 1/αr*(np.exp(β*Vbc)-1))
    def Vdiodo(I,Is=1e-13):
        β = 39.6 #[1/V]
        return 1/β*np.log(1+I/Is)
    def KVL(V,Vin,R):
        return Vin-R*Ic(V)-V
    def KVLb(V,Vin,R):
        return Vin-R*Ib(V)-V
    def Vdiodo(Vin,V0,R):
        return optimize.brentq(KVL, -1.1*V0, 1.1*V0, args = (Vin,R))
    def Vdiodob(Vin,V0,R):
        return optimize.brentq(KVLb, -1.1*V0, 1.1*V0, args = (Vin,R))
    #return fixed_point(lambda x: Vin-R*Idiodo(x)-x,0.6,args=(1.0,100))
    fig_size = (18,6)
    fig,ax = plt.subplots(1,3,figsize=fig_size)
    colors=list(mcolors.TABLEAU_COLORS.keys())
    for ii,Vbb in enumerate(Vbb_vec):
        npt=50
        Vin = Vcc
        Vb0 = Vbb
        #---

        #------------------
        ax0 = ax[0]
        draw_transistor(2.5).draw(ax=ax0)
        ax0.set_aspect('equal')
        #DivTensao([e.RES,'R'],[e.DIODE,'D'],fonte = [False,e.SOURCE_V]).draw(ax=ax0)
        ax0.axes.get_xaxis().set_visible(False)
        ax0.axes.get_yaxis().set_visible(False)
        ax0.set_frame_on(False)
        ax0.set_xticklabels(())
        ax0.set_yticklabels(())
        ax0.get_figure().set_size_inches(fig_size[0]*0.7,fig_size[1])

        #------------------
        #BASE
        Vin_min, Vin_max = 0,1.5 # [V]
        I_min, I_max = 0,1500e-6 # [μA]
        I=np.linspace(I_min,I_max,npt)
        V = np.linspace(0,1,npt)
        Vlhs = Vb0-Rb*I # equação LHS
        ax0 = ax[1]
        if ii==0: 
            ax0.plot(Vlhs,I*1e6,c=colors[ii],label = r'$V_{BB}-R_B I_B-V_{BE}(I_B)=0$')
            ax0.plot(V, Ib(V)*1e6, c='gray',lw=2, label = r'$I_B(V_{BE})$',zorder=4)
        else: 
            ax0.plot(Vlhs,I*1e6,c=colors[ii]) 
        #solução para corrente e tensão
        Vd = Vdiodob(Vb0,Vb0,Rb) # equação RHS
        Id = Ib(Vd)
#         ax0.axhline(1e6*Id, c='k', ls = '--',zorder=0)
#         ax0.axvline(Vd, c='k', ls = '--',zorder=0)
        lab =  r'$I_B$,$V_{BE}$'+'={:2.0f} μA, {:2.0f} mV'.format(1e6*Id,1e3*Vd)
        ax0.scatter(Vd,1e6*Id, c=colors[ii], marker='o', s=100)
        #---
        #lab = '$V_{aberto}$'+'={} V'.format(Vb0)
        ax0.scatter(Vb0,0, color='b', marker='o', s=70,zorder=3)
        #lab = '$I_{curto}$'+'={:2.1f} mA'.format(1e6*Vin/Rb)
        ax0.scatter(0,Vb0/Rb*1e6, color='b', marker='P', s=70,zorder=3)
        #---
        #eixos x-y
        ax0.axhline(0, color='k', linestyle = '-',lw=2)
        ax0.axvline(0, color='k', linestyle = '-',lw=2)
        #-----------------------
        ax0.set_xlabel('Tensão, $V_{BE}$ (V)')
        ax0.set_ylabel('Corrente, $I_B$ (μA)')
        ax0.set_xlim([Vin_min,Vin_max])
        ax0.set_ylim(np.array([I_min,I_max])*1e6)
        ax0.legend(loc = 'lower center',bbox_to_anchor=[0.5,1.0])
        ax0.grid(True,which='both')


        ax0 = ax[2]
        #------------------
        #COLETOR_EMISSOR
        Vbe = Vd # from previous
        #limites dos eixos
        Vin_min, Vin_max = -1,10 # [V]
        I_min, I_max = -1,100 # [mA]
        #-------------
        V = np.linspace(0,10,npt)
        #I = Idiodo(V)  # equação diodo
        I=np.linspace(I_min,I_max,npt)
        #----------------------
        Vlhs = Vin-Rc*I # equação LHS
        #Vlhs = Vin-R*Id # equação LHS
        #Vrhs = Vdiodo(Vin,Vin,R) # equação RHS


        if ii==0:     
            ax0.plot(Vlhs,I*1e3,c='gray' ,label = r'$V_{CC}-R_C I_C-V_{CE}(I_C)=0$')
            ax0.plot(V, Ic(V)*1e3, c=colors[ii],lw=2,label = r'$I_C(V_{CE})$',zorder=4)
        else:
            #ax0.plot(Vlhs,I*1e3)
            ax0.plot(V, Ic(V)*1e3,c=colors[ii],lw=2,zorder=4)            
        #---
        #eixos x-y
        ax0.axhline(0, color='k', linestyle = '-',lw=2)
        ax0.axvline(0, color='k', linestyle = '-',lw=2)
        #---
        #lab = '$V_{aberto}$'+'={} V'.format(Vin)
        ax0.scatter(Vin,0, color='b', marker='o', s=70,zorder=3)
        #lab = '$I_{curto}$'+'={:2.1f} mA'.format(1e3*Vin/Rc)
        ax0.scatter(0,Vin/Rc*1e3, color='b', marker='P', s=70,zorder=3)
        #solução para corrente e tensão
        Vd = Vdiodo(Vin,Vin,Rc) # equação RHS
        Id = Ic(Vd)
#         ax0.axhline(1e3*Id, c='k', ls = '--',zorder=0)
#         ax0.axvline(Vd, c='k', ls = '--',zorder=0)
        lab = r'$I_C$,$V_{CE}$'+'={:2.0f} mA, {:2.0f} V'.format(1e3*Id,Vd)
        ax0.scatter(Vd,1e3*Id, c=colors[ii], marker='o', s=100)
        #-----------------------
        ax0.set_xlabel('Tensão, $V_{CE}$ (V)')
        ax0.set_ylabel('Corrente, $I_C$ (mA)')
        ax0.set_xlim([Vin_min,Vin_max])
        ax0.set_ylim([I_min,I_max])
        ax0.legend(loc = 'lower center',bbox_to_anchor=[0.5,1.0])
        ax0.grid(True,which='both')
        ax0.xaxis.set_major_locator(plticker.MultipleLocator(2))
        ax0.yaxis.set_major_locator(plticker.MultipleLocator(10)) 

        #ax0.xaxis.set_major_locator(plticker.MultipleLocator(1))
        #ax0.yaxis.set_major_locator(plticker.MultipleLocator(2)) 
    plt.tight_layout()
    return fig

vbbvec=np.arange(0.4,1.8,0.4)
fig = plot_ic_curves_transistor(Vcc=10,Rc=100,Vbb_vec=vbbvec,Rb=1000)
glue("fig_ic_ib_curves",fig,display=False)
glue("vbbvec",print(vbbvec))

Base mesh: $ V_{BB}-R_B I_B-V_{BE}=0$

Colector mesh: $V_{CC}-R_C I_C - V_{CE}=0$

Coupling between base and collector meshes:$I_C = \beta I_B$

The load curve that characterizes the transistor relates the value of $ I_C $ versus $ V_ {CE} $. Note that $ I_C = \ beta I_B $, where $ \beta $ is defined by the transistor and $ I_B $ by the base loop circuit:

$$I_B = \cfrac{V_{BB} - V_{BE}}{R_B}$$

The value of $ V_ {CE} $ is defined by the collector's mesh by the relation:
$$ V_{CE} = V_{CC} - R_C I_C = V_{CC} - R_C (\beta I_B)$$

```{figure} figs/transistor.gif
---
width: 650px
name: "fig:transistor_gif"
---
Solving the transistor using the load line method for varying values of the base current. In this animation, generated in the notebook {doc}`aula_transistor_interativo`, the base voltage $V_BB$ was varied in the range   $0.2 V\leq V_B\leq 1.2 V$.
```

We can see in these relations that for each value of $ I_B $ we have a value of $ I_C $ independent of $ R_C $ and $ V_ {CC} $. In this case, we will have load curves that are plateaus called active operating regions delimited by the region where the reverse polarization of the base-collector diode occurs and the rupture region, where the transistor is damaged and starts to work as a short circuit. The figure on the side illustrates this behavior for a transistor with $ \beta = 100 $.


```{glue:figure} fig_ic_ib_curves
:figwidth: 800px
:name: "fig:fig_ic_ib_curves"
:align: center

$I_C$ curves using $V_BB=${glue:}`vbbvec` V.
```

* when $ V_ {CE} $ is between 0 and 1 V, the base-collector diode is not reverse polarized and therefore $ I_C \rightarrow $ 0 A to $ V_ {CE} \rightarrow $ 0 V, growing exponentially as a function of $ V_ {CE} $: saturation region;
* $ I_C (= \beta I_B) $ is almost constant for a range of $ V_ {CE} $ forming a plateu: active regions;
* transistor rupture region.

def boxsmu(d, smu):
    ''' Draw a dotted box around the SMU element '''
    topleft = smu.inpt + np.array([-.5,1])
    d.add(e.LINE, xy=topleft, tox=topleft[0]+6, d='right', ls=':')
    d.add(e.LINE, d='down', toy=topleft[1]-7, ls=':')
    d.add(e.LINE, d='left', tox=topleft[0], ls=':')
    d.add(e.LINE, d='up',   toy=topleft[1], ls=':')

import SchemDraw as schem
import SchemDraw.elements as e

# d = schemdraw.Drawing()
# d += (V1 := elm.SourceV().label('5V'))

# d = schem.Drawing(unit=2.5)
# d += (iC := e.LINE().right() )



source_color='blue'
#gnd1 = d.add(e.GND,color=source_color)
#d.add(e.LINE, d='up', l=1)
#d.add(e.SOURCE_V, label='$V_{B}$',color=source_color)
VB = d.add(e.DOT_OPEN, label='$V_{B}$')
# d += (iC := e.LINE().right() )
# d.labelI(L1, '$i_g$', top=False)


#---
#transistor
d.add(e.LINE, d='right', xy=RB.end, l=1)
bjt = d.add(e.BJT_NPN_C, d='right')
#----
# #voltage divider
d.add(e.LINE, d='up', xy=bjt.collector, label='$R_C$')
Vcc = d.add(e.DOT_OPEN, label='$V_{C}$')
# RE = d.add(e.RES, d='down', xy=bjt.emitter, label='$R_E$')
# gnd = d.add(e.GNDd)
#---
d.draw()
# d.save(os.path.join(figure_path,'transistor_basic.pdf'))


d = schem.Drawing(unit=2.5)

source_color='blue'
#gnd1 = d.add(e.GND,color=source_color)
#d.add(e.LINE, d='up', l=1)
#d.add(e.SOURCE_V, label='$V_{B}$',color=source_color)
VB = d.add(e.DOT_OPEN, label='$V_{B}$')
RB = d.add(e.RES, d='right',label='$R_{B}$')


#---
#transistor
#d.add(e.LINE, d='right', xy=RB.end, l=1)
bjt = d.add(e.BJT_NPN_C, d='right')
#----
# #voltage divider
Rc = d.add(e.RES, d='up', xy=bjt.collector, label='$R_C$')
Vcc = d.add(e.DOT_OPEN, label='$V_{C}$')
RE = d.add(e.RES, d='down', xy=bjt.emitter, label='$R_E$')
gnd = d.add(e.GND)
# d.add(e.LINE, d='left', l=1.5)
# d.add(e.LINE, d='up', l=0.5)
# Vcc = d.add(e.DOT_OPEN, label='$V_{CC}$')
# #d.add(e.LINE, d='left', y=Rc.end)
# d.add(e.LINE, d='down', l=0.5)
# d.add(e.LINE, d='left', tox=Vout.end)
# d.add(e.RES, d='down', toy=Vout.end, label='$R_1$', color='black')
# d.add(e.RES, d='down', toy=gnd1.start, label='$R_2$', color='black')
# gnd2 = d.add(e.GND)
# #---
# #emitter
# d.add(e.RES, d='down', xy=bjt.emitter, toy=gnd1.start, label='$R_E$')
# gnd3 = d.add(e.GND)
# d.add(e.LINE, d='right', xy=bjt.emitter, l=1)
# cap_out = d.add(e.CAP, d='down', toy=gnd1.start)
# gnd4 = d.add(e.GND)
# #emitter output
# d.add(e.LINE, d='right', xy=cap_out.start, l=0.5)
# d.add(e.DOT_OPEN, label='$V_{out}^{E}$')
# #collector output
# d.add(e.LINE, d='right', xy=bjt.collector, l=1)
# d.add(e.DOT_OPEN, label='$V_{out}^{C}$')
#---
d.draw()
# d.save(os.path.join(figure_path,'transistor_basic.pdf'))


d = schem.Drawing(unit=2.5)

source_color='blue'
gnd1 = d.add(e.GND,color=source_color)
#d.add(e.LINE, d='up', l=1)
d.add(e.SOURCE_SIN, label='$V_{Th}$',color=source_color)
#d.add(e.LINE, d='right', l=1)
d.add(e.RES, d='right',label='$R_{Th}$',color=source_color)
Vout0 = d.add(e.DOT_OPEN,label='$V_{in}$',color=source_color)
#---
# anchors = {
#     'inpt':[0,0],
#     'F':gnd1.start,
#     'S':Vout0.end,}

# gp = schem.group_elements(d, anchors=anchors)
# #---
#boxsmu(d, S1)

#--
d.add(e.CAP, d='right',label='$C_{in}$',color=source_color)
Vout = d.add(e.DOT_OPEN)




#---
#transistor
d.add(e.LINE, d='right', xy=Vout.start, l=2)
bjt = d.add(e.BJT_NPN_C, d='right')
#----
#voltage divider
Rc = d.add(e.RES, d='up', xy=bjt.collector, label='$R_C$')
d.add(e.LINE, d='left', l=1.5)
d.add(e.LINE, d='up', l=0.5)
Vcc = d.add(e.DOT_OPEN, label='$V_{CC}$')
#d.add(e.LINE, d='left', y=Rc.end)
d.add(e.LINE, d='down', l=0.5)
d.add(e.LINE, d='left', tox=Vout.end)
d.add(e.RES, d='down', toy=Vout.end, label='$R_1$', color='black')
d.add(e.RES, d='down', toy=gnd1.start, label='$R_2$', color='black')
gnd2 = d.add(e.GND)
#---
#emitter
d.add(e.RES, d='down', xy=bjt.emitter, toy=gnd1.start, label='$R_E$')
gnd3 = d.add(e.GND)
d.add(e.LINE, d='right', xy=bjt.emitter, l=1)
cap_out = d.add(e.CAP, d='down', toy=gnd1.start)
gnd4 = d.add(e.GND)
#emitter output
d.add(e.LINE, d='right', xy=cap_out.start, l=0.5)
d.add(e.DOT_OPEN, label='$V_{out}^{E}$')
#collector output
d.add(e.LINE, d='right', xy=bjt.collector, l=1)
d.add(e.DOT_OPEN, label='$V_{out}^{C}$')
#---
d.draw()
#plt.savefig(os.path.join(figure_path,'curvas_transistor.pdf'),bbox_inches="tight")
d.save(os.path.join(figure_path,'transistor_amplifier.pdf'))

d = schem.Drawing(unit=2.5)

source_color='blue'
gnd1 = d.add(e.GND,color=source_color)
#d.add(e.LINE, d='up', l=1)
d.add(e.SOURCE_SIN, label='$V_{Th}$',color=source_color)
#d.add(e.LINE, d='right', l=1)
d.add(e.RES, d='right',label='$R_{Th}$',color=source_color)
Vout0 = d.add(e.DOT_OPEN,label='$V_{in}$',color=source_color)
#---
# anchors = {
#     'inpt':[0,0],
#     'F':gnd1.start,
#     'S':Vout0.end,}

# gp = schem.group_elements(d, anchors=anchors)
# #---
#boxsmu(d, S1)

#--
d.add(e.CAP, d='right',label='$C_{in}$')
Vout = d.add(e.DOT_OPEN)




#---
#transistor
d.add(e.LINE, d='right', xy=Vout.start, l=2)
bjt = d.add(e.BJT_NPN_C, d='right')
#----
#voltage divider
Rc = d.add(e.RES, d='up', xy=bjt.collector, label='$R_C$')
d.add(e.LINE, d='left', l=1.5)
d.add(e.LINE, d='up', l=0.5)
Vcc = d.add(e.DOT_OPEN, label='$V_{CC}$')
#d.add(e.LINE, d='left', y=Rc.end)
d.add(e.LINE, d='down', l=0.5)
d.add(e.LINE, d='left', tox=Vout.end)
d.add(e.RES, d='down', toy=Vout.end, label='$R_1$', color='black')
d.add(e.RES, d='down', toy=gnd1.start, label='$R_2$', color='black')
gnd2 = d.add(e.GND)
#---
#emitter
d.add(e.RES, d='down', xy=bjt.emitter, toy=gnd1.start, label='$R_E$')
gnd3 = d.add(e.GND)
d.add(e.LINE, d='right', xy=bjt.emitter, l=1)
cap_out = d.add(e.CAP, d='down', toy=gnd1.start)
gnd4 = d.add(e.GND)
#emitter output
d.add(e.LINE, d='right', xy=cap_out.start, l=0.5)
d.add(e.DOT_OPEN, label='$V_{out}^{E}$')
#collector output
d.add(e.LINE, d='right', xy=bjt.collector, l=1)
d.add(e.DOT_OPEN, label='$V_{out}^{C}$')
#---
d.draw()
d.save('transistor_bias_voltage_divider.pdf')

d = schem.Drawing(unit=2.5)

source_color='blue'
gnd1 = d.add(e.GND,color=source_color)
#d.add(e.LINE, d='up', l=1)
d.add(e.SOURCE_SIN, label='$V_{Th}$',color=source_color)
#d.add(e.LINE, d='right', l=1)
d.add(e.RES, d='right',label='$R_{Th}$',color=source_color)
Vout0 = d.add(e.DOT_OPEN,label='$V_{in}$',color=source_color)
#---
# anchors = {
#     'inpt':[0,0],
#     'F':gnd1.start,
#     'S':Vout0.end,}

# gp = schem.group_elements(d, anchors=anchors)
# #---
#boxsmu(d, S1)

#--
d.add(e.CAP, d='right',label='$C_{in}$')
Vout = d.add(e.DOT_OPEN)




#---
#transistor
d.add(e.LINE, d='right', xy=Vout.start, l=2)
bjt = d.add(e.BJT_NPN_C, d='right')
#----
#voltage divider
Rc = d.add(e.RES, d='up', xy=bjt.collector, label='$R_C$')
d.add(e.LINE, d='left', l=1.5)
d.add(e.LINE, d='up', l=0.5)
Vcc = d.add(e.DOT_OPEN, label='$V_{CC}$')
#d.add(e.LINE, d='left', y=Rc.end)
d.add(e.LINE, d='down', l=0.5)
d.add(e.LINE, d='left', tox=Vout.end)
d.add(e.RES, d='down', toy=Vout.end, label='$R_1$', color='black')
d.add(e.RES, d='down', toy=gnd1.start, label='$R_2$', color='black')
gnd2 = d.add(e.GND)
#---
#emitter
d.add(e.LINE, d='down', xy=bjt.emitter, l=1)
gnd3 = d.add(e.GND)
#emitter output
#collector output
d.add(e.LINE, d='right', xy=bjt.collector, l=1)
d.add(e.DOT_OPEN, label='$V_{out}^{C}$')
#---
d.draw()
d.save('transistor_bias_voltage_divider.pdf')


d = schem.Drawing(unit=2.5)
R7 = d.add(e.RES, d='right', botlabel='$R_7$')
R6 = d.add(e.RES, d='right', botlabel='$R_6$')
d.add(e.LINE, d='right', l=2)
d.add(e.LINE, d='right', l=2)
R5 = d.add(e.RES, d='up' , botlabel='$R_5$')
R4 = d.add(e.RES, d='up', botlabel='$R_4$')
d.add(e.LINE, d='left', l=2)
d.push()
R3 = d.add(e.RES, d='down', toy=R6.end, botlabel='$R_3$')
# d.pop()
# d.add(e.LINE, d='left', l=2)
# d.push()
# R2 = d.add(e.RES, d='down', toy=R6.end, botlabel='$R_2$')
# d.pop()
# R1 = d.add(e.RES, d='left', tox=R7.start, label='$R_1$')
# Vt = d.add(e.BATTERY, d='up', xy=R7.start, toy=R1.end, label='$V_t$', lblofst=0.3)
# d.labelI(Vt, arrowlen=1.5, arrowofst=0.5)
d.draw()
d.save('7_resistors_3_loops.png')


d = schem.Drawing(inches_per_unit=.5, unit=3)
D1 = d.add(e.DIODE, theta=-45)
d.add(e.DOT)
D2 = d.add(e.DIODE, theta=225, reverse=True)
d.add(e.DOT)
D3 = d.add(e.DIODE, theta=135, reverse=True)
d.add(e.DOT)
D4 = d.add(e.DIODE, theta=45)
d.add(e.DOT)

d.add(e.LINE, xy=D3.end, d='left', l=d.unit*1.5)
d.add(e.DOT_OPEN)
d.add(e.GAP, d='up', toy=D1.start, label='AC IN')
d.add(e.LINE, xy=D4.end, d='left', l=d.unit*1.5)
d.add(e.DOT_OPEN)

top = d.add(e.LINE, xy=D2.end, d='right', l=d.unit*3)
Q2 = d.add(e.BJT_NPN_C, anchor='collector', d='up', label='Q2\n2n3055')
d.add(e.LINE, xy=Q2.base, d='down', l=d.unit/2)
Q2b = d.add(e.DOT)
d.add(e.LINE, d='left', l=d.unit/3)
Q1 = d.add(e.BJT_NPN_C, anchor='emitter', d='up', label='Q1\n    2n3054')
d.add(e.LINE, d='up', xy=Q1.collector, toy=top.center)
d.add(e.DOT)

d.add(e.LINE, d='down', xy=Q1.base, l=d.unit/2)
d.add(e.DOT)
d.add(e.ZENER, d='down', reverse=True, botlabel='D2\n500mA')
d.add(e.DOT)
G = d.add(e.GND)
d.add(e.LINE, d='left')
d.add(e.DOT)
d.add(e.CAP_P, botlabel='C2\n100$\mu$F\n50V', d='up', reverse=True)
d.add(e.DOT)
d.push()
d.add(e.LINE, d='right')
d.pop()
d.add(e.RES, d='up', toy=top.end, botlabel='R1\n2.2K\n50V')
d.add(e.DOT)

d.here = [d.here[0]-d.unit, d.here[1]]
d.add(e.DOT)
d.add(e.CAP_P, d='down', toy=G.start, label='C1\n 1000$\mu$F\n50V', flip=True)
d.add(e.DOT)
d.add(e.LINE, xy=G.start, tox=D4.start, d='left')
d.add(e.LINE, d='up', toy=D4.start)

d.add(e.RES, d='right', xy=Q2b.center, label='R2', botlabel='56$\Omega$ 1W')
d.add(e.DOT)
d.push()
d.add(e.LINE, d='up', toy=top.start)
d.add(e.DOT)
d.add(e.LINE, d='left', tox=Q2.emitter)
d.pop()
d.add(e.CAP_P, d='down', toy=G.start, botlabel='C3\n470$\mu$F\n50V')
d.add(e.DOT)
d.add(e.LINE, d='left', tox=G.start, move_cur=False)
d.add(e.LINE, d='right')
d.add(e.DOT)
d.add(e.RES, d='up', toy=top.center, botlabel='R3\n10K\n1W')
d.add(e.DOT)
d.add(e.LINE, d='left', move_cur=False)
d.add(e.LINE, d='right')
d.add(e.DOT_OPEN)
d.add(e.GAP, d='down', toy=G.start, label='$V_{out}$')
d.add(e.DOT_OPEN)
d.add(e.LINE, d='left')
#d.draw(showplot=True)
# d.save('powersupply.svg')

d.draw(showplot=True)

