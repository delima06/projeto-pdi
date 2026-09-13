# modulo para calcular as metricas das imagens (pedro davi)
# calcula ruido do fundo, distorcao espacial da moeda e fidelidade de cor

import os
import cv2
import numpy as np
import pandas as pd

def extrair_metricas_imagem(caminho_imagem, cor_fundo, diametro_real_mm=27.0):
    # le a imagem original
    img = cv2.imread(caminho_imagem)
    if img is None:
        return None
    
    h, w = img.shape[:2]
    
    # 1. metrica de ruido no fundo (eva)
    # pegamos uma regiao de interesse (roi) central homogenea de 600x600 pixels longe de bordas e objetos
    centro_y, centro_x = h // 2, w // 2
    roi_tamanho = 300
    roi_eva = img[centro_y - roi_tamanho : centro_y + roi_tamanho, centro_x - roi_tamanho : centro_x + roi_tamanho]
    
    # desvio padrao no canal de cinza
    roi_cinza = cv2.cvtColor(roi_eva, cv2.COLOR_BGR2GRAY)
    ruido_std = float(np.std(roi_cinza))
    
    # snr local do fundo (media / desvio padrao)
    media_fundo = float(np.mean(roi_cinza))
    snr_fundo = float(media_fundo / (ruido_std + 1e-6))
    
    # psnr estimativo considerando sinal maximo de 255 e mse = ruido_std^2
    psnr_estimado = float(10.0 * np.log10((255.0 ** 2) / ((ruido_std ** 2) + 1e-6)))
    
    # 2. metrica de distorcao espacial e erro dimensional
    # detectar a moeda de 1 real na imagem
    # a moeda possui miolo escuro e borda de bronze com alto contraste em relacao ao fundo
    cinza_total = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mascara_escura = (cinza_total < 85).astype(np.uint8) * 255
    
    contornos, _ = cv2.findContours(mascara_escura, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    moeda_contorno = None
    melhor_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        # a moeda em 3000x4000 ocupa entre 10.000 e 35.000 pixels quadrados
        if 10000 < area < 35000:
            bx, by, bw, bh = cv2.boundingRect(c)
            proporcao = float(bw) / bh if bh > 0 else 0
            if 0.8 < proporcao < 1.25:
                if area > melhor_area:
                    melhor_area = area
                    moeda_contorno = c
                    
    if moeda_contorno is not None:
        (cx, cy), raio = cv2.minEnclosingCircle(moeda_contorno)
        diametro_px = float(2.0 * raio)
        bx, by, bw, bh = cv2.boundingRect(moeda_contorno)
        
        # razao de aspecto da moeda (o ideal do circulo eh 1.0)
        razao_aspecto = float(bw) / float(bh) if bh > 0 else 1.0
        distorcao_circularidade = abs(1.0 - razao_aspecto) * 100.0
        
        # centro do miolo prateado da moeda para medicao de cor
        mask_nucleo = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask_nucleo, (int(cx), int(cy)), int(raio * 0.50), 255, -1)
        
        # extrair cor lab do miolo
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_nucleo, a_nucleo, b_nucleo, _ = cv2.mean(img_lab, mask=mask_nucleo)
        
        # extrair bgr do miolo
        b_val, g_val, r_val, _ = cv2.mean(img, mask=mask_nucleo)
        
        moeda_encontrada = True
    else:
        # fallback caso falhe deteccao automatica
        diametro_px = np.nan
        distorcao_circularidade = np.nan
        l_nucleo, a_nucleo, b_nucleo = np.nan, np.nan, np.nan
        b_val, g_val, r_val = np.nan, np.nan, np.nan
        moeda_encontrada = False

    return {
        'arquivo': os.path.basename(caminho_imagem),
        'cor_fundo': cor_fundo,
        'ruido_std': ruido_std,
        'snr_fundo': snr_fundo,
        'psnr_estimado': psnr_estimado,
        'diametro_px': diametro_px,
        'distorcao_circularidade': distorcao_circularidade,
        'lab_l': l_nucleo,
        'lab_a': a_nucleo,
        'lab_b': b_nucleo,
        'bgr_b': b_val,
        'bgr_g': g_val,
        'bgr_r': r_val,
        'moeda_detectada': moeda_encontrada
    }

def processar_dataset_completo(pasta_dataset='dataset_original', pasta_saida='.'):
    # mapeia as pastas de cores existentes
    pastas_cores = {
        'azul': os.path.join(pasta_dataset, 'AZUL'),
        'branco': os.path.join(pasta_dataset, 'BRANCA'),
        'verde': os.path.join(pasta_dataset, 'VERDE')
    }
    
    dados = []
    
    print("iniciando extracao de metricas de todas as imagens...")
    for cor, pasta in pastas_cores.items():
        if not os.path.exists(pasta):
            print(f"aviso: pasta {pasta} nao encontrada")
            continue
            
        arquivos = sorted([f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f"processando fundo {cor} ({len(arquivos)} imagens)...")
        
        for arq in arquivos:
            caminho = os.path.join(pasta, arq)
            res = extrair_metricas_imagem(caminho, cor)
            if res is not None:
                dados.append(res)
                
    df = pd.DataFrame(dados)
    
    # calcular resolucao espacial media em pixels por mm (usando diametro real de 27.0 mm da moeda)
    media_diametro_global = df['diametro_px'].mean()
    escala_global_px_por_mm = media_diametro_global / 27.0
    
    # calcular o diametro medido em mm e o erro dimensional relativo (%)
    df['diametro_medido_mm'] = df['diametro_px'] / escala_global_px_por_mm
    df['erro_dimensional_relativo'] = np.abs(df['diametro_medido_mm'] - 27.0) / 27.0 * 100.0
    
    # calcular fidelidade de cor (delta e) tomando como referencia a media do miolo prateado de todas as amostras
    l_ref = df['lab_l'].mean()
    a_ref = df['lab_a'].mean()
    b_ref = df['lab_b'].mean()
    
    df['delta_e'] = np.sqrt(
        (df['lab_l'] - l_ref) ** 2 +
        (df['lab_a'] - a_ref) ** 2 +
        (df['lab_b'] - b_ref) ** 2
    )
    
    # salvar planilha csv com todas as metricas
    caminho_csv = os.path.join(pasta_saida, 'metricas_experimento.csv')
    df.to_csv(caminho_csv, index=False, float_format='%.4f')
    print(f"tabela de metricas salva com sucesso em: {caminho_csv}")
    print(f"total de fotos processadas: {len(df)}")
    
    return df

if __name__ == '__main__':
    processar_dataset_completo()
