# %%
import mne
import matplotlib.pyplot as plt
import numpy as np

# --- HARDWARE CONFIGURATION ---
# Device: waveguard™ original (CA-505) | 24 Channels
# Amplifier: eego™ mylab (EE-511) | SN: 200593
# Hardware Ref: Cz | GND: AFz
path = 'YOUR_PATH_TO_GEL_DATA.cnt'
hardware_ref = "Cz"

def analyze_gel():
    raw = mne.io.read_raw_ant(path, preload=True, verbose=False)
    raw.resample(250)

    def clean_ch_names(name):
        name = str(name).split('-')[0].upper().replace(' ', '')
        if name.startswith('FP'): return name.replace('FP', 'Fp')
        if name.endswith('Z'): return name[:-1] + 'z'
        return name.capitalize()

    raw.rename_channels({ch: clean_ch_names(ch) for ch in raw.ch_names})
    montage = mne.channels.make_standard_montage('standard_1020')
    eeg_channels = [ch for ch in raw.ch_names if ch in montage.ch_names]
    raw.pick_channels(eeg_channels)
    raw.set_montage(montage)

    raw.filter(2.0, 30.0, fir_design='firwin', verbose=False)
    raw.notch_filter(50, verbose=False)

    psd = raw.compute_psd(method='welch', fmin=1, fmax=30, n_fft=250)
    psd_data = 10 * np.log10(psd.get_data())

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.2)

    # Panel A: Global Spectrum
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(psd.freqs, psd_data.T, color='gray', alpha=0.2)
    ax1.plot(psd.freqs, psd_data.mean(axis=0), color='#2c3e50', linewidth=2.5)
    ax1.set_title(f"A. Global Power Spectrum (Ref: {hardware_ref})", fontweight='bold')
    ax1.set_xlabel("Frequency (Hz)"), ax1.set_ylabel("Power (dB)")

    # Panel B: Heatmap
    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(psd_data, aspect='auto', extent=[psd.freqs[0], psd.freqs[-1], 0, psd_data.shape[0]], cmap='viridis')
    ax2.set_title("B. Electrode Performance Heatmap", fontweight='bold')
    plt.colorbar(im2, ax=ax2, label='Power (dB)')

    # Panel C: Topomap
    ax3 = fig.add_subplot(gs[1, 0])
    noise_data = psd.get_data(fmin=25, fmax=30).mean(axis=1)
    im3, _ = mne.viz.plot_topomap(noise_data, raw.info, axes=ax3, cmap='Oranges', show=False)
    ax3.set_title("C. Noise Floor Distribution (25-30 Hz)", fontweight='bold')
    plt.colorbar(im3, ax=ax3, shrink=0.8, label='Mean Power (µV²/Hz)')

    # Panel D: SNR
    ax4 = fig.add_subplot(gs[1, 1])
    alpha_pow = psd.get_data(fmin=8, fmax=13).mean(axis=1)
    noise_pow = psd.get_data(fmin=25, fmax=30).mean(axis=1)
    snr_per_ch = 10 * np.log10(alpha_pow / noise_pow)
    ax4.bar(range(len(snr_per_ch)), snr_per_ch, color='#2c3e50')
    ax4.set_xticks(range(len(snr_per_ch)))
    ax4.set_xticklabels(raw.ch_names, rotation=90, fontsize=8)
    ax4.set_title("D. SNR per Electrode", fontweight='bold')

    plt.suptitle("GEL-BASED QUALITY REPORT: waveguard™ original (CA-505)", fontsize=20, fontweight='bold')
    plt.show()

analyze_gel()
