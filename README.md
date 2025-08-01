# 🧠 Previsão de Surtos na Doença de Crohn com Machine Learning

Este projeto é uma exploração de como a ciência de dados pode ser aplicada para resolver um problema real e impactante na área da saúde: prever crises (surtos) em pacientes com Doença de Crohn, trazendo mais previsibilidade e a chance de um cuidado médico proativo.

---

## 🎯 O Problema: Trazendo Previsibilidade para a Incerteza

A Doença de Crohn é uma condição crônica que afeta milhões de pessoas, e sua principal característica é a imprevisibilidade. Um paciente pode estar bem em um dia e em meio a uma crise debilitante no outro. Essa incerteza afeta profundamente a qualidade de vida.

A pergunta central deste projeto foi: **É possível usar dados clínicos de uma visita médica para prever se um paciente terá um surto na visita seguinte?**

---

## 📊 O Dataset: IBDMDB

Para responder a essa pergunta, utilizei o **IBDMDB (Inflammatory Bowel Disease Multi'omics Database)**, um dataset público e extremamente rico, fruto de um estudo de pesquisa que acompanhou pacientes ao longo do tempo.

O desafio inicial foi navegar em um arquivo com quase 500 colunas, identificando os dados mais relevantes para o nosso objetivo, como:

* **Índice Harvey-Bradshaw (HBI):** A métrica clínica que define a atividade da doença.
* **Biomarcadores de Inflamação:** Como a Proteína C Reativa (CRP).
* **Dados Demográficos e Clínicos:** Idade, sexo, diagnóstico, etc.

---

## 🛠️ A Metodologia: Da Limpeza à Previsão

O processo para transformar dados brutos em um modelo funcional seguiu 4 passos principais:

1.  **Limpeza e Pré-processamento:** O primeiro passo foi filtrar o dataset massivo para manter apenas os pacientes com diagnóstico de Crohn e as colunas de interesse. Também lidei com dados faltantes e converti as datas para um formato utilizável.

2.  **Engenharia de Features (O Coração do Projeto):** Para criar um problema de previsão, a engenharia de features foi crucial. A principal técnica utilizada foi:
    * **Criação do Alvo Futuro:** Ordenei as visitas de cada paciente e, usando a função `shift(-1)` do Pandas, criei uma nova coluna `flare_future`. Esta coluna continha, para cada visita, o status da doença da **próxima visita**, transformando o dataset em um problema de aprendizado supervisionado.

3.  **Modelagem com `RandomForestClassifier`:** Escolhi o `RandomForestClassifier` por sua robustez e performance. Pense nele como um "comitê de especialistas": ele constrói centenas de árvores de decisão e chega a uma previsão final baseada na votação da maioria.

4.  **Lidando com o Desbalanceamento:** Como os casos de "surto" eram muito mais raros que os de "remissão", utilizei o parâmetro `class_weight='balanced'`. Isso força o modelo a dar mais importância aos erros cometidos na classe minoritária, tornando-o muito mais sensível para detectar as crises.

---

## ✨ Resultados: Um Alerta Precoce Confiável

O modelo final demonstrou uma performance excelente e, o mais importante, clinicamente relevante.

* **Acurácia Geral:** **91%**
* **Recall (Surto):** **83%** (O modelo conseguiu detectar 5 de cada 6 surtos reais)
* **Precisão (Surto):** **83%** (Quando o modelo previu um surto, ele estava certo 83% das vezes)

A matriz de confusão final foi:

[[15  1]
[ 1  5]]

Isso mostra que o modelo cometeu pouquíssimos erros, principalmente o erro mais crítico (Falso Negativo), onde um surto não é detectado.

---

## 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone (https://github.com/pedropaulopy/crohnsdisease_predict)
    cd crohnsdisease_predict
    ```
2.  **Instale as dependências:**
    ```bash
    pip install requirements.txt
    ```
3.  **Execute o script:**
    * Certifique-se de que o arquivo `hmp2_metadata_2018-08-20.csv` esteja no diretório correto.
    * Rode o script Python:
        ```bash
        python cd.py
        ```

---

## 🔮 O Futuro: Próximos Passos

O potencial desta abordagem é imenso. Os próximos passos para evoluir este projeto seriam:

* **Incorporar Mais Dados:** Adicionar mais features clínicas e de medicação.
* **Integração com Wearables:** O sonho seria alimentar o modelo com dados em tempo real de smartwatches (frequência cardíaca, sono, atividade) para criar um sistema de alerta verdadeiramente pessoal e contínuo.
