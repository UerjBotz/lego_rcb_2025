# Carcará Branco / Carrara Táxi Carrara

Repositório criado para o desafio RCB Challenge Kit da CBR 2024 (antigo SEK).

## Pré-requisitos

Usamos o vscode no Ubuntu 24.04 com o pybricksdev para o upload e desenvolvimento do código e um SPIKE Prime Hub, da LEGO, como alvo.
Não recomendamos o uso do windows.

Certifique-se de ter o Python 3 instalado na sua máquina, na versão 3.9 ou maior. Você pode verificar a versão do Python com o comando:

```bash
python --version
```

A seção seguinte é baseada no tutorial oficial da pybricks sobre o uso de outros editores.

Fonte: <https://pybricks.com/project/pybricks-other-editors/>


## Configurando o Ambiente

Este projeto utiliza um ambiente virtual para gerenciar dependências de forma isolada. Siga as instruções abaixo para configurar o ambiente.

### Passo 1: Crie o Ambiente Virtual

Crie um ambiente virtual na pasta do projeto (normalmente chamado de `.venv`):

```bash
python -m venv .venv
```

### Passo 2: Instale as Dependências

Instale as dependências do projeto listadas no arquivo `requirements.txt`:

No linux:
```bash
.venv/bin/pip install -r requirements.txt
```
No Windows:
```bash
.venv/Scripts/pip install -r requirements.txt
```

Agora seu ambiente virtual está configurado e pronto para uso!


## Executando o Projeto

Escreva make no terminal para fazer upload para o dos dois spikes.
O script espera que você tenha um chamado

## Contribuição

### Interna
Se desejar contribuir com o projeto, faça um clone do repositório, crie uma branch com a sua feature, e envie um push para a sua branch. **Não comite para a master** 

1. Faça o clone do projeto (`git clone https://github.com/UerjBotz/lego_rcb_2024.git`)
2. Crie uma branch para sua feature (`git switch -c nome-da-sua-branch`)
3. Adicione suas mudanças (`git add $arquivo1 $arquivo2 ... $arquivoN`)
4. Comite suas mudanças explicando o que/porque mudou (`git commit`) com uma mensagem descritiva.
5. Faça o push para a branch (`git push origin nome-da-sua-branch`)
6. Abra um Pull Request


### Externa 
1. Faça o fork do projeto
2. Siga os passos para a contribuição interna

Qualquer dúvida, entre em contato ou abra uma issue no repositório.
