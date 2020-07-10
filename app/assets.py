
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
from pandas_datareader import data as wb 
from svglib.svglib import svg2rlg
from io import BytesIO
import six, os, webbrowser, style

class Relatorio:
    def __init__(self):
        pass

    def organizarTiker(self, texto):
        texto = texto.replace(' ', '')
        texto = texto.replace('\n', '')
        texto = texto.upper()
        acoes = []
        texto = texto.replace(' ', '')
        for i in range(len(texto)):
            anterior = -1
            proximo = -1
            if (texto[i] == ';'):
                anterior = i
                for j in range(i+1,len(texto)):
                    if texto[j] == ';':
                        proximo = j
                        break
                
                if (texto[anterior+1:proximo] != ''):
                    acoes.append(texto[anterior+1:proximo])
        return acoes

    def get_dataframe(self, tikers, data_inicio, data_fim):
        data_frame = pd.DataFrame()
        for t in tikers:
            data_frame[t] = wb.DataReader(t, data_source='yahoo', start=data_inicio, end=data_fim)['Adj Close']
        return data_frame

    def plot_graph(self, data_frame, size):
        return data_frame.plot(figsize=size).get_figure()

    def normalize(self, data_frame):
        return (data_frame / data_frame.iloc[0] * 100)

    def simple_return(self, data_frame):
        return (data_frame / data_frame.shift(1)) - 1

    def log_return(self, data_frame):
        return np.log(data_frame / data_frame.shift(1))

    def s_day_return(self, tikers, data_frame):
        return self.simple_return(data_frame).mean()

    def s_anual_return(self, tikers, data_frame):
        return self.s_day_return(tikers, data_frame) * 250

    def s_percentual_return(self, tikers, data_frame):
        return self.s_anual_return(tikers, data_frame) * 100

    def l_day_return(self, tikers, data_frame):
        return self.log_return(data_frame).mean()

    def l_anual_return(self, tikers, data_frame):
        return self.l_day_return(tikers, data_frame) * 250

    def l_percentual_return(self, tikers, data_frame):
        return self.l_anual_return(tikers, data_frame) * 100

    def vol_return(self, log_return, acoes):
        quant_pesos = log_return.shape[1]
        retorno_portifolio = []
        retorno_volatividade = []
        pesos = []
        
        for i in range(50):

            weigth = []
            for i in range(quant_pesos):
                weigth.append(np.random.random())
            weigth = np.array(weigth)
            weigth /= sum(weigth)

            retorno_portifolio.append(np.sum(weigth * log_return.mean()) * 250)
            retorno_volatividade.append(np.sqrt(np.dot(weigth.T, np.dot(log_return.cov() * 250, weigth))))
            pesos.append(weigth)

        retorno_portifolio = np.array(retorno_portifolio)
        retorno_volatividade = np.array(retorno_volatividade)

        portfolios = pd.DataFrame({'Return': retorno_portifolio, 'Volatility': retorno_volatividade})
        
        pesos = pd.DataFrame(pesos)

        for p in range(pesos.shape[1]):
            portfolios[acoes[p]] = pesos[p]

        return portfolios

    def plot_volatility(self, dados):
        return dados.plot(figsize=(12,8), y = 'Return', x = 'Volatility', kind = 'scatter', marker = '*', s = 100, color='b').get_figure()

    def render_mpl_table(self, data, col_width=3.0, row_height=0.625, font_size=8.5,
                        header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                        bbox=[0, 0, 1, 1], header_columns=0,
                        ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax


    def gerar_relatorio(self, flag_imprimir_tabela, flag_imprimir_grafico, flag_imprimir_grafico_normalizado,flag_imprimir_grafico_volatividade, flag_imprimir_retorno_volatividade, flag_imprimir_melhores_ativos, data_inicio, data_fim, acoes):

        with PdfPages(os.path.dirname(__file__)+'/dados.pdf') as pdf:

            dados = self.get_dataframe(acoes, data_inicio, data_fim)


            if flag_imprimir_tabela:
                dados_fig = self.render_mpl_table(dados.head(15), header_columns=0, col_width=2.0)
                plt.title('Valor de fechamento dos tikers')
                pdf.savefig()  # saves the current figure into a pdf page
                plt.close()
            
            
            if flag_imprimir_grafico:
                fig_dados = self.plot_graph(dados, (13,8))
                plt.title('Valor de fechamento dos tikers')
                pdf.savefig(figure=fig_dados)
                plt.close()
            

            if flag_imprimir_grafico_normalizado:
                dados_normalizados = self.normalize(dados)
                fig_dados_norm = self.plot_graph(dados_normalizados, (13,8))
                plt.title('Percentual de valorização das ações')
                pdf.savefig(figure=fig_dados_norm)
                plt.close()
            

            if flag_imprimir_grafico_volatividade:
                retorno_simples = self.simple_return(dados)
                fig_dados_sr = self.plot_graph(retorno_simples, (13,8))
                plt.title('Variação dos tikers em relação a média (volatividade)')
                pdf.savefig(figure=fig_dados_sr)
                plt.close()


            if flag_imprimir_retorno_volatividade:
                retorno_logaritmo = self.log_return(dados)
                retorno_volatividade = self.vol_return(retorno_logaritmo, acoes)
                retorno_volatividade.sort_values(['Return', 'Volatility'], ascending=[True, False], inplace=True)
                dados_fig = self.render_mpl_table(retorno_volatividade.tail(25), header_columns=0, col_width=2.0)
                plt.title('%% de distribuição dos tikers (melhor caso)')
                pdf.savefig()  # saves the current figure into a pdf page
                plt.close()

                dados_fig = self.render_mpl_table(retorno_volatividade.head(25), header_columns=0, col_width=2.0)
                plt.title('%% de distribuição dos tikers (melhor caso)')
                pdf.savefig()  # saves the current figure into a pdf page
                plt.close()
            

            if flag_imprimir_melhores_ativos:
                fig_dados = self.plot_volatility(retorno_volatividade)
                plt.title('Indicador de retorno e volatividade segundo Markowitz')
                pdf.savefig(figure=fig_dados)  # saves the current figure into a pdf page
                plt.close()
            

            webbrowser.open(os.path.dirname(__file__)+'/dados.pdf')

