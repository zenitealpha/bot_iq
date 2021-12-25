import sys, os, getpass
import telebot, time, json
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timezone
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import base64
from github import Github
import requests
from pprint import pprint

api_bot = "2118641728:AAG5uHqiYHEh3WRYc-gOtHSLOvAmGY4sh7U"
bot = telebot.TeleBot(api_bot)
g = Github(login_or_token="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")
repo = g.get_user().get_repo('bot_iq')
all_files = []
contents = repo.get_contents("")
content = str(contents)

login_dict = {}
class login:
    def __init__(self, email):
        self.email = email
        self.senha = None

config_mhi = {}
class mhi_config:
    def __init__(self, conta):
        self.conta = conta
        self.operacao = None
        self.tipo_mhi = None
        self.time_frame = None
        self.par = None
        self.valor_entrada = None
        self.martingale = None
        self.stop_loss = None
        self.stop_gain = None

config_lista_sinais = {}
class lista_sinais_config:
    def __init__(self, conta):
        self.conta = conta
        self.operacao = None
        self.valor_entrada = None
        self.martingale = None
        self.stop_loss = None
        self.stop_gain = None

global ligado

def cliente_permitido(id):
    valores = []
    arq_dados = 'cliente_permitido.txt'
    try:
        file = open(arq_dados, 'r').read()
    except:
        print("Nenhum cliente regitrado.")

    for index, dados in enumerate(file.split('\n')):
        if len(dados) > 0 and dados != '':
            dados_ = dados.split(',')
            if dados_[0] == id:
                valores.append({
                    'id_telegram': dados_[0],
                    'estado': dados_[1],
                    'plano': dados_[2],
                    'mes_espiracao': dados_[3]
                })

    return valores

def nao_exist(id):
    result = False
    file = open("{}.txt".format(id), 'r')
    for dado in file:
        if dado.strip() != '':
            result = True
    file.close()
    return result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    id_user = message.from_user.id
    dados_cli = cliente_permitido(str(id_user))
    if len(dados_cli) > 0:
        for data in dados_cli:
            id_telegram = int(data['id_telegram'])
            estado = int(data['estado'])
            plano = str(data['plano'])
            mes_espiracao = int(data['mes_espiracao'])

    if message.chat.type == 'private' and plano != 'admin' and plano != 'super_admin' and id_telegram == id_user and estado == 1:
        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('🤖Listar Bots')
        markup.row(itembtna)
        bot.send_message(message.chat.id,"Bem-vindo de Volta " + message.from_user.first_name +
            "\nPara atualização do plano, contacte: @Zcreations1" +
            "\nNão te esqueças de fornecer a ele o seu ID:"+str(message.from_user.id),reply_markup=markup)
        '''
        id_user = message.from_user.id
        file = open("{}.txt".format(id_user), 'a+')
        if (not nao_exist(str(id_user))):
            file.close()
        '''
        
    elif message.chat.type == 'private' and id_telegram != id_user:
        #message obtem os dados do usuário: id, nomes, data da sms, e o testo ou conteúdo enviado
        #a linha abaixo recupera o id, primeiro nome, e o último nome e enviar uma sms ao usuário de boas vindas
        bot.send_message(message.chat.id, "Olá tudo bem " + message.from_user.first_name +
                        " " + message.from_user.last_name + "?" +
                        "\nSeja bem vindo(a) ao ROBÔ FÉNIX este é o seu ID: " +str(message.chat.id) +
                        "\nContacte @Zcreations1 para obter acesso ao bot! ")

    elif message.chat.type == 'private' and id_telegram == id_user and estado == 1 and plano == 'super_admin':
        '''
        id_user = message.from_user.id
        file = open("{}.txt".format(id_user), 'a+')
        if (not nao_exist(str(id_user))):
            file.close()
        '''
        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('✅Add usuário')
        itembtnb = types.KeyboardButton('Excluir usuário')
        itembtnc = types.KeyboardButton('Listar usuários')
        itembtnd = types.KeyboardButton('Alterar Pacote')
        itembtne = types.KeyboardButton('Alterar data de expiração')
        itembtnf = types.KeyboardButton('Restringir usuário')
        itembtng = types.KeyboardButton('🤖Listar Bots')
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtnf, itembtng)
        bot.send_message(message.chat.id,
                         "Bem-vindo de volta Super-Admin " +
                         message.from_user.first_name,
                         reply_markup=markup)

    elif message.chat.type == 'private' and id_telegram == id_user and estado == 1 and plano == 'admin':
        '''
        id_user = message.from_user.id
        file = open("{}.txt".format(id_user), 'a+')
        if (not nao_exist(str(id_user))):
            file.close()
        '''
        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Prestar Suporte')
        itembtnb = types.KeyboardButton('Dados do Usuário')
        itembtnc = types.KeyboardButton('Usuários Ativos')
        itembtnd = types.KeyboardButton('Pacotes disponíveis')
        itembtne = types.KeyboardButton('Verificação de Usuário')
        itembtng = types.KeyboardButton('🤖Listar Bots')
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtng)
        bot.send_message(message.chat.id,
                         "Bem-vindo de volta Admin " +
                         message.from_user.first_name,
                         reply_markup=markup)

    elif message.chat.type != 'private':
        bot.send_message(message.chat.id,
                         "Não tens permissão para usar este Bot")

