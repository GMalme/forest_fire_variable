<h2>Descrição da hipótese casual:</h2>

O experimento original descreve um inicio de fogo uniforme, o que provavelmente descreve uma chama forte vinda de outro ponto da floresta devido a sua força, meu exeprimento visa experimentar como seria o comportamento da chama inicial dependendo da intensidade da mesma e como ela interage com a floresta a depender da intensidade. a simulação desse comportamento é descrita alterando o tamanho da chama inicial pela variavel "start_fire", então é possivel alterar o fogo inicial de um fogo com tamanho 5 a um fogo padrão como descrito no experimento original de tamanho 100. Também foi adicionado uma variavel para alterar a probabilidade de uma arvore passar o fogo para outra, esse comportamento tem a inteção de simular diferentes tipos de florestas e dependendo da arvore o fogo se espalhara de forma diferente, este comportamento é feito utilizando a variavel "prob_fire" para aumentar ou diminuir a probabilidade da chama se espalhar.

<h2>Justificativa para as mudanças que você fez, em relação ao código original:</h2>

Eu adicionei uma nova variavel chamada "start_fire", que descreve o tamanho da chama inicial, podendo iniciar em uma chama de tamanho 5, para ter um comportamento aceitavel para probabilidades baixas de se espalhar, até um tamanho 10 que é o tamanho original do experimento, também foi adicionado a variavel "prob_fire" que descreve a probabilidade de uma arvore queimando passar as chamas para as vizinhas.

<h2>Orientação sobre como usar o simulador:</h2>

Basta instalar as dependencias do mesa e em um terminal com o python 10 instalado, executar o arquivo run.py para executar a interface iterativa ou batch_run.py para executar uma simulação que gerara um relatorio para os casos descritos na função batch_run no arquivo model.py.

<h2>Descrição das variáveis armazenada no arquivo CSV:</h2>

As variaveis são densisidade que descreve a densidade da floresta, prob_fire que descreve a probabilidade de uma arvore passar a chama para suas vizinhas, start_fire que indica o tamanho da chama inicial na floresta, as variaveis padrões altura e largura da floresta, e as variaveis para indicar se as arvores foram queimadas(Burned Out), Fine(não foi queimada) e está queimando(On fine).

<h2>Qualquer outra informação:</h2>

Foi utilizado a versão 3.9 do python neste projeto. 
