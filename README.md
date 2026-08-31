# rpg-2.1🌊🔥 ELEMENTARIA RPG

Um RPG 2D de exploração e combate por turnos ambientado no Reino de Elementaria.

Você é um jovem mago que precisa escolher seu elemento, explorar diversas ilhas, derrotar monstros, evoluir seus poderes, comprar equipamentos e conquistar as dez masmorras para finalmente enfrentar o Guardião de Elementaria: um poderoso dragão capaz de controlar todos os elementos.

🎮 Requisitos
Python 3.10 ou superior
Pygame

Instale o Pygame:

pip install pygame


Execute:

python main.py

🧙 Elementos

No início da aventura, o jogador deve escolher obrigatoriamente um elemento:

Elemento	Ataque 1	Ataque 2	Ataque 3
🔥 Fogo	Brasa	Bola de Fogo	Explosão de Fogo
💧 Água	Jato d'Água	Surfar	Hidro Bomba
⚡ Elétrico	Faísca	Raio	Trovoada
🌿 Planta	Chicote de Vinha	Folha Navalha	Bomba de Sementes
Ataques

Ataque 1

20–25 de dano
10–15 de mana

Ataque 2

30–40 de dano
15–25 de mana
Liberado no nível 2 do elemento

Ataque 3

45–55 de dano
30–45 de mana
Liberado no nível 4 do elemento

Ataque físico

Punho: 10 de dano
0 mana

Quando equipada a Espada de Ferro, o Punho passa a se chamar Espada e causa +20 de dano.

A cada turno, o jogador recupera entre 10 e 25 de mana.

📈 Nível do jogador

O jogador possui nível próprio de 1 a 20.

A cada nível:

+20 Vida máxima
+20 Mana máxima
⭐ Nível elemental

Cada elemento possui nível de 1 a 5.

Cada 100 XP elemental aumentam 1 nível.

O nível elemental também aumenta o dano elemental em +5.

❤️ Status inicial
Vida: 100
Mana: 100
Nível: 1
XP: 0
Moedas: 0
🛡️ Equipamentos
Item	Preço	Efeito
Armadura de Ferro	250	+10% defesa
Armadura de Escamas	350	+25% defesa
Cajado Arcano	150	+15 dano elemental
Espada de Ferro	200	+20 dano físico
Escudo Elemental	300	30% chance de esquiva

Cada item comprado aumenta o ataque dos monstros em 15.

🧪 Lojas

Todas as ilhas possuem uma loja.

Item	Preço	Efeito
Poção de Regeneração	15	Recupera 20–35 Vida
Poção de Mana	20	Recupera 20–35 Mana
🗺️ Ilhas
🌿 Ilha Inicial

Local onde o jogador começa.

Possui:

Árvores
Rios
Vegetação
Loja
Médico
Entrada da aventura
3 monstros de Planta

O médico restaura completamente Vida e Mana.

🔥 Ilha Vulcânica
Vulcões
Lava
Rochas
Cenário predominantemente vermelho
3 monstros de Fogo
💧 Ilha Aquática
Água
Corais
Peixes
Praias
Estruturas marítimas
3 monstros de Água
⚡ Ilha Eletrônica
Fábricas
Prédios
Cabos
Máquinas
Geradores
Iluminação elétrica
3 monstros Elétricos
🌑 Ilha Sombria
Casas abandonadas
Prédios abandonados
Ruas escuras
Névoa
3 monstros Sombrios
🪨 Ilha de Terra
Montanhas
Pedras
Desfiladeiros
Ambiente simples
3 monstros de Terra
🪽 Ilha Voadora
Ilhas suspensas
Construções voadoras
Pontes
Muitos pássaros
3 monstros Voadores
❄️ Ilha de Gelo
Gelo
Estacas congeladas
Iglus
Neve
3 monstros de Gelo
👻 Ilha Fantasmagórica
Prédios abandonados
Névoa
Fantasmas
Ambiente assustador
3 monstros Fantasmas
☠️ Ilha Venenosa
Vegetação
Áreas tóxicas
Cobras
Pântanos
3 monstros Venenosos
⚔️ Fraquezas e forças
Elemento	Fraqueza	Força
Fogo	Água	Planta
Água	Elétrico	Fogo
Planta	Fogo	Elétrico
Elétrico	Planta	Água
Sombrio	Nenhuma	Todos
Terra	Voador	Veneno
Voador	Gelo	Terra
Gelo	Fogo	Voador
Fantasma	Veneno	Água, Fogo, Planta e Elétrico
Veneno	Terra	Fantasma

Ataques contra a fraqueza do alvo causam dano aumentado.

Ataques contra elementos aos quais o alvo é resistente causam dano reduzido.

👹 Monstros

Os monstros possuem níveis de 1 a 5.

Nível 1
24–50 moedas
30–50 XP
Nível 2
45–75 moedas
45–50 XP
Nível 3
70–100 moedas
50–60 XP
Nível 4
100–125 moedas
55–65 XP
Nível 5
120–150 moedas
65–80 XP

Independentemente do nível do monstro, a experiência elemental recebida é de 10–35 XP.

O nível do monstro determina a quantidade de ataques elementais que ele pode utilizar.

Os monstros se movimentam pelo mapa e perseguem o jogador quando entram em sua área de detecção.

🏝️ Masmorras

Cada ilha possui uma masmorra correspondente.

Ao concluir uma masmorra:

O jogador recebe 45–60 moedas.
O jogador recebe 45–60 XP.
Recebe um pergaminho 📜 do elemento da masmorra.
A masmorra é marcada como concluída.

Quando todas as dez masmorras forem concluídas, o caminho para o chefe final é desbloqueado.

🏆 Missões
Primeiro Monstro

Derrote seu primeiro monstro.

Recompensa:

25 moedas
15 XP do jogador
Caçador de Monstros

Derrote 5 monstros diferentes.

Recompensa:

50 moedas
30 XP do jogador
Guardião de Elementaria

Derrote o chefe final.

Recompensa:

Vitória do jogo
🐉 Chefe Final

O chefe final é o Dragão Guardião de Elementaria.

Ele possui todos os elementos.

Fraqueza: Água
Força: todos os outros elementos

Para chegar à arena final, é necessário pagar:

150 moedas

Depois do pagamento começa a batalha final.

🎒 Inventário

O inventário mostra:

Moedas
Poções
Equipamentos
Pergaminhos
Elemento escolhido
Nível
XP
Nível elemental
Vida
Mana
🎮 Controles
WASD — movimentação
E — interagir
I — inventário
M — mapa
ESC — voltar/fechar menu
Mouse — menus e combate
🏗️ Gerando o EXE

Instale o PyInstaller:

pip install pyinstaller


Depois execute:

pyinstaller --onefile --windowed --name Elementaria main.py


O executável será criado em:

dist/Elementaria.exe

🎨 Gráficos

O projeto utiliza Pygame e desenha o mundo em tempo real.

A arquitetura foi preparada para posteriormente substituir os desenhos procedurais por:

Sprites de personagens
Sprites de monstros
Tilesets
Animações
Efeitos de partículas
Sons
Música
Efeitos elementais
📜 Objetivo

Escolha seu elemento.

Explore Elementaria.

Derrote monstros.

Evolua seu mago.

Colete moedas.

Compre equipamentos.

Conquiste todas as ilhas.

Colete os dez pergaminhos.

E enfrente o Dragão Guardião.

O destino de Elementaria está em suas mãos.
