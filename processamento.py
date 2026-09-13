# script de processamento e padronizacao das imagens
# corrigido e integrado com deteccao robusta da moeda e calibracao espacial

import os
import cv2
import numpy as np

pasta_entrada = 'dataset_original'
pasta_saida = 'imagens_processadas'

# mapeamento dos nomes das pastas do dataset original
mapa_cores = {
    'AZUL': 'azul',
    'BRANCA': 'branco',
    'VERDE': 'verde'
}

# diametro real da moeda de 1 real em centimetros (27 mm = 2.7 cm)
tamanho_real_cm = 2.7 

print("iniciando script de processamento de imagens...")

for pasta_cor, cor_saida in mapa_cores.items():
    caminho_dir = os.path.join(pasta_entrada, pasta_cor)
    dir_destino = os.path.join(pasta_saida, cor_saida)
    os.makedirs(dir_destino, exist_ok=True)
    
    if not os.path.exists(caminho_dir):
        print(f"aviso: diretorio {caminho_dir} nao existe, pulando...")
        continue
        
    arquivos = sorted([f for f in os.listdir(caminho_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    for arquivo in arquivos:
        caminho_img = os.path.join(caminho_dir, arquivo)
        img = cv2.imread(caminho_img)
        
        if img is None:
            continue
            
        altura, largura = img.shape[:2]
        
        # se tiver em orientacao horizontal, rotaciona para vertical
        if largura > altura:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            altura, largura = img.shape[:2]
            
        # deteccao robusta da moeda de 1 real (alvo com nucleo escuro na imagem)
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mascara_alvo = (cinza < 85).astype(np.uint8) * 255
        
        contornos, _ = cv2.findContours(mascara_alvo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        moeda_encontrada = None
        melhor_area = 0
        diametro_pixels = 0
        
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if 10000 < area < 35000:
                bx, by, bw, bh = cv2.boundingRect(contorno)
                if bh == 0:
                    continue
                proporcao = float(bw) / bh
                if 0.8 < proporcao < 1.25 and area > melhor_area:
                    melhor_area = area
                    moeda_encontrada = contorno
                    # pega o diametro do menor circulo circunscrito
                    (_, _), raio = cv2.minEnclosingCircle(contorno)
                    diametro_pixels = 2.0 * raio
                    
        # se detectou a moeda, faz o reescalonamento espacial padrao (ex: 100 px por cm)
        if moeda_encontrada is not None and diametro_pixels > 0:
            escala_atual = diametro_pixels / tamanho_real_cm
            escala_alvo_px_por_cm = 70.0 # padrao de resolucao uniforme
            fator_correcao = escala_alvo_px_por_cm / escala_atual
            
            nova_largura = int(img.shape[1] * fator_correcao)
            nova_altura = int(img.shape[0] * fator_correcao)
            img_escala = cv2.resize(img, (nova_largura, nova_altura), interpolation=cv2.INTER_AREA)
        else:
            img_escala = img
            
        # padronizacao e balanco de branco (gray-world balanceado)
        cinza_escala = cv2.cvtColor(img_escala, cv2.COLOR_BGR2GRAY)
        limiar_adaptativo = np.percentile(cinza_escala, 95)
        _, mascara_branco = cv2.threshold(cinza_escala, limiar_adaptativo, 255, cv2.THRESH_BINARY)
        
        b, g, r = cv2.split(img_escala)
        media_b = cv2.mean(b, mask=mascara_branco)[0]
        media_g = cv2.mean(g, mask=mascara_branco)[0]
        media_r = cv2.mean(r, mask=mascara_branco)[0]
        media_total = (media_b + media_g + media_r) / 3.0
        
        b_novo = cv2.convertScaleAbs(b, alpha=(media_total / (media_b + 0.001)))
        g_novo = cv2.convertScaleAbs(g, alpha=(media_total / (media_g + 0.001)))
        r_novo = cv2.convertScaleAbs(r, alpha=(media_total / (media_r + 0.001)))
        
        img_final = cv2.merge((b_novo, g_novo, r_novo))
        
        caminho_out = os.path.join(dir_destino, f"proc_{arquivo}")
        cv2.imwrite(caminho_out, img_final)
        print(f"foto {arquivo} [{cor_saida}] corrigida e processada com sucesso!")

print("processamento concluido com sucesso!")