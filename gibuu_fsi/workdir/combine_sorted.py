import os
import numpy as np
import uproot
import awkward as ak

# Root directory of incident folders
incident_root_dir = "./"  

# Lists of arrays per incident
incident_numbers = []
id_list = []
charge_list = []
perweight_list = []
posX_list = []
posY_list = []
posZ_list = []
momE_list = []
momX_list = []
momY_list = []
momZ_list = []
history_list = []
prod_id_list = []
enu_list = []

def parse_line(line):
    tokens = line.strip().split()
    if len(tokens) < 15:
        return None
    try:
        ID = int(tokens[2])
        Charge = int(tokens[3])
        perweight = float(tokens[4].replace("-318", "e-318"))
        pos = list(map(float, tokens[5:8]))
        mom = list(map(float, tokens[8:12]))
        history = int(tokens[12])
        prod_id = int(tokens[13])
        enu = float(tokens[14])
        return {
            "ID": ID,
            "Charge": Charge,
            "perweight": perweight,
            "pos": pos,
            "mom": mom,
            "history": history,
            "prod_id": prod_id,
            "enu": enu
        }
    except Exception as e:
        print(f"Skipping line due to error: {e}")
        return None

incident_counter = 50001
count_final=0
# Get top-level folders, sorted numerically
top_dirs = sorted(
    [d for d in os.listdir(incident_root_dir) if os.path.isdir(os.path.join(incident_root_dir, d))],
    key=lambda x: int(x)
)

# Walk through each incident folder in ascending order
for d in top_dirs:
    root_path = os.path.join(incident_root_dir, d)
    print(root_path)
    for root, dirs, files in os.walk(root_path):
        if "FinalEvents.dat" in files:
            filepath = os.path.join(root, "FinalEvents.dat")    
            ids = []
            charges = []
            perweights = []
            posX = []
            posY = []
            posZ = []
            momE = []
            momX = []
            momY = []
            momZ = []
            histories = []
            prod_ids = []
            enus = []

            with open(filepath) as f:
                for line in f:
                    if line.startswith("#") or line.strip() == "":
                        continue
                    entry = parse_line(line)
                    if entry:
                        ids.append(entry["ID"])
                        charges.append(entry["Charge"])
                        perweights.append(entry["perweight"])
                        posX.append(entry["pos"][0])
                        posY.append(entry["pos"][1])
                        posZ.append(entry["pos"][2])
                        momE.append(entry["mom"][0])
                        momX.append(entry["mom"][1])
                        momY.append(entry["mom"][2])
                        momZ.append(entry["mom"][3])
                        histories.append(entry["history"])
                        prod_ids.append(entry["prod_id"])
                        enus.append(entry["enu"])

            # Append per-incident arrays
            incident_numbers.append(incident_counter)
            id_list.append(np.array(ids))
            charge_list.append(np.array(charges))
            perweight_list.append(np.array(perweights))
            posX_list.append(np.array(posX))
            posY_list.append(np.array(posY))
            posZ_list.append(np.array(posZ))
            momE_list.append(np.array(momE))
            momX_list.append(np.array(momX))
            momY_list.append(np.array(momY))
            momZ_list.append(np.array(momZ))
            history_list.append(np.array(histories))
            prod_id_list.append(np.array(prod_ids))
            enu_list.append(np.array(enus))
            count_final +=1
        incident_counter += 1

# Convert everything to awkward arrays
tree = {
    "incident": np.array(incident_numbers),
    "ID": ak.Array(id_list),
    "Charge": ak.Array(charge_list),
    "perweight": ak.Array(perweight_list),
    "posX": ak.Array(posX_list),
    "posY": ak.Array(posY_list),
    "posZ": ak.Array(posZ_list),
    "momE": ak.Array(momE_list),
    "momX": ak.Array(momX_list),
    "momY": ak.Array(momY_list),
    "momZ": ak.Array(momZ_list),
    "history": ak.Array(history_list),
    "prod_id": ak.Array(prod_id_list),
    "enu": ak.Array(enu_list),
}
print(incident_counter,count_final)
# Write ROOT file
with uproot.recreate("jg_FinalEvents2.root") as f:
    f["Events"] = tree
  
