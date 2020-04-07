Encode,decode programme

- in terminal run: py lab1.py
- choose method that u want to encode text data (1/2/3)
  + 1st method: change 'o' and 'p' of english symbol to 'o' and 'p' of russian symbol
  + 2nd method: add blank space, tab before endline
  + 3rd method: add special symbol that dont show on common text editor
- input your text data

Analysis programme

- in terminal run: py lab1_analysis.py
- programme'll output the list of every symbol and number of them.
- if u see some double symbol, can probly say that they are different symbols and maybe some text data hidden in container.
- if u see some blank symbols ('' - special symbol that dont show on common text editor), that's the sight of hidden text in container.
- if u see huge amount of tab and space symbol, that's the sight of hidden text in container too.

Note

- text data must be lower case and just contants russian symbol
- in my example text data input = 'отлично'
  + 1st method: container before encoding has 8914 bytes, after: 8949 bytes
  + 2nd method: container before encoding has 8914 bytes, after: 8949 bytes
  + 3rd method: container before encoding has 8914 bytes, after: 8965 bytes
- in my example text data input = 'лабораторнуюработусдал'
  + 1st method: container before encoding has 8914 bytes, after: 9024 bytes
  + 2nd method: container before encoding has 8914 bytes, after: 9024 bytes
  + 3rd method: container before encoding has 8914 bytes, after: 9094 bytes
