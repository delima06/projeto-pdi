# metodo computacional de padronizacao de imagens
# feito por thiago (desenvolvedor pdi)
# usando apenas as tecnicas basicas das aulas de pdi do professor antonino
# leitura e escrita de imagens (aula 2)
# canais de cor split e merge (aula 2)
# limiarizacao simples por limiar estatico (aula 2)
# interpolacao e redimensionamento espacial (aula 4)
# operacoes matriciais e clip (aula 4)
# balanco de branco com referencia de altas luzes e gray world (aula 5 slide 53 e 54)

import os
import sys
import cv2
import numpy as np

# diametro real da moeda de 1 real em centimetros
diametro_real_cm = 2.7

# escala padrao que o professor pediu de 70 pixels por centimetro
escala_alvo_px_cm = 70.0

def achar_moeda_e_diametro(img):
    # converte a foto para escala de cinza conforme a aula 2
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # aplica a limiarizacao simples vista na aula 2
    # o miolo da moeda de 1 real eh bem escuro entao fica abaixo de 85
    mascara = (cinza < 85).astype(np.uint8) * 255
    
    h, w = cinza.shape
    
    # varredura em blocos para localizar a regiao com maior densidade de pixels escuros da moeda
    # sem usar funcoes avancadas de contornos de outras unidades
    passo = 80
    tamanho_bloco = 250
    melhor_bloco = None
    max_pixels = 0
    
    for y in range(0, h - tamanho_bloco, passo):
        for x in range(0, w - tamanho_bloco, passo):
            qtd = np.count_nonzero(mascara[y:y+tamanho_bloco, x:x+tamanho_bloco])
            if qtd > max_pixels:
                max_pixels = qtd
                melhor_bloco = (y, x)
                
    if melhor_bloco is None or max_pixels < 5000:
        return None, 0.0
        
    by, bx = melhor_bloco
    roi = mascara[by:by+tamanho_bloco, bx:bx+tamanho_bloco]
    ys, xs = np.where(roi == 255)
    cy_roi = int(np.mean(ys))
    cx_roi = int(np.mean(xs))
    
    # pega a regiao quadrada centrada no miolo da moeda
    y1 = max(0, by + cy_roi - 100)
    y2 = min(h, by + cy_roi + 100)
    x1 = max(0, bx + cx_roi - 100)
    x2 = min(w, bx + cx_roi + 100)
    
    roi_moeda = mascara[y1:y2, x1:x2]
    area = np.count_nonzero(roi_moeda == 255)
    
    # calcula o diametro aproximado pela formula basica da area do circulo
    # area = pi * r^2 entao diametro = 2 * raiz(area / pi)
    diametro_px = float(2.0 * np.sqrt(area / np.pi))
    centro = (x1 + cx_roi, y1 + cy_roi)
    
    return centro, diametro_px

