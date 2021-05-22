# MPEG-1 Coder: Estimação de Movimento

- https://github.com/brenoafb/video-compression

## Informações

**Versão Python:** 3.7.1

**Necessários os seguintes pacotes (versões utilizadas):** bitstring (3.1.7), Pillow (8.2.0), numpy (1.20.2)

## Execução

Será pedido para que seja informado o nome do arquivo ".yuv" de resolução CIQV a ser utilizado. Além disso, caso seja passado um argumento no momento da execução do programa (não importando o valor), devem ser indicados o valor da qualidade do jpeg e o delta a serem utilizados (default = 95 e 50, respectivamente).

**Exemplo1:**
  >python3 main.py

  >Informe o nome (caminho) do video YUV a ser codificado: "foreman_qcif.yuv"

**Exemplo2:**
  >python3 main.py ETC

  >Informe o nome (caminho) do video YUV a ser codificado: foreman_qcif.yuv

  >Informe a qualidade do Jpeg a ser utilizado: 65

  >Informe o tamanho da região de busca utilizada (ex: 50 para 25 pixels em cada direção): 50

## Resultado

O arquivo resultante da compressão é salvo no diretório local com o nome "video.vid". E o resultado após descompressão é mostrado frame a frame como última etapa da execução do algoritmo.

Os códigos utilizados para comparações e análises estão presentes no código "teste.py", gerado a partir de um codebook do Google Colab (https://colab.research.google.com/drive/1uTQyqHDka0SKU6Dl3QK8hFL291azWVQd?usp=sharing) para maior interessados. As linhas de código que fazem o salvamento das imagens dos resultados estão comentadas a fim de serem utilizadas somente caso seja a escolha do usuário.

## Fonte

Obs.: Vídeos YUV obtidos de
-  http://trace.eas.asu.edu/yuv/
