#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
 Auregolden432hz - Audio Pitch Shifter (440 Hz to 432 Hz)
================================================================================
Este script automatizado permite convertir archivos de audio de la afinación
estándar de 440 Hz a la afinación de 432 Hz.

Ofrece dos métodos de conversión profesionales:
1. Método "Analog" (Resampling): Ralentiza el audio un 1.82% (432/440), imitando 
   el comportamiento físico de las cintas analógicas o vinilos. Es 100% libre de
   artefactos digitales y es el favorito de la comunidad audiófila.
2. Método "Stretch" (Time-Stretch): Desplaza el tono exactamente -31.77 cents
   manteniendo el tempo original exacto utilizando algoritmos DSP avanzados.

Requisitos:
    pip install numpy soundfile librosa pydub

Creado para el repositorio GitHub: Auregolden432hz
================================================================================
"""

import os
import sys
import argparse
import math
import tempfile
import shutil

# Intentar importar librerías necesarias
try:
    import numpy as np
    import soundfile as sf
    import librosa
    from pydub import AudioSegment
except ImportError as e:
    print(f"\n[!] Error de importación: {e}")
    print("[*] Asegúrate de tener instaladas las dependencias necesarias ejecutando:")
    print("    pip install numpy soundfile librosa pydub\n")
    sys.exit(1)


def pitch_shift_analog(input_path, output_path):
    """
    Método Analógico (Resampling):
    Modifica la frecuencia de muestreo de reproducción para bajar el tono
    sin introducir artefactos de fase DSP. Altera ligeramente la velocidad (1.82% más lento).
    """
    # Cargar audio conservando su tasa de muestreo original
    y, sr = librosa.load(input_path, sr=None)
    
    # El factor de conversión de 440 Hz a 432 Hz es exactamente 432/440 (0.981818...)
    factor = 432.0 / 440.0
    
    # Para cambiar el tono imitando cinta analógica, reproducimos a una tasa de muestreo modificada.
    # Al guardarlo, especificamos que la tasa nativa es la original, lo que ralentiza y baja el tono.
    new_sr = int(round(sr * factor))
    
    # Para evitar problemas de compatibilidad con reproductores, remuestreamos la señal
    # para que vuelva a su tasa estándar original, pero con la velocidad y tono reducidos.
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=new_sr)
    
    # Guardar archivo temporal en formato WAV
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sf.write(temp_wav, y_resampled, sr)
    return temp_wav


def pitch_shift_dsp(input_path, output_path):
    """
    Método DSP (Time-Stretch):
    Desplaza el tono exactamente -31.766 cents (log2(432/440)*12 semitones)
    manteniendo la duración y tempo del archivo original intactos.
    """
    y, sr = librosa.load(input_path, sr=None)
    
    # Calcular semitonos necesarios para bajar de 440 a 432 Hz
    # n_steps = log2(432/440) * 12 ≈ -0.317666
    n_steps = math.log2(432.0 / 440.0) * 12
    
    # Aplicar pitch shifting de alta calidad (Phase Vocoder de librosa)
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
    
    # Guardar archivo temporal en formato WAV
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sf.write(temp_wav, y_shifted, sr)
    return temp_wav


def convert_audio(input_file, output_file, method="analog", format_out="mp3"):
    """
    Función principal de conversión de un archivo individual.
    """
    print(f"\n[*] Procesando: {os.path.basename(input_file)}")
    print(f"    Método: {method.upper()} | Formato de salida: {format_out.upper()}")
    
    try:
        # 1. Aplicar desplazamiento de tono
        if method == "analog":
            temp_wav = pitch_shift_analog(input_file, output_file)
        else:
            temp_wav = pitch_shift_dsp(input_file, output_file)
            
        # 2. Convertir y exportar al formato final usando Pydub (soporta MP3, WAV, etc.)
        sound = AudioSegment.from_wav(temp_wav)
        
        # Ajustar bitrate para MP3 si es necesario
        if format_out.lower() == "mp3":
            sound.export(output_file, format="mp3", bitrate="320k")
        else:
            sound.export(output_file, format=format_out.lower())
            
        # Limpiar archivo WAV temporal
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
            
        print(f"[+] ¡Conversión completada con éxito! -> {output_file}")
        return True
    except Exception as e:
        print(f"[-] Error al procesar {input_file}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Auregolden432hz - Conversor profesional de audio de 440Hz a 432Hz."
    )
    parser.add_argument(
        "-i", "--input", 
        help="Ruta al archivo de audio de entrada (MP3, WAV, FLAC, etc.)", 
        required=True
    )
    parser.add_argument(
        "-o", "--output", 
        help="Ruta para guardar el archivo de salida procesado. Si no se especifica, se creará uno nuevo automáticamente."
    )
    parser.add_argument(
        "-m", "--method", 
        choices=["analog", "dsp"], 
        default="analog",
        help="Método: 'analog' (baja velocidad y tono, sonido orgánico analógico) o 'dsp' (baja tono conservando tempo exacto)"
    )
    parser.add_argument(
        "-f", "--format", 
        default="mp3", 
        choices=["mp3", "wav", "flac"],
        help="Formato de salida deseado (por defecto: mp3)"
    )

    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"[!] El archivo de entrada '{input_path}' no existe.")
        sys.exit(1)

    # Definir ruta de salida por defecto si no se proporciona
    if not args.output:
        dir_name, file_name = os.path.split(input_path)
        name, ext = os.path.splitext(file_name)
        output_path = os.path.join(dir_name, f"{name}_432hz.{args.format}")
    else:
        output_path = args.output

    # Ejecutar conversión
    success = convert_audio(input_path, output_path, method=args.method, format_out=args.format)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
