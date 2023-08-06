# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: charles-david
"""


import numpy as np
# import configparser
import os
import sys
import unittest
# import copy



from .. import statsobs

# You CAN (not necessary) comment the last two lines and uncomment the next two when testing
# but the first import seems to work better when adding auto-completion features in IDE


# import stats_files
# from stats_files.statsobs import statsobs3 as statsobs
# with these lines last two lines you can run "python -m unittest discover"
# or "python -m unittest tests/test_..." from the source directory

class TestStatsObs(unittest.TestCase):
    """ """

    input_dir = "statsfiles/tests/testinfiles"
    
    def test_init(self):
        """ """
        # out_dir =   "TestOutFiles"
        obs_files = ["test1.txt", "test2.txt", "test3.dat"]
        obs = statsobs.StatsObs(obs_files=obs_files, ignore_col=0, in_dir=self.input_dir)  

        # Test that the given values are ok
        self.assertEqual(obs.in_dir, os.path.abspath(self.input_dir))
        self.assertEqual(obs.ignore_col, 0)
        self.assertEqual(obs.obs_files, obs_files)


    def test_check_sanity(self):
        """Check if the constructing attributes are sain"""

        # out_dir =   "TestOutFiles"
        obs_files = ["test1.txt", "test2.txt", "test3.dat"]
        bad_files = ["lalalla", "peete"]
        obs = statsobs.StatsObs(obs_files=obs_files, ignore_col=0, in_dir=self.input_dir, warning_only=False)  
        # test that an statsobs object with bad file names exits ok with asserts
        self.assertRaises(AssertionError, obs.check_sanity, bad_files)
        
        #Check that an statsObs exits ok if warning_only= True and some files are none existent
        #and check that obs.obs_files is only given by the good files
        del obs
        files = ["test1.txt", "test2.txt", "test3.dat", "lalalla", "peete"]
        obs = statsobs.StatsObs(obs_files=files, ignore_col=0, in_dir=self.input_dir, warning_only=True)         
        self.assertEqual(obs.obs_files, obs_files)
        del obs
        obs = statsobs.StatsObs(obs_files=obs_files, iter_start=2, ignore_col=0, in_dir=self.input_dir,
                 warning_only=True)

        cut_data = [np.array([[1.2, 0.111], [6.3, 0.999999], [0.99, 1.2]]),
                    np.array([[12.2, 0.111], [63.3, 0.999999], [0.99, 1.2]]),
                    np.array([[12.2, 0.0], [63.3, 0.0], [0.0, 0.0]])]
        #print(obs.datas)            
        try:
            np.testing.assert_allclose(obs.datas, cut_data)
        except AssertionError:
            self.fail("np.testing.assert_allclose failed")            
        

    def test_read_files(self):
        """reads the files and their contents in numpy arrays (list of numpy arrays)"""

        # out_dir =   "TestOutFiles"
        obs_files = ["test1.txt", "test2.txt", "test3.dat"]
        obs = statsobs.StatsObs(obs_files=obs_files, ignore_col=None, in_dir=self.input_dir)  

        obs.read_files()
        good_data = [np.loadtxt(os.path.join(self.input_dir, file)) for file in obs_files]
        bad_data = np.multiply(0.5, good_data)

        # print("\n\n\n\n\n good data \n", good_data, "\n\n\n")
        # print()
        # print("bad_data", bad_data, "\n\n\n\n")
        # print("type of bad_data ", type(bad_data))

        for i in range(len(obs.datas)):
            bool_array = np.array(obs.datas[i] == good_data[i])
            self.assertEqual(bool_array.all(), True)

        # This try block is identical in checking as the preceding for
        try:
            np.testing.assert_array_equal(obs.datas, good_data, err_msg='', verbose=True)
        except AssertionError:
            self.fail("np.testing.assert_array_equal failed")

        self.assertRaises(AssertionError, np.testing.assert_array_equal, obs.datas, bad_data, err_msg='', verbose=True)



    #@unittest.skip("")
    def test_mean(self):
        """ """
        # out_dir =   "TestOutFiles"
        obs_files = ["test1.txt", "test2.txt", "test3.dat"]
        obs = statsobs.StatsObs(obs_files=obs_files, ignore_col=0, in_dir=self.input_dir) 
        obs.mean()

        # print(obs.datas)
        # print(obs.means)
        # print(type(obs.means))
        good_means = np.array([
                      [2.358, 0.5221998],
                      [20.758, 0.5221998],
                      [20.56, 0.0]
                      ])
                      
        bad_means = np.array([
                      [200.1358, 1.5221998],
                      [220.8, 2.5221998],
                      [10.56, 3.0]
                      ])

        np.testing.assert_allclose(obs.means, good_means)
        self.assertEqual(False, np.allclose(a=obs.means, b=bad_means))

        # Another way of testing the same thing
        for (i, j) in zip (obs.means.flatten(), good_means.flatten()):
            self.assertAlmostEqual(i, j)

        for (i, j) in zip (obs.means.flatten(), bad_means.flatten()):
            self.assertNotEqual(i, j)

        #now I test for big files: 
        # out_dir =   "TestOutFiles"
        obs_files = ["energy.dat", "ChiSz.dat", "docc.dat"]
        obs = statsobs.StatsObs(obs_files=obs_files, iter_start=100, ignore_col=0,
                                in_dir=os.path.join(self.input_dir, "b60"), warning_only=True )    
        obs.mean()
        good_means = np.array([
                      [-13.8817351724, 0.0104441619],
                      [0.1153189276, 0.004808949],
                      [0.0276861303, 0.0002756482]
                      ])
                      
        for (i, j) in zip (obs.means.flatten(), good_means.flatten()):
            self.assertAlmostEqual(i, j)              

    #@unittest.skip("")
    def test_std(self):
        """Compute the std errors"""
        
        # out_dir =   "TestOutFiles"
        obs_files = ["test1.txt", "test2.txt", "test3.dat"]
        obs = statsobs.StatsObs(obs_files=obs_files, ignore_col=None, in_dir=self.input_dir) 
        obs.std()
        
        # print("stds = ", obs.stds)
        good_stds = np.array([
            [1.8547236991, 2.0178840403, 0.4772537783],
            [1.8547236991, 22.985592357, 0.4772537783],
            [1.8547236991, 23.1586355384, 0.0]
            ])
        
        bad_stds = np.array([
                             [12.20736441353, 2.25960629424, 10.5335859454],
                             [288.30736441353, 25.26986735066, 80.5335859454],
                             [22.0736441353, 25.4892141665, 10]
                             ])
        
        np.testing.assert_allclose(obs.stds, good_stds)
        self.assertEqual(False, np.allclose(a=obs.stds, b=bad_stds))

        # Another way of testing the same thing
        for (i, j) in zip (obs.stds.flatten(), good_stds.flatten()):
            self.assertAlmostEqual(i, j)

        for (i, j) in zip (obs.stds.flatten(), bad_stds.flatten()):
            self.assertNotEqual(i, j)

    #@unittest.skip("")
    def test_write_results(self, file_out="results_statsobs.txt"):
        """ """
        pass


if __name__ == "__main__":
    unittest.main() 
               