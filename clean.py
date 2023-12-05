#!/usr/bin/env python
# run `chmod +x clean.py` to allow running this script without writing `python3`

import sys
import re
import os

regexes = [
  # Nubank
  r'<MEMO>Transferência enviada pelo Pix - (.*?) - ',
  r'<MEMO>Transferência recebida pelo Pix - (.*?) - ',
  r'<MEMO>Compra no débito - (.+?)<\/MEMO>',
  r'<MEMO>Pagamento de boleto efetuado - (.+?)<\/MEMO>',
  r'<MEMO>Transferência enviada - (.*?) - ',
  r'<MEMO>Transferência recebida - (.*?) - ',
  # Bradesco
  r'<MEMO>Transfe Pix Des: (.*?)(\\r\\n|\\n|$)',
  r'<MEMO>Transfe Pix Rem: (.*?)(\\r\\n|\\n|$)',
  r'<MEMO>Pix Qrcode Din Des: (.*?)(\\r\\n|\\n|$)',
  r'<MEMO>Pix Qrcode Est Des: (.*?)(\\r\\n|\\n|$)',
  r'<MEMO>Ted-t Elet Disp Remet.(.*?)(\\r\\n|\\n|$)',
  r'<MEMO>Pagto Cobranca (.*?)(\\r\\n|\\n|$)',
  ]


def process_file(file_path):
  file_directory = os.path.dirname(file_path)
  output_file_path = os.path.join(file_directory, f'{file_path}-PROCESSED.ofx')

  with open(file_path, "r") as file, open(output_file_path, 'w') as output_file:
    lines = file.readlines()

    for line in lines:
      processed_line = process_line(line)
      output_file.write(processed_line)

  file.close()
  output_file.close()

  print(f"File {os.path.basename(file_path)} processing complete. See output data.")

def process_line(line):
  processed_line = line
  if '<MEMO>' in line:
    for regex in regexes:
      match = re.search(regex, line, re.I)
      if match:
        processed_line = (f"<MEMO>{match.group(1)}</MEMO>")

  return processed_line


def clean_ofx():
  # "2" because sys.argv includes the script name
  if len(sys.argv) < 2:
    print('Not enough arguments')
    return

  for arg in sys.argv:
    if arg in __file__:
      continue

    if "ofx" not in arg:
      print(f"file {arg} is not a valid OFX file")
      continue

    process_file(arg)

clean_ofx()


