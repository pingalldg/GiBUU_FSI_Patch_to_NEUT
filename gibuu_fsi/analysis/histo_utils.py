# histo_utils.py
import uproot
import numpy as np
import awkward as ak
def histo(f1,f2):
    last_run = 1
    file_path = f1
    
    first = True
    
    current_run = 0
    current_event = 0
    events = {}
    with open(file_path, 'r') as file:
        for line in file:
            if first:
                first = False
            else:
                x = line.split()
                if int(x[0]) > current_run:
                    current_run = int(x[0])
                    events[current_run] = {}
                    current_event = 0
                if int(x[1]) > current_event:
                    current_event = int(x[1])
                    events[current_run][current_event] = []
                events[current_run][current_event].append({'id': int(x[2]), 'charge': int(x[3]), 'perweight': float(x[4]), 'position': (float(x[5]), float(x[6]), float(x[7])), 'momentum': (float(x[8]), float(x[9]), float(x[10]), float(x[11])), 'history': int(x[12]), 'production_id': int(x[13]), 'enu': float(x[14])})
    num_runs = len(events)
    
    file_path =  f1
    first = True
    
    current_run = 0
    current_event = 0
    eventid=[]
    ID = []
    Charge = []
    perweight = []
    x_g = []
    y_g = []
    z_g = []
    E_g = []
    px_g = []
    py_g = []
    pz_g = []
    history = []
    production_ID = []
    enu = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if first:
                first = False
            else:
                x = line.split()
                if int(x[0]) > current_run:
                    # print("current_run, (x[0])", x[0],current_run)
                    current_run = int(x[0])
                    current_event = 0
                if current_run != last_run:
                    continue
                if int(x[1]) > current_event:
                    # print("current_event, (x[1])", x[1],current_event)  
                    current_event = int(x[1])
                    perweight.append(float(x[4]))
                    production_ID.append(int(x[13]))
                    enu.append(float(x[14]))
                    eventid.append([])
                    ID.append([])
                    Charge.append([])
                    x_g.append([])
                    y_g.append([])
                    z_g.append([])
                    E_g.append([])
                    px_g.append([])
                    py_g.append([])
                    pz_g.append([])
                    history.append([])
                eventid[-1].append(current_event)
                ID[-1].append(int(x[2]))
                Charge[-1].append(int(x[3]))
                x_g[-1].append(float(x[5]))
                y_g[-1].append(float(x[6]))
                z_g[-1].append(float(x[7]))
                E_g[-1].append(float(x[8]))
                px_g[-1].append(float(x[9]))
                py_g[-1].append(float(x[10]))
                pz_g[-1].append(float(x[11]))
                history[-1].append(float(x[12]))
    eventid=ak.Array(eventid)            
    ID = ak.Array(ID)
    Charge = ak.Array(Charge)
    perweight_g = ak.Array(perweight)
    x_g = ak.Array(x_g)
    y_g = ak.Array(y_g)
    z_g = ak.Array(z_g)
    E_g = ak.Array(E_g)
    px_g = ak.Array(px_g)
    py_g = ak.Array(py_g)
    pz_g = ak.Array(pz_g)
    history = ak.Array(history)
    production_ID = ak.Array(production_ID)
    enu = ak.Array(enu)
    
    file_path2 = f2
    first = True
    
    current_run = 0
    current_event = 0
    init_id=[]
    init_charge=[]
    init_x = []
    init_y = []
    init_z = []
    init_E = []
    init_px = []
    init_py = []
    init_pz = []
    init_event_number = []
    init_perweight = []
    
    with open(file_path2, 'r') as file:
        for line in file:
            if first:
                first = False
            else:
                x = line.split()
                init_id.append(int(x[3]))
                init_charge.append(int(x[4]))                
                init_E.append(float(x[8]))
                init_px.append(float(x[9]))
                init_py.append(float(x[10]))
                init_pz.append(float(x[11][:-1]))
                init_x.append(float(x[12]))
                init_y.append(float(x[13]))
                init_z.append(float(x[14][:-1]))
                init_event_number.append(int(x[16][:-1]))
                init_perweight.append(float(x[19]))
    init_id= ak.Array(init_id[:])   
    init_charge= ak.Array(init_id[:])                
    init_E = ak.Array(init_E[:])
    init_px = ak.Array(init_px[:])
    init_py = ak.Array(init_py[:])
    init_pz = ak.Array(init_pz[:])
    init_x = ak.Array(init_x[:])
    init_y = ak.Array(init_z[:])
    init_z = ak.Array(init_z[:])
    init_event_number = ak.Array(init_event_number[:])
    init_perweight = ak.Array(init_perweight[:]) 

    init_id_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_ch_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_E_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_px_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_py_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_pz_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_x_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_y_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_z_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_perweight_mod=np.zeros(np.max(np.unique(ak.flatten(eventid))))
    init_id_mod[init_event_number-1]=init_id
    init_ch_mod[init_event_number-1]=init_charge    
    init_E_mod[init_event_number-1]=init_E
    init_px_mod[init_event_number-1]=init_px
    init_py_mod[init_event_number-1]=init_py
    init_pz_mod[init_event_number-1]=init_pz
    init_x_mod[init_event_number-1]=init_x
    init_y_mod[init_event_number-1]=init_y
    init_z_mod[init_event_number-1]=init_z
    init_perweight_mod[init_event_number-1]=init_perweight
    len(production_ID)
    Q2_g = - (enu-E_g[:,0])**2 + px_g[:,0]**2 + py_g[:,0]**2 + (enu-pz_g[:,0])**2
    
    W_g = np.sqrt((enu-E_g[:,0]+E_g[:,1])**2 - (-px_g[:,0]+px_g[:,1])**2 - (-py_g[:,0]+py_g[:,1])**2 - (enu-pz_g[:,0]+pz_g[:,1])**2)
    
    costheta_g = pz_g / np.sqrt(px_g**2 + py_g**2 + pz_g**2)
    
    perweight = perweight_g*1e-38
    
    final = ak.local_index(ID, axis=1) != 1
    chase_g = ak.local_index(ID, axis=1) != 1
    pdg_to_mass = {
        13: 0.10566,
        14: 0,
    
        22: 0,
    
        130: 0.49761,
        310: 0.49761,
    
        111: 0.13498,
        211: 0.13957,
    
        221: 0.54785,
        223: 0.78265,
    
        311: 0.49761,
        321: 0.49368,
    
        2112: 0.93957,
        2212: 0.93827,
    
        1114: 1.232,
        2114: 1.232,
        2214: 1.232,
        2224: 1.232,
    
        3122: 1.1157,
    
        3112: 1.1974,
        3212: 1.1926,
        3222: 1.1894,
    
        3312: 1.3217,
        3322: 1.3149,
    }
    ID_to_pdg = {
        # Nucleons resonance
        (1,+0): 2112,
        (1,+1): 2212,
    
        (2,-1): 1114,
        (2,+0): 2114,
        (2,+1): 2214,
        (2,2): 2224,
        
        (3,+0): 202112,
        (3,+1): 202212,
    
        (4,+0): 102112,
        (4,+1): 102212,
    
        (5,+0): 122112,
        (5,+1): 122212,
    
        (7,+0): 102114,
        (7,+1): 102214,
    
        (8,+0): 112114,
        (8,+1): 112214,
    
        (10,+0): 102116,
        (10,+1): 102216,
    
        (12,+0): 212112,
        (12,+1): 212212,
    
        (14,+0): 212114,
        (14,+1): 212214,
    
        (16,+0): 202116,
        (16,+1): 202216,
    
        (19,-1): 111112,
        (19,+0): 112112,
        (19,+1): 112212,
        (19,+2): 112222,
    
        (21,-1): 121114,
        (21,+0): 122114,
        (21,+1): 122214,
        (21,+2): 122224,
    
        (26,-1): 221112,
        (26,+0): 222112,
        (26,+1): 222212,
        (26,+2): 222222,
    
        (27,-1): 201114,
        (27,+0): 202114,
        (27,+1): 202214,
        (27,+2): 202224,
    
        (28,-1): 221114,
        (28,+0): 222114,
        (28,+1): 222214,
        (28,+2): 222224,
    
        (30,-1): 211116,
        (30,+0): 212116,
        (30,+1): 212216,
        (30,+2): 212226,
        
        (31,-1): 201118,
        (31,+0): 202118,
        (31,+1): 202218,
        (31,+2): 202228,
    
        # Baryons with strangeness s=-1
        (32,+0): 3122,
    
        (33,-1): 3112,
        (33,+0): 3212,
        (33,+1): 3222,
    
        (34,-1): 3114,
        (34,+0): 3214,
        (34,+1): 3224,
    
        (35,+0): 102132,
        (36,+0): 102134,
        (37,+0): 203122,
        (38,+0): 103122,
        (39,+0): 103124,
        (40,+0): 213122,
        (41,+0): 203126,
        (42,+0): 103126,
    
        (43,-1): 103114,
        (43,+0): 103214,
        (43,+1): 103224,
    
        (44,-1): 103116,
        (44,+0): 103216,
        (44,+1): 103226,
    
        (45,-1): 203118,
        (45,+0): 203218,
        (45,+1): 203228,
    
        (46,+0): 123122,
        (47,+0): 213124,
    
        (50,-1): 203112,
        (50,+0): 203212,
        (50,+1): 203222,
    
        (51,-1): 113112,
        (51,+0): 113212,
        (51,+1): 113222,
    
        (52,-1): 203116,
        (52,+0): 203216,
        (52,+1): 203226,
    
        # Baryons with strangeness s=-2
        (53,-1): 3312,
        (53,+0): 3322,
    
        (54,-1): 3314,
        (54,+0): 3324,
    
        # Baryons with strangeness s=-3
        (55,-1): 3334,
    
        # Baryons with charm c=+1
        (56,+1): 4122,
    
        (57,+0): 4112,
        (57,+1): 4212,
        (57,+2): 4222,
    
        (58,+0): 4114,
        (58,+1): 4214,
        (58,+2): 4224,
    
        (59,+0): 4132,
        (59,+1): 4232,
    
        (60,+0): 4314,
        (60,+1): 4324,
    
        (61,+0): 4332,
    
        # Mesons
        (101,-1): -211,
        (101,+0): +111,
        (101,+1): +211,
    
        (102,+0): 221,
    
        (103,-1): -213,
        (103,+0): +113,
        (103,+1): +213,
    
        (104, +0): 9000221,
        (105, +0): 223,
        (106, +0): 331,
        (107, +0): 333,
        (108, +0): 441,
        (109, +0): 443,
    
        (110,+0): 311,
        (110,+1): 321,
        
        (111,-1): -321,
        (111,+0): -311,
    
        (112,+0): 313,
        (112,+1): 323,
    
        (113,-1): -323,
        (113,+0): -313,
    
        (114,+0): 411,
        (114,+1): 421,
    
        (115,-1): -421,
        (115,+0): -411,
    
        (116,+0): 413,
        (116,+1): 423,
    
        (117,-1): -423,
        (117,+0): -413,
        
        (118,+1): 431,
        (119,-1): -431,
        (120,+1): 433,
        (121,-1): -433,
        (122,+0): 225,
    
        # Leptons
        (901,-1): 11,
        (902,-1): 13,
        (903,-1): 15,
        
        (911,+0): 12,
        (912,+0): 14,
        (913,+0): 16,
    
        # Gauge bosons
        (997,-1): -24,
        (997,+1): 24,
        (998,+0): 23,
        (999,+0): 22,
    
        # Antiparticles
        (-1,+0): -2112,
        (-1,-1): -2212,
    }
    
    def mass_from_pdg(PDG):
        """
        Determine masses of particles from PDG ID

        """
        pdg_flatten = np.abs(ak.flatten(PDG))
        
        res = ak.to_numpy(ak.zeros_like(ak.values_astype(pdg_flatten, 'float64')))
        for (i, val) in pdg_to_mass.items():
            mask = (pdg_flatten == i)
            res[mask] = val
    
        remaining = np.unique(pdg_flatten[(res==0) & ~((pdg_flatten==12)|(pdg_flatten==14)|(pdg_flatten==16)|(pdg_flatten==22))])
        if len(remaining) > 0:
            print(f"Unassigned masses : {remaining}")
        return ak.unflatten(res, ak.num(PDG))
    # GiBUU particles that have no PDG equivalent
    no_PDG = [6, 9, 11, 13, 15, 17, 18, 20, 22, 23, 24, 25, 29, 48, 49]
