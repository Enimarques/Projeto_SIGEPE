from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from django.core.signing import TimestampSigner

def gerar_etiqueta_pdf(visita):
    """
    Gera uma etiqueta em PDF para a visita.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Configurações da etiqueta
    c.setFont("Helvetica", 12)
    
    # Desenha a etiqueta
    x = 1 * cm
    y = A4[1] - 2 * cm
    
    c.drawString(x, y, f"Visitante: {visita.visitante.nome_completo}")
    c.drawString(x, y - 20, f"Setor: {visita.setor.nome}")
    c.drawString(x, y - 40, f"Data/Hora: {visita.data_entrada.strftime('%d/%m/%Y %H:%M')}")
    c.drawString(x, y - 60, f"Objetivo: {visita.objetivo}")
    
    c.showPage()
    c.save()
    
    # Pega o valor do buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def generate_password_token(assessor_id):
    """
    Gera um token assinado para definição de senha do assessor.
    O token tem validade de 24 horas.
    """
    signer = TimestampSigner()
    return signer.sign(str(assessor_id))
