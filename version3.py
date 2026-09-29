import math

class MotorDifuso:
    """Contiene los operadores matemáticos, funciones de pertenencia y modificadores."""
    
    # --- 1. OPERADORES DE ZADEH (Estándar Min/Max) ---
    @staticmethod
    def and_zadeh(a, b):
        return min(a, b)

    @staticmethod
    def or_zadeh(a, b):
        return max(a, b)

    # --- 2. OPERADORES PROBABILÍSTICOS / ALGEBRAICOS (Suavizados) ---
    @staticmethod
    def and_algebraico(a, b):
        """Producto algebraico: ambas condiciones atenúan el resultado continuamente."""
        return a * b

    @staticmethod
    def or_probabilistico(a, b):
        """Suma algebraica: a + b - (a * b)"""
        return (a + b) - (a * b)

    @staticmethod
    def not_difuso(a):
        return 1.0 - a

    # --- 3. MODIFICADORES LINGÜÍSTICOS (HEDGES) ---
    @staticmethod
    def muy(a):
        """Concentración: exige valores más altos para activarse (a^2)."""
        return a ** 2

    @staticmethod
    def algo(a):
        """Dilatación: suaviza la exigencia dando más peso a valores medios (sqrt(a))."""
        return math.sqrt(a)

    # --- 4. FUZZIFICACIÓN (Función de Pertenencia Triangular) ---
    @staticmethod
    def triangular(x, a, b, c):
        """
        Calcula el grado de pertenencia de 'x' en un triángulo definido por (a, b, c)
        donde 'b' es el pico máximo (1.0) y 'a', 'c' son los límites (0.0).
        """
        if x <= a or x >= c:
            if x == b:  # Caso especial para bordes exactos (0 o 100)
                return 1.0
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        else:
            return (c - x) / (c - b) if c != b else 1.0

    @classmethod
    def fuzzificar_entrada(cls, valor):
        """Convierte un número de 0 a 100 en tres conjuntos difusos: Bajo, Medio y Alto."""
        return {
            "bajo": round(cls.triangular(valor, 0, 0, 50), 3),
            "medio": round(cls.triangular(valor, 20, 50, 80), 3),
            "alto": round(cls.triangular(valor, 50, 100, 100), 3)
        }


def pedir_valor_crisp(numero, pregunta):
    """Solicita un valor entero o decimal en escala de 0 a 100."""
    while True:
        try:
            print(f"\n[Pregunta {numero}] {pregunta}")
            val = float(input("  👉 Ingresa un nivel del 0 al 100: "))
            if 0 <= val <= 100:
                return val
            print("  ⚠️ Error: El valor debe estar entre 0 y 100.")
        except ValueError:
            print("  ⚠️ Error: Ingresa un número válido.")


def evaluar_reglas(f):
    """
    Evalúa un banco de 8 reglas complejas combinando conjuntos (bajo/medio/alto),
    modificadores (muy/algo) y diferentes T-normas (Zadeh y Algebraica).
    """
    m = MotorDifuso

    # --- GUERRERO BERSERKER (2 Reglas agregadas con OR) ---
    # R1: Fuerza MUY alta Y Riesgo alto (Zadeh)
    r1_guerrero = m.and_zadeh(m.muy(f["fuerza"]["alto"]), f["riesgo"]["alto"])
    # R2: Fuerza media Y Riesgo MUY alto Y Magia baja (Algebraico)
    r2_guerrero = m.and_algebraico(
        f["fuerza"]["medio"],
        m.and_algebraico(m.muy(f["riesgo"]["alto"]), f["magia"]["bajo"])
    )
    grado_guerrero = m.or_zadeh(r1_guerrero, r2_guerrero)

    # --- ARCHIMAGO ARCANO (2 Reglas) ---
    # R1: Magia MUY alta Y Fuerza baja
    r1_mago = m.and_zadeh(m.muy(f["magia"]["alto"]), f["fuerza"]["bajo"])
    # R2: Magia alta Y (NO Riesgo alto) Y Fuerza media
    r2_mago = m.and_algebraico(
        f["magia"]["alto"],
        m.and_zadeh(m.not_difuso(f["riesgo"]["alto"]), f["fuerza"]["medio"])
    )
    grado_mago = m.or_zadeh(r1_mago, r2_mago)

    # --- ASESINO DE LAS SOMBRAS (2 Reglas) ---
    # R1: Sigilo MUY alto Y Equipo bajo Y Riesgo ALGO alto
    r1_asesino = m.and_zadeh(
        m.muy(f["sigilo"]["alto"]),
        m.and_zadeh(f["equipo"]["bajo"], m.algo(f["riesgo"]["alto"]))
    )
    # R2: Sigilo alto Y Fuerza media Y (NO Equipo alto)
    r2_asesino = m.and_algebraico(
        f["sigilo"]["alto"],
        m.and_zadeh(f["fuerza"]["medio"], m.not_difuso(f["equipo"]["alto"]))
    )
    grado_asesino = m.or_zadeh(r1_asesino, r2_asesino)

    # --- PALADÍN PROTECTOR (2 Reglas) ---
    # R1: Equipo MUY alto Y (Fuerza alta O Magia media) Y Sigilo bajo
    r1_paladin = m.and_zadeh(
        m.muy(f["equipo"]["alto"]),
        m.and_zadeh(
            m.or_probabilistico(f["fuerza"]["alto"], f["magia"]["medio"]),
            f["sigilo"]["bajo"]
        )
    )
    # R2: Equipo alto Y Fuerza media Y Magia media
    r2_paladin = m.and_algebraico(
        f["equipo"]["alto"],
        m.and_algebraico(f["fuerza"]["medio"], f["magia"]["medio"])
    )
    grado_paladin = m.or_zadeh(r1_paladin, r2_paladin)

    # --- MONJE MÍSTICO (Regla híbrida de equilibrio) ---
    # Se activa cuando el jugador tiene valores MEDIOS en Fuerza, Magia y Sigilo
    grado_monje = m.and_zadeh(
        f["fuerza"]["medio"],
        m.and_zadeh(f["magia"]["medio"], m.algo(f["sigilo"]["medio"]))
    )

    return {
        "Guerrero Berserker": round(grado_guerrero, 3),
        "Archimago Arcano": round(grado_mago, 3),
        "Asesino de las Sombras": round(grado_asesino, 3),
        "Paladín Protector": round(grado_paladin, 3),
        "Monje del Equilibrio": round(grado_monje, 3)
    }


