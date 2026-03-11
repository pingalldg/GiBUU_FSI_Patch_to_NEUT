### GiBUU_FSI_Patch_to_NEUT
 step 1:  run download package release using 'download_package.sh'
 
 step 2:  follow https://gibuu.hepforge.org/trac/wiki/compiling for compilation
 
 step 3 : follow https://gibuu.hepforge.org/trac/wiki/running for running the code
 
 step 4:  replace the code/init/initNeutrino.f90 with the version available in this repo : gibuu_fsi/.....
           (purpose is to modify initNeutrino.90 so that it can read and initialize NEUT hard scattering events)
           
 step 5 : recompile everything with modified code, the new executable will be located inside the directory named 'testRun'
 
 step 5:  go to work dir and find some shell and python scripts.
       
                 A. generate_inputfile.py: it creates a input file corresponding to 'n'th NEUT hard scattering event. The
                  purpose is to create kinematic info in GiBUU format so that it can be read inside initNeutrino.f90 easily.

                  Usage: python3 generate_inputfile.py 'n' ##(it also reads the NEUT event roort file , I attach here an example, jg_test_NIWG_dnn.root)
                 B. jobcopy.py : It actually creates a job card file specifically for the n-th event, so you’ll find an external path pointing to the specific location of  'input_file{n}.f90' , which is created by running  'generate_inputfile.py' .
                 Usage: python3 jobcopy.py 
                 
                 C. combine_sorted.py : It combines all outputs from all the 'FinalEvents.dat' files created in folder named 1 2 3 ......n 
                 to create a final output root files.

                 Usage: python3 combine_sorted.py


                 D. see specific *.sh files useful for submitting batch jobs:

                 example:
                    
                    bsub < mkdir_batch.sh
                    python3 jobcopy.py
                    ./run2.sh
                    (for cleaning unneccessary info ./clean_output.sh or ./clear.sh)
                    python3 combine_sorted.py

                    
step 6: After creating 'jg_FinalEvents.root' you can use the *.ipynb to do basic analysis. 
                    