## Determine masses of particles according to pdg
    
    def pdg_from_id(ID, Charge):
        """
        Determine PDG id from GiBUU ID and charge of particles
    
        """
        ID_flatten = ak.flatten(ID)
        Charge_flatten = ak.flatten(Charge)
        
        res= ak.to_numpy(ak.zeros_like(Charge_flatten))
        for ((i, charge), val) in ID_to_pdg.items():
            mask = (ID_flatten == i) & (Charge_flatten == charge)
            res[mask] = val
        for i in no_PDG:
            errors = Charge_flatten[ID_flatten==i]
            if len(errors) > 0:
                for c in errors:
                    print(f"Particle with ID {i} and charge {c} has no PDG")
        mask = res==0
        masked_id = ID_flatten[mask]
        masked_charge = Charge_flatten[mask]
        remaining = np.column_stack((masked_id, masked_charge))
        uniques = np.unique(remaining, axis=0)
        for (i,c) in uniques:
            print(f"! No pdg found for particle with ID {i} and charge {c}")
        return ak.unflatten(res, ak.num(ID))
    
    
####################################################
    M_P = 0.93827
    E_CUT = 0.035

    # finalstate particle quantities
    pdg_g = pdg_from_id(ID, Charge)
    mass_g = mass_from_pdg(pdg_g)
    pmom_g = np.sqrt(px_g**2 + py_g**2 + pz_g**2)
    Ekin_g = np.sqrt(pmom_g**2 + mass_g**2) - mass_g - E_CUT

    # initial state quantities (one per event)
    pinit = np.sqrt(init_px_mod**2 + init_py_mod**2 + init_pz_mod**2)
    Ekin_init = np.sqrt(pinit**2 + M_P**2) - M_P - E_CUT

    # DENOMINATOR selection: initial particle is a proton above threshold
    weight_ok = abs(init_perweight_mod - perweight_g) < 1e-4
    sel_den = (init_id_mod == 1) & (init_ch_mod == 1) & weight_ok & (Ekin_init > 0.)

    # NUMERATOR selection: exactly one chased proton above threshold,
    # no other chased hadrons, and the event has passed the denominator cut
    is_p   = (pdg_g == 2212) & (chase_g == 1) & (Ekin_g > 0.)
    is_had = (pdg_g > 99) & (chase_g == 1)
    one_p  = (ak.num(pdg_g[is_p]) == 1) & (ak.num(pdg_g[is_had]) == 1)
    mask   = ak.to_numpy(one_p & sel_den)

    # pick the proton 
    px_p   = ak.to_numpy(ak.firsts(px_g[is_p])[mask])
    py_p   = ak.to_numpy(ak.firsts(py_g[is_p])[mask])
    pz_p   = ak.to_numpy(ak.firsts(pz_g[is_p])[mask])
    p_p    = ak.to_numpy(ak.firsts(pmom_g[is_p])[mask])
    hist_p = ak.to_numpy(ak.firsts(history[is_p])[mask])

    # angle between final proton and initial proton (radians)
    pinit_sel = np.asarray(pinit[mask])
    cos_th = (px_p * np.asarray(init_px_mod[mask])+
              py_p * np.asarray(init_py_mod[mask])+
              pz_p * np.asarray(init_pz_mod[mask])) / (p_p*pinit_sel)
    deviation = np.arccos(np.clip(cos_th, -1.0, 1.0))

    angle_ok = deviation < np.radians(5.0)   # 5 degrees
    no_int   = hist_p == 0                   # proton did not interact

    # binning
    N = 25
    bins = np.linspace(0, 6.5, N + 1)
    bins_mid = 0.5 * (bins[1:] + bins[:-1])

    # histograms: everything in INITIAL proton momentum
    case_1 = pinit_sel[angle_ok]
    case_2 = pinit_sel[no_int]
    denominator = np.asarray(pinit[sel_den])

    case_1_hist      = np.histogram(case_1, bins=bins)[0]
    case_2_hist      = np.histogram(case_2, bins=bins)[0]
    denominator_hist = np.histogram(denominator, bins=bins)[0]

    #sanity check: ratio must be <= 1 in every bin
    assert np.all(case_1_hist <= denominator_hist)
    assert np.all(case_2_hist <= denominator_hist)

    return bins_mid, case_1_hist, case_2_hist, denominator_hist
    # return eventid, init_perweight_mod
base = '/data/neutrinos/scratch/pingal/GiBUU2023/release2023'
def compute(i):
    part_path = f'{base}/eqs3_ccqe_BBA05/{i}/PertParticles_Init_ALL.dat'
    part_path2= f'{base}/eqs5_ccqe_BBA05/{i}/PertParticles_Init_ALL.dat'
    part_path3= f'{base}/eqs0_ccqe_BBA05/{i}/PertParticles_Init_ALL.dat'
    a_i = histo(f'{base}/eqs3_ccqe_BBA05/{i}/FinalEvents.dat', part_path)
    b_i = histo(f'{base}/eqs5_ccqe_BBA05/{i}/FinalEvents.dat', part_path2)
    c_i = histo(f'{base}/eqs0_ccqe_BBA05/{i}/FinalEvents.dat', part_path3)
    return a_i, b_i,c_i
   #I created 1000 runs for each EQS and added the histograms properly to create the transparency plot.
