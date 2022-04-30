# Divisor_PDF
Implementação de um software que separa as páginas de um PDF em arquivos únicos. Possui uma interface gráfica onde é possível escolher o arquivo e onde será salvo os arquivos que correspondem às páginas.

A aplicação está finalizada em um executável (.exe) e funciona no windows. Porém, a partir do código fonte disposto aqui é póssivel compilar para qualquer dispositivo, inclusive dispositivos móveis (IOS e Android).

## Ferramentas e Bibliotecas utilizadas

- <a href="https://www.python.org/">Python</a>
- <a href="https://kivy.org/">Kivy</a>
- <a href="https://github.com/py-pdf/PyPDF2">PyPDF2</a>
- <a href="https://pyinstaller.org/">PyInstaller</a> (build para executável)

## Como usar
O uso é simples e intuitivo, você pode colocar o caminho do arquivo pdf no primeiro campo de texto, ou pode procurar o arquivo pdf clicando no botão Escolher PDF. O mesmo método serve para escolher a pasta de saída, ou seja, onde os arquivos referente as páginas serão salvos. Após escolher o arquivo e o diretório, é possivel optar por compactar tudo em um arquivo zip e definir um intervalo de páginas. Por fim, basta apenas clicar o botão Split PDF para concluir o processo e pronto, seu PDF já foi dividido em várias páginas.
