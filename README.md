# Diseño de filtros digitales con Python

## Descripción
Este proyecto implementa filtros digitales pasa bajos, pasa altos y pasa bandas.
Se genera una señal compuesta por tonos de 5, 50 y 120 Hz, contaminada con ruido
blanco. Después se aplican filtros IIR Butterworth y un filtro FIR diseñado
con ventana Hamming.

## Requisitos
- Python 3.9 o superior
- NumPy
- SciPy
- Matplotlib

Instalación:

```bash
pip install numpy scipy matplotlib
```

## Ejecución

```bash
python filtros_digitales.py
```

El programa muestra y guarda:
- `comparacion_senales.png`
- `respuesta_frecuencia.png`
- `comparacion_espectros.png`

## Configuración de los filtros
- IIR pasa bajos: Butterworth de orden 4, corte de 20 Hz.
- IIR pasa altos: Butterworth de orden 4, corte de 40 Hz.
- IIR pasa bandas: Butterworth de orden 4, banda de 40 a 80 Hz.
- FIR pasa bajos: 101 coeficientes, corte de 20 Hz, ventana Hamming.

## Estructura
- `filtros_digitales.py`: código principal de simulación.
- `README.md`: descripción, requisitos e instrucciones.
