import os
import json
import uproot


def make_json(process, name):
    rootdirec = "root://eosuser.cern.ch/"
    directory = "/eos/user/p/pllerena/4topsoutput/ntuples/"
    path_directory = os.path.join(directory, process)
    
    files = [f for f in os.listdir(path_directory) if os.path.isfile(os.path.join(path_directory, f))]
    
    if name == "data":
        data = {
            "data": {
                "SingleMuon": {
                    "files": [{"path": rootdirec + os.path.join(path_directory, f)} for f in files]
                }
            }
        }
        return data
    else:
        data = {
            name: {
                "nominal": {
                    "nevts_total": 0,
                    "files": []
                }
            }
        }
        data = get_nevents(data, name, path_directory, files)
        return data

def get_nevents(data, name, directory, files):
    nevts_total = 0

    rootdirec="root://eosuser.cern.ch/"
    for f in files:
        root_file_path = os.path.join(directory, f)
        archivo_root = uproot.open(root_file_path)
        num_eventos = archivo_root["Events"].num_entries
        data[name]["nominal"]["files"].append({
            "path": rootdirec+root_file_path,
            "nevts": num_eventos
        })
        nevts_total += num_eventos

    data[name]["nominal"]["nevts_total"] = nevts_total

    return data

if __name__ == "__main__":
    data = {}
    PROCESS = [
        ["Run2015D_SingleMuon", "data"],
        ["_TT_", "ttbar"],
        ["TTTT", "tttt"],
        ["WJets", "wjets"],
        ["DYJets", "dyjets"]
    ]
    
    for p in PROCESS:
        process = p[0]
        name = p[1]
        data.update(make_json(process, name))
    
    output_path = "/eos/user/p/pllerena/4topsoutput/ntuples/ntuples.json"

    with open(output_path, 'w') as file:
        json.dump(data, file, indent=2)
