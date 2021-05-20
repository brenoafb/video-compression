# MPEG-1 Coder: Estimação de Movimento

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

O arquivo resultante da compressão é salvo no diretório local com o nome "video.vid".

Os códigos utilizados para comparações e análises estão presentes no codebook do Google Colab para maior interessados.