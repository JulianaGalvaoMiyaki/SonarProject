import sys
import os
from datetime import datetime
from github import Github

def publicar_no_pages(mensagem_release):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "JuGalvaoMiyaki/desafio-security"
    file_path = "changelog.md"

    if not token:
        print("❌ Erro: Variável GITHUB_TOKEN não encontrada.")
        return

    try:
        print("🔄 Conectando à API do GitHub...")
        g = Github(token)
        repo = g.get_repo(repo_name)

        try:

            contents = repo.get_contents(file_path, ref="main")
            conteudo_atual = contents.decoded_content.decode("utf-8")
            sha_arquivo = contents.sha
            print(f"📂 Arquivo {file_path} encontrado. Atualizando...")
        except:
            conteudo_atual = "# Histórico de Versões\n\n"
            sha_arquivo = None
            print(f"⚠️ Arquivo {file_path} não encontrado. Criando novo...")

        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        nova_entrada = f"## 🚀 Release - {data_hoje}\n{mensagem_release}\n\n---\n\n"
        novo_conteudo_completo = nova_entrada + conteudo_atual

        commit_msg = f"docs: atualiza release notes via script - {data_hoje}"

        if sha_arquivo:
            repo.update_file(file_path, commit_msg, novo_conteudo_completo, sha_arquivo, branch = "teste-regras")
        else:
            repo.create_file(file_path, commit_msg, novo_conteudo_completo, branch = "teste-regras")

        
        print("✅ Sucesso! O GitHub Pages deve atualizar em instantes.")

    except Exception as e:
        print(f"❌ Falha ao publicar no GitHub: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso incorreto. Execute: python publish_release.py 'Texto da Release'")
    else:
        msg = sys.argv[1]
        publicar_no_pages(msg)