
import asyncio
import csv
import json
from pathlib import Path

from pydantic import BaseModel, Field
from agents import Agent, Runner, SQLiteSession

BASE = Path(__file__).resolve().parent
MODELO = "gpt-4.1-mini"
TURNOS = 10

DB = str(BASE / "terapia_estado.db")
ESTADO_FILE = BASE / "paciente_estado.json"
CSV_FILE = BASE / "evolucion_paciente.csv"
CONTROL_FILE = BASE / "control_terapia.json"


class Evaluacion(BaseModel):
    empatia: int = Field(ge=0, le=10)
    escucha: int = Field(ge=0, le=10)
    presion: int = Field(ge=0, le=10)
    observacion: str


psicologo = Agent(
    name="Psicologo",
    model=MODELO,
    instructions="""
    Eres un psicólogo ficticio en una simulación educativa.
    Emplea escucha activa, empatía y preguntas abiertas.
    Utiliza técnicas inspiradas en TCC.
    No diagnostiques ni prescribas medicamentos.
    No presentes la simulación como terapia real.
    Haz una sola pregunta por intervención.
    Responde en español, en menos de 100 palabras.
    Ante riesgo inmediato o suicidio, prioriza
    la seguridad y recomienda ayuda humana urgente.
    """
)

paciente = Agent(
    name="Marcos",
    model=MODELO,
    instructions="""
    Interpretas a Marcos, un paciente ficticio
    de 35 años con síntomas depresivos.

    Trabajas en una oficina.
    Desde hace tres meses tienes tristeza,
    problemas de sueño, apatía y aislamiento.
    En este escenario no tienes ideas suicidas.

    Mantén coherencia con tus conversaciones previas.
    Tu estado emocional actual se incluirá
    en cada intervención.

    No mejores repentinamente.
    Habla en español y de forma natural.
    Máximo 100 palabras.
    """
)

evaluador = Agent(
    name="Evaluador",
    model=MODELO,
    instructions="""
    Evalúas intervenciones de un psicólogo simulado.

    Puntúa de 0 a 10:
    - Empatía: comprensión y validación emocional.
    - Escucha: atención a lo expresado por el paciente.
    - Presión: insistencia o exigencia excesiva.

    No evalúas eficacia clínica.
    No diagnostiques.
    Basa la puntuación únicamente en el texto recibido.
    """,
    output_type=Evaluacion
)


def estado_inicial():
    return {
        "animo": 3,
        "ansiedad": 7,
        "energia": 2,
        "confianza": 4,
        "aislamiento": 8
    }


def cargar_json(ruta, defecto):
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    return defecto


def guardar_json(ruta, datos):
    ruta.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def limitar(valor):
    return max(0, min(10, valor))


def evolucionar(estado, evaluacion, turno):
    nuevo = estado.copy()

    # Reglas experimentales, no clínicas.
    if evaluacion.empatia >= 7 and evaluacion.escucha >= 7:
        nuevo["confianza"] += 1

    if evaluacion.presion >= 7:
        nuevo["confianza"] -= 1
        nuevo["ansiedad"] += 1
    elif evaluacion.empatia >= 7:
        nuevo["ansiedad"] -= 1

    # Cambios lentos: como máximo cada 3 turnos.
    if turno % 3 == 0 and nuevo["confianza"] >= 6:
        nuevo["animo"] += 1
        nuevo["energia"] += 1
        nuevo["aislamiento"] -= 1

    return {k: limitar(v) for k, v in nuevo.items()}


def guardar_csv(turno, estado, evaluacion):
    existe = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        campos = [
            "turno", "animo", "ansiedad", "energia",
            "confianza", "aislamiento",
            "empatia", "escucha", "presion"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)

        if not existe:
            writer.writeheader()

        writer.writerow({
            "turno": turno,
            **estado,
            "empatia": evaluacion.empatia,
            "escucha": evaluacion.escucha,
            "presion": evaluacion.presion
        })


async def main():
    estado = cargar_json(ESTADO_FILE, estado_inicial())
    control = cargar_json(
        CONTROL_FILE,
        {
            "turno": 0,
            "ultimo_mensaje": (
                "Comienza la primera sesión con Marcos. "
                "Pregúntale cómo se encuentra."
            )
        }
    )

    sesion_psicologo = SQLiteSession("psicologo", DB)
    sesion_paciente = SQLiteSession("marcos", DB)

    for _ in range(TURNOS):
        turno = control["turno"] + 1

        respuesta = await Runner.run(
            psicologo,
            control["ultimo_mensaje"],
            session=sesion_psicologo
        )
        texto_psicologo = str(respuesta.final_output)

        print(f"\n=== TURNO {turno} ===")
        print(f"PSICÓLOGO: {texto_psicologo}")

        resultado_eval = await Runner.run(
            evaluador,
            texto_psicologo
        )
        evaluacion = resultado_eval.final_output

        estado = evolucionar(estado, evaluacion, turno)

        entrada_paciente = (
            f"Estado emocional simulado actual:\n"
            f"{json.dumps(estado, ensure_ascii=False)}\n\n"
            f"Última intervención del psicólogo:\n"
            f"{texto_psicologo}\n\n"
            "Responde como Marcos, de manera coherente."
        )

        respuesta_paciente = await Runner.run(
            paciente,
            entrada_paciente,
            session=sesion_paciente
        )
        texto_paciente = str(respuesta_paciente.final_output)

        print(f"PACIENTE: {texto_paciente}")
        print(f"ESTADO: {estado}")
        print(f"EVALUACIÓN: {evaluacion.observacion}")

        guardar_csv(turno, estado, evaluacion)

        control = {
            "turno": turno,
            "ultimo_mensaje": texto_paciente
        }
        guardar_json(ESTADO_FILE, estado)
        guardar_json(CONTROL_FILE, control)

    print("\nSimulación finalizada.")
    print("Estado:", ESTADO_FILE)
    print("Evolución:", CSV_FILE)


if __name__ == "__main__":
    asyncio.run(main())
