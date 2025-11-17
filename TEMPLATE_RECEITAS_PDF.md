# 📚 TEMPLATE PARA PDF DE RECEITAS ESTRUTURADAS

## 📋 Formato Recomendado para Cada Receita:

```
**NOME DA RECEITA**

INGREDIENTES:
- [quantidade] [ingrediente]
- [quantidade] [ingrediente]
- [quantidade] [ingrediente]

MODO DE PREPARO:
1. [passo detalhado]
2. [passo detalhado]  
3. [passo detalhado]

TEMPO: [tempo de preparo]
PORÇÕES: [número de porções]
DIFICULDADE: [Fácil/Média/Difícil]

---
```

## 📖 Exemplo de Receita Bem Estruturada:

```
**BRIGADEIRO SAUDÁVEL**

INGREDIENTES:
- 200g de chocolate 80%
- 1 xícara de creme de leite fresco
- 1/2 xícara de xilitol
- 1 colher de sopa de manteiga
- Granulado para enrolar

MODO DE PREPARO:
1. Derreta o chocolate em banho-maria em fogo baixo
2. Adicione o creme de leite e misture bem até ficar homogêneo
3. Acrescente o xilitol e misture até dissolver completamente
4. Adicione a manteiga e misture até obter consistência cremosa
5. Deixe esfriar e despeje em forminhas ou faça bolinhas
6. Passe no granulado e leve à geladeira por 2 horas

TEMPO: 15 minutos de preparo + 2 horas na geladeira
PORÇÕES: 20 brigadeiros
DIFICULDADE: Fácil
```

## 🎯 Benefícios Desta Estrutura:

1. **Seções claras**: INGREDIENTES e MODO DE PREPARO bem definidos
2. **Formatação consistente**: Listas com '-' e passos numerados
3. **Informações completas**: Tempo, porções, dificuldade
4. **Fácil parsing**: O sistema RAG consegue extrair facilmente
5. **Interface amigável**: Dados estruturados para a interface de cozinha

## 📝 Dicas Importantes:

- Use **negrito** para nomes das receitas
- Mantenha ingredientes em **lista com '-'**
- Numere os passos do preparo **1, 2, 3...**
- Inclua sempre **TEMPO, PORÇÕES, DIFICULDADE**
- Separe receitas com **'---'**

## ✅ Validação:

Após criar o PDF estruturado:
1. Substitua o arquivo atual na pasta `data/pdf/`
2. Execute o sistema de busca
3. Teste a interface de cozinha passo-a-passo
4. Verifique se ingredientes e passos aparecem corretamente