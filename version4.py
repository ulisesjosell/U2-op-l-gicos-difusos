def difuso_and(a, b):
    """Operador AND difuso (Intersección / Mínimo)"""
    return min(a, b)

def difuso_or(a, b):
    """Operador OR difuso (Unión / Máximo)"""
    return max(a, b)

def difuso_not(a):
    """Operador NOT difuso (Complemento)"""
    return round(1.0 - a, 2)

def pedir_grado(numero, pregunta):
    """Solicita un valor válido entre 0 y 1 al usuario"""
    while True:
        try:
            print(f"\nPregunta {numero}: {pregunta}")
            valor = float(input("Ingresa un valor entre 0 (nada) y 100 (totalmente): "))
            if 0 <= valor <= 100:
                return valor
            else:
                print("⚠️ Error: El número debe estar dentro del rango [0, 100].")
        except ValueError:
            print("⚠️ Error: Por favor ingresa un número válido (ejemplo: 70).")

def jugar():
    print("=" * 60)
    print(" 🎮 JUEGO DE ROL CON LÓGICA DIFUSA: DESCUBRE QUIEN ERES EN LA MITOLOGIA 🎮")
    print("=" * 60)
    print("Responde las 5 preguntas con un grado de verdad entre 0 y 100.")

    # 5 Preguntas de entrada (Grados de pertenencia)
    fuerza = pedir_grado(1, "¿Qué tanto prefieres el combate cuerpo a cuerpo")
    magia = pedir_grado(2, "¿Qué tanta afinidad tienes por los hechizos?")
    sigilo = pedir_grado(3, "¿Qué tan bueno eres siendo sigiloso?")
    riesgo = pedir_grado(4, "¿Qué tanto te gusta tomar decisiones arriesgadas?")
    equipo = pedir_grado(5, "¿Te gusta trabajar en equipo?")

    print("\n" + "=" * 60)
    print(" ⚙️ EVALUANDO REGLAS CON OPERADORES LÓGICOS DIFUSOS...")
    print("=" * 60)

    # Aplicación de operadores difusos (AND, OR, NOT)
    # Regla 1 (Guerrero): Alta fuerza Y (alto riesgo O trabajo en equipo)
    regla_guerrero = difuso_and(fuerza, difuso_or(riesgo, difuso_not(equipo)))

    # Regla 2 (Mago): Alta magia Y NO combate cuerpo a cuerpo
    regla_mago = difuso_and(magia, difuso_not(fuerza))

    # Regla 3 (Pícaro/Asesino): Alto sigilo Y NO trabajo en equipo Y alto riesgo
    regla_picaro = difuso_and(difuso_and(sigilo, difuso_not(equipo)), riesgo)

    # Regla 4 (Paladín): Trabajo en equipo Y (fuerza O magia) Y NO sigilo
    regla_paladin = difuso_and(equipo, difuso_and(difuso_or(fuerza, magia), difuso_not(sigilo)))

    resultados = {
        "Tank": regla_guerrero,
        "Healer": regla_mago,
        "Ladron": regla_picaro,
        "Rey Mago": regla_paladin
    }

    # Mostrar el desglose de cada regla
    for clase, grado in resultados.items():
        barra = "█" * int(grado * 20)
        print(f"- {clase:<22}: {grado:.2f} | {barra}")

    # Determinar la clase ganadora (mayor grado de pertenencia)
    clase_final = max(resultados, key=resultados.get)
    puntaje_max = resultados[clase_final]

    print("\n" + "=" * 60)
    print(f" 🏆 RESULTADO FINAL: Eres un {clase_final} (Grado: {puntaje_max:.2f})")
    print("=" * 60)

if __name__ == "__main__":
    jugar()