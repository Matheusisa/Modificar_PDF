import fitz  # PyMuPDF

def listar_conteudo_pdf(input_pdf):
    # Abrir o arquivo PDF
    documento = fitz.open(input_pdf)
    conteudo = []

    # Iterar por todas as páginas do PDF
    for num_pagina in range(documento.page_count):
        pagina = documento.load_page(num_pagina)
        texto = pagina.get_text("text")
        conteudo.append(texto)

    return conteudo

def modificar_pdf(input_pdf, output_pdf, substituicoes):
    # Abrir o arquivo PDF existente
    documento = fitz.open(input_pdf)

    # Iterar por todas as páginas do PDF
    for num_pagina in range(documento.page_count):
        pagina = documento.load_page(num_pagina)

        # Substituir os parâmetros no conteúdo da página
        for old_text, new_text in substituicoes.items():
            areas = pagina.search_for(old_text)
            for area in areas:
                # Redigir o texto antigo
                pagina.add_redact_annot(area, fill=(1, 1, 1))
                pagina.apply_redactions()

                # Inicializar variáveis de fonte, tamanho e cor com valores padrão
                fonte = "helv"
                tamanho_fonte = 8
                cor = (0, 0, 0)

                # Identificar a fonte e o tamanho do texto original
                blocos = pagina.get_text("dict")["blocks"]
                for bloco in blocos:
                    if "lines" in bloco:
                        for linha in bloco["lines"]:
                            for span in linha["spans"]:
                                if old_text in span["text"]:
                                    fonte = span["font"]
                                    tamanho_fonte = span["size"]
                                    cor = span["color"]
                                    break

                # Ajustar o tamanho da fonte especificamente para a substituição desejada
                if old_text == 'Exemplo':#Exemplo de substituição na fonte exata em que o PDF se encontra
                    tamanho_fonte -= 8  # Diminuir o tamanho da fonte

                # Inserir o novo texto com a mesma fonte e tamanho, sem negrito
                pagina.insert_text(area.tl, new_text, fontsize=tamanho_fonte, fontname=fonte, color=cor, render_mode=0)

    # Salvar o PDF modificado
    documento.save(output_pdf)

# Exemplo de uso
input_pdf = 'Exemplo.pdf' #Caminho do PDF a ser modificado
output_pdf = 'Exemplo_PDF_modificado.pdf'#Caminho do PDF modificado
# Dicionário de substituições a serem feitas no PDF (chave: texto antigo, valor: novo texto)
substituicoes = {
    'Nome antigo': 'Novo nome',
    'Dados antigos': 'Dados novos',
    'Exemplo a ser substiuido': 'Exemplo que sera implementado no lugar do antigo'
}

# Listar conteúdo do PDF antes da modificação
conteudo_pdf = listar_conteudo_pdf(input_pdf)
for pagina_num, texto in enumerate(conteudo_pdf):
    print(f"Conteúdo antes da modificação - Página {pagina_num + 1}:\n{texto}\n")

# Modificar o PDF
modificar_pdf(input_pdf, output_pdf, substituicoes)

# Listar conteúdo do PDF depois da modificação
conteudo_pdf_modificado = listar_conteudo_pdf(output_pdf)
for pagina_num, texto in enumerate(conteudo_pdf_modificado):
    print(f"Conteúdo depois da modificação - Página {pagina_num + 1}:\n{texto}\n")