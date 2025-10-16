"""Cronómetro interactivo de línea de comandos.

Este pequeño programa permite medir el tiempo transcurrido con la
posibilidad de registrar vueltas, pausar, reanudar y reiniciar el
cronómetro. Está pensado para ser sencillo de usar directamente desde
la terminal.
"""

from __future__ import annotations

import time


def formatear_tiempo(segundos: float) -> str:
    """Devuelve una cadena HH:MM:SS.mmm a partir de segundos."""

    minutos, segundos = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    milisegundos = int(round((segundos - int(segundos)) * 1000))
    segundos = int(segundos)
    if milisegundos == 1000:
        # Corrección por redondeo: 59.9995 -> 60.000
        milisegundos = 0
        segundos += 1
        if segundos == 60:
            segundos = 0
            minutos += 1
            if minutos == 60:
                minutos = 0
                horas += 1
    return f"{int(horas):02d}:{int(minutos):02d}:{segundos:02d}.{milisegundos:03d}"


def ejecutar_cronometro() -> None:
    """Ejecuta un cronómetro interactivo en la terminal."""

    print("Cronómetro iniciado. Las opciones son:")
    print("  [Enter] Registrar una vuelta")
    print("  p      Pausar/Reanudar")
    print("  r      Reiniciar")
    print("  q      Salir")

    inicio = time.perf_counter()
    tiempo_pausado = 0.0
    ejecutando = True
    vueltas: list[str] = []

    while True:
        comando = input("Acción (Enter/p/r/q): ").strip().lower()

        momento_actual = time.perf_counter()
        transcurrido = (momento_actual - inicio) if ejecutando else tiempo_pausado

        if comando == "":
            if not ejecutando:
                print("El cronómetro está en pausa. Usa 'p' para reanudar.")
                continue

            vueltas.append(formatear_tiempo(transcurrido))
            print(f"Vuelta {len(vueltas)}: {vueltas[-1]}")

        elif comando == "p":
            if ejecutando:
                tiempo_pausado = transcurrido
                ejecutando = False
                print(f"Cronómetro pausado en {formatear_tiempo(tiempo_pausado)}")
            else:
                inicio = time.perf_counter() - tiempo_pausado
                ejecutando = True
                print("Cronómetro reanudado.")

        elif comando == "r":
            inicio = time.perf_counter()
            tiempo_pausado = 0.0
            ejecutando = True
            vueltas.clear()
            print("Cronómetro reiniciado.")

        elif comando == "q":
            print(f"Tiempo final: {formatear_tiempo(transcurrido)}")
            if vueltas:
                print("Vueltas registradas:")
                for numero, vuelta in enumerate(vueltas, start=1):
                    print(f"  {numero:02d}: {vuelta}")
            break

        else:
            print("Comando no reconocido. Usa Enter, p, r o q.")


if __name__ == "__main__":
    ejecutar_cronometro()
