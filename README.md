# Comparative Analysis of EEG Electrode Systems

This repository contains the analysis scripts used to validate and compare the performance of **Gel**, **Sponge**, and **Dry** electrode systems. 

## 🛠 Hardware Used
* **Gel System:** waveguard™ original (CA-505) with eego™ mylab (EE-511).
* **Sponge System:** EEG net 21ch (CW-06035) with eego™ mini (EE-701).
* **Dry System:** EEG dry flower net 22ch (CW-06879) with eego™ mini (EE-701).

## 🧪 Recording Protocol
* **Conditions:** 3 minutes Eyes Open (EO) vs 3 minutes Eyes Closed (EC).
* **Selection:** First and last 10 seconds of each condition are clipped to ensure stability.
* **Sampling Rate:** All data standardized to 250 Hz for unbiased comparison.

## 📊 Pre-processing Pipeline
* Standard 10-20 channel renaming.
* Band-pass filter (2.0 - 30.0 Hz) and Notch filter (50 Hz).
* Power Spectral Density (PSD) calculation using Welch's method.
* Alpha Ratio (EC/EO) calculation from O1, O2, Oz, and Pz.

  ## References
- ANT Neuro eego™ mylab (EE-511) User Manual.
- waveguard™ original (CA-505) Datasheet.
- waveguard™ net (CW-06035) Technical Specifications.