@bot.message_handler(func=lambda message: message.text == '🤖Listar Bots')
def listar_bots(message):
    id_user = message.from_user.id
    dados_cli = cliente_permitido(str(id_user))
    if len(dados_cli) > 0:
        for data in dados_cli:
            id_telegram = int(data['id_telegram'])
            estado = int(data['estado'])
            plano = str(data['plano'])
            mes_espiracao = int(data['mes_espiracao'])

    if (id_telegram == id_user) and (estado == 1) and plano == "Grátis":
        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('✅Fazer Login')
        itembtnb = types.KeyboardButton('Bot de Lista de Sinais')
        markup.row(itembtna)
        markup.row(itembtnb)
        bot.send_message(message.chat.id,
                         "Bot disponível para o plano grátis",
                         reply_markup=markup)
    elif (id_telegram == id_user) and (estado == 1) and plano == "Bronze":

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Lista de Sinais')
        itembtnb = types.KeyboardButton('MHI')
        itembtnc = types.KeyboardButton('✅Fazer Login')
        markup.row(itembtnc)
        markup.row(itembtna, itembtnb)
        bot.send_message(message.chat.id,
                         "Bots disponíveis para o plano bronze",
                         reply_markup=markup)
    elif (id_telegram == id_user) and (estado == 1) and plano == "Prata":

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Lista de Sinais')
        itembtnb = types.KeyboardButton('MHI')
        itembtnc = types.KeyboardButton('Catalogador de Sinais')
        itembtnd = types.KeyboardButton('Estratégia Chinesa')
        itembtne = types.KeyboardButton('✅Fazer Login')
        markup.row(itembtne)
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd)
        bot.send_message(message.chat.id,
                         "Bots disponíveis para o plano prata",
                         reply_markup=markup)
    elif (id_telegram == id_user) and (estado == 1) and plano == "Ouro":

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Lista de Sinais')
        itembtnb = types.KeyboardButton('MHI')
        itembtnc = types.KeyboardButton('Catalogador de Sinais')
        itembtnd = types.KeyboardButton('Estratégia Chinesa')
        itembtne = types.KeyboardButton('CopyTrade')
        itembtng = types.KeyboardButton('Estratégia Berman')
        itembtnf = types.KeyboardButton('Indicadores Técnicos')
        itembtnh = types.KeyboardButton('Scalper')
        itembtni = types.KeyboardButton('✅Fazer Login')
        markup.row(itembtni)
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtng, itembtnf, itembtnh)
        bot.send_message(message.chat.id,
                         "Bots disponíveis para o plano ouro",
                         reply_markup=markup)
    elif (id_telegram == id_user) and (plano == "Grátis" or plano == "Bronze"
                                       or plano == "Prata"
                                       or plano == "Ouro") and estado != 1:
        bot.send_message(
            message.chat.id,
            "Por Algum motivo você já não tem acesso ao Bot." +
            "\nContacte o suporte para lhe prestar ajuda: --> @Zcreations1")

    elif ((id_telegram == id_user) and (estado == 1)
          and plano == "admin") or ((id_telegram == id_user) and
                                    (estado == 1) and plano == "super_admin"):

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Lista de Sinais')
        itembtnb = types.KeyboardButton('MHI')
        itembtnc = types.KeyboardButton('Catalogador de Sinais')
        itembtnd = types.KeyboardButton('Estratégia Chinesa')
        itembtne = types.KeyboardButton('CopyTrade')
        itembtng = types.KeyboardButton('Estratégia Berman')
        itembtnf = types.KeyboardButton('Indicadores Técnicos')
        itembtni = types.KeyboardButton('Scalper')
        itembtnh = types.KeyboardButton('🔙VOLTAR')
        itembtnj = types.KeyboardButton('✅Fazer Login')
        markup.row(itembtnj)
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtng, itembtnf, itembtni)
        markup.row(itembtnh)
        bot.send_message(message.chat.id,
                         "====Bots Disponíveis====",
                         reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Lista de Sinais')
def bot_lista_sinais(message):

    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar Bot de Sinais')
    itembtnb = types.KeyboardButton('🔴Desligar Bot de Sinais')
    itembtnc = types.KeyboardButton('Adicionar Sinais')
    itembtnd = types.KeyboardButton('⚙Configurar Bot de Sinais')
    itembtne = types.KeyboardButton('🆘Ajuda')
    itembtnf = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnd)
    markup.row(itembtnc, itembtne)
    markup.row(itembtnf)
    bot.send_message(message.chat.id,"Bot de lista de sinais",reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == '✅Ligar Bot de Sinais')
    def ligar_lista(message):
        global ligado
        ligado = True
        bot.send_message(message.chat.id, "✅Bot de Lista de sinais✅")
        chat_id = message.chat.id
        dados_config_lista_sinais = config_lista_sinais[chat_id]
        dados_config_login = login_dict[chat_id]
        id_user = message.from_user.id
        dados_cli = cliente_permitido(str(id_user))
        if len(dados_cli) > 0:
            for data in dados_cli:
                id_telegram = int(data['id_telegram'])
                estado = int(data['estado'])
                plano = str(data['plano'])
                mes_espiracao = int(data['mes_espiracao'])
        def stop(lucro, gain, loss):
            if lucro <= float('-' + str(abs(loss))):
                bot.send_message(message.chat.id, '🔴Stop Loss batido!')
                return
            if lucro >= float(abs(gain)):
                bot.send_message(message.chat.id, '✅Stop Gain Batido!')
                return

        def Martingale(valor, payout):
            lucro_esperado = valor * payout
            perca = float(valor)

            while True:
                if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
                    return round(valor, 2)
                    break
                valor += 0.01

        def Payout(par):
            API.subscribe_strike_list(par, 1)
            while True:
                d = API.get_digital_current_profit(par, 1)
                if d != False:
                    d = round(int(d) / 100, 2)
                    break
                time.sleep(1)
            API.unsubscribe_strike_list(par, 1)

            return d

        if (dados_config_login.email == None) or (dados_config_login.senha == None):
            bot.send_message(message.chat.id,'🚨Erro verifique os dados de Login, tente novamente🚨')
        else:
            usuario = dados_config_login.email  # input("Digite o usuário da IQ Option: ")
            senha = dados_config_login.senha  #getpass.getpass(f"Digite a senha da IQ Option: ")
            API = IQ_Option(usuario, senha)
            print(API.connect())

        if API.check_connect():
            bot.send_message(message.chat.id, '✅Conectado com sucesso!✅')
        else:
            bot.send_message(message.chat.id, '🚨Erro ao se conectar🚨')
            return

        try:
            conta = int(dados_config_lista_sinais.conta)  
            if int(conta) == 1:
                API.change_balance('PRACTICE')
            elif int(conta) == 2:
                API.change_balance('REAL')  # PRACTICE / REAL
            else:
                bot.send_message(message.chat.id,
                                 "❌Erro ao escolher o tipo de conta❌")
        except:
            bot.send_message(message.chat.id, "❌Erro, tente novamente❌")
            return

        while True:
            try:
                operacao = int(dados_config_lista_sinais.operacao)  
                if operacao > 0 and operacao < 3: break
            except:
                bot.send_message(message.chat.id,'❌Opção de escolha entre digital e binária errada❌')
                break

        def get_sinal():
            sinais=[]
            arq_sinais = "{}.txt".format(id_user)
            try:
                file = open(arq_sinais, 'r').read()
            except:
                print("Todos os sinais já foram analisados.")
                exit()
            for index,sinal in enumerate(file.split('\n')):
                if len(sinal) > 0 and sinal != '':
                    sinal_ = sinal.split(',')
                    #formato da lista: TIMESTAMP,PARIDADE,call,1
                    if sinal_[0] == datetime.now().strftime('%H:%M'):

                            sinais.append({'timestamp': sinal_[0],
                                            'par': sinal_[1],
                                            'dir': sinal_[2],
                                            'timeframe': sinal_[3]})
                            open(arq_sinais, 'w').write(file.replace(sinal, ''))
            return sinais

        valor_entrada = float(dados_config_lista_sinais.valor_entrada)
        valor_entrada_b = float(valor_entrada)

        martingale = int(dados_config_lista_sinais.martingale)
        martingale += 1

        stop_loss = float(dados_config_lista_sinais.stop_loss)
        stop_gain = float(dados_config_lista_sinais.stop_gain)

        lucro = 0
        bot.send_message(
            message.chat.id, "✅Aguarde os resultados das suas operações✅\n" +
            "\t\t\tProcessando...")
        ops=0
        try:

            while True:
                sinais = get_sinal()

                if len(sinais) > 0:
                    for data in sinais:
                        valor_entrada = valor_entrada_b
                        par=str(data['par']).upper()
                        dir=str(data['dir']).lower()
                        time_frame=int(data['timeframe'])
                        payout = Payout(par)    

                        valor_entrada = valor_entrada_b
                        for i in range(martingale):
                        
                            status,id = API.buy_digital_spot(par, valor_entrada, dir, time_frame) if operacao == 1 else API.buy(valor_entrada, par, dir, time_frame)
                            bot.send_message(message.chat.id,"✅Uma operações em andamento✅\n" +
                                                                "Paridade: "+str(par)+
                                                                "\nDireção: "+str(dir)+
                                                                "\nTime Frame: "+str(time_frame)+
                                                                "\nPayout: "+str(payout))
                            if status:
                                while True:
                                    try:
                                        status,valor = API.check_win_digital_v2(id) if operacao == 1 else API.check_win_v3(id)
                                    except:
                                        status = True
                                        valor = 0
                                    
                                    if status:
                                        valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
                                        lucro += round(valor, 2)
                                        
                                        msg = '''
                                💹Resultado da operação💹\n

                                RESULTADO: ''' + ('✅WIN' if valor > 0 else '🚨LOSS') + '''
                                LUCRO: 💲''' + str(round(valor, 2)) + '''\n
                                ''' + (str(i)+ ' ♻GALE' if i > 0 else '') + '''\n'''
                                        bot.send_message(message.chat.id,msg)
                                    
                                        valor_entrada = Martingale(valor_entrada, payout)
                                        if lucro <= float('-' +str(abs(stop_loss))):
                                            bot.send_message(message.chat.id,'🔴Stop Loss batido!')
                                            return
                                            break
                                        if lucro >= float(abs(stop_gain)):
                                            bot.send_message(message.chat.id,'✅Stop Gain Batido!')
                                            return
                                            break
                                        if valor > 0 : break
                                        break
                                if valor > 0 : break
                            else:
                                bot.send_message(message.chat.id,'🚨ERRO AO REALIZAR OPERAÇÃO\n' +
                                'O activo selecionado não se encontra aberto.')
                                break
                print(ops+1, 'Operações abertas |', datetime.now().strftime('%H:%M:%S'), end='\r')
        except Exception as e:
                        print("O Bot encontrou o erro abaixo:\n",e+'')

    @bot.message_handler(func=lambda message: message.text == '🔴Desligar Bot de Sinais')
    def desligar_lista(message):
        bot.send_message(message.chat.id,"✅Bot de Lista de sinais desligado!✅")
        exit()

