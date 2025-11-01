# inserir_dados.py

import sqlite3
import os
import datetime
import random

# Nome do arquivo do banco de dados
DB_FILE = "db.sqlite3"

# Verifica se o banco de dados existe
if not os.path.exists(DB_FILE):
    print(f"Erro: O arquivo de banco de dados '{DB_FILE}' não foi encontrado.")
    print("Por favor, rode 'python manage.py migrate' primeiro.")
    exit()

print("Conectando ao banco de dados...")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    print("Limpando dados antigos...")
    cursor.executescript("""
        DELETE FROM usuario_agendamento;
        DELETE FROM usuario_horariosdisponiveis;
        DELETE FROM usuario_tiposdevisita;
        DELETE FROM sqlite_sequence WHERE name IN ('usuario_agendamento', 'usuario_horariosdisponiveis', 'usuario_tiposdevisita');
    """)

    print("Cadastrando Tipos de Visita...")
    cursor.executescript("""
        INSERT INTO usuario_tiposdevisita (id, titulo, capacidade_maxima_pessoas, preco_grupo_fechado) VALUES
        (1, 'Visita com Educador (Escolas/Grupos)', 40, 250.00),
        (2, 'Visita Livre (Individual ou Família)', 15, 0.00);
    """)

    print("Gerando agenda de horários para o próximo ano...")
    horarios_para_inserir = []
    hoje = datetime.date.today()
    dias_para_gerar = 365

    for i in range(dias_para_gerar):
        dia_atual = hoje + datetime.timedelta(days=i)
        # Pula as segundas-feiras
        if dia_atual.weekday() == 0:
            continue

        # Horários da manhã
        for inicio, fim in [('09:00:00', '10:30:00'), ('10:30:00', '12:00:00')]:
            horarios_para_inserir.append((1, dia_atual.strftime('%Y-%m-%d'), inicio, fim, random.choice([0, 1, 1, 1])))
        # Horários da tarde
        for inicio, fim in [('14:00:00', '15:30:00'), ('15:30:00', '17:00:00')]:
            horarios_para_inserir.append((random.choice([1,2]), dia_atual.strftime('%Y-%m-%d'), inicio, fim, random.choice([0, 1])))

    if horarios_para_inserir:
        cursor.executemany("INSERT INTO usuario_horariosdisponiveis (tipo_visita_id, data, hora_inicio, hora_fim, grupos_disponiveis) VALUES (?, ?, ?, ?, ?)", horarios_para_inserir)
        print(f"{len(horarios_para_inserir)} horários disponíveis foram criados.")

    print("Criando 10 agendamentos de teste pendentes...")
    horarios_ids = cursor.execute("SELECT id FROM usuario_horariosdisponiveis WHERE data > ? AND grupos_disponiveis > 0 LIMIT 10", (hoje.strftime('%Y-%m-%d'),)).fetchall()

    if len(horarios_ids) >= 10:
        agendamentos = []
        nomes = ["Mariana Costa", "Ricardo Lima", "Beatriz Almeida", "Lucas Ferreira", "Júlia Santos", "Guilherme Oliveira", "Sofia Rodrigues", "Enzo Pereira", "Laura Gonçalves", "Felipe Martins"]
        for i, nome in enumerate(nomes):
            data_criacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            agendamentos.append((
                nome, f"{nome.lower().replace(' ', '.')}@emailteste.com", f"849{random.randint(98000000,99999999)}",
                horarios_ids[i][0], 'Pendente', random.randint(1,5), random.randint(5,30), random.randint(0,3),
                f'Instituição de Teste {i+1}', 200.00, data_criacao
            ))
        
        cursor.executemany("""
            INSERT INTO usuario_agendamento (
                nome_completo, email, telefone, horario_id, status, 
                quantidade_inteira, quantidade_meia, quantidade_gratuidade, 
                nome_instituicao, valor_total, data_agendamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, agendamentos)
        print(f"{len(agendamentos)} agendamentos pendentes foram criados.")
    
    conn.commit()
    print(f"\n✅ Dados de teste em massa inseridos com sucesso!")

except sqlite3.Error as e:
    print(f"\n❌ Ocorreu um erro ao inserir os dados: {e}")
finally:
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")