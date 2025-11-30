#!/usr/bin/env python3
"""
Teste rápido de conectividade RPC
"""
import xmlrpc.client
import sys

def test_rpc_connection():
    server_host = "192.168.1.160"
    server_port = "8000"
    server_url = f"http://{server_host}:{server_port}/RPC2"
    
    print(f"Testando conexão RPC com: {server_url}")
    
    try:
        # Criar cliente RPC
        client = xmlrpc.client.ServerProxy(server_url, allow_none=True)
        
        # Testar operação simples
        print("Testando operação: 5 + 3")
        resultado = client.somar(5, 3)
        print(f"Resultado: {resultado}")
        
        if resultado == 8:
            print("✅ SUCESSO: Comunicação RPC funcionando!")
            return True
        else:
            print(f"❌ ERRO: Resultado esperado 8, obtido {resultado}")
            return False
            
    except ConnectionRefusedError:
        print("❌ ERRO: Conexão recusada - servidor não está rodando ou firewall bloqueando")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    success = test_rpc_connection()
    sys.exit(0 if success else 1)