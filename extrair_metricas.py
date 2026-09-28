# modulo para extracao das metricas das imagens
# feito por pedro davi (analista de estatistica)
# usando as tecnicas basicas das aulas de pdi:
# ruido do sensor e dispersao (aula 1 e 2)
# relacao sinal-ruido snr (aula 2)
# resolucao espacial e erro dimensional (aula 3 e 4)
# diferenca de cor delta e cielab cie76 (aula 5 slide 59)

import os
import cv2
import numpy as np
import pandas as pd

# diametro real da moeda em milimetros (27 mm)
diametro_real_mm = 27.0

def extrair_metricas_imagem(caminho_imagem, cor_fundo):
    # le a foto colorida original usando opencv da aula 2
    img = cv2.imread(caminho_imagem)
    if img is None:
        return None
        
    h_orig, w_orig = img.shape[:2]
    
    # ajusta orientacao se estiver na horizontal
    if w_orig > h_orig:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
    h, w = img.shape[:2]
    
    # 1. medicao do ruido no fundo homogêneo de eva (aula 1 e 2)
    # pegamos uma regiao de interesse (roi) central de 600x600 pixels
    centro_y, centro_x = h // 2, w // 2
    raio_roi = 300
    roi_fundo = img[centro_y - raio_roi : centro_y + raio_roi, centro_x - raio_roi : centro_x + raio_roi]
    
    # converte para escala de cinza para medir a intensidade do sinal
    roi_cinza = cv2.cvtColor(roi_fundo, cv2.COLOR_BGR2GRAY)
    
    # calcula o desvio padrao sigma (ruido do sensor na aquisicao)
    ruido_std = float(np.std(roi_cinza))
    
    # media de brilho do fundo
    media_fundo = float(np.mean(roi_cinza))
    
    # snr local do fundo (razao sinal-ruido da aula 2: media dividida pelo desvio)
    snr_fundo = float(media_fundo / (ruido_std + 1e-6))
    
    # psnr considerando valor maximo de 8 bits (255)
    psnr_estimado = float(10.0 * np.log10((255.0 ** 2) / ((ruido_std ** 2) + 1e-6)))
    
    # 2. medicao dimensional da moeda com tecnicas basicas da aula 2 e 4
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mascara = (cinza < 85).astype(np.uint8) * 255
    
    # busca simples da regiao da moeda
    passo = 80
    tam_bloco = 250
    melhor_bloco = None
    max_pixels = 0
    
    for y in range(0, h - tam_bloco, passo):
        for x in range(0, w - tam_bloco, passo):
            qtd = np.count_nonzero(mascara[y:y+tam_bloco, x:x+tam_bloco])
            if qtd > max_pixels:
                max_pixels = qtd
                melhor_bloco = (y, x)
                
    if melhor_bloco is not None and max_pixels > 5000:
        by, bx = melhor_bloco
        roi_bloco = mascara[by:by+tam_bloco, bx:bx+tam_bloco]
        ys, xs = np.where(roi_bloco == 255)
        cy_roi = int(np.mean(ys))
        cx_roi = int(np.mean(xs))
        
        y1 = max(0, by + cy_roi - 100)
        y2 = min(h, by + cy_roi + 100)
        x1 = max(0, bx + cx_roi - 100)
        x2 = min(w, bx + cx_roi + 100)
        
        roi_moeda = mascara[y1:y2, x1:x2]
        area_moeda = np.count_nonzero(roi_moeda == 255)
        
        # diametro pela formula geometrica basica d = 2 * raiz(area / pi)
        diametro_px = float(2.0 * np.sqrt(area_moeda / np.pi))
        
        # centro absoluto da moeda
        centro_moeda_x = int(x1 + cx_roi)
        centro_moeda_y = int(y1 + cy_roi)
        
        # escala nominal aproximada do experimento a 45 cm (~60.5 px/cm -> 6.05 px/mm)
        # erro dimensional relativo percentual em relacao aos 27 mm nominais
        diametro_medido_mm = float(diametro_px / 6.02)
        erro_dimensional_relativo = float(abs(diametro_medido_mm - diametro_real_mm) / diametro_real_mm * 100.0)
        
        # 3. fidelidade de cor no centro do miolo metalico (cielab da aula 5 slide 59)
        # pega uma pequena regiao circular de raio 25 pixels no centro do miolo
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        miolo_lab = img_lab[centro_moeda_y - 25 : centro_moeda_y + 25, centro_moeda_x - 25 : centro_moeda_x + 25]
        miolo_bgr = img[centro_moeda_y - 25 : centro_moeda_y + 25, centro_moeda_x - 25 : centro_moeda_x + 25]
        
        lab_l = float(np.mean(miolo_lab[:, :, 0]))
        lab_a = float(np.mean(miolo_lab[:, :, 1]))
        lab_b = float(np.mean(miolo_lab[:, :, 2]))
        
        bgr_b = float(np.mean(miolo_bgr[:, :, 0]))
        bgr_g = float(np.mean(miolo_bgr[:, :, 1]))
        bgr_r = float(np.mean(miolo_bgr[:, :, 2]))
        
        moeda_ok = True
    else:
        diametro_px = np.nan
        diametro_medido_mm = np.nan
        erro_dimensional_relativo = np.nan
        lab_l, lab_a, lab_b = np.nan, np.nan, np.nan
        bgr_b, bgr_g, bgr_r = np.nan, np.nan, np.nan
        moeda_ok = False
        
    return {
        'arquivo': os.path.basename(caminho_imagem),
        'cor_fundo': cor_fundo,
        'ruido_std': ruido_std,
        'snr_fundo': snr_fundo,
        'psnr_estimado': psnr_estimado,
        'diametro_px': diametro_px,
        'diametro_medido_mm': diametro_medido_mm,
        'erro_dimensional_relativo': erro_dimensional_relativo,
        'lab_l': lab_l,
        'lab_a': lab_a,
        'lab_b': lab_b,
        'bgr_b': bgr_b,
        'bgr_g': bgr_g,
        'bgr_r': bgr_r,
        'moeda_detectada': moeda_ok
    }

