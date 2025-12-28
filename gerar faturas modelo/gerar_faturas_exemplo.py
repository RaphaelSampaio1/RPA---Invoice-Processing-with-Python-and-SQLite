from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import date

def desenhar_fatura(c, dados):
    largura, altura = A4

    # Cabeçalho - Dados da empresa emissora
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, altura - 30 * mm, dados["empresa_nome"])

    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, altura - 36 * mm, f"NIF: {dados['empresa_nif']}")
    c.drawString(30 * mm, altura - 42 * mm, dados["empresa_endereco"])

    # Título Fatura + Número
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(largura - 30 * mm, altura - 30 * mm, "FATURA")

    c.setFont("Helvetica", 10)
    c.drawRightString(largura - 30 * mm, altura - 36 * mm, f"Nº: {dados['numero_fatura']}")
    c.drawRightString(largura - 30 * mm, altura - 42 * mm, f"Data emissão: {dados['data_emissao']}")
    c.drawRightString(largura - 30 * mm, altura - 48 * mm, f"Vencimento: {dados['data_vencimento']}")

    # Dados do cliente
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30 * mm, altura - 60 * mm, "Cliente:")

    c.setFont("Helvetica", 10)
    c.drawString(30 * mm, altura - 66 * mm, dados["cliente_nome"])
    c.drawString(30 * mm, altura - 72 * mm, f"NIF: {dados['cliente_nif']}")
    c.drawString(30 * mm, altura - 78 * mm, dados["cliente_endereco"])

    # Tabela de itens
    y_itens = altura - 95 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(30 * mm, y_itens, "Descrição")
    c.drawRightString(140 * mm, y_itens, "Qtd")
    c.drawRightString(165 * mm, y_itens, "Preço")
    c.drawRightString(190 * mm, y_itens, "Total")

    c.line(25 * mm, y_itens - 2 * mm, 195 * mm, y_itens - 2 * mm)

    c.setFont("Helvetica", 10)
    y_itens -= 10 * mm
    total = 0

    for item in dados["itens"]:
        descricao = item["descricao"]
        qtd = item["quantidade"]
        preco = item["preco_unitario"]
        subtotal = qtd * preco
        total += subtotal

        c.drawString(30 * mm, y_itens, descricao[:60])
        c.drawRightString(140 * mm, y_itens, f"{qtd}")
        c.drawRightString(165 * mm, y_itens, f"{preco:.2f} €")
        c.drawRightString(190 * mm, y_itens, f"{subtotal:.2f} €")

        y_itens -= 7 * mm

    # Totais
    y_totais = y_itens - 10 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(165 * mm, y_totais, "Total:")
    c.drawRightString(190 * mm, y_totais, f"{total:.2f} €")

    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawString(30 * mm, 20 * mm, "Condições de pagamento: 30 dias.")
    c.drawString(30 * mm, 15 * mm, "Este é um documento gerado automaticamente para fins de teste.")

def gerar_faturas():
    faturas = [
        {
            "arquivo": r"C:\Users\WIN11\Documents\1. RPA\Python\projects\Lancamento de Faturas\faturas\fatura_001.pdf",
            "empresa_nome": "Tech Solutions Lda.",
            "empresa_nif": "PT500000001",
            "empresa_endereco": "Av. da Liberdade 1000, Lisboa, Portugal",
            "numero_fatura": "2025-001",
            "data_emissao": "2025-01-05",
            "data_vencimento": "2025-02-04",
            "cliente_nome": "Loja Online XYZ Lda.",
            "cliente_nif": "PT509999991",
            "cliente_endereco": "Rua das Flores 50, Porto, Portugal",
            "itens": [
                {"descricao": "Serviço de hospedagem cloud - Janeiro/2025", "quantidade": 1, "preco_unitario": 120.00},
                {"descricao": "Suporte técnico premium", "quantidade": 1, "preco_unitario": 80.00},
            ],
        },
        {
            "arquivo": r"C:\Users\WIN11\Documents\1. RPA\Python\projects\Lancamento de Faturas\faturas\fatura_002.pdf",
            "empresa_nome": "Energy Plus S.A.",
            "empresa_nif": "PT500000002",
            "empresa_endereco": "Rua da Energia 200, Lisboa, Portugal",
            "numero_fatura": "2025-1023",
            "data_emissao": "2025-01-10",
            "data_vencimento": "2025-01-25",
            "cliente_nome": "Indústria Alfa S.A.",
            "cliente_nif": "PT501111111",
            "cliente_endereco": "Zona Industrial, Lote 12, Braga, Portugal",
            "itens": [
                {"descricao": "Consumo de energia elétrica - Dez/2024", "quantidade": 1, "preco_unitario": 945.32},
                {"descricao": "Taxa de potência contratada", "quantidade": 1, "preco_unitario": 54.68},
            ],
        },
        {
            "arquivo": r"C:\Users\WIN11\Documents\1. RPA\Python\projects\Lancamento de Faturas\faturas\fatura_003.pdf",
            "empresa_nome": "Office Supply Europa",
            "empresa_nif": "PT500000003",
            "empresa_endereco": "Rua dos Escritórios 10, Coimbra, Portugal",
            "numero_fatura": "2025-775",
            "data_emissao": "2025-01-15",
            "data_vencimento": "2025-02-14",
            "cliente_nome": "Banco Projeto RPA S.A.",
            "cliente_nif": "PT502222222",
            "cliente_endereco": "Av. Central 500, Lisboa, Portugal",
            "itens": [
                {"descricao": "Papel A4 - Caixa 5 resmas", "quantidade": 3, "preco_unitario": 14.90},
                {"descricao": "Tinteiro impressora HP", "quantidade": 4, "preco_unitario": 35.50},
                {"descricao": "Cadeiras ergonômicas", "quantidade": 2, "preco_unitario": 189.99},
            ],
        },
    ]

    for f in faturas:
        c = canvas.Canvas(f["arquivo"], pagesize=A4)
        desenhar_fatura(c, f)
        c.showPage()
        c.save()
        print(f"Fatura gerada: {f['arquivo']}")

if __name__ == "__main__":
    gerar_faturas()