def padronizar_imagem(caminho_ou_img, escala_alvo=70.0):
    # le a imagem caso venha uma string com o caminho do arquivo
    if isinstance(caminho_ou_img, str):
        img = cv2.imread(caminho_ou_img)
        if img is None:
            raise FileNotFoundError(f"nao deu para abrir a imagem: {caminho_ou_img}")
    else:
        img = caminho_ou_img.copy()
        
    h_orig, w_orig = img.shape[:2]
    
    # padroniza a orientacao se a foto foi tirada na horizontal
    if w_orig > h_orig:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
    h, w = img.shape[:2]
    
    # acha a moeda para calibrar a escala espacial de pixels por centimetro
    centro_moeda, diametro_px = achar_moeda_e_diametro(img)
    
    if diametro_px > 0:
        escala_detectada = diametro_px / diametro_real_cm
        fator_escala = escala_alvo / escala_detectada
        nova_w = int(round(w * fator_escala))
        nova_h = int(round(h * fator_escala))
        # redimensiona usando a interpolacao linear mostrada no slide 28 da aula 4
        img_redim = cv2.resize(img, (nova_w, nova_h), interpolation=cv2.INTER_LINEAR)
        sucesso_escala = True
    else:
        escala_detectada = None
        fator_escala = 1.0
        img_redim = img
        sucesso_escala = False
        
    # padronizacao cromatica usando o modelo gray/white balance da aula 5 (slides 53 e 54)
    # para evitar que fundos muito saturados (como verde e azul) tenham suas cores distorcidas
    # usamos a referencia dos pixels mais claros da cena (regua, reflexo difuso ou fundo branco)
    # obtidos por limiarizacao simples da aula 2 sem funcoes avancadas
    cinza_escala = cv2.cvtColor(img_redim, cv2.COLOR_BGR2GRAY)
    _, mascara_clara = cv2.threshold(cinza_escala, 185, 255, cv2.THRESH_BINARY)
    qtd_claros = np.count_nonzero(mascara_clara)
    
    b, g, r = cv2.split(img_redim)
    
    if qtd_claros > 1000:
        # calcula a media de cor nos pixels de referencia de alta luz da cena
        media_b = float(cv2.mean(b, mask=mascara_clara)[0])
        media_g = float(cv2.mean(g, mask=mascara_clara)[0])
        media_r = float(cv2.mean(r, mask=mascara_clara)[0])
    else:
        # fallback para a media global da cena (gray world do slide 56)
        media_b = float(np.mean(b))
        media_g = float(np.mean(g))
        media_r = float(np.mean(r))
        
    media_cinza = (media_b + media_g + media_r) / 3.0
    
    # calcula o fator multiplicativo para cada canal conforme slide 54 da aula 5
    k_b = media_cinza / (media_b + 1e-4)
    k_g = media_cinza / (media_g + 1e-4)
    k_r = media_cinza / (media_r + 1e-4)
    
    # multiplica cada canal pelo fator e usa clip de 0 a 255 da aula 4
    b_corrigido = np.clip(b * k_b, 0, 255).astype(np.uint8)
    g_corrigido = np.clip(g * k_g, 0, 255).astype(np.uint8)
    r_corrigido = np.clip(r * k_r, 0, 255).astype(np.uint8)
    
    # junta os canais de novo usando merge da aula 2
    img_padronizada = cv2.merge((b_corrigido, g_corrigido, r_corrigido))
    
    info = {
        'dimensao_original': (h_orig, w_orig),
        'dimensao_final': img_padronizada.shape[:2],
        'moeda_detectada': sucesso_escala,
        'diametro_px': diametro_px,
        'escala_detectada_px_cm': escala_detectada,
        'escala_alvo_px_cm': escala_alvo,
        'fator_escala': fator_escala
    }
    
    return img_padronizada, info

def processar_todas_as_fotos(pasta_origem='dataset_original', pasta_destino='imagens_processadas'):
    # mapeia as pastas das cores do experimento
    pastas = {
        'AZUL': 'azul',
        'BRANCA': 'branco',
        'VERDE': 'verde'
    }
    
    print("iniciando o processamento das fotos com as tecnicas das aulas...")
    total = 0
    sucessos = 0
    
    for pasta_in, pasta_out in pastas.items():
        caminho_in = os.path.join(pasta_origem, pasta_in)
        caminho_out = os.path.join(pasta_destino, pasta_out)
        os.makedirs(caminho_out, exist_ok=True)
        
        if not os.path.exists(caminho_in):
            print(f"pasta {caminho_in} nao existe, pulando")
            continue
            
        arquivos = sorted([f for f in os.listdir(caminho_in) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        for arq in arquivos:
            total += 1
            src = os.path.join(caminho_in, arq)
            dst = os.path.join(caminho_out, f"proc_{arq}")
            
            try:
                img_proc, info = padronizar_imagem(src, escala_alvo=escala_alvo_px_cm)
                cv2.imwrite(dst, img_proc)
                print(f"[{pasta_out}] {arq} -> salvo com sucesso (dimensao {info['dimensao_final'][1]}x{info['dimensao_final'][0]})")
                sucessos += 1
            except Exception as e:
                print(f"erro ao processar {arq}: {e}")
                
    print(f"\nfinalizado! {sucessos} de {total} imagens processadas com sucesso")

if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        caminho_teste = sys.argv[1]
        print(f"processando imagem individual: {caminho_teste}")
        img_saida, meta = padronizar_imagem(caminho_teste)
        cv2.imwrite("saida_padronizada.jpg", img_saida)
        print("imagem salva em saida_padronizada.jpg")
    else:
        processar_todas_as_fotos()
