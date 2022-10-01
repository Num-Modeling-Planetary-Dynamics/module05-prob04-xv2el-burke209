# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 13:08:25 2022

@author: angel
"""
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

files= glob.glob("../data/*XV.csv")

for f in files:
    df = pd.read_csv(f)
    R_sq = df['xh']**2 + df['yh']**2 + df['zh']**2  
    V_sq = df['vxh']**2 + df['vyh']**2 + df['vz']**2
    h_sq = ((df['yh']*df['vz'] - df['zh']*df['vyh'])**2
            + (df['zh']*df['vxh']-df['xh']*df['vz'])**2
            + (df['xh']*df['vyh']-df['yh']*df['vxh'])**2)
    R_dot = np.sqrt(V_sq - h_sq/R_sq)
    
    a = (2.0/np.sqrt(R_sq) - (V_sq))**-1
    e = np.sqrt(1.0-(h_sq/a))
    I = np.arccos((df['xh']*df['vyh']-df['yh']*df['vxh'])/np.sqrt(h_sq))
    long_ascend = np.arcsin((df['yh']*df['vz'] - df['zh']*df['vyh'])/(np.sqrt(h_sq)*np.sin(I)))
    true_anomaly = np.arcsin(((a*(1.0-e**2))/np.sqrt(h_sq)*e)*R_dot)
    arg_periapsis = np.arcsin(df['zh']/np.sqrt(R_sq)*np.sin(I)) - true_anomaly
    
    orbit = {'t':df[' t'],'a':a, 'e':e, 'I':I, 'lon_asc_node':long_ascend,
            'true_anom':true_anomaly, 'arg_peri':arg_periapsis}
    
    df_orbit = pd.DataFrame(data=orbit)
    
    df_orbit.to_csv(f.replace("XV", "EL"))
    
    plt.plot(df[' t'],a)
    plt.title("a vs t")
    plt.savefig('../plots/a_vs_t_'+f.split('\\')[-1][:-4]+'.png',bbox='tight',dpi=300)
    plt.clf()
    plt.plot(df[' t'],I)
    plt.title("I vs t")
    plt.savefig('../plots/I_vs_t_'+f.split('\\')[-1][:-4]+'.png',bbox='tight',dpi=300)
    plt.clf()
    
    