def processar_dataset(pasta_raiz='dataset_original', arquivo_saida='metricas_experimento.csv'):
    pastas = {
        'AZUL': 'azul',
        'BRANCA': 'branco',
        'VERDE': 'verde'
    }
    
    linhas = []
    print("iniciando extracao de metricas com tecnicas de pdi...")
    
    for pasta_in, cor_nome in pastas.items():
        dir_cor = os.path.join(pasta_raiz, pasta_in)
        if not os.path.exists(dir_cor):
            print(f"aviso: pasta {dir_cor} nao existe")
            continue
            
        arquivos = sorted([f for f in os.listdir(dir_cor) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        for arq in arquivos:
            caminho_completo = os.path.join(dir_cor, arq)
            res = extrair_metricas_imagem(caminho_completo, cor_nome)
            if res is not None:
                linhas.append(res)
                print(f"[{cor_nome}] {arq}: ruido={res['ruido_std']:.2f}, snr={res['snr_fundo']:.2f}, diam={res['diametro_px']:.1f}px")
                
    df = pd.DataFrame(linhas)
    
    # calcula a distancia euclidiana de cor delta e cie76 da aula 5 (slide 59)
    # delta e = raiz((l - l_ref)^2 + (a - a_ref)^2 + (b - b_ref)^2)
    # usamos a media de todas as fotos como referencia de cor neutra
    l_ref = df['lab_l'].mean()
    a_ref = df['lab_a'].mean()
    b_ref = df['lab_b'].mean()
    
    df['delta_e'] = np.sqrt(
        (df['lab_l'] - l_ref) ** 2 +
        (df['lab_a'] - a_ref) ** 2 +
        (df['lab_b'] - b_ref) ** 2
    )
    
    df.to_csv(arquivo_saida, index=False)
    print(f"\nconcluido! {len(df)} amostras salvas em {arquivo_saida}")
    return df

if __name__ == '__main__':
    processar_dataset()
