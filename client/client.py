import xmlrpc.client
import time
import os


def clear_screen():
    # Funciona em Windows e Unix
    os.system("cls" if os.name == "nt" else "clear")


def _log_event(source, typ, payload):
    try:
        shared = os.environ.get("RPC_SHARED_PATH", "/shared")
        path = os.path.join(shared, "events.log")
        import json
        from datetime import datetime
        entry = {"ts": datetime.utcnow().isoformat() + "Z", "source": source, "type": typ, "payload": payload}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ======= CAMADA MIDDLEWARE / STUB =======


class CalculadoraClient:
    """
    Stub do lado do cliente.
    Encapsula o ServerProxy e expõe métodos locais.
    """
    def __init__(self, url):
        print(f"[CLIENT] Inicializando stub RPC para {url}")
        self.proxy = xmlrpc.client.ServerProxy(url, allow_none=True)

    def somar(self, a, b):
        print("[CLIENT] Preparando chamada remota: somar")
        _log_event("client", "request", {"method": "somar", "a": a, "b": b})
        time.sleep(0.3)
        print("[CLIENT] Serializando parâmetros e enviando requisição XML-RPC...")
        time.sleep(0.3)
        try:
            resultado = self.proxy.somar(a, b)
            print("[CLIENT] Resposta recebida e desserializada com sucesso.")
            _log_event("client", "response", {"method": "somar", "result": resultado})
            return resultado
        except xmlrpc.client.Fault as fault:
            print(f"[CLIENT] Erro remoto em somar: {fault}")
            raise

    def subtrair(self, a, b):
        print("[CLIENT] Preparando chamada remota: subtrair")
        _log_event("client", "request", {"method": "subtrair", "a": a, "b": b})
        time.sleep(0.3)
        print("[CLIENT] Serializando parâmetros e enviando requisição XML-RPC...")
        time.sleep(0.3)
        try:
            resultado = self.proxy.subtrair(a, b)
            print("[CLIENT] Resposta recebida e desserializada com sucesso.")
            _log_event("client", "response", {"method": "subtrair", "result": resultado})
            return resultado
        except xmlrpc.client.Fault as fault:
            print(f"[CLIENT] Erro remoto em subtrair: {fault}")
            raise

    def multiplicar(self, a, b):
        print("[CLIENT] Preparando chamada remota: multiplicar")
        _log_event("client", "request", {"method": "multiplicar", "a": a, "b": b})
        time.sleep(0.3)
        print("[CLIENT] Serializando parâmetros e enviando requisição XML-RPC...")
        time.sleep(0.3)
        try:
            resultado = self.proxy.multiplicar(a, b)
            print("[CLIENT] Resposta recebida e desserializada com sucesso.")
            _log_event("client", "response", {"method": "multiplicar", "result": resultado})
            return resultado
        except xmlrpc.client.Fault as fault:
            print(f"[CLIENT] Erro remoto em multiplicar: {fault}")
            raise

    def dividir(self, a, b):
        print("[CLIENT] Preparando chamada remota: dividir")
        _log_event("client", "request", {"method": "dividir", "a": a, "b": b})
        time.sleep(0.3)
        print("[CLIENT] Serializando parâmetros e enviando requisição XML-RPC...")
        time.sleep(0.3)
        try:
            resultado = self.proxy.dividir(a, b)
            print("[CLIENT] Resposta recebida e desserializada com sucesso.")
            _log_event("client", "response", {"method": "dividir", "result": resultado})
            return resultado
        except xmlrpc.client.Fault as fault:
            print(f"[CLIENT] Erro remoto em dividir: {fault}")
            raise


# ======= INTERFACE INTERATIVA (TELINHA) =======


def menu():
    print("====== CLIENTE RPC - CALCULADORA DISTRIBUÍDA ======")
    print("Selecione a operação:")
    print("1 - Somar")
    print("2 - Subtrair")
    print("3 - Multiplicar")
    print("4 - Dividir")
    print("0 - Sair")
    print("===================================================")


def ler_operandos():
    a = float(input("Digite o primeiro operando (a): "))
    b = float(input("Digite o segundo operando (b): "))
    return a, b


def main():
    server_url = "http://server:8000/RPC2"  # vamos usar 'server' como hostname no Docker
    calc = CalculadoraClient(server_url)

    while True:
        clear_screen()
        menu()
        opcao = input("Opção: ").strip()

        if opcao == "0":
            print("Saindo do cliente...")
            time.sleep(0.5)
            break

        if opcao not in {"1", "2", "3", "4"}:
            print("Opção inválida. Pressione ENTER para continuar.")
            input()
            continue

        clear_screen()
        try:
            a, b = ler_operandos()
        except ValueError:
            print("Entrada inválida. Use apenas números. Pressione ENTER para continuar.")
            input()
            continue

        clear_screen()
        try:
            if opcao == "1":
                print(f"Requisição: somar({a}, {b})")
                resultado = calc.somar(a, b)
                print(f"Resultado: {a} + {b} = {resultado}")
            elif opcao == "2":
                print(f"Requisição: subtrair({a}, {b})")
                resultado = calc.subtrair(a, b)
                print(f"Resultado: {a} - {b} = {resultado}")
            elif opcao == "3":
                print(f"Requisição: multiplicar({a}, {b})")
                resultado = calc.multiplicar(a, b)
                print(f"Resultado: {a} * {b} = {resultado}")
            elif opcao == "4":
                print(f"Requisição: dividir({a}, {b})")
                try:
                    resultado = calc.dividir(a, b)
                    print(f"Resultado: {a} / {b} = {resultado}")
                except Exception as e:
                    print(f"Ocorreu um erro na divisão: {e}")

        except ConnectionRefusedError:
            print("[CLIENT] Não foi possível conectar ao servidor. Ele está rodando?")
        except Exception as e:
            print(f"[CLIENT] Erro inesperado: {e}")

        print("\nPressione ENTER para fazer outra operação...")
        input()


if __name__ == "__main__":
    main()