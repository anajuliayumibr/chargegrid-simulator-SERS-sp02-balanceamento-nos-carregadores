# -*- coding: utf-8 -*-
"""
ChargeGrid — Simulador de Recarga + Balanceamento de Carga
FIAP + GoodWe | EV Challenge 2026 | Sprint 2
"""

import time

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
CAPACIDADE_BATERIA = 75       # kWh — capacidade total da bateria simulada
LIMITE_REDE        = 22.0     # kW  — limite máximo da rede elétrica


# ─────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ─────────────────────────────────────────────

def ler_numero(texto, minimo, maximo):
    """Valida entradas numéricas do usuário."""
    while True:
        try:
            valor = int(input(texto))
            if minimo <= valor <= maximo:
                return valor
            print(f"  ⚠️  Digite entre {minimo} e {maximo}")
        except:
            print("  ⚠️  Valor inválido")


def calcular_custo(energia, tarifa, taxa):
    """Calcula o custo total da sessão."""
    return (energia * tarifa) + taxa


# ─────────────────────────────────────────────
# BALANCEAMENTO DE CARGA
# ─────────────────────────────────────────────

def balancear(carros):
    """
    Divide a potência disponível igualmente entre todos os carros conectados.
    Garante que o total nunca ultrapasse LIMITE_REDE.

    Exemplos:
      1 carro  → 22,00 kW
      2 carros → 11,00 kW cada   (total: 22,00 kW)
      3 carros →  7,33 kW cada   (total: 21,99 kW < 22 kW ✔)
    """
    if not carros:
        return
    potencia_por_carro = LIMITE_REDE / len(carros)
    for c in carros:
        c["potencia"] = round(potencia_por_carro, 2)


def exibir_rede(carros):
    """Exibe o status da rede e a tabela de veículos em tempo real."""
    total_kw = sum(c["potencia"] for c in carros)
    uso_pct  = (total_kw / LIMITE_REDE) * 100
    barras   = int(uso_pct / 5)
    barra    = "█" * barras + "░" * (20 - barras)

    print(f"\n  Rede: [{barra}] {uso_pct:.1f}%  ({total_kw:.2f} / {LIMITE_REDE} kW)")

    if not carros:
        print("  Nenhum veículo conectado.")
        return

    print(f"\n  {'ID':<6} {'Potência':<12} {'Energia est.':<14} {'Custo est.'}")
    print(f"  {'─'*5} {'─'*11} {'─'*13} {'─'*10}")

    for c in carros:
        energia_est = c["potencia"] * (c["tempo_min"] / 60)
        custo_est   = calcular_custo(energia_est, c["tarifa"], c["taxa"])
        print(
            f"  {c['id']:<6}"
            f"{c['potencia']:.2f} kW{'':>4}"
            f"{energia_est:.3f} kWh{'':>3}"
            f"R$ {custo_est:.2f}"
        )


def menu_balanceamento():
    """
    Módulo de gerenciamento de múltiplos veículos com balanceamento automático.
    Permite conectar e desconectar carros, mostrando a redistribuição em tempo real.
    """
    print("\n" + "=" * 50)
    print("  CHARGEGRID — GERENCIAMENTO DE REDE")
    print(f"  Limite da rede: {LIMITE_REDE} kW")
    print("=" * 50)

    carros   = []
    contador = 1

    while True:
        print("\n  [1] Conectar veículo")
        print("  [2] Desconectar veículo")
        print("  [3] Ver status da rede")
        print("  [4] Voltar ao menu principal")

        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            if len(carros) >= 6:
                print("  ⚠️  Limite de 6 veículos atingido.")
                continue

            print(f"\n  → Conectando C{contador:02d}")
            nome = input("  Nome do usuário: ").strip() or f"Usuário{contador}"

            premium = input("  Premium? (s/n): ").lower()
            tarifa  = 1.2 if premium == "s" else 1.8
            taxa    = 2   if premium == "s" else 5

            tempo = ler_numero("  Tempo estimado (min): ", 1, 480)

            novo = {
                "id":       f"C{contador:02d}",
                "nome":     nome,
                "potencia": 0.0,
                "tempo_min": tempo,
                "tarifa":   tarifa,
                "taxa":     taxa,
            }
            carros.append(novo)
            balancear(carros)

            total = sum(c["potencia"] for c in carros)
            print(f"\n  ✔ C{contador:02d} conectado.")
            print(f"  ✔ Balanceamento: {total:.2f} kW divididos entre {len(carros)} veículo(s).")
            exibir_rede(carros)
            contador += 1

        elif opcao == "2":
            if not carros:
                print("  Nenhum veículo conectado.")
                continue

            print(f"  Conectados: {', '.join(c['id'] for c in carros)}")
            id_rem = input("  ID para desconectar (ex: C01): ").strip().upper()

            encontrado = next((c for c in carros if c["id"] == id_rem), None)
            if not encontrado:
                print(f"  ⚠️  {id_rem} não encontrado.")
                continue

            carros.remove(encontrado)
            balancear(carros)

            total = sum(c["potencia"] for c in carros)
            print(f"\n  ✔ {id_rem} desconectado.")
            if carros:
                print(f"  ✔ Rede rebalanceada: {total:.2f} kW para {len(carros)} veículo(s).")
            exibir_rede(carros)

        elif opcao == "3":
            exibir_rede(carros)

        elif opcao == "4":
            break


