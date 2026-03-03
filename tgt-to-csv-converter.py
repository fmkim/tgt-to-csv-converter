import xml.etree.ElementTree as ET
import csv
import os

def parse_tgt_to_csv(input_file):
    try:
        # 1. Parse the XML
        tree = ET.parse(input_file)
        root = tree.getroot()

        # 2. Find Waveform data (looking for 'trace1' or general Waveform)
        # The script uses a simplified XPath-like search
        waveform = None
        for wf in root.iter('Waveform'):
            if wf.get('pid') == 'trace1':
                waveform = wf
                break
        
        if waveform is None:
            waveform = root.find('.//Waveform') or root.find(".//*[@pid='trace1']")

        if waveform is None:
            print(f"Error: Could not find waveform data in {input_file}")
            return

        # Extract Y values (Amplitude)
        y_values = [float(y.text) for y in waveform.findall('y')]
        num_points = len(y_values)

        if num_points == 0:
            print("Error: No data points found.")
            return

        # 3. Helper to find Frequency Tags
        def get_tag_number(tags):
            for tag in tags:
                element = root.find(f".//{tag}")
                if element is not None:
                    try:
                        return float(element.text)
                    except ValueError:
                        continue
            return None

        # 4. Auto Frequency Detection
        start_freq = get_tag_number(["StartFrequency", "StartFreq", "XStart", "Start"])
        stop_freq = get_tag_number(["StopFrequency", "StopFreq", "XStop", "Stop"])

        # Fallback to Center/Span
        if start_freq is None or stop_freq is None:
            center = get_tag_number(["CenterFrequency", "CenterFreq", "XCenter"])
            span = get_tag_number(["Span", "FrequencySpan", "XSpan"])
            if center is not None and span is not None:
                start_freq = center - (span / 2)
                stop_freq = center + (span / 2)

        if start_freq is None or stop_freq is None:
            print("Error: Could not detect frequency range.")
            return

        # 5. Generate CSV Data
        output_file = input_file.lower().replace('.tgt', '.csv')
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Frequency (Hz)", "Amplitude (dBm)"])
            
            for i in range(num_points):
                # Linear interpolation for frequency
                freq = start_freq + (stop_freq - start_freq) * (i / (num_points - 1))
                writer.writerow([f"{freq:.3f}", y_values[i]])

        print(f"Success! Saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
file_path = "your_file.tgt" # Replace with your filename
if os.path.exists(file_path):
    parse_tgt_to_csv(file_path)
else:
    print("File not found.")