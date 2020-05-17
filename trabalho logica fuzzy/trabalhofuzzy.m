%Programa de avaliação de satisfação ao comprar determinado jogo%

%mostrar na tela a mensagem que pede preço e logo abaixo a variavel que guarda o preço do jogo%
 disp("Entre com o preço do jogo");
 preco=input("Preco do jogo:");
 
 %O preço do jogo vai ser de 1 a 300 reais%
 
 
 %mostrar na tela a mensagem que pede a nota crítica ou pontuação do jogo segundo críticas e logo abaixo a variavel que vai guardar esse valor%
 disp("Entre com a nota da crítica/score do jogo");
 crit=input("Nota crítica do jogo:");
 %a variavel de crítica vai de 1 a 100%
 
 
 %%mostrar na tela a mensagem que pede o tempo de jogo/gameplay/tempo para terminar o jogo e logo a baixo a variavel que guardae esse valor%
 disp("Entre com o gameplay/ tempo para terminar o jogo");
 tempo=input("tempo do jogo:");
 %tempo vai de 1 a 100 horas%
 
 % função de pertinência preco%
  x = 0:1:300;
 preco_baixo=trapmf(x,[-1,0,20,75]);
 preco_regular=trimf(x,[50,120,190]);
 preco_alto=trapmf(x,[120,190,300,301]);
 
 
 
 %função pertinencia pontuação/notas/crit%
 x1=0:1:100;
 crit_ruim=trapmf(x1,[-1,0,1,40]);
 crit_regular=trimf(x1,[30,55,80]);
 crit_alto=trapmf(x1,[55,80,100,101]);
 
 
 
 %função de pertinencia horas de jogo/gameplay/tempo para concluir o jogo%
 x2=0:1:100;
 tempo_baixo=trapmf(x2,[-1,0,25,50]);
 tempo_medio=trimf(x2,[25,50,75]);
 tempo_alto=trapmf(x2,[50,75,100,101]);
 
 
 %grau de pertinencia da satisfação ao comprar o jogo/ou se vale a pena comprar%
 
 x3=0:1:100;
 
 sat_baixo=trapmf(x3,[-1,0,1,30]);
 sat_medio=trimf(x3,[20,50,80]);
 sat_alto=trapmf(x3,[50,80,100,101]);
 
  
  
 %Inferência de Mamdani segundo o conjunto de Regras%
 
 %R1: se tempo de jogo baixo e crítica do jogo ruim então satisfação igual a baixo%
 r1=min(tempo_baixo(tempo),crit_ruim(crit));
 regra1=min(r1,sat_baixo);
 
 %R2: se tempo de jogo medio e crítica do jogo regular então satisfação igual a medio%
 r2=min(tempo_medio(tempo),crit_regular(crit));
 regra2=min(r2,sat_medio);
 
 %R3: se tempo de jogo alto e crítica de jogo alto então satisfação igual a alto%
r3=min(tempo_alto(tempo),crit_alto(crit));
regra3=min(r3,sat_alto);

%R4: se crítica do jogo alto e preço do jogo baixo então satisfação igual a alto% 
 r4=min(crit_alto(crit),preco_baixo(preco));
 regra4=min(r4,sat_alto);
 
 %R5: se crítica do jogo regular e preço do jogo regular então satisfação igual medio%
 r5=min(crit_regular(crit),preco_regular(preco));
 regra5=min(r5,sat_medio);
 
 %R6: se crítica do jogo ruim e preço do jogo alto então satisfação igual baixa%
 r6=min(crit_ruim(crit),preco_alto(preco));
 regra6=min(r6,sat_baixo);
 
 %R7: se tempo do jogo alto e preço do jogo baixo então satisfação igual a alto%
 r7=min(tempo_alto(tempo),preco_baixo(preco));
 regra7=min(r7,sat_alto);
 
 %R8: se tempo de jogo medio e preço do jogo regular então satisfação igual a medio%
 r8=min(tempo_medio(tempo),preco_regular(preco));
 regra8=min(r8, sat_medio);
 
 %R9: se tempo do jogo baixo e preço do jogo alto então satisfação igual a baixo%
 r9=min(tempo_baixo(tempo),preco_alto(preco));
 regra9=min(r9,sat_baixo);
 
 satisf_alt=max(regra3, regra4);
 satisf_alt1=max(satisf_alt,regra7);
 
 satisf_med=max(regra2,regra5);
 satisf_med1=max(satisf_med,regra8);
 
 satisf_baix=max(regra1,regra6);
 satisf_baix1=max(satisf_baix,regra9);
 
 Y1=max(satisf_alt1,satisf_med1);
 ytotal=max(Y1, satisf_baix1);
 
 figure('NumberTitle', 'off', 'Name', 'Grau de Satisfação');
grid on;
hold on;
plot(ytotal,'b');
title('Resultado do grau de satisfação segundo a inferência Mamdani');

 %desfuzzificação segundo o método do centro de massa%
 
 
 %valor que será usado para o x%
 resultadoMamdani = (ytotal.*x3)/ytotal;
 
 %valor que será usado para encontrar o y%
Mamd = ytotal/2;
hold on;
plot(resultadoMamdani,mean(Mamd),'rx:');
 
 %fim da desfuzzificação segundo o método do centro de massa%
 
 %Resultado da inferencia de mamdani que será usado para determinar o grau de satisfação%
 fprintf('\n\n RESULTADOS \n\n');
disp('Grau de satisfação segundo a Inferencia de Mamdani');
fprintf('%g',resultadoMamdani);


%Condições que geram sugestões para o usuário%

disp("\n Sugestão do sistema para o usuario");

if (resultadoMamdani<60)
    disp("\n\n Não vale muito a pena comprar o jogo");
elseif(resultadoMamdani<75)
  disp("\n\n Talvez valha a pena jogar o jogo");
else
    disp("\n\n Vale muito a pena jogar o jogo");
end
