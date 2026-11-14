"""
Actividad: Diseño de filtros digitales pasa bajos, pasa altos y pasa bandas.
Tecnologías: Python, NumPy, SciPy y Matplotlib.

La señal de prueba contiene componentes de 5 Hz, 50 Hz y 120 Hz,
además de ruido blanco. Se diseñan filtros IIR Butterworth y FIR
por ventana Hamming, se aplican y se comparan sus resultados.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ------------------------------------------------------------
# 1. Definición de la señal de entrada
# ------------------------------------------------------------
fs = 500                 # Frecuencia de muestreo en Hz
duracion = 2.0           # Duración de la señal en segundos
t = np.arange(0, duracion, 1 / fs)
rng = np.random.default_rng(42)  # Semilla para reproducir el ruido

# Señal formada por tres frecuencias: 5, 50 y 120 Hz
senal_original = (
    1.0 * np.sin(2 * np.pi * 5 * t)
    + 0.7 * np.sin(2 * np.pi * 50 * t)
    + 0.4 * np.sin(2 * np.pi * 120 * t)
)

ruido = 0.5 * rng.normal(size=len(t))
senal_ruidosa = senal_original + ruido

# ------------------------------------------------------------
# 2. Diseño de filtros IIR Butterworth
# ------------------------------------------------------------
# Pasa bajos: conserva frecuencias menores a 20 Hz
sos_bajos = signal.butter(
    4, 20, btype="lowpass", fs=fs, output="sos"
)

# Pasa altos: conserva frecuencias mayores a 40 Hz
sos_altos = signal.butter(
    4, 40, btype="highpass", fs=fs, output="sos"
)

# Pasa bandas: conserva frecuencias entre 40 y 80 Hz
sos_banda = signal.butter(
    4, [40, 80], btype="bandpass", fs=fs, output="sos"
)

# ------------------------------------------------------------
# 3. Diseño de un filtro FIR por ventana Hamming
# ------------------------------------------------------------
# Ejemplo FIR pasa bajos con frecuencia de corte de 20 Hz
coef_fir = signal.firwin(
    numtaps=101, cutoff=20, fs=fs, window="hamming"
)

# ------------------------------------------------------------
# 4. Aplicación de los filtros
# ------------------------------------------------------------
# sosfiltfilt aplica filtrado hacia adelante y hacia atrás,
# evitando desfase de fase en la señal resultante.
salida_bajos = signal.sosfiltfilt(sos_bajos, senal_ruidosa)
salida_altos = signal.sosfiltfilt(sos_altos, senal_ruidosa)
salida_banda = signal.sosfiltfilt(sos_banda, senal_ruidosa)

# filtfilt aplica el filtro FIR en ambas direcciones.
salida_fir = signal.filtfilt(coef_fir, [1.0], senal_ruidosa)

# ------------------------------------------------------------
# 5. Gráficas de señales antes y después del filtrado
# ------------------------------------------------------------
fig, ejes = plt.subplots(5, 1, figsize=(12, 13), sharex=True)

ejes[0].plot(t, senal_ruidosa, linewidth=0.8)
ejes[0].set_title("Señal original con ruido blanco")
ejes[0].set_ylabel("Amplitud")
ejes[0].grid(True)

ejes[1].plot(t, salida_bajos, linewidth=0.9)
ejes[1].set_title("Filtro IIR Butterworth pasa bajos (20 Hz)")
ejes[1].set_ylabel("Amplitud")
ejes[1].grid(True)

ejes[2].plot(t, salida_altos, linewidth=0.9)
ejes[2].set_title("Filtro IIR Butterworth pasa altos (40 Hz)")
ejes[2].set_ylabel("Amplitud")
ejes[2].grid(True)

ejes[3].plot(t, salida_banda, linewidth=0.9)
ejes[3].set_title("Filtro IIR Butterworth pasa bandas (40–80 Hz)")
ejes[3].set_ylabel("Amplitud")
ejes[3].grid(True)

ejes[4].plot(t, salida_fir, linewidth=0.9)
ejes[4].set_title("Filtro FIR pasa bajos (20 Hz, ventana Hamming)")
ejes[4].set_ylabel("Amplitud")
ejes[4].set_xlabel("Tiempo (segundos)")
ejes[4].grid(True)

plt.tight_layout()
plt.savefig("comparacion_senales.png", dpi=150)
plt.show()

# ------------------------------------------------------------
# 6. Respuesta en frecuencia de los filtros
# ------------------------------------------------------------
f_bajos, h_bajos = signal.sosfreqz(sos_bajos, worN=2048, fs=fs)
f_altos, h_altos = signal.sosfreqz(sos_altos, worN=2048, fs=fs)
f_banda, h_banda = signal.sosfreqz(sos_banda, worN=2048, fs=fs)
f_fir, h_fir = signal.freqz(coef_fir, worN=2048, fs=fs)

plt.figure(figsize=(12, 6))
plt.plot(f_bajos, 20 * np.log10(np.maximum(np.abs(h_bajos), 1e-10)),
         label="IIR pasa bajos")
plt.plot(f_altos, 20 * np.log10(np.maximum(np.abs(h_altos), 1e-10)),
         label="IIR pasa altos")
plt.plot(f_banda, 20 * np.log10(np.maximum(np.abs(h_banda), 1e-10)),
         label="IIR pasa bandas")
plt.plot(f_fir, 20 * np.log10(np.maximum(np.abs(h_fir), 1e-10)),
         label="FIR pasa bajos", linestyle="--")

plt.title("Respuesta en frecuencia de los filtros")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud (dB)")
plt.xlim(0, 150)
plt.ylim(-100, 5)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("respuesta_frecuencia.png", dpi=150)
plt.show()

# ------------------------------------------------------------
# 7. Comparación del espectro antes y después del filtrado
# ------------------------------------------------------------
frecuencias = np.fft.rfftfreq(len(t), d=1 / fs)

def magnitud_espectro(x):
    """Calcula la magnitud normalizada de la transformada FFT."""
    return np.abs(np.fft.rfft(x)) / len(x) * 2

plt.figure(figsize=(12, 6))
plt.plot(frecuencias, magnitud_espectro(senal_ruidosa),
         label="Señal con ruido", alpha=0.7)
plt.plot(frecuencias, magnitud_espectro(salida_bajos),
         label="Pasa bajos")
plt.plot(frecuencias, magnitud_espectro(salida_altos),
         label="Pasa altos")
plt.plot(frecuencias, magnitud_espectro(salida_banda),
         label="Pasa bandas")
plt.title("Comparación espectral de las señales")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.xlim(0, 150)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparacion_espectros.png", dpi=150)
plt.show()

print("Filtrado terminado. Se generaron tres imágenes de resultados.")
