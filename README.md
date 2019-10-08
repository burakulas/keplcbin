
KEPLCBIN.py is a Python script that reads the TIME and PDCSAP FLUX from a series of Kepler .fits files, converts the fluxes to magnitudes, subtract a linear fit from the magnitude data (to eliminate any unphysical effect), clear the datapoints exceeding given dispersion criteria in the phase interval calculated from the input. It extracts a file containing 'phase and binned data points' as output based on user input. It is written for binning the huge light curve data of binary systems to achieve lighter binned data which can be used in speeding up the solution in light curve analysis software (This process generally needed in the elimination of binary effects from the data). However, the script can be used for fits file (containing time and flux data) of any type of targets which desired to be binned according to phase by entering time and period values. 

KEPLCBIN.py works on Python 2.x without any error. It may need a series of modification for running in Python 3.x.



The script needs:

. astropy.io.fits package

. glob module

. numpy library

. os module

. pandas library

. scikit-learn library




Usage:

. Put all Kepler .fits files you want to combine and bin to the same folder with the keplcnorm.py script (Do not change the original name of the fits file).

. Since the script runs under Python 2.x it is recommended to check your default python version by typing python -V

. Run the script by typing: python keplcnorm.py

. Enter the time of minimum light.

. Enter the period.

. Enter the desired number of data points in the output file.

. The script writes the binned points to the file called 'binlc.dat'.




Notes: . Beginning from the second run, the program asks the user for deleting the output files from the previous run. The user should enter y(yes) and confirm the deletion to proceed.

. MAGREGMAG word in the code is the abbreviation for the subtraction of magnitude values from the linear fit.

. The fluxes (F) are converted to magnitude values by using the equation -2.5LOG(F)




An application:

. Download all available fits file of the binary system KIC 7871200 and put all fits file in the same folder with the keplcbin.py. (https://archive.stsci.edu/kepler/data_search/search.php)

. Run the script by typing python keplcbin.py. (Assuming that your default Python version is 2.x)

. Enter 120.677320 as the time of minimum. (http://keplerebs.villanova.edu/overview/?k=7871200)

. Enter 0.2429038 as the period (http://keplerebs.villanova.edu/overview/?k=7871200)

. Enter the desired number of bins in the output file. Say 100.

. Enter the dispersion amount. For 1sigma, enter 1.

. Check the output file binlc.dat. (see Figure 1 in repository, keplcbin.png)


When used the script, you may want to give reference to its GitHub address: https://github.com/burakulas/keplcbin


For comments and further questions: bulash@gmail.com




