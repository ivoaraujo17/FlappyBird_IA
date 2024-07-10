# Flappy Bird NEAT AI

Este repositório contém um jogo do Flappy Bird implementado usando Pygame, com a integração do algoritmo NEAT (NeuroEvolution of Augmenting Topologies) para treinar agentes de IA a jogar o jogo. O projeto demonstra como redes neurais podem evoluir para desempenhar bem em um ambiente de jogo ajustando seus pesos e estrutura ao longo das gerações.

## Visão Geral

O jogo simula o clássico Flappy Bird, onde o pássaro deve navegar através dos canos sem colidir com eles. O algoritmo NEAT é empregado para treinar múltiplos pássaros de IA a aprenderem a pular nos momentos certos para maximizar sua pontuação.

## Funcionalidades

- **Jogo Baseado em Pygame**: O jogo usa Pygame para renderização de gráficos e manipulação da lógica do jogo.
- **Algoritmo NEAT**: Utiliza o algoritmo NEAT para evoluir redes neurais para os pássaros de IA.
- **Obstáculos Dinâmicos**: Canos são gerados dinamicamente e se movem pela tela.
- **Avaliação de Fitness**: Os pássaros de IA são avaliados com base em sua habilidade de evitar os canos e sobreviver mais tempo.
- **Opção de Jogo Humano**: Inclui um modo onde o jogo pode ser jogado por um humano.

## Instalação

1. **Clone o Repositório**:
    ```sh
    git clone https://github.com/ivoaraujo17/flappy-bird-neat.git
    cd flappy-bird-neat
    ```

2. **Instale as Dependências**:
    Certifique-se de ter Python e Pygame instalados. Você pode instalar os pacotes necessários usando:
    ```sh
    pip install pygame neat-python
    ```

3. **Baixe as Imagens**:
    Coloque as seguintes imagens no diretório `imgs`:
    - `bg.png`: Imagem de fundo
    - `base.png`: Imagem do chão
    - `pipe.png`: Imagem do cano
    - `bird1.png`, `bird2.png`, `bird3.png`: Frames de animação do pássaro

## Uso

1. **Treinamento de IA**:
    Para treinar os pássaros de IA usando NEAT, retire o # da chamada da funcao run(config_path) e comente a main(None, None, False) e execute o seguinte comando:
    ```sh
    python main.py
    ```

2. **Jogo Humano**:
    Para jogar o jogo manualmente, modifique a chamada da função `main` no script `main.py` da seguinte forma:
    ```python
    main(None, None, False)
    ```
    Em seguida, execute o script:
    ```sh
    python main.py
    ```

## Mecânica do Jogo

- **Movimento do Pássaro**: O pássaro pula com uma velocidade fixa e cai devido à gravidade.
- **Canos**: Canos aparecem em alturas aleatórias e se movem da direita para a esquerda.
- **Detecção de Colisão**: O jogo detecta colisões entre o pássaro e os canos ou o chão.
- **Pontuação**: A pontuação aumenta conforme o pássaro passa com sucesso pelos canos.

## Configuração do NEAT

A configuração do NEAT é definida no arquivo `config.txt`. Parâmetros principais incluem:
- **Tamanho da População**: Número de pássaros de IA em cada geração.
- **Critérios de Fitness**: Determina como a aptidão de cada pássaro é calculada.
- **Taxas de Mutação**: Taxas nas quais as mutações ocorrem nas redes neurais.

## Estrutura de Arquivos

- `main.py`: Script principal que executa o jogo e lida com o treinamento da IA.
- `config.txt`: Arquivo de configuração para o algoritmo NEAT.
- `imgs/`: Diretório contendo os recursos de imagem.
- `README.md`: Este arquivo.

Sinta-se à vontade para contribuir com melhorias e novos recursos!
