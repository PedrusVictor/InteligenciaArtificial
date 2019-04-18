

import pandas as pd;

import matplotlib.pyplot as plt;


dataset=pd.read_csv("Classificacao_Q3.csv");
colunas=["Genero", "Idade", "Escolaridade","Profissao"];#criando variavel para guardar valor das colunas
#vai ser usado em conjunto com estrutura de loop para percorrer o dataset
campos=[list(dataset[a].unique()) for a in colunas];#pegando os valores/campos unicos de cada coluna

tamTeste=900;#variavel para tamanho do vetor de teste. 900 tamanho inicial do vetor de teste
tamTreinamento=100;# variavel para tamanho do vetor de treinamento. 100 tamanho inicial do vetor de treinamento
AcertoClassif={"Treinamento/Teste":[],"TxMin":[],"TxMedia":[],"TxMax":[],"TxClasse0":[],"TxClasse1":[]};
#dicionário para armazenar os valores,taxas que serão usados em gráfico e etc

#função para calcular as taxas que serão usadas pelo classificador de classes naivebayes
#o resultado da função retorna um dicionário contendo as taxas
#
def calcular(teste):
    #criando dicinário para guardar os valores calculados das taxas
    dic={}
    #dividindo dados de teste em classe 0 e 1
    target0=teste.loc[teste["Target"]==0];
    target1=teste.loc[teste["Target"]==1];
    
    #guardando tamanho para cada classe
    tamTarg0=target0.shape[0];
    tamTarg1=target1.shape[0];
    
    #preenchendo o dicionário com os valores de cada classe
    #os elementos do dicionário usam tupla para poder haver uma diferenciação entre as classes
    #index = indice, a igual ao valor, elemento da coluna
    for index, a in enumerate(colunas):
        aux=list(target0[a]);
        aux2=list(target1[a]);
        for b in campos[index]:
            dic[0,b]=(aux.count(b))/tamTarg0;
            dic[1,b]=(aux2.count(b))/tamTarg1;
    
    dic[0]=tamTarg0/tamTeste;#adicionando ao dicionário a taxa da classe 0
    dic[1]=tamTarg1/tamTeste;#adicionando ao dicionário a taxa da classe 1
    #dic[0] seria a quantidade de elementos da classe 0/ tamanho de elementos de teste
    #dic[1] seria a quantidade de elementos da classe 1/ tamanho de elementos de teste
    return dic;#retornando dicionário com todas as taaxas   

#função para classificar se é da classe 0 ou 1
def classificar( treinamento,dic):
    
    #lista que guardará os resultados, ou valores correspondentes a classe 0  e 1
    resultado=[];
    #fazendo o calculo da classe 0. Para isso multiplica as taxas da lista "valores" e multiplica
    #por quantidade de elementos da classe 0 no vetor de teste/ pelo total de elementos
    #no final fica um único valor que é resultado da multiplicação no indice 0.
    resultado.append((dic[0,(treinamento[0])]*dic[0,(treinamento[1])]*dic[0,(treinamento[2])]*dic[0,(treinamento[3])]*dic[0]));
    
    #fazendo o calculo da classe 1. Para isso multiplica as taxas da lista "valores" e multiplica
    #por quantidade de elementos da classe 1 no vetor de teste/ pelo total de elementos
     #no final fica um único valor que é resultado da multiplicação no indice 1.
    resultado.append((dic[1,(treinamento[0])]*dic[1,(treinamento[1])]*dic[1,(treinamento[2])]*dic[1,(treinamento[3])]*dic[1]));
    
 
 
   # print(resultado)
    return resultado.index(max(resultado));#imprimindo o indice do maior valor da lista resultado
#loop que continuará enquanto as proporções não forem 900/100(treinamento/teste)
while(tamTreinamento<=900 and tamTeste>=100):
    print("Calculando para proporção %r / %r"%((tamTreinamento/10),(tamTeste/10)));
    
    acertosclasse0=0;#variavel aux para contar os acertos da classe 0
    acertosclasse1=0;#variavel aux para contar os acertos da classe 1
    acertototal=0;#variavel aux para contar acerto total
    minAcerto=10000;#variavel que guardará o valor min de acerto para cada proporção. é atualizada após cada rodada
    maxAcerto=0;#variavel para armazenar a quantidade máxima de acerto para cada proporção. é atualizada após cada rodada

    for x in range(0,30):
        somaAcerto=0;#variavel temp que somará o número de acertos de cada rodada, e ao final de cada rodada, é utilizada
        #pelo minAcerto, maxAcerto e acertototal
        #variavel para armazenar o dataset embaralhado
        datEmb= dataset.sample(frac=1);
        dictaxas=calcular(datEmb[:tamTeste]);
        #print(classificar(dataset[0:948],dataset.values[948]));
        #for para iterar pelo vetor de treinamento e utilizar o classificador
        #[tamTeste:] cria uma lista que começa a partir do fim do vetor de teste. depois do ultimo elemento
        for a in datEmb.values[tamTeste:]:
            if(classificar(a,dictaxas)==a[4]):
                somaAcerto+=1;#se o resultado da classificação for igual ao do vetor de treinamento
                #incrementa a variavel somaAcerto
                if(a[4]==1):
                    acertosclasse1+=1;#incrementa a variavel caso o resultado seja da classe 1
                elif(a[4]==0):
                    acertosclasse0+=1;#incrementa a variavel caso o resultado seja da classe 0
           

        #verificando se o valor de somaAerto é maior do que o maior valor atual
        if(somaAcerto>maxAcerto):
            maxAcerto=somaAcerto;#caso seja, o valor de somaAcerto é atribuido a maxAcerto

        #verificando se o valor de somaAcerto é menor do que o menor valor atual
        if(somaAcerto<minAcerto):
            minAcerto=somaAcerto;#caso seja, o valor de somaAcerto é atribuido a minAcerto

        acertototal+=somaAcerto;#incrementando acertotal com valor de somaAcerto
        
    #adiconando os valores de cada proporção ao campo correspondente no dicionário AcertoClassif
    #ao mesmo tempo que adiciona, calcula os valores das taxas, transforma em porcentagem
    AcertoClassif["Treinamento/Teste"].insert(0,str(tamTreinamento/10)+" / "+str(tamTeste/10));
    AcertoClassif["TxMin"].insert(0,minAcerto/tamTreinamento);
    AcertoClassif["TxMedia"].insert(0,acertototal/(tamTreinamento*30));
    AcertoClassif["TxMax"].insert(0,maxAcerto/tamTreinamento);
    AcertoClassif["TxClasse0"].insert(0,acertosclasse0/(acertototal));
    AcertoClassif["TxClasse1"].insert(0,acertosclasse1/(acertototal));

    tamTeste-=100;#reduzindo em 100  tamanho do vetor de teste
    tamTreinamento+=100;#incrementando em 100 o tamanho do vetor de treinamento

#criando um dataframe com os valores do dicionário. Isso é só para ficar mais organizado
#na hora de mostrar os resultados de cada proporção
tabelaTx = pd.DataFrame(AcertoClassif, columns=["Treinamento/Teste","TxMin","TxMedia","TxMax","TxClasse0","TxClasse1"]);

#printando o resultado da classificação
print(tabelaTx)

#plotando gráfico com as taxas de acerto por proporção

plt.figure();
plt.title("Taxas de acerto por proporção");
plt.grid();
plt.plot(AcertoClassif["Treinamento/Teste"][::-1],AcertoClassif["TxMedia"])[::-1];
plt.xlabel("Proporção  Treinamento / Teste");
plt.ylabel("Taxa de acerto");
plt.show();





