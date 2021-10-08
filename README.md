# DataMining
Extracting Time Series Properties of Glucose Levels in Artificial Pancreas
Objectives
● Extract feature data from a data set.
● Synchronize data from two sensors.
● Compute and report overall statistical measures from data.

Directions
Dataset:
You will be given two datasets:
a) from the Continuous Glucose Sensor (CGMData.csv) and
b) from the insulin pump (InsulinData.csv)
The output of the CGM sensor consists of three columns:
a) data time stamp (Columns B and C combined),
b) the 5 minute filtered CGM reading in mg/dL, (Column AE)and
c) the ISIG value which is the raw sensor output every 5 mins.
The output of the pump has the following information:
a) data time stamp,
b) Basal setting,
c) Micro bolus every 5 mins,
d) Meal intake amount in terms of grams of carbohydrate,
e) Meal bolus,
f) correction bolus,
g) correction factor,
h) CGM calibration or insulin reservoir related alarms, and
i) auto mode exit events and unique codes representing reasons (Column Q).
The bold items are the columns that you will be using in this assignment.
Metrics to be extracted:
a) Percentage time in hyperglycemia (CGM > 180 mg/dL),
b) percentage of time in hyperglycemia critical (CGM > 250 mg/dL),
c) percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL),
d) percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL),
e) percentage time in hypoglycemia level 1 (CGM < 70 mg/dL), and
f) percentage time in hypoglycemia level 2 (CGM < 54 mg/dL).
3
Each of the above mentioned metrics are extracted in three different time intervals: daytime (6 am to
midnight), overnight (midnight to 6 am) and whole day (12 am to 12 am).
Percentage is with respect to the total number of CGM data that should be available each day. Assume that the
total number of CGM data that should be available is 288. There will be days such that the number of data
available is less than 288, but still consider the percentage to be with respect to 288.
You have to extract these metrics for each day and then report the mean value of each metric over all days.
Hence there are 18 metrics to be extracted.
The metrics will be computed for two cases:
Case A: Manual mode
Case B: Auto mode

Analysis Procedure:
The data is in reverse order of time. This means that the first row is the end of the data collection whereas the
last row is the beginning of the data collection. The data starts with manual mode. Manual mode continues
until you get a message AUTO MODE ACTIVE PLGM OFF in the column “Q” of the InsulinData.csv. From then
onwards Auto mode starts. You may get multiple AUTO MODE ACTIVE PLGM OFF in column Q but only use the
earliest one to determine when you switch to auto mode. There is no switching back to manual mode. So the
first task is to determine the time stamp when Auto mode starts. Remember that the time stamp of the CGM
data is not the same as the time stamp of the insulin pump data because these are two different devices
which operate asynchronously.
Once you determine the start of Auto Mode from InsulinData.csv, you have to figure out the time stamp in
CGMData.csv where Auto mode starts. This can be done simply by searching for the time stamp that is
nearest to (and later than) the Auto mode start time stamp obtained from InsulinData.csv.
For each user, CGM data is first parsed and divided into segments, where each segment corresponds to a day
worth of data. One day is considered to start at 12 am and end at 11:59 pm. If there is no CGM data loss, then
there should be 288 samples in each segment. The segment as a whole is used to compute the metrics for the
whole day time period. Each segment is then divided into two sub-segments: daytime sub-segment and
overnight subsegment. For each subsegment, the CGM series is investigated to count the number of samples
that belong to the ranges specified in the metrics. To compute the percentage with respect to 24 hours, the
total number of samples in the specified range is divided by 288.
Note that here you have to tackle the “missing data problem”. So a particular may not have all 288 data points.
In the data files those are represented as NaN. You need to devise a strategy to tackle the missing data
problem. Popular strategies include deletion of the entire day of data, or interpolation.
4
Write a Python script that accepts two csv files: CGMData.csv and InsulinData.csv and runs the analysis
procedure and outputs the metrics discussed in the metrics section in another csv file using the format
described in Results.csv.

