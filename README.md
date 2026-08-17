# Calculadora — Console + Flet

🇧🇷 Português | [🇺🇸 English](README.en.md)

Projeto de calculadora em Python, construído em duas etapas: primeiro uma versão de terminal (console), depois um app visual usando a biblioteca Flet. As duas versões compartilham a mesma lógica de cálculo, testada com pytest.

Este README documenta não só o resultado final, mas o processo — decisões tomadas, erros encontrados no caminho, e o porquê de cada mudança. A ideia é que o histórico de evolução seja tão parte do portfólio quanto o código pronto.

## Funcionalidades

- Operações: soma, subtração, multiplicação, divisão, raiz quadrada, porcentagem
- Histórico de cálculos salvo em arquivo (`history.csv`), com data e hora
- Tratamento de erro para divisão por zero e raiz de número negativo, nas duas versões
- App visual (Flet) com:
  - Teclado numérico completo, vírgula decimal, backspace (⌫) e limpar (AC)
  - Formatação de resultado no padrão brasileiro (vírgula em vez de ponto, sem `.0` desnecessário)
  - Limite de dígitos exibidos na tela, com indicação (`...`) quando o resultado é maior que o espaço disponível
  - Layout em grade, cores diferenciadas para números e operadores

## Estrutura do projeto

```
Calculator/
├── system.py             # versão console (terminal)
├── app.py                 # versão visual (Flet)
├── lib/
│   ├── operations.py       # funções de cálculo, puras e testadas
│   └── history.py           # salvar e ler histórico em arquivo
├── tests/
│   └── test_operations.py
├── .gitignore
└── README.md
```

## Como rodar

```bash
python system.py              # versão console
python app.py                  # versão visual (Flet)
python -m pytest tests/        # roda os 8 testes automatizados
```

Dependência externa: `flet` (`pip install flet`). O restante usa apenas biblioteca padrão do Python.

---

## Evolução do projeto

### 1. Ponto de partida: separar lógica de interface

Antes de escrever qualquer coisa, a decisão estrutural mais importante foi: **as funções de cálculo nunca leem entrada nem imprimem nada.**

```python
def add(a: float, b: float) -> float:
    return a + b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
```

Cada função recebe números e devolve um resultado — nada de `input()` ou `print()` dentro delas. Essa escolha, feita logo no início, é o motivo pelo qual foi possível:
- Testar cada função automaticamente com pytest, sem precisar simular digitação
- Reaproveitar exatamente as mesmas funções no console e, mais tarde, no app Flet, sem duplicar lógica

### 2. Testes antes de tudo

Cada função tem um teste de caso normal e, quando aplicável, um teste de erro:

```python
def test_division_by_zero():
    with pytest.raises(ValueError):
        division(5, 0)

def test_square_root_negative():
    with pytest.raises(ValueError):
        square_root(-4)
```

Erro comum no início: escrever `assert add(2 + 2) == 4` em vez de `assert add(2, 2) == 4` — resolvendo a conta *antes* de chamar a função, em vez de deixar a função fazer a conta. Corrigido ao entender que o `assert` deve testar com os números "crus", e comparar com o resultado já calculado de cabeça.

### 3. Console (`system.py`)

Menu simples em loop, com `try/except` nas duas operações que podem falhar:

```python
elif option == 4:
    a = float(input("First number: "))
    b = float(input("Second number: "))
    try:
        result = division(a, b)
        print(f'Result: {result}')
        save_operations('division', result)
    except ValueError as error:
        print(f'ERROR: {error}')
```

Histórico salvo em CSV, com data formatada (`datetime.now().strftime(...)`) em vez do timestamp completo com microssegundos, que era ilegível.

### 4. Removi a potenciação (`power`) do projeto inteiro

Ao planejar os botões do app visual, ficou claro que adicionar potenciação e raiz quadrada quebraria o layout de grade (5 linhas de 4 botões viraria uma linha final incompleta). Decisão: manter só a raiz quadrada no app, e **remover completamente** a potenciação — função, teste e opção de menu — em vez de deixar ela "esquecida" só no console. Prioridade foi consistência entre as duas versões, não cobertura total de operações.

### 5. App visual — primeiros obstáculos com o Flet

O Flet mudou bastante entre versões, e boa parte do início foi adaptar exemplos desatualizados à versão instalada (0.86.5):

