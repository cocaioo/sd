from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time
import json
import os
from datetime import datetime


# ======= CAMADA "DE NEGÓCIO" (LÓGICA DA APLICAÇÃO) =======

class CalculadoraService:
    def somar(self, a, b):
        print("\n[SERVER] ===== NOVA CHAMADA RPC: somar =====")
        print(f"[SERVER] Parâmetros recebidos: a={a}, b={b}")
        self._log_event("server", "request", {"method": "somar", "a": a, "b": b})
        time.sleep(0.3)
        resultado = a + b
        print(f"[SERVER] Processando: {a} + {b} = {resultado}")
        time.sleep(0.3)
        print("[SERVER] Retornando resultado ao middleware RPC...")
        self._log_event("server", "response", {"method": "somar", "result": resultado})
        return resultado

    def subtrair(self, a, b):
        print("\n[SERVER] ===== NOVA CHAMADA RPC: subtrair =====")
        print(f"[SERVER] Parâmetros recebidos: a={a}, b={b}")
        time.sleep(0.3)
        resultado = a - b
        print(f"[SERVER] Processando: {a} - {b} = {resultado}")
        time.sleep(0.3)
        print("[SERVER] Retornando resultado ao middleware RPC...")
        return resultado

    def multiplicar(self, a, b):
        print("\n[SERVER] ===== NOVA CHAMADA RPC: multiplicar =====")
        print(f"[SERVER] Parâmetros recebidos: a={a}, b={b}")
        time.sleep(0.3)
        resultado = a * b
        print(f"[SERVER] Processando: {a} * {b} = {resultado}")
        time.sleep(0.3)
        print("[SERVER] Retornando resultado ao middleware RPC...")
        return resultado

    def dividir(self, a, b):
        print("\n[SERVER] ===== NOVA CHAMADA RPC: dividir =====")
        print(f"[SERVER] Parâmetros recebidos: a={a}, b={b}")
        self._log_event("server", "request", {"method": "dividir", "a": a, "b": b})
        time.sleep(0.3)
        if b == 0:
            print("[SERVER] Erro: divisão por zero detectada!")
            self._log_event("server", "error", {"method": "dividir", "error": "divisao_por_zero"})
            raise ZeroDivisionError("Divisão por zero não permitida")
        resultado = a / b
        print(f"[SERVER] Processando: {a} / {b} = {resultado}")
        time.sleep(0.3)
        print("[SERVER] Retornando resultado ao middleware RPC...")
        self._log_event("server", "response", {"method": "dividir", "result": resultado})
        return resultado

    def _log_event(self, source, typ, payload):
        try:
            shared = os.environ.get("RPC_SHARED_PATH", "/shared")
            path = os.path.join(shared, "events.log")
            entry = {"ts": datetime.utcnow().isoformat() + "Z", "source": source, "type": typ, "payload": payload}
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass


# ======= CAMADA MIDDLEWARE / RPC =======

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


def main():
    host = "0.0.0.0"  # importante para Docker
    port = 8000

    with SimpleXMLRPCServer((host, port),
                            requestHandler=RequestHandler,
                            allow_none=True,
                            logRequests=True) as server:
        server.register_introspection_functions()
        calculadora = CalculadoraService()

        server.register_function(calculadora.somar, "somar")
        server.register_function(calculadora.subtrair, "subtrair")
        server.register_function(calculadora.multiplicar, "multiplicar")
        server.register_function(calculadora.dividir, "dividir")

        print(f"Servidor RPC rodando em http://{host}:{port}/RPC2")
        print("Métodos disponíveis: somar, subtrair, multiplicar, dividir")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()