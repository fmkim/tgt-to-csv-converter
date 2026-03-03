# tgt-to-csv-converter
A Python utility to parse TGT XML waveform data and reconstruct frequency axes for RF analysis
A robust python utility designed for RF engineers and data scientists to convert proprietary .tgt XML waveform files into standard analysis ready CSV format.

# The Problem
Many spectrum analyzers and signal generators export trace data in a nested XML format (TGT). These files often omit an explicit frequency value for every data point to save space, instead providing only the start and  stop or center/span. This issue makes it difficult to open the data directly in Excel or Pytho for plotting.

# The Solution
This script automates the data extraction process:
1. XML Parsing: the script goes through the TGT structure to locate waveform amplitudes (y) values.
2. Frequency reconstruction: Automatically detects frequency parameters and uses linear interpolation to calculate the exact frequency for every data point.
3. Professional output: Generates a clean CSV with two columns: Frequency (Hz) and Amplitude (dBm)

# Features
1. Smart tag detection: supports multiple XML tag variations (e.g. StartFrequency, XStart, Start)
2. Fallback Logic: If Start/Stop values are missing, it automatically calculates the range using Center and Span
3. No Dependencies: Built using Python's standard library (xml.etree, pathlib) -no complex installation required.
4. CLI Support: Run it via comand line for easy integration into larger testing pipelines.

# Installation and Usage
if you are using Anaconda, create a dedicated environment
conda create --name tgt_env python=3.10
conda activate tgt_env

# Run the converter
Place your .tgt file in the project folder and run:
python converter.py your_file.tgt

Technical Logic
The frequency (f_i) for each point i is reconstructed using the formula:

f_i = f_start +(f_stop - f_start)*i/(N-1)

Where N is the total number of points in the trace

# License
This project is licensed under the MIT License

