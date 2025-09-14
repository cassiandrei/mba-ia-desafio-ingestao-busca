from search import search_prompt


def main():
    """
    Função principal que implementa um chat simples no terminal.
    Permite ao usuário fazer perguntas e receber respostas baseadas no contexto dos documentos.
    """
    print("=" * 50)
    print("Digite suas perguntas e receba respostas baseadas nos documentos.")
    print("Para sair, digite 'sair', 'quit' ou 'exit'.")
    print("-" * 50)
    print()

    while True:
        try:
            # Solicita pergunta do usuário
            pergunta = input("Faça sua pergunta: ").strip()

            # Verifica se o usuário quer sair
            if pergunta.lower() in ["sair", "quit", "exit", ""]:
                print("\n👋 Encerrando o chat. Até logo!")
                break

            # Busca a resposta usando o sistema de IA
            try:
                resposta = search_prompt(pergunta)
                print(f"RESPOSTA: {resposta}")

            except Exception as e:
                print(
                    f"ERRO: Não foi possível processar sua pergunta. Detalhes: {str(e)}"
                )
                print("Verifique se o banco de dados está configurado corretamente.")

            print("\n" + "-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\nChat interrompido!")
            break
        except EOFError:
            print("\n\nEncerrando o chat!")
            break


if __name__ == "__main__":
    main()
