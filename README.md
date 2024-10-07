# Seismic Event Detection Using STA/LTA Algorithm (by MaphiaQuantica)

This project aims to detect seismic events in lunar seismic data by applying the Short-Term Average / Long-Term Average (STA/LTA) algorithm and other signal processing techniques. The goal is to predict the start times of seismic events and output the results in a structured format.

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
│   └── run_final_algorithm.ipynb    # Jupyter notebook running the arrival_time_predictor algorithm
│   └──arrival_times_results.csv    # Output file containing detection results
├── signal_processing_algorithms
│   └── final_algorithm.ipynb        # Python code with the arrival_time_predictor implementation
├── README.md                    # This README file
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

   The `run_final_algorithm.ipynb` notebook processes all `.mseed` files within a specified directory (`./data/lunar/training/data/S15_GradeA`) and writes the output to a CSV file (`arrival_times_results.csv`).

### Output

The output CSV file (`arrival_times_results.csv`) will contain the following columns:

- `filename`: The name of the processed `.mseed` file.
- `detection_times_rel(sec)`: A list of predicted detection times relative to the start of the file (in seconds).
- `detection_times(%Y-%m-%dT%H:%M:%S.%f)`: A list of predicted detection times in human-readable format.

Example output:

```
filename,detection_times_rel(sec),detection_times(%Y-%m-%dT%H:%M:%S.%f)
xa.s12.00.mhz.1970-01-19HR00_evid00002,73450.41509433962,1970-01-19T20:24:11.080094
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
