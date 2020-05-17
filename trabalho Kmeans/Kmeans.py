#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import math;
import matplotlib.pyplot as plt;


#variavel "centroides" guardará o arquivo dos centroides.
#abrindo o arquivo csv utilizando o pandas
centroides=pd.read_csv("agrup_centroides_Q1.csv")
#aqui é feita uma pequena "limpeza dos dados" para remover alguns elementos que nao serão necessários;
#neste caso, será removida a coluna "Unnamed: 0" que é uma coluna dos indices do centroides
centroides=centroides.drop("Unnamed: 0",axis=1)
#o comando "drop", do pandas, serve para remover algum tipo de elemento, e utilizando o drop(nome da coluna, axis=1)
#digo para remover somente os elementos da coluna passada como parâmetro

#abrindo o arquivo csv que contem as instancias que serão classificadas pelo Kmeans
agrupamento=pd.read_csv("agrupamento_Q1.csv")
#criando uma variavel para armazenar o tamanho, a quantidade de linhas do arquivo que contém as instancias
#isso foi feito para não precisar ficar chamando a função de contagem de linhas direto, assim, diminuindo a quantidade de processos
#desnecessários
tamAgr=len(agrupamento.values)


#função para calcular a distância euclidiana entre dois elementos passados
#nesse caso, ele calcula a distância entre um centroide e uma instância(elementos) passado como parâmetro

def CalcDistancia(p1,p2):
    #retorna a distância euclidiana
    #para esse calculo foi utilizado a função zip para juntar centroide e instancia numa única lista
    #dessa forma, por exemplo se usarmos instancia=[1,2,3]e centroide[4,5,6]
    #eles ficariam assim depois de usarmos o "zip":[[1,4],[2,5],[3,6]]
    #os elementos ficariam juntos e mais facil de trabalhar enquanto se faz a iteração
    
    #depois de criar uma lista com os elementos do centroide e da instancia, criamos uma lista
    #que contém as diferenças entre os pontos do centroide e instancia ao quadrado
    #isso é feito para que depois seja possível somar cada elemento da lista utilizando a função sum()
    #para que em seguida possamos utilizar a raiz quadrada e a assim podermos retornar a distância euclidiana
    #esse calculo feito abaixo representa isso:
    #math.sqrt(pow(p2x1-p1x1,2)+pow(p2x2-p1x2,2)+pow(p2x3-p1x3,2)+pow(p2x4-p1x4,2))
    return math.sqrt(sum([pow(a[1]-a[0],2) for a in list(zip(p1,p2))]))

#classe para armazenar os resultados dos Kmeans para cada K centroides
class KmeansStoreData():
    #metodo construtor dessa classe
    def __init__(self):
        self.centroids=[];#lista para armazenar os centroides finais(posições finais dos centroides)
        self.DistMedias=[];#lista para armazenar as distâncias medias
        self.Kideal=-1;
        
#metodo para adicionar as informações para cada K
#centrs seriam os centroides finais para determinado K
#DistM seria a distância media das instâncias para o centroide num determinado k
    def AddK(self,centrs,DistM):
        self.centroids.append(centrs);#adicionando centroides de determinado K a lista
        self.DistMedias.append(DistM);#adicionando distancia media de determinado k A lista

#função que calcula a nova posição do centroide a partir das posições de suas instancias
def CalcCentroides(agrup):
    tamGrup=len(agrup);#pegando tamanho, quantidade de elementos próximos, que fazem parte do centroide
    if(tamGrup>0):
        novoCentr=[0]*4;#criando uma lista de quatro elementos para servir de acumulador
        #os elementos dessa lista representarão cada elemento do centroide novo(x1,x2,x3,x4)
        #cada elemento começa como sendo 0 para guardar a somatoria dos elementos das intancias
        #para que depois possa usar esse somatoria para calcular a media e assim conseguir o novo centroide
        
        #loop que vai iterar entre as instancias do centroide e o segundo loop para para percorrer(x1,x2,x3,x4) e somar
        #esse valores das instancias ao do novo centroide

        for a in agrup:
            for ind in range(0,4):
                novoCentr[ind]+=a[ind];


        return [a/tamGrup for a in novoCentr];
        #retornando uma lista com a divisão de cada x acumulado pela quantidade de instancias do centroide
        #pega a media de x1,x2,x3,x4 acumulado (pega a media dos valores) e retornar numa lista contendo x1,x2,x3,x4 do novo centroide
    
    return [];#precaução para caso não tiver elementos no centroide, ele retornar uma lista vazia

