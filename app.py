# app.py
import streamlit as st
import os
import struct
from tabela_hash import HashExtensivel, RegistroHashExtensivel

# Classe de Registro
class TestRecord(RegistroHashExtensivel):
    def __init__(self, key: int = 0, value: str = ""):
        self.key = key
        self.value = value

    def hash_code(self) -> int:
        return self.key

    def size(self) -> int:
        return 4 + 20

    def to_byte_array(self) -> bytes:
        value_bytes = self.value.encode('utf-8')[:20]
        value_bytes += b' ' * (20 - len(value_bytes))
        return struct.pack('>i', self.key) + value_bytes

    def from_byte_array(self, ba: bytes):
        self.key = struct.unpack('>i', ba[:4])[0]
        self.value = ba[4:24].decode('utf-8').rstrip()

    def __str__(self):
        return f"({self.key}, '{self.value}')"

# Caminhos para os arquivos binários
dir_file = "__pycache__/gui_dir.bin"
buckets_file = "__pycache__/gui_buckets.bin"

# Inicialização da tabela hash
if 'hash_table' not in st.session_state:
    if os.path.exists(dir_file): os.remove(dir_file)
    if os.path.exists(buckets_file): os.remove(buckets_file)
    st.session_state.hash_table = HashExtensivel(TestRecord, 3, dir_file, buckets_file)

# Quantidade máxima de registros por cesto = 3
# 🔧 Para alterar a capacidade dos buckets, mude o valor abaixo:
MAX_POR_CESTO = 3

# Inicializa a Tabela Hash Extensível com capacidade por bucket
if 'hash_table' not in st.session_state:
    if os.path.exists(dir_file): os.remove(dir_file)
    if os.path.exists(buckets_file): os.remove(buckets_file)
    st.session_state.hash_table = HashExtensivel(TestRecord, MAX_POR_CESTO, dir_file, buckets_file)

ht = st.session_state.hash_table

st.title("Visualizador de Tabela Hash Extensível")

# Seção de Inserção
st.subheader("Inserir Registro")
with st.form("insert_form"):
    insert_key = st.number_input("Chave (int)", step=1)
    insert_value = st.text_input("Valor (string)")
    submitted = st.form_submit_button("Inserir")
    if submitted:
        try:
            registro = TestRecord(int(insert_key), insert_value)
            ht.create(registro)
            st.success(f"Registro {registro} inserido com sucesso.")
        except Exception as e:
            st.error(str(e))

# Seção de Leitura
st.subheader("Buscar Registro")
read_key = st.number_input("Chave para buscar", step=1)
if st.button("Buscar"):
    rec = ht.read(int(read_key))
    if rec:
        st.info(f"Registro encontrado: {rec}")
    else:
        st.warning("Registro não encontrado.")

# Seção de Atualização
st.subheader("Atualizar Registro")
update_key = st.number_input("Chave para atualizar", step=1)
update_value = st.text_input("Novo valor")
if st.button("Atualizar"):
    updated = ht.update(TestRecord(int(update_key), update_value))
    if updated:
        st.success("Registro atualizado com sucesso.")
    else:
        st.error("Registro não encontrado.")

# Seção de Remoção
st.subheader("Remover Registro")
delete_key = st.number_input("Chave para remover", step=1)
if st.button("Remover"):
    if ht.delete(int(delete_key)):
        st.success("Registro removido com sucesso.")
    else:
        st.error("Registro não encontrado.")

# Exibir Estrutura Visual
st.subheader("Visualização Estruturada da Tabela Hash")

# Diretório
ht.arq_diretorio.seek(0)
bd = ht.arq_diretorio.read()
ht.diretorio = ht.Diretorio()
ht.diretorio.from_byte_array(bd)

st.markdown("### Diretório")
# Mostrar profundidade global
st.markdown(f"**Profundidade Global:** {ht.diretorio.profundidade_global}")

dir_data = []
for i, endereco in enumerate(ht.diretorio.enderecos):
    bin_index = format(i, f'0{ht.diretorio.profundidade_global}b')
    dir_data.append({"Índice Binário": bin_index, "Endereço (byte offset)": endereco})
st.table(dir_data)

# Buckets
st.markdown("### Buckets (Cestos)")
bucket_visualizados = set()
ht.arq_cestos.seek(0)
end = os.path.getsize(ht.nome_arquivo_cestos)
while ht.arq_cestos.tell() < end:
    offset = ht.arq_cestos.tell()
    if offset in bucket_visualizados:
        break
    bucket_visualizados.add(offset)
    cesto = ht.Cesto(ht.cls, ht.quantidade_dados_por_cesto)
    ba = ht.arq_cestos.read(cesto.size())
    cesto.from_byte_array(ba)

    ocupacao = cesto.quantidade / cesto.quantidade_maxima
    if ocupacao == 1.0:
        cor = "#DF0505"  # vermelho claro (cheio)
    elif ocupacao == 0.0:
        cor = "#B36C03"  # amarelo claro (vazio)
    else:
        cor = "#047004"  # verde claro (parcial)

    st.markdown(
        f"<div style='background-color:{cor}; padding:10px; border-radius:10px;'>"
        f"<b>Endereço:</b> {offset} bytes — <b>Profundidade Local:</b> {cesto.profundidade_local}</div>",
        unsafe_allow_html=True
    )

    registros = [{"Posição": i + 1,
                  "Chave": str(cesto.elementos[i].key),
                  "Valor": cesto.elementos[i].value}
                 if i < cesto.quantidade else
                 {"Posição": i + 1, "Chave": "-", "Valor": "-"}
                 for i in range(cesto.quantidade_maxima)]

    st.table(registros)
