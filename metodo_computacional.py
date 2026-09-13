"""
Método Computacional de Padronização de Imagens para PDI
Projeto: Avaliação Experimental das Condições de Aquisição em PDI

Função principal:
  padronizar_imagem(imagem_ou_caminho, escala_alvo_px_cm=70.0, diametro_real_cm=2.7)

Recebe uma imagem produzida sob o protocolo experimental proposto e produz:
  1. Correção automática de orientação (garante orientação vertical padronizada).
  2. Calibração e redimensionamento espacial métrico (relação fixa de pixels por unidade real: 70 px/cm).
  3. Padronização cromática (balanço de branco adaptativo gray-world baseado nas altas luzes).

Pode ser importado como módulo ou executado diretamente via terminal (CLI).
"""

import os
import sys
import argparse
import cv2
import numpy as np


def padronizar_imagem(entrada, escala_alvo_px_cm=70.0, diametro_real_cm=2.7):
    """
    Padroniza uma imagem quanto à escala espacial métrica e características de cor.

    Parâmetros:
      entrada: string com caminho da imagem OU array numpy (imagem BGR carregada).
      escala_alvo_px_cm: float, escala métrica final desejada em pixels por centímetro (padrão: 70.0 px/cm).
      diametro_real_cm: float, diâmetro real do objeto de referência em centímetros (padrão: 2.7 cm para moeda de 1 Real).

    Retorna:
      img_padronizada: imagem processada (array numpy BGR).
      info: dicionário com metadados do processamento (escala original, fator de escala, detecção).
    """
    if isinstance(entrada, str):
        if not os.path.exists(entrada):
            raise FileNotFoundError(f"Arquivo de imagem não encontrado: {entrada}")
        img = cv2.imread(entrada)
        if img is None:
            raise ValueError(f"Não foi possível decodificar a imagem: {entrada}")
    elif isinstance(entrada, np.ndarray):
        img = entrada.copy()
    else:
        raise TypeError("A entrada deve ser um caminho de arquivo (str) ou um array numpy.")

    h_orig, w_orig = img.shape[:2]
    rotacionada = False

    # 1. Padronização de Orientação
    if w_orig > h_orig:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        rotacionada = True

    h, w = img.shape[:2]

    # 2. Detecção do Objeto de Referência Métrico (Moeda de 1 Real)
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mascara_alvo = (cinza < 85).astype(np.uint8) * 255
    contornos, _ = cv2.findContours(mascara_alvo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    moeda_encontrada = None
    melhor_area = 0
    diametro_pixels = 0.0

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if 8000 < area < 40000:
            bx, by, bw, bh = cv2.boundingRect(contorno)
            if bh == 0:
                continue
            proporcao = float(bw) / bh
            if 0.80 < proporcao < 1.25 and area > melhor_area:
                melhor_area = area
                moeda_encontrada = contorno
                (_, _), raio = cv2.minEnclosingCircle(contorno)
                diametro_pixels = float(2.0 * raio)

    # 3. Calibração Espacial e Redimensionamento Métrico
    if moeda_encontrada is not None and diametro_pixels > 0:
        escala_detectada_px_cm = diametro_pixels / diametro_real_cm
        fator_correcao = escala_alvo_px_cm / escala_detectada_px_cm
        nova_largura = int(round(w * fator_correcao))
        nova_altura = int(round(h * fator_correcao))
        img_escala = cv2.resize(img, (nova_largura, nova_altura), interpolation=cv2.INTER_AREA)
        sucesso_escala = True
    else:
        escala_detectada_px_cm = None
        fator_correcao = 1.0
        img_escala = img
        sucesso_escala = False

    # 4. Padronização Cromática (Balanço de Branco Adaptativo Gray-World)
    cinza_escala = cv2.cvtColor(img_escala, cv2.COLOR_BGR2GRAY)
    limiar_branco = np.percentile(cinza_escala, 95)
    _, mascara_branco = cv2.threshold(cinza_escala, limiar_branco, 255, cv2.THRESH_BINARY)

    b, g, r = cv2.split(img_escala)
    media_b = cv2.mean(b, mask=mascara_branco)[0]
    media_g = cv2.mean(g, mask=mascara_branco)[0]
    media_r = cv2.mean(r, mask=mascara_branco)[0]
    media_total = (media_b + media_g + media_r) / 3.0

    b_padrao = cv2.convertScaleAbs(b, alpha=(media_total / (media_b + 1e-4)))
    g_padrao = cv2.convertScaleAbs(g, alpha=(media_total / (media_g + 1e-4)))
    r_padrao = cv2.convertScaleAbs(r, alpha=(media_total / (media_r + 1e-4)))

    img_padronizada = cv2.merge((b_padrao, g_padrao, r_padrao))

    info = {
        'dimensao_original': (h_orig, w_orig),
        'dimensao_final': img_padronizada.shape[:2],
        'rotacionada_90graus': rotacionada,
        'moeda_detectada': sucesso_escala,
        'diametro_pixels_detectado': diametro_pixels,
        'escala_detectada_px_cm': escala_detectada_px_cm,
        'escala_alvo_px_cm': escala_alvo_px_cm,
        'fator_redimensionamento': fator_correcao
    }

    return img_padronizada, info


def processar_lote(pasta_origem='dataset_original', pasta_destino='imagens_processadas', escala_alvo_px_cm=70.0):
    """Processa em lote todas as imagens organizadas por pastas de cores."""
    mapa_pastas = {'AZUL': 'azul', 'BRANCA': 'branco', 'VERDE': 'verde'}
    total = 0
    sucesso = 0

    print(f"Iniciando padronização em lote a partir de: {pasta_origem}")
    for pasta_in, pasta_out in mapa_pastas.items():
        caminho_in = os.path.join(pasta_origem, pasta_in)
        caminho_out = os.path.join(pasta_destino, pasta_out)
        os.makedirs(caminho_out, exist_ok=True)

        if not os.path.exists(caminho_in):
            continue

        arquivos = sorted([f for f in os.listdir(caminho_in) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        for arq in arquivos:
            total += 1
            src = os.path.join(caminho_in, arq)
            dst = os.path.join(caminho_out, f"proc_{arq}")
            try:
                img_proc, info = padronizar_imagem(src, escala_alvo_px_cm=escala_alvo_px_cm)
                cv2.imwrite(dst, img_proc)
                status_escala = "Escala OK" if info['moeda_detectada'] else "Sem calibração"
                print(f"[{pasta_out.upper()}] {arq} -> {os.path.basename(dst)} ({status_escala}, Res: {info['dimensao_final'][1]}x{info['dimensao_final'][0]})")
                sucesso += 1
            except Exception as e:
                print(f"Erro ao processar {arq}: {e}", file=sys.stderr)

    print(f"\nFinalizado! Total: {total}, Processadas com êxito: {sucesso}")


def main():
    parser = argparse.ArgumentParser(
        description="Método Computacional de Padronização de Imagens (Cor e Escala Espacial) - Projeto PDI"
    )
    parser.add_argument("-i", "--imagem", help="Caminho de uma imagem individual para padronizar.")
    parser.add_argument("-o", "--saida", help="Caminho do arquivo de saída (se -i for especificado).", default="imagem_padronizada.png")
    parser.add_argument("--lote", action="store_true", help="Processar todo o dataset experimental.")
    parser.add_argument("--dir-in", default="dataset_original", help="Diretório raiz com subpastas AZUL, BRANCA, VERDE.")
    parser.add_argument("--dir-out", default="imagens_processadas", help="Diretório de saída para lote.")
    parser.add_argument("--escala", type=float, default=70.0, help="Escala espacial padronizada em pixels/cm (padrão: 70.0).")

    args = parser.parse_args()

    if args.imagem:
        print(f"Processando imagem única: {args.imagem}...")
        img_out, meta = padronizar_imagem(args.imagem, escala_alvo_px_cm=args.escala)
        cv2.imwrite(args.saida, img_out)
        print(f"Imagem salva em: {args.saida}")
        print(f"Dimensão final: {meta['dimensao_final'][1]}x{meta['dimensao_final'][0]} px")
        print(f"Moeda detectada: {meta['moeda_detectada']} (Escala original: {meta['escala_detectada_px_cm']:.2f} px/cm -> Final: {meta['escala_alvo_px_cm']} px/cm)")
    else:
        processar_lote(pasta_origem=args.dir_in, pasta_destino=args.dir_out, escala_alvo_px_cm=args.escala)


if __name__ == "__main__":
    main()