def defuzzificar_atributos(resultados):
    """
    Defuzzificación por Centroide (Promedio Ponderado):
    Calcula estadísticas numéricas exactas combinando la influencia de TODAS las clases activadas.
    """
    # Centroides base de cada clase: (Ataque Físico, Poder Mágico, Velocidad/Crítico)
    arquetipos = {
        "Guerrero Berserker":     (95, 10, 50),
        "Archimago Arcano":       (15, 98, 40),
        "Asesino de las Sombras": (75, 25, 95),
        "Paladín Protector":      (70, 65, 30),
        "Monje del Equilibrio":   (60, 60, 80)
    }

    suma_grados = sum(resultados.values())
    if suma_grados == 0:
        return {"Ataque Físico": 50.0, "Poder Mágico": 50.0, "Velocidad": 50.0}

    ataque = sum(resultados[c] * arquetipos[c][0] for c in resultados) / suma_grados
    magia  = sum(resultados[c] * arquetipos[c][1] for c in resultados) / suma_grados
    veloc  = sum(resultados[c] * arquetipos[c][2] for c in resultados) / suma_grados

    return {
        "Ataque Físico": round(ataque, 1),
        "Poder Mágico": round(magia, 1),
        "Velocidad": round(veloc, 1)
    }


def jugar():
    print("=" * 70)
    print(" ⚔️ SISTEMA DE INFERENCIA DIFUSA: GENERADOR DE PERSONAJE AVANZADO ⚔️")
    print("=" * 70)
    print("Evalúa cada atributo del 0 al 100. El motor lo fuzzificará en")
    print("conjuntos (Bajo, Medio, Alto) para procesar las reglas de inferencia.")

    preguntas = {
        "fuerza": "¿Qué tanto prefieres el combate cuerpo a cuerpo brutal?",
        "magia":  "¿Qué tanta afinidad sientes por las artes arcanas y hechizos?",
        "sigilo": "¿Qué tanto prefieres el sigilo, la infiltración y las emboscadas?",
        "riesgo": "¿Qué tanto te gusta apostar el todo por el todo en situaciones límite?",
        "equipo": "¿Qué tanto priorizas proteger y coordinarte con tus aliados?"
    }

    # Paso 1: Captura y Fuzzificación
    datos_difusos = {}
    for clave, texto in preguntas.items():
        num = list(preguntas.keys()).index(clave) + 1
        valor_crisp = pedir_valor_crisp(num, texto)
        datos_difusos[clave] = MotorDifuso.fuzzificar_entrada(valor_crisp)

    # Mostrar tabla de Fuzzificación
    print("\n" + "=" * 70)
    print(" 📊 1. ETAPA DE FUZZIFICACIÓN (Grados de pertenencia por conjunto)")
    print("=" * 70)
    print(f"{'Atributo':<12} | {'Bajo':<10} | {'Medio':<10} | {'Alto':<10}")
    print("-" * 50)
    for attr, conjuntos in datos_difusos.items():
        print(f"{attr.capitalize():<12} | {conjuntos['bajo']:<10.2f} | {conjuntos['medio']:<10.2f} | {conjuntos['alto']:<10.2f}")

    # Paso 2: Inferencia y Agregación de Reglas
    resultados = evaluar_reglas(datos_difusos)

    print("\n" + "=" * 70)
    print(" ⚙️ 2. EVALUACIÓN DE REGLAS Y AGREGACIÓN DIFUSA")
    print("=" * 70)
    for clase, grado in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
        barra = "█" * int(grado * 25)
        print(f"- {clase:<24}: {grado:.3f} | {barra}")

    # Paso 3: Defuzzificación (Cálculo de Estadísticas y Clase Híbrida)
    stats = defuzzificar_atributos(resultados)
    clases_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
    principal, segundaria = clases_ordenadas[0], clases_ordenadas[1]

    print("\n" + "=" * 70)
    print(" 🏆 3. DEFUZZIFICACIÓN Y FICHA FINAL DEL PERSONAJE")
    print("=" * 70)
    
    if principal[1] == 0:
        print("🎭 Clase: Aventurero Indeciso (Ninguna regla superó el umbral)")
    elif segundaria[1] > 0.35 and (principal[1] - segundaria[1]) < 0.25:
        print(f"🎭 Clase Híbrida: {principal[0]} / {segundaria[0]}")
        print(f"   (Afinidad dual detectada: {principal[1]:.2f} y {segundaria[1]:.2f})")
    else:
        print(f"🎭 Clase Pura: {principal[0]} (Grado de certeza: {principal[1]:.2f})")

    print("\n📈 Estadísticas Base (Calculadas por Centroide Difuso):")
    for stat_nombre, valor in stats.items():
        print(f"   • {stat_nombre:<15}: {valor} pts")
    print("=" * 70)


if __name__ == "__main__":
    jugar()