#função do metodo de elbow
def Elbow():
    DataKmeans=KmeansStoreData();#criando um objeto para guardar as informações dos centroides para cada valor de k
    #for que vai de 2 a 12. esse for vai atribuir o valor de k na chamada de função do kmeans que por sua vez vai retornar
    #as informações referentes àquele valor de k
    for k in range(2,13):
        ValoresParaK= KMeans(k);#guardando o valor para k centroides numa variavel aux
        DataKmeans.AddK(ValoresParaK[0],ValoresParaK[1]);
        #armazenando as informações de k no objeto que guarda todas as informações do método de elbows
    #printando as medias    
    for indice in range(0,len(DataKmeans.DistMedias)):
        print("Media/variância para %r clusters:%r\n\n"%((indice+2),DataKmeans.DistMedias[indice]));
        
    
    #printando centroides do k Ideal
    print("k ideal : 5");
    print("Posição final dos centroides do k Ideal:");
    for x in DataKmeans.centroids[3]:
        print("%r\n\n"%(x));
    
    print(DataKmeans.centroids[3]);
    
    #plotando gráfico de elbows
    plt.figure();
    plt.title("gráfico do Método de Elbow/cotovelo");
    plt.grid();
    plt.plot(list(range(2,13)),DataKmeans.DistMedias);
    plt.plot(5,DataKmeans.DistMedias[3],'ro');
    plt.xlabel("K clusters");
    plt.ylabel("Variância");
    
    plt.annotate("K Ideal", xy=(5.3,DataKmeans.DistMedias[3]),xytext=(6,0.6),arrowprops=dict(facecolor='black',shrink=0.05));
    plt.show();

    
def KMeans(k):
    
    centros=[list(a) for a in centroides.values[:k]];#k clusters. se inicia com os k clusters do arquivo centroide
    somaDistAux=0;
    #print(centros)
    listCentTrein=[-1]*tamAgr;#lista que guardará o id do cluster de cada instância
    
    print("--Executando Kmeans para %r clusters--"%(k));
    
   
    cont=0;#contador de etapas para estabilizar. Vai contar quantas loops foram necessários até estabilizar
    while True:
        cont+=1;#incrementando contador
        #lista para guardar as classificações atuais
        listAuxC=[];
        somaDistAux=0;#variavel que guarda as somas das distâncias
        agrupamC=[[] for x in range(0,k)];
        #lista que guardará as informações de cada centroid para depois poder calcular novos centroides
        
        #loop para percorrer todas as instâncias
        for a in range(0,tamAgr):
            distancias=[];#lista de distâncias de tal instancias para cada cluster/centroide
            
            #loop que percorre todos os centroides para que assim possa ser feito o calculo da distância para todos os centroides

            for cent in centros:
                distancias.append(CalcDistancia(agrupamento.values[a],cent));
                
                #fim do loop dos centroides

            idCentro=distancias.index(min(distancias));#pegando o id do centroide com menor distância
            listAuxC.append(idCentro);#adicionando a lista, na posição da instância, o numero do cluster
            #listCentTrein[a]=idCentro
            somaDistAux+=(distancias[idCentro]);#incrementando a soma de distâncias com a dist para o cluster
            agrupamC[idCentro].append(agrupamento.values[a]);
            

        nCentroids=[CalcCentroides(agrupamC[x]) for x in range(0,k)]
        #print([listCentTrein.count(y) for y in range(0,k)])
        
        #print("\n\n")
        if(listAuxC==listCentTrein):      
            #condição para parar o loop. quando a classe(cluster) de cada instancia não muda mais
            break;
        
        for a in range(0,k):
            if(len(nCentroids[a])>0):
                centros[a]=nCentroids[a];#adicionando os novos centroides na lista de centroides
                
        listCentTrein=listAuxC;
    print("Execução com %r clusters estabilizada na rodada %r\n\n"%(k,cont));
       
    return [centros,somaDistAux/tamAgr]
    
Elbow(); 
  


# In[ ]:





# In[ ]:




