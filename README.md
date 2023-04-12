# sidex_seismo
Example code for use with SIDEx'21 seismo-acoustic data. This work was funded by the US Office of Naval Research.

Raw data can be located at: 
https://drive.google.com/drive/folders/11bwEb643vWLq-D29wE91sKItUvqpyJfL?usp=sharing

How to use this code:
1) Pull the git repo 
2) Download metadata and selected .csv.zip files, put them somewhere. Unzip .csv.zip files.
3) Edit sidex_seismoacoustic_plot_bydate.py to point to the directories containing meta data and raw csvs. Select a datestruse string to pull all files with that pattern. Modify to point to your desired output directory.
4) Run sidex_seismoacoustic_plot_bydate.py; this will plot each 10 minute raw csv file including time series and spectrogram plots for the hydrophones and geophones. 

Data Use Notes: Data is public and available for use with attribution. 

____________________________________________________________________
Code organization:

* src/ contains python scripts

* "*_utils.py" files have utilities

* Future versions will include event detection and localization code
____________________________________________________________________

Information for SIDEx seismo-acoustic cabled array data set

Contact: Erin Fischell, PhD; JPAnalytics, LLC; efischell@gamil.com
Date: April 2023
Other authors: Kevin Manganini (WHOI), Caileigh Fitzgerald (WHOI), Henrik Schmidt (MIT), Rui Chen (APL Johns Hopkins)

______________________________________________________________________
Data Summary
This data set includes raw geophone and hydrophone data from the ONR Sea Ice Dynamics Experiment (SIDEx). The SIDEx seismo-acoustic cabled array data set consists of near-continuous 1000 Hz data from an ice-mounted array in the Beaufort Sea from 3/5/21 - 4/7/21 from the following sensing:
* 4 x 3-axis 10 Hz geophones
* 15 HTI-96-MIN hydrophones at depths of 1 m to 13.5 m below the ice as a part of 5 sub-arrays (18 hydrophones were deployed, but 3 channels were corrupted thus not included in this data set).

The locations of the hydrophones and geophones in relative coordinates, GPS coordinate .csv, and example python code for working with this data set are provided.

_______________________________________________________________________
Data files:
* One CSV is provided for geophone and hydrophone data per 10 minute interval, encompassing all data e.g. 00:00:00 - 00:09:59, 00:10:00 - 00:19:59 based on UTC time from GPS
* 3/5/21-4/7/21
* Most csvs will have approximately 60000 rows [1000 samples/s * 60 s/min * 10 min/file]; 
* Time stamps are PPS corrected to the hundreth second median offset within the 10 minute window; this may lead to time shifts in the tenths of seconds between 10 minute files
* Some csvs will have less data, if than 10 minutes has less data recorded.
* A few files were corrupted, leading to 5 or so short (1 minute) gaps in the data between 3/5-4/5; 4/5-4/7 the incidence of file corruption is higher due to low battery power levels.   
* Longer data gaps exist in several intervals:
	1) 3/12 00:02 - 3/13 20:29 (power setting issue)
	2) 3/19 17:33-3/20 12:04 (disk flub with data offload, Auto-reset at noon fixed the issue)
	3) 3/23 20:33-3/24 12:56 (disk flub with data offload, auto-reset at noon fixed the issue)

_______________________________________________________________________
GPS

A Garmin GPS provided timing and location to the system. PPS was recorded along with hydrophone and geophone data to provide timing correction to within 1/100 of a second or so. The GPS quality degraded over the experiment for unknown reasons but may be used as an approximate absolute reference. 
_______________________________________________________________________
Data Quality

Data was recorded on a United Electronics Incorperated PowerPC Data Acquisition and Control I/O Cube with 2 x DNA-AI-217 data aquisition boards.

Precision: 24 bits
Gain: 1 V P2P
Hydrophone calibration: HTI-96-MIN with preamp, -167 dB/uPa
Geophone calibration:  
_______________________________________________________________________
Coordinate System Notes

Array-on-ice coordinate system: The array was deployed oriented 20 degrees East of North of 3/5/21; all array coordinates in SIDEx_geophones.csv and SIDEx_hydrophones.csv are in a easting/northing coordinate system as surveyed on 3/16/21. Geophones were oriented 20  degrees E of N on 3/5/21, with the "L" geophone pointed 20 degrees E of N and the "T" geophone pointed 20 degrees N of W.

The center of the array-on-ice coordinate system is the control box for the array data recording system, and included a GPS. This GPS provided a standard time base and latitude/longitude for the coordinate system.

To translate from array-on-ice-centric coordinates to global coordinates, apply a transformation matrix to rotate 20 degrees to the East then translate using the GPS coordinates for the appropriate time in SIDEx_seismoacoustic_GPS.py

______________________________________________________________________
Timing notes

The original data set was saved based on the board time of the data aquisition system, with seperately noted GPS time and a dedicated channel to provide a pulse per second (PPS) signal. The timestamps provided in the .csv files are the PPS-corrected GPS time. This means that the times associated with each measurements should have ms accuracy; a column "time_since_GPS" is provided in each hydrophone and geophone .csv data file to provide a user with information on the last GPS fix. If "time_since_GPS" is a long internal, there may be drift in the system as the differential is based on the internal clock. 


 