# ─────────────────────────────────────────────
# RECARGA INDIVIDUAL (lógica original)
# ─────────────────────────────────────────────

def executar_recarga(bateria, limite, potencia, tarifa, taxa):
    """
    Simula a recarga minuto a minuto.
    Eficiência reduz para 50% após 80% de carga — replica comportamento real.
    """
    energia_total = 0
    tempo = 0

    print("\n⚡ Iniciando recarga...\n")

    while bateria < limite:

        # Eficiência reduz após 80% — evita desperdício e protege a bateria
        if bateria < 80:
            eficiencia = 1
        else:
            eficiencia = 0.5

        energia_min    = (potencia * eficiencia) / 60
        ganho          = (energia_min / CAPACIDADE_BATERIA) * 100
        energia_total += energia_min
        bateria       += ganho

        if bateria > limite:
            bateria = limite

        tempo += 1
        custo  = calcular_custo(energia_total, tarifa, taxa)

        print("-" * 40)
        print(f"Bateria: {bateria:.1f}%")
        print(f"Energia: {energia_total:.2f} kWh")
        print(f"Tempo: {tempo} min")
        print(f"Custo: R$ {custo:.2f}")

        time.sleep(0.2)

    return bateria, energia_total, tempo


def mostrar_recibo(bateria, energia, tempo, tarifa, taxa):
    """Exibe o recibo final da sessão."""
    subtotal = energia * tarifa
    total    = subtotal + taxa

    print("\n" + "=" * 40)
    print("🧾 RECIBO FINAL")
    print("=" * 40)
    print(f"Tempo: {tempo} min")
    print(f"Energia: {energia:.2f} kWh")
    print(f"Bateria final: {bateria:.1f}%")
    print(f"Tarifa: R$ {tarifa:.2f}/kWh")
    print(f"Taxa: R$ {taxa:.2f}")
    print(f"Subtotal: R$ {subtotal:.2f}")
    print("-" * 40)
    print(f"TOTAL: R$ {total:.2f}")
    print("=" * 40)


# ─────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────

print("=" * 50)
print("  CHARGEGRID")
print("=" * 50)

while True:
    print("\n  [1] Recarga individual")
    print("  [2] Gerenciar múltiplos veículos (balanceamento)")
    print("  [3] Sair")

    escolha = input("\n  Escolha: ").strip()

    if escolha == "1":

        premium = input("\nUsuário premium? (s/n): ").lower()
        tarifa  = 1.2 if premium == "s" else 1.8
        taxa    = 2   if premium == "s" else 5

        print("\nPotências disponíveis:")
        print("1 - 22 kW")
        print("2 - 50 kW")
        print("3 - 150 kW")

        opcao = ler_numero("Escolha: ", 1, 3)
        if opcao == 1:   potencia = 22
        elif opcao == 2: potencia = 50
        else:            potencia = 150

        bateria = ler_numero("\nBateria atual (%): ", 5, 70)
        limite  = ler_numero("Limite desejado (%): ", bateria + 1, 100)

        bateria, energia, tempo = executar_recarga(bateria, limite, potencia, tarifa, taxa)
        mostrar_recibo(bateria, energia, tempo, tarifa, taxa)

    elif escolha == "2":
        menu_balanceamento()

    elif escolha == "3":
        print("\n  Até logo!")
        break
