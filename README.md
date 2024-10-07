# Seismic Event Detection Using STA/LTA Algorithm (by MaphiaQuantica)

This project aims to detect seismic events in lunar seismic data by applying the Short-Term Average / Long-Term Average (STA/LTA) algorithm and other signal processing techniques. The goal is to predict the start times of seismic events and output the results in a structured format.

https://www.spaceappschallenge.org/nasa-space-apps-2024/find-a-team/maphiaquantica/

## Project Overview

Planetary seismology is fundamentally constrained by the limited availability of data, primarily due to difficulties in transmitting high-resolution seismic signals back to Earth. This project seeks to overcome these challenges by performing on-site analysis using pre-existing datasets from lunar missions. The solution aims to differentiate seismic events from noise and determine the arrival times of these events.

The project uses the following:
- **STA/LTA Triggering**: A classic seismic signal detection approach based on comparing short-term and long-term energy averages.
- **Bandpass Filtering**: To remove noise and focus on frequencies associated with seismic events.
- **Simpson's Rule Integration**: Used to assess the area under the seismic curve, helping to filter out false positives.

## Directory Structure

```
project-directory/
│
├── data/
│   └── lunar/
│       └── training/
│           └── data/
│               └── S15_GradeA/
│                   └── *.mseed  # Input seismic data files
│
├── notebooks/
│   └── run_final_algorithm.ipynb                     # Jupyter notebook running the arrival_time_predictor algorithm
│   └── lunar_test_data_S15_GradeA_predictions.csv    # Output file containing detection results
├── signal_processing_algorithms
│   └── final_algorithm_mofidfied.ipynb               # Python code with the arrival_time_predictor implementation
├── README.md                                         # This README file
```

## How to Use

### Running the Seismic Event Detection

1. **Arrival Time Predictor**

   The `arrival_time_predictor.py` script contains the main logic for detecting seismic events in a given `.mseed` file. The function `arrival_time_predictor()` reads a Mini-SEED file, filters the data, applies the STA/LTA algorithm, and returns the predicted arrival times of seismic events.

   Example usage:

   ```python
   from arrival_time_predictor import arrival_time_predictor

   result = arrival_time_predictor('./data/lunar/training/data/S15_GradeA/example.mseed')
   print(result)
   ```

2. **Batch Processing All Files**

   The `run_final_algorithm.ipynb` notebook processes all `.mseed` files within a specified directory (`./data/lunar/training/data/S15_GradeA`) and writes the output to a CSV file (`lunar_test_data_S15_GradeA_predictions.csv`).

### Output

The output CSV file (`lunar_test_data_S15_GradeA_predictions.csv`) will contain the following columns:

- `filename`: The name of the processed `.mseed` file.
- `time_rel(sec)`: A list of predicted detection times relative to the start of the file (in seconds).
- `time_abs(%Y-%m-%dT%H:%M:%S.%f)`: A list of predicted detection times in human-readable format.

Example output:

```
filename,time_abs(%Y-%m-%dT%H:%M:%S.%f),time_rel(sec)
xa.s15.00.mhz.1973-10-27HR00_evid00134,1973-10-27T11:14:09.006830,40448.45283018868
xa.s15.00.mhz.1975-06-22HR00_evid00194,1975-06-22T19:55:02.717566,71702.49056603774
xa.s15.00.mhz.1974-11-17HR00_evid00162,1974-11-17T19:54:58.833981,71698.71698113208
...
```

## Parameters

The following parameters are used in the STA/LTA algorithm and can be tuned in `arrival_time_predictor.py`:

- **Bandpass Filter Frequency Range**:
  - `minfreq = 0.5` Hz
  - `maxfreq = 1.5` Hz

- **STA/LTA Window Lengths**:
  - `sta_len = 100` seconds
  - `lta_len = 2700` seconds

- **Trigger Thresholds**:
  - `thr_on = 2.7`
  - `thr_off = 1.5`

- **Duration Threshold**:
  - `duration_threshold_secs = 3` seconds to avoid false positives.

## Results

- **Filtered Detection Times**: Arrival times are filtered based on the duration threshold and area under the curve.
- **Output Format**: A CSV file with arrival times that are more likely to indicate true seismic events.