@bot.message_handler(func=lambda message: message.text == 'MHI')
def bot_mhi(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar Bot de MHI')
    itembtnb = types.KeyboardButton('🔴Desligar Bot de MHI')
    itembtnc = types.KeyboardButton('⚙Configurar Bot de MHI')
    itembtnd = types.KeyboardButton('🆘Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id, "Bot de MHI", reply_markup=markup)
    
    @bot.message_handler(func=lambda message: message.text == '✅Ligar Bot de MHI')
    def ligar(message):
        global ligado
        ligado = True
        bot.send_message(message.chat.id, "✅Bot de MHI ligado✅")
        chat_id = message.chat.id
        dados_config_mhi = config_mhi[chat_id]
        dados_config_login = login_dict[chat_id]
        id_user = message.from_user.id
        dados_cli = cliente_permitido(str(id_user))
        if len(dados_cli) > 0:
            for data in dados_cli:
                id_telegram = int(data['id_telegram'])
                estado = int(data['estado'])
                plano = str(data['plano'])
                mes_espiracao = int(data['mes_espiracao'])
        
        def Martingale(valor, payout):
            lucro_esperado = valor * payout
            perca = float(valor)

            while True:
                if round(valor * payout, 2) > round(
                        abs(perca) + lucro_esperado, 2):
                    return round(valor, 2)
                    break
                valor += 0.01

        def Payout(par):
            API.subscribe_strike_list(par, 1)
            while True:
                d = API.get_digital_current_profit(par, 1)
                if d != False:
                    d = round(int(d) / 100, 2)
                    break
                time.sleep(1)
            API.unsubscribe_strike_list(par, 1)

            return d

        if (dados_config_login.email == None) or (dados_config_login.senha
                                                  == None):
            bot.send_message(
                message.chat.id,
                '🚨Erro verifique os dados de Login e tente novamente🚨')
        else:
            usuario = dados_config_login.email  # input("Digite o usuário da IQ Option: ")
            senha = dados_config_login.senha  #getpass.getpass(f"Digite a senha da IQ Option: ")
            API = IQ_Option(usuario, senha)
            print(API.connect())

        if API.check_connect():
            bot.send_message(message.chat.id, '✅Conectado com sucesso!✅')
        else:
            bot.send_message(message.chat.id, '🚨Erro ao se conectar🚨')
            return

        try:

            conta = int(
                dados_config_mhi.conta
            )  #int(input('\nEscolha em qual conta Operar:\n 1 - Treinamento\n 2 - REAL\n:: '))

            if int(conta) == 1:
                API.change_balance('PRACTICE')
            elif int(conta) == 2:
                API.change_balance('REAL')  # PRACTICE / REAL
            else:
                bot.send_message(message.chat.id,
                                 "❌Erro ao escolher o tipo de conta❌")
        except:
            bot.send_message(message.chat.id, "❌Erro, tente novamente❌")
            return

        while True:
            try:
                operacao = int(
                    dados_config_mhi.operacao
                )  #int(input('\n Deseja operar na\n  1 - Digital\n  2 - Binaria\n  :: '))

                if operacao > 0 and operacao < 3: break
            except:
                bot.send_message(
                    message.chat.id,
                    '❌Opção de escolha entre digital e binária errada❌')
                break

        while True:
            try:
                tipo_mhi = int(
                    dados_config_mhi.tipo_mhi
                )  #int(input('Deseja operar a favor da\n  1 - Minoria\n  2 - Maioria\n  :: '))

                if tipo_mhi > 0 and tipo_mhi < 3: break
            except:
                bot.send_message(message.chat.id, '❌Tipo de HMI incorreto❌')
                break

        while True:
            try:
                time_frame = int(dados_config_mhi.time_frame)
                break
            except:
                bot.send_message(message.chat.id, '❌Time frame incorreto❌')
                break

        par = str(dados_config_mhi.par).upper()
        valor_entrada = float(dados_config_mhi.valor_entrada)
        valor_entrada_b = float(valor_entrada)

        martingale = int(dados_config_mhi.martingale)
        martingale += 1

        stop_loss = float(dados_config_mhi.stop_loss)
        stop_gain = float(dados_config_mhi.stop_gain)

        lucro = 0
        payout = Payout(par)
        bot.send_message(
            message.chat.id, "✅Aguarde os resultados das suas operações✅\n" +
            "\t\t\tProcessando...")
        
        while ligado:
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58
                              and minutos <= 5) or minutos >= 9.58 else False

            if entrar:
                dir = False
                velas = API.get_candles(par, 60, 3, time.time())

                velas[0] = 'g' if velas[0]['open'] < velas[0][
                    'close'] else 'r' if velas[0]['open'] > velas[0][
                        'close'] else 'd'
                velas[1] = 'g' if velas[1]['open'] < velas[1][
                    'close'] else 'r' if velas[1]['open'] > velas[1][
                        'close'] else 'd'
                velas[2] = 'g' if velas[2]['open'] < velas[2][
                    'close'] else 'r' if velas[2]['open'] > velas[2][
                        'close'] else 'd'

                cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]

                if cores.count('g') > cores.count('r') and cores.count(
                        'd') == 0:
                    dir = ('put' if tipo_mhi == 1 else 'call')
                if cores.count('r') > cores.count('g') and cores.count(
                        'd') == 0:
                    dir = ('call' if tipo_mhi == 1 else 'put')

                if dir:

                    bot.send_message(
                        message.chat.id, '✅Uma operação em andamento✅' +
                        '\nTempo de análise: ' + str(minutos) + '⏰' +
                        '\nCor da entrada: ' +
                        str('💹' if dir == 'call' else '🚨') + '\nDireção: ' +
                        str('Compra' if dir == 'call' else 'Venda'))

                    valor_entrada = valor_entrada_b
                    for i in range(martingale):

                        status, id = API.buy_digital_spot(
                            par, valor_entrada, dir,
                            time_frame) if operacao == 1 else API.buy(
                                valor_entrada, par, dir, time_frame)

                        if status:
                            while True:
                                try:
                                    status, valor = API.check_win_digital_v2(
                                        id
                                    ) if operacao == 1 else API.check_win_v3(
                                        id)
                                except:
                                    status = True
                                    valor = 0

                                if status:
                                    valor = valor if valor > 0 else float(
                                        '-' + str(abs(valor_entrada)))
                                    lucro += round(valor, 2)

                                    msg = '''
                            💹Resultado da operação💹\n

                            RESULTADO: ''' + ('✅WIN' if valor > 0 else '🚨LOSS') + '''
                            LUCRO: 💲''' + str(round(valor, 2)) + '''\n
                            ''' + (str(i)+ ' ♻GALE' if i > 0 else '') + '''\n'''
                                    bot.send_message(message.chat.id,msg)

                                    valor_entrada = Martingale(valor_entrada, payout)

                                    if lucro <= float('-' +str(abs(stop_loss))):
                                        bot.send_message(message.chat.id,'🔴Stop Loss batido!')
                                        return
                                        break
                                    if lucro >= float(abs(stop_gain)):
                                        bot.send_message(message.chat.id,'✅Stop Gain Batido!')
                                        return
                                        break

                                    if valor > 0: break

                                    break

                            if valor > 0: break

                        else:
                            bot.send_message(message.chat.id,'🚨ERRO AO REALIZAR OPERAÇÃO\n' +
                                'O activo selecionado não se encontra aberto.')
                            break
                            return

    @bot.message_handler(func=lambda message: message.text == '🔴Desligar Bot de MHI')
    def desligar(message):
        global ligado
        ligado = False
        bot.send_message(message.chat.id,"✅Bot de MHI desligado!✅")
        
