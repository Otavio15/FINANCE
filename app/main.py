from .assets import Relatorio
from flask import Flask, render_template, request, send_file
import os
import time

app = Flask(__name__, template_folder=os.path.dirname(__file__))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        result = request.form
        result = result.to_dict(flat=False)
        if result['DataInicio'] != [''] and result['DataFim'] != ['']:
            data_inicio = result['DataInicio'][0]
            data_fim = result['DataFim'][0]
            flag_imprimir_tabela = False
            flag_imprimir_grafico = False
            flag_imprimir_grafico_normalizado = False
            flag_imprimir_grafico_volatividade = False
            flag_imprimir_retorno_volatividade = False
            flag_imprimir_melhores_ativos = False

            if 'aux1' in result:
                flag_imprimir_tabela = True
            if 'aux2' in result:
                flag_imprimir_grafico = True
            if 'aux3' in result:
                flag_imprimir_grafico_normalizado = True
            if 'aux4' in result:
                flag_imprimir_grafico_volatividade = True
            if 'aux5' in result:
                flag_imprimir_retorno_volatividade = True
            if 'aux6' in result:
                flag_imprimir_melhores_ativos = True

            texto = result['tikers'][0]
            rel = Relatorio()
            acoes = rel.organizarTiker(texto)

            try:
                rel.gerar_relatorio(flag_imprimir_tabela, flag_imprimir_grafico, flag_imprimir_grafico_normalizado, flag_imprimir_grafico_volatividade,
                                    flag_imprimir_retorno_volatividade, flag_imprimir_melhores_ativos, data_inicio, data_fim, acoes)
                time.sleep(2)
                # Corrigindo o caminho do arquivo
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dados.pdf'))

                # Usando o argumento correto 'download_name'
                return send_file(file_path, as_attachment=True, download_name='dados.pdf')
            except:
                print("Erro ao gerar relatório")
                pass

        return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