- `ft.app(target=main)` → `ft.run(main)` (método antigo descontinuado)
- `ElevatedButton(text="1", ...)` → `ElevatedButton(content="1", ...)` (parâmetro renomeado)
- `ElevatedButton` → `Button` (o próprio controle foi descontinuado na versão instalada)

Aprendizado principal: em vez de confiar em tutoriais desatualizados, usar `help()` direto na biblioteca instalada resolve com mais confiabilidade:
```bash
python -c "import flet as ft; help(ft.ElevatedButton.__init__)"
```

### 6. `global` vs `nonlocal`

As variáveis de estado da calculadora (`num_current`, `num_previous`, `pending_operator`) são criadas dentro de `main()`, não no nível do arquivo. Usar `global` dentro da função de clique criava uma variável nova e desconectada, em vez de atualizar a existente — o app "esquecia" o que já tinha sido digitado. Corrigido trocando para `nonlocal`, que busca a variável no escopo da função logo acima (`main`), não no nível do arquivo.

### 7. Bug de indentação: bloco do "=" rodando sempre

Em certo ponto, o bloco de cálculo do `"="` foi escrito como um `try` separado, fora da cadeia de `if/elif` de `select()`, em vez de ser mais um `elif`. Resultado: o bloco de cálculo rodava em **toda** chamada de `select()`, mesmo ao clicar em um número — gerando `cannot access local variable 'result'` porque nenhuma condição interna batia. Corrigido reestruturando como `elif value_click == "=":`, no mesmo nível dos outros `elif`.

### 8. Formatação do resultado

Como toda função de `operations.py` retorna `float`, `7 + 2` chegava como `"9.0"` no visor, com ponto em vez de vírgula. `format_result()` resolve isso em um único lugar:

```python
def format_result(result):
    result = round(result, 8)
    if result == int(result):
        return str(int(result))
    else:
        return str(result).replace(".", ",")
```

Arredondar em 8 casas decimais também evita resultados do tipo `94.44444444444444`, comuns em divisões, que não cabem na tela.

### 9. Limite de dígitos e o "..."

Tentativa inicial: fonte que encolhia dinamicamente conforme o número crescia. Funcionou, mas o resultado era visualmente inconsistente (fonte mudando de tamanho a cada dígito digitado). Decisão final: **fonte fixa**, com um limite de dígitos (`max_digits`) tanto na digitação quanto no resultado exibido.

Quando o resultado calculado excede o limite, em vez de cortar o texto silenciosamente (o que mostraria um número errado sem avisar) ou travar com uma mensagem de erro genérica, o app mostra os dígitos que cabem seguidos de reticências:

```python
if len(text_result) > max_digits:
    num_current = text_result[:max_digits - 3] + "..."
else:
    num_current = text_result
```

Isso comunica ao usuário que o valor foi truncado, sem impedir o uso da calculadora.

### 10. Cópia para área de transferência — implementada e depois removida

Cheguei a implementar clipboard, usando o serviço `Clipboard` do Flet (API assíncrona, com `async/await`):

```python
async def copy_visor(e):
    await clipboard.set(visor.value)
```

Funcionou, mas exigiu envolver o visor em um `Container` extra para capturar o clique, o que desalinhou a grade de botões abaixo dele. Removida a funcionalidade — nesse projeto, layout visual consistente teve prioridade sobre uma funcionalidade secundária.

### 11. Estrutura de arquivos — pastas viradas arquivo (e vice-versa)

Durante o desenvolvimento, aconteceram duas confusões de pasta/arquivo:
- `test_operations.py` criado como pasta em vez de arquivo (continha um `__init__.py` dentro)
- `operations.py` e `history.py` inicialmente escritos dentro do `__init__.py` de uma pasta `operations/`, em vez de como arquivos diretos

Ambos os casos funcionavam (Python aceita lógica dentro de `__init__.py`), mas fogem do padrão esperado por quem revisa o código. Corrigido movendo o conteúdo para arquivos diretos (`lib/operations.py`, `lib/history.py`) e removendo as pastas extras.

---

## Testes

8 testes cobrindo os casos normais de cada operação e os 2 casos de erro tratados (divisão por zero, raiz de número negativo):

```bash
python -m pytest tests/
```

## Possíveis próximos passos

- Notação científica para resultados que excedem o limite de dígitos, em vez de truncar
- Potenciação de volta, com ajuste de layout para acomodar o botão extra
- Copiar para área de transferência, revisitando o layout para não desalinhar a grade