@bot.message_handler(func=lambda message: message.text == '🆘Ajuda')
def ajuda(message):
    bot.send_message(message.chat.id,"Olá " + message.from_user.first_name + " caso tenhas algum\n" +
        "problema com o bot, contacte o suporte--> @Zcreations1")

@bot.message_handler(func=lambda message: message.text == 'Estratégia Chinesa')
def bot_estrategia_chinesa(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id,"Bot de Estratégia Chinesa",reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'CopyTrade')
def bot_copytrade(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id, "Bot de CopyTrade", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Estratégia Berman')
def bot_estrategia_berman(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id,"Bot de Estratégia Berman",reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Catalogador de Sinais')
async def bot_catalogador(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id,"Catalogação de Sinais",reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Indicadores Técnicos')
def bot_indicadores_tecnicos(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id, "Indicador Técnico", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Scalper')
def bot_scalper(message):
    markup = types.ReplyKeyboardMarkup(row_width=-1)
    itembtna = types.KeyboardButton('✅Ligar')
    itembtnb = types.KeyboardButton('Desligar')
    itembtnc = types.KeyboardButton('Configurações')
    itembtnd = types.KeyboardButton('Ajuda')
    itembtne = types.KeyboardButton('🤖Listar Bots')
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc)
    markup.row(itembtnd, itembtne)
    bot.send_message(message.chat.id, "Bot de Scalper", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🔙VOLTAR')
def voltar(message):
    id_user = message.from_user.id
    dados_cli = cliente_permitido(str(id_user))
    if len(dados_cli) > 0:
        for data in dados_cli:
            id_telegram = int(data['id_telegram'])
            estado = int(data['estado'])
            plano = str(data['plano'])
            mes_espiracao = int(data['mes_espiracao'])
    if message.chat.type == "private" and estado == 1 and plano == "admin":

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('Prestar Suporte')
        itembtnb = types.KeyboardButton('Dados do Usuário')
        itembtnc = types.KeyboardButton('✅Usuários Ativos')
        itembtnd = types.KeyboardButton('Pacotes disponíveis')
        itembtne = types.KeyboardButton('Verificação de Usuário')
        itembtng = types.KeyboardButton('🤖Listar Bots')
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtng)
        bot.send_message(message.chat.id,
                         "=======ROBÔ ALPHA=======",
                         reply_markup=markup)

    elif message.chat.type == "private" and estado == 1 and plano == "super_admin":

        markup = types.ReplyKeyboardMarkup(row_width=-1)
        itembtna = types.KeyboardButton('✅Add usuário')
        itembtnb = types.KeyboardButton('Excluir usuário')
        itembtnc = types.KeyboardButton('Listar usuários')
        itembtnd = types.KeyboardButton('Alterar Pacote')
        itembtne = types.KeyboardButton('Alterar data de expiração')
        itembtnf = types.KeyboardButton('Restringir usuário')
        itembtng = types.KeyboardButton('🤖Listar Bots')
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd, itembtne)
        markup.row(itembtnf, itembtng)
        bot.send_message(message.chat.id,
                         "=======ROBÔ ALPHA=======",
                         reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '✅Fazer Login')
def fazer_login(message):
    msg = bot.reply_to(message,
                       "🔐Entrar na iq Option🔐\n" + "Digite seu Email:")
    bot.register_next_step_handler(msg, process_email_step)

def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        if (email == None) or (email == ''):
            msg = bot.reply_to(message,
                               '❌O campo e-mail não pode estar vazio❌')
            bot.register_next_step_handler(msg, process_email_step)
            return
        dados = login(email)
        login_dict[chat_id] = dados
        msg = bot.reply_to(message, '🔑Digite sua Senha🔑')
        bot.register_next_step_handler(msg, process_senha_step)
    except Exception as e:
        bot.reply_to(message,
                     '❌Upsi, ocorreu um erro, tente novamente /start❌')

def process_senha_step(message):
    try:
        chat_id = message.chat.id
        senha = message.text
        if (senha == None) or (senha == ''):
            msg = bot.reply_to(message, '❌O campo senha não pode estar vazio❌')
            bot.register_next_step_handler(msg, process_senha_step)
            return
        dados = login_dict[chat_id]
        dados.senha = senha
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('✅Salvar', '🔙Cancelar')
        msg = bot.reply_to(message,
                           '✅Desejas salvar os dados?✅',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, salvar_iq_option)
    except Exception as e:
        bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def salvar_iq_option(message):
    try:
        chat_id = message.chat.id
        salvar = message.text
        dados = login_dict[chat_id]
        id_user = message.from_user.id
        dados_cli = cliente_permitido(str(id_user))
        if len(dados_cli) > 0:
            for data in dados_cli:
                id_telegram = int(data['id_telegram'])
                estado = int(data['estado'])
                plano = str(data['plano'])
                mes_espiracao = int(data['mes_espiracao'])

        if (salvar == u'✅Salvar') and estado == 1:

            bot.send_message(
                message.chat.id, "✅Dados salvos com sucesso✅" + "\nEmail: " +
                str(dados.email) + "\nSenha: " + str(dados.senha))
            listar_bots(message)

        elif (salvar == u'🔙Cancelar'):
            dados.email = None
            dados.senha = None
            listar_bots(message)
    except Exception as e:
        bot.reply_to(message, 'Email/Senha não foram salvos!' +
            '\nOpção inválida por falta de email e senha')

@bot.message_handler(func=lambda message: message.text == 'Adicionar Sinais')
def add_lista(message):
        msg=bot.reply_to(message, "✅Digite sua lista de sinais✅"
                                         +"\nPara tal tenha em conta o seguinte formato:\n"+
                                         "07:25,EURUSD-OTC,call,5 ou 07:25,EURUSD,put,1")
        bot.register_next_step_handler(msg, process_add_lista_step)

def process_add_lista_step(message):
        try:
            lista = message.text
            if lista != '':
                git_file ='{}.txt'.format(message.chat.id)
                if git_file in content:
                    contents = repo.get_contents("{}.txt".format(message.chat.id))
                    repo.delete_file(contents.path, "remove {}.txt".format(message.chat.id), contents.sha)
                    repo.create_file(git_file, "committing files", lista)
                else:
                    repo.create_file(git_file, "committing files", lista)
            else:
                bot.reply_to(message, 'Envie pelo menos um sinal')

            bot_lista_sinais(message)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

@bot.message_handler(func=lambda message: message.text == '⚙Configurar Bot de MHI')
def config_do_mhi(message):
        msg = bot.reply_to(
            message,"Escolha em qual conta Operar:\n 1 - Treinamento\n 2 - REAL:")
        bot.register_next_step_handler(msg, process_conta_step)

def process_conta_step(message):
        try:
            chat_id = message.chat.id
            conta = message.text
            if (not conta.isdigit()):
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, escolha: \n1 para conta de Treinamento \n2 para Real'
                )
                bot.register_next_step_handler(msg, process_conta_step)
                return
            dados = mhi_config(conta)
            config_mhi[chat_id] = dados
            msg = bot.reply_to(message,
                            'Desejas operar na\n  1 - Digital\n  2 - Binaria:')
            bot.register_next_step_handler(msg, process_operacao_step)
        except Exception as e:
            bot.reply_to(message,
                        '❌Upsi, ocorreu um erro, tente novamente /start❌')

def process_operacao_step(message):
        try:
            chat_id = message.chat.id
            operacao = message.text
            if (not operacao.isdigit()):
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, escolha: \n1 para Digital \n2 para Binaria:')
                bot.register_next_step_handler(msg, process_operacao_step)
                return
            dados = config_mhi[chat_id]
            dados.operacao = operacao
            msg = bot.reply_to(
                message,
                'Desejas operar a favor da\n  1 - Minoria\n  2 - Maioria:')
            bot.register_next_step_handler(msg, process_tipo_mhi_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_tipo_mhi_step(message):
        try:
            chat_id = message.chat.id
            tipo_mhi = message.text
            if (not tipo_mhi.isdigit()):
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, escolha: \n1 para Minoria \n2 para Maioria:')
                bot.register_next_step_handler(msg, process_tipo_mhi_step)
                return
            dados = config_mhi[chat_id]
            dados.tipo_mhi = tipo_mhi
            msg = bot.reply_to(
                message, 'Selecione o Time Frame\n' +
                'Obs.: o Bot opera apenas em M1, M5 e M15\n' +
                'Digite 1 para M1, 5 para M5 e 15 para M15')
            bot.register_next_step_handler(msg, process_time_frame_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_time_frame_step(message):
        try:
            chat_id = message.chat.id
            time_frame = message.text
            if not time_frame.isdigit():
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, escolha: \n1 para M1, 5 para M5 ou 15 para M15:'
                )
                bot.register_next_step_handler(msg, process_time_frame_step)
                return
            dados = config_mhi[chat_id]
            dados.time_frame = time_frame
            msg = bot.reply_to(
                message, 'Digite a paradidade por onde operar\n' +
                'Lembre-se de selecionar apenas paridades abertas\n' +
                'Ex.: EURUSD ou então EURUSD-OTC para mercado OTC:')
            bot.register_next_step_handler(msg, process_par_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_par_step(message):
        try:
            chat_id = message.chat.id
            par = message.text
            if par.isdigit() or par == '':
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, escolha por Ex.: EURUSD ou EURUSD-OTC:')
                bot.register_next_step_handler(msg, process_par_step)
                return
            dados = config_mhi[chat_id]
            dados.par = par
            msg = bot.reply_to(message, 'Digite o valor de entrada')
            bot.register_next_step_handler(msg, process_valor_entrada_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_valor_entrada_step(message):
        try:
            chat_id = message.chat.id
            valor_entrada = message.text
            if float(valor_entrada) < 1:
                msg = bot.reply_to(message,
                                '❌O valor de entrada não pode ser menor que 1')
                bot.register_next_step_handler(msg, process_valor_entrada_step)
                return
            dados = config_mhi[chat_id]
            dados.valor_entrada = valor_entrada
            msg = bot.reply_to(
                message, 'Indique a quantidade de Martingale\n' +
                'Coloque 0 caso não queiras utilizá-lo\n' +
                'Aconcelho indicar no máximo 2 níveis de Martingale')
            bot.register_next_step_handler(msg, process_martingale_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_martingale_step(message):
        try:
            chat_id = message.chat.id
            martingale = message.text
            if (not martingale.isdigit()):
                msg = bot.reply_to(
                    message, '❌Opção inválida, digite apenas número inteiros')
                bot.register_next_step_handler(msg, process_martingale_step)
                return
            dados = config_mhi[chat_id]
            dados.martingale = martingale
            msg = bot.reply_to(message, 'Digite o valor do stop Loss')
            bot.register_next_step_handler(msg, process_stop_loss_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_stop_loss_step(message):
        try:
            chat_id = message.chat.id
            stop_loss = message.text
            if float(stop_loss) < 1:
                msg = bot.reply_to(
                    message,
                    '❌Opção inválida, digite apenas números e maior ou igual a 1')
                bot.register_next_step_handler(msg, process_stop_loss_step)
                return
            dados = config_mhi[chat_id]
            dados.stop_loss = stop_loss
            msg = bot.reply_to(message, 'Digite o valor do Stop Gain')
            bot.register_next_step_handler(msg, process_stop_gain_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_stop_gain_step(message):
        try:
            chat_id = message.chat.id
            stop_gain = message.text
            if float(stop_gain) < 1:
                msg = bot.reply_to(
                    message, '❌Opção inválida, digite apenas número e maior que 0')
                bot.register_next_step_handler(msg, process_stop_gain_step)
                return
            dados = config_mhi[chat_id]
            dados.stop_gain = stop_gain
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('✅Guardar', 'Alterar')
            msg = bot.reply_to(message,
                            '✅Desejas guardar os dados?✅',
                            reply_markup=markup)
            bot.register_next_step_handler(msg, process_guardar_mhi_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_guardar_mhi_step(message):
        try:
            chat_id = message.chat.id
            salvar = message.text
            dados = config_mhi[chat_id]
            if salvar == u'✅Guardar':

                bot.send_message(message.chat.id, '✅Dados inseridos com sucesso✅' +
                    '\nTipo de Conta: '+('Real' if int(dados.conta)==2 else 'Treinamento')
                    +'\nOperar na: '+('Digital' if int(dados.operacao)==1 else 'Binária') 
                    +'\nTipo de MHI: '+ 'Minoria' if int(dados.tipo_mhi)==1 else 'Maioria' +
                    '\nTime Frame: M' + str(dados.time_frame) + '\nParidade: ' +
                    str(dados.par) + '\nValor de entrada: ' +
                    str(dados.valor_entrada) + '\nNível de Martingale:' +
                    str(dados.martingale) + '\nStop Loss: ' +
                    str(dados.stop_loss) + '\nStop Gain: ' + str(dados.stop_gain))

                bot_mhi(message)

            elif salvar == u'Alterar':
                bot.register_next_step_handler(chat_id, process_conta_step)
            else:
                dados.conta = None
                dados.operacao = None
                dados.tipo_mhi = None
                dados.time_frame == None
                dados.par = None
                dados.valor_entrada = None
                dados.martingale = None
                dados.stop_loss == None
                dados.stop_gain = None
                bot_mhi(message)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

@bot.message_handler(func=lambda message: message.text == '⚙Configurar Bot de Sinais')
def config_da_lista_de_sinais(message):
        msg = bot.reply_to(message,"Escolha em qual conta Operar:\n 1 - Treinamento\n 2 - REAL:")
        bot.register_next_step_handler(msg, process_conta_sinais_step)

def process_conta_sinais_step(message):
        try:
            chat_id = message.chat.id
            conta = message.text
            if (not conta.isdigit()):
                msg = bot.reply_to(message,'❌Opção inválida, escolha: \n1 para conta de Treinamento \n2 para Real')
                bot.register_next_step_handler(msg, process_conta_sinais_step)
                return
            dados = lista_sinais_config(conta)
            config_lista_sinais[chat_id] = dados
            msg = bot.reply_to(message,'Desejas operar na\n  1 - Digital\n  2 - Binaria:')
            bot.register_next_step_handler(msg, process_operacao_sinais_step)
        except Exception as e:
            bot.reply_to(message,
                        '❌Upsi, ocorreu um erro, tente novamente /start❌')

def process_operacao_sinais_step(message):
        try:
            chat_id = message.chat.id
            operacao = message.text
            if (not operacao.isdigit()):
                msg = bot.reply_to(message,'❌Opção inválida, escolha: \n1 para Digital \n2 para Binaria:')
                bot.register_next_step_handler(msg, process_operacao_sinais_step)
                return
            dados = config_lista_sinais[chat_id]
            dados.operacao = operacao
            msg = bot.reply_to(message,'Digite o valor de entrada')
            bot.register_next_step_handler(msg, process_valor_entrada_sinais_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_valor_entrada_sinais_step(message):
        try:
            chat_id = message.chat.id
            valor_entrada = message.text
            if float(valor_entrada) < 1:
                msg = bot.reply_to(message,'❌O valor de entrada não pode ser menor que 1')
                bot.register_next_step_handler(msg, process_valor_entrada_sinais_step)
                return
            dados = config_lista_sinais[chat_id]
            dados.valor_entrada = valor_entrada
            msg = bot.reply_to(message, 'Indique a quantidade de Martingale\n' +
                'Coloque 0 caso não queiras utilizá-lo\n' +
                'Aconcelho indicar no máximo 2 níveis de Martingale')
            bot.register_next_step_handler(msg, process_martingale_sinais_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_martingale_sinais_step(message):
        try:
            chat_id = message.chat.id
            martingale = message.text
            if (not martingale.isdigit()):
                msg = bot.reply_to(message, '❌Opção inválida, digite apenas número inteiros')
                bot.register_next_step_handler(msg, process_martingale_sinais_step)
                return
            dados = config_lista_sinais[chat_id]
            dados.martingale = martingale
            msg = bot.reply_to(message, 'Digite o valor do stop Loss')
            bot.register_next_step_handler(msg, process_stop_loss_sinais_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_stop_loss_sinais_step(message):
        try:
            chat_id = message.chat.id
            stop_loss = message.text
            if float(stop_loss) < 1:
                msg = bot.reply_to(message,'❌Opção inválida, digite apenas números e maior ou igual a 1')
                bot.register_next_step_handler(msg, process_stop_loss_sinais_step)
                return
            dados = config_lista_sinais[chat_id]
            dados.stop_loss = stop_loss
            msg = bot.reply_to(message, 'Digite o valor do Stop Gain')
            bot.register_next_step_handler(msg, process_stop_gain_sinais_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_stop_gain_sinais_step(message):
        try:
            chat_id = message.chat.id
            stop_gain = message.text
            if float(stop_gain) < 1:
                msg = bot.reply_to(message,'❌Opção inválida, digite apenas número e maior que 0')
                bot.register_next_step_handler(msg, process_stop_gain_sinais_step)
                return
            dados = config_lista_sinais[chat_id]
            dados.stop_gain = stop_gain
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('✅Guardar', 'Alterar')
            msg = bot.reply_to(message,'✅Desejas guardar os dados?✅',reply_markup=markup)
            bot.register_next_step_handler(msg, process_guardar_sinais_step)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')

def process_guardar_sinais_step(message):
        try:
            chat_id = message.chat.id
            salvar = message.text
            dados = config_lista_sinais[chat_id]
            if salvar == u'✅Guardar':

                bot.send_message(message.chat.id, '✅Dados inseridos com sucesso✅' +
                    '\nTipo de Conta: '+('Real' if int(dados.conta)==2 else 'Treinamento')
                    +'\nOperar na: '+('Digital' if int(dados.operacao)==1 else 'Binária')
                    +'\nValor de entrada: '+str(dados.valor_entrada) + 
                    '\nNível de Martingale:' +str(dados.martingale) + '\nStop Loss: ' +
                    str(dados.stop_loss) + '\nStop Gain: ' + str(dados.stop_gain))

                bot_lista_sinais(message)

            elif salvar == u'Alterar':
                bot.register_next_step_handler(chat_id, process_conta_sinais_step)
            else:
                dados.conta = None
                dados.operacao = None
                dados.valor_entrada = None
                dados.martingale = None
                dados.stop_loss == None
                dados.stop_gain = None
                bot_lista_sinais(message)
        except Exception as e:
            bot.reply_to(message, '❌Upsi, houve um erro, tente novamente➡ /start')
            
time.sleep(1)
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling(allowed_updates=util.update_types)
