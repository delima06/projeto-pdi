import cv2
import numpy as np
import os

pasta_entrada = 'dataset_original'
pasta_saida = 'imagens_processadas'
cores_eva = ['verde', 'branco', 'azul']

tamanho_real_cm = 2.7 

for cor in cores_eva:
    os.makedirs(f"{pasta_saida}/{cor}", exist_ok=True)
    
    if not os.path.exists(f"{pasta_entrada}/{cor}"):
        continue
        
    arquivos = os.listdir(f"{pasta_entrada}/{cor}")
    
    for arquivo in arquivos:
        img = cv2.imread(f"{pasta_entrada}/{cor}/{arquivo}")
        
        
        if img is None: continue 
        
        altura, largura = img.shape[:2]
        if largura > altura:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
 
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, limiar = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY)
        
        contornos, _ = cv2.findContours(limiar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        moeda_encontrada = None
        
        for contorno in contornos:
            x, y, w, h = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if h == 0: continue
            
            proporcao = float(w) / h
            if 0.8 < proporcao < 1.2 and area > 500:
                moeda_encontrada = contorno
                largura_pixels = w
                break
                
        if moeda_encontrada is not None:
            escala_atual = largura_pixels / tamanho_real_cm
            fator_correcao = 100 / escala_atual 
            
            nova_largura = int(img.shape[1] * fator_correcao)
            nova_altura = int(img.shape[0] * fator_correcao)
            img_escala = cv2.resize(img, (nova_largura, nova_altura))
        else:
            img_escala = img
            

        cinza_cor = cv2.cvtColor(img_escala, cv2.COLOR_BGR2GRAY)
        

        _, mascara_branco = cv2.threshold(cinza_cor, 200, 255, cv2.THRESH_BINARY)
        
        b, g, r = cv2.split(img_escala)
        

        if cv2.countNonZero(mascara_branco) > 1000:

            media_b = cv2.mean(b, mask=mascara_branco)[0]
            media_g = cv2.mean(g, mask=mascara_branco)[0]
            media_r = cv2.mean(r, mask=mascara_branco)[0]
        else:
            media_b, media_g, media_r = np.mean(b), np.mean(g), np.mean(r)
            
        media_total = (media_b + media_g + media_r) / 3
        
        b_novo = cv2.convertScaleAbs(b, alpha=(media_total / (media_b + 0.001)))
        g_novo = cv2.convertScaleAbs(g, alpha=(media_total / (media_g + 0.001)))
        r_novo = cv2.convertScaleAbs(r, alpha=(media_total / (media_r + 0.001)))
        
        img_final = cv2.merge((b_novo, g_novo, r_novo))
        
        cv2.imwrite(f"{pasta_saida}/{cor}/proc_{arquivo}", img_final)
        print(f"Foto {arquivo} corrigida e processada!")