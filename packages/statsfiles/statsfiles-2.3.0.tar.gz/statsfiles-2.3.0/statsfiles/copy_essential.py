import shutil
import os
import glob


class CopyEssential:
    def __init__(self, out_dir):
        """ """
        self.out_dir = out_dir
        self.obs_files = [
            "n.dat",
            "n0Up.dat",
            "n0Down.dat",
            "ChiSz.dat",
            "amagn.dat",
            "docc.dat",
            "sign.dat",
            "k.dat",
            "nSites.dat",
            "energy.dat",
            "KEnergy.dat",
            "NMeas.dat",
            "NWorkers.dat",
            "Sz.dat",
            "outPutConvention.dat",
            "Obs.json",
        ]
        self.array_files = ["green", "self", "hyb"]
        self.middles = ["", "Up", "Down"]
        self.exts = [".dat", ".dat", ".dat"]
        self.json_files = ["Hyb", "Self", "params"]

        try:
            self.iter_max = self.get_iter_max()
        except FileNotFoundError:
            # print("Not doing copy essential...")
            self.iter_max = -100

        self.divers_files = [
            "Updates.json",
            "Link.json",
            "script",
            "params" + str(self.iter_max),
            "params" + str(self.iter_max) + ".json",
        ]

    def get_iter_max(self):
        """ """
        with open(self.obs_files[0]) as fin:
            iter_max = len(fin.readlines()) - 1
        return iter_max

    def copy_obs_files(self):
        """ """

        for obs_file in self.obs_files:
            if os.path.isfile(obs_file):
                shutil.copy(obs_file, os.path.join(self.out_dir, obs_file))

        model_files = list(glob.glob("*.model"))
        if len(model_files) == 1:
            model_file = model_files[0]
            shutil.copy(model_file, os.path.join(self.out_dir, model_file))
        elif len(model_files) == 0:
            pass
        else:
            raise ValueError("To many model files")

    def copy_json(self):
        """ """
        for json_file in self.json_files:
            file_name = json_file + str(self.iter_max) + ".json"
            if os.path.isfile(file_name):
                shutil.copy(file_name, os.path.join(self.out_dir, file_name))

    def copy_arrays(self):
        """ """
        for (ii, array_file) in enumerate(self.array_files):
            for middle in self.middles:
                file_name = array_file + middle + str(self.iter_max) + self.exts[ii]
                if os.path.isfile(file_name):
                    shutil.copy(file_name, os.path.join(self.out_dir, file_name))

    def copy_divers(self):
        """ """

        for divers_file in self.divers_files:
            if os.path.isfile(divers_file):
                shutil.copy(divers_file, os.path.join(self.out_dir, divers_file))

    def run(self):
        """ """
        self.copy_obs_files()
        self.copy_json()
        self.copy_arrays()
        self.copy_divers()
