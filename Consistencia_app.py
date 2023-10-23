#%%
import pandas as pd
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from io import BytesIO

from datetime import datetime

# from utils import Diagnosticador
from utils_minedu import loadShareFile, _get_file_XLSX
from reglas import _rules
# antes teníamos la '1.21.0', ahoar actualizamo a la '1.27.0'
import streamlit as st
# from st_aggrid import AgGrid

#%%
class Diagnosticador():

    def __init__(self, username, password):
      self.url = r'https://mineduperu.sharepoint.com'
      self.path = r'https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu'
      self.username = username
      self.password = password
      list_subdomains, list_domains, list_uos_acronims, list_cod_process, list_fuentes_datos_cods = self._get_inputs()
      self.list_subdomains = list_subdomains
      self.list_domains = list_domains
      self.list_uos_acronims = list_uos_acronims
      self.list_cod_process = list_cod_process
      self.list_fuentes_datos_cods = list_fuentes_datos_cods
    
    #########################################

    def _get_dominios(self):
      pathfolder_integration = "https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/06. Diseño/00. dominios de datos/"
      file_integration = "Propuesta de Dominios de Datos.xlsx"
      sheet_integration = 'Propuesta de Dominios_1'
      dfdoms = _get_file_XLSX(pathfolder_integration, file_integration, sheet_name=sheet_integration, url=self.url, path=self.path, username=self.username, password=self.password, header=[0,1])
      dfdoms[('Dominios de nivel 0','Cod')] = dfdoms[('Dominios de nivel 0','Cod')].fillna(method='ffill')
      return dfdoms

    def _get_process(self):
      pathfolder_integration = "https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/07. Operativo/03. Inventario de Datos/00. toolkit/"
      file_integration = "04. Procesos_codigos_nombres.xlsx"
      sheet_integration = 'Hoja1'
      dfprocs = _get_file_XLSX(pathfolder_integration, file_integration, sheet_name=sheet_integration, url=self.url, path=self.path, username=self.username, password=self.password)
      return dfprocs

    def _get_acronims(self):
      pathfolder_integration = "https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/07. Operativo/03. Inventario de Datos/00. toolkit/"
      file_integration = "Siglas_UO_MINEDU.xlsx"
      sheet_integration = 'Hoja1'
      dfacr = _get_file_XLSX(pathfolder_integration, file_integration, sheet_name=sheet_integration, url=self.url, path=self.path, username=self.username, password=self.password)
      return dfacr

    def _get_sources(self):
      pathfolder_integration = "https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/07. Operativo/03. Inventario de Datos/00. toolkit/"
      file_integration = "05. Formato_fuentes_de_datos.xlsx"
      sheet_integration = 'source'
      dfsrc = _get_file_XLSX(pathfolder_integration, file_integration, sheet_name=sheet_integration, url=self.url, path=self.path, username=self.username, password=self.password)
      return dfsrc
    
    @st.cache_data(hash_funcs={"__main__.Diagnosticador": lambda x: hash(x.url)})
    def _get_inputs(self):
      dfdoms = self._get_dominios()
      dfacr = self._get_acronims()
      dfprocs = self._get_process()
      dfsrc = self._get_sources()
      list_subdomains = list(set(dfdoms[('Dominios de nivel 1','Cod')].to_list()))
      list_domains = list(set(dfdoms[('Dominios de nivel 0','Cod')].to_list()))
      list_uos_acronims = list(set(dfacr['SIGLAS'].to_list()))
      list_cod_process = list(set(dfprocs['Process_n0_cod'].to_list() + dfprocs['Process_n1_cod'].to_list()))
      list_fuentes_datos_cods = list(set(dfsrc['source_id'].to_list()))
      return list_subdomains, list_domains, list_uos_acronims, list_cod_process, list_fuentes_datos_cods

    @st.cache_data(hash_funcs={"__main__.Diagnosticador": lambda x: hash(x.url)})
    def _get_diagnostic(self, df, _reglas):
      df_diagnostic = pd.DataFrame(columns=pd.MultiIndex([[],[]], [[],[]],names=['Metadato','Regla']))
      for name_regla in _reglas:
        regla = _reglas[name_regla]
        if regla['type']=='field':
          cname = regla['cname']
          fun = regla['fun']
          df_diagnostic[(cname,name_regla)] = df[cname].apply(fun)
        elif regla['type']=='row':
          # cname = regla['cname']
          fun = regla['fun']
          df_diagnostic[(cname,name_regla)] = df.apply(fun, axis=1)
        elif regla['type']=='column':
          cname = regla['cname']
          fun = regla['fun']
          df_diagnostic[(cname,name_regla)] = fun(df[cname])
        else:
          print('Tipo de regla no encontrado')
          continue
      return df_diagnostic
    


#%%
username = st.text_input("Email institucional",'juan@minedu.gob.pe')
password = st.text_input("Contraseña", type="password")
direccion0 = st.text_input('Ubicación del archivo', 'https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/01. Data Stewardship/01. Stewarship DIGEBR/DIGEBR_data_catalog_minedu_stewarship.xlsx')
sheet = st.text_input('Nombre de la hoja', 'tables')

if st.button('Diagnosticar...'):
  diagnosticador = Diagnosticador(username, password)
  # diagnosticador.get_init()

  # %%
  # reglas

  reglas = _rules(diagnosticador.list_subdomains, diagnosticador.list_domains,
                  diagnosticador.list_uos_acronims, diagnosticador.list_cod_process,
                  diagnosticador.list_fuentes_datos_cods)

  #%%

  file_and_pathfolder = direccion0[::-1].split('/',1)
  pathfolder = file_and_pathfolder[1][::-1] + "/"
  file = file_and_pathfolder[0][::-1]
  # pathfolder = "https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu/Documentos compartidos/01. Data Stewardship/01. Stewarship DIGEBR/"
  # file = "DIGEBR_data_catalog_minedu_stewarship.xlsx"
  # sheet = 'tables'

  url = r'https://mineduperu.sharepoint.com'
  path = r'https://mineduperu.sharepoint.com/sites/00.EquipoGobiernodeDatosMinedu'
  username = 'uegobdat04@MINEDU.GOB.PE'
  password = 'Rwarela123$'

  # @st.cache_data
  def _get_file_XLSX_main(pathfolder, file, sheet_name,  url, path, username, password, header=[0]):
      df = pd.read_excel(BytesIO(loadShareFile(pathfolder=pathfolder, filename=file, url=url, path=path, username=username, password=password)), sheet_name=sheet_name, dtype='str', header=header)
      return df


  dftables = _get_file_XLSX_main(pathfolder, file, sheet_name=sheet, url=url, path=path, username=username, password=password)
  dftables0 = dftables.rename({'source_type':'table_file_type',
                              'source_format':'table_file_format',
                              'source_name':'source_cod',
                              'cod_system':'system_cod',
                              'cod_process':'process_cod',
                              'desc_system':'system_desc',
                              'id_table':'table_id',
                              'id_table_destino':'table_id_destino',
                              'status_ownership':'data_ownership_status',
                              'taxonomy':'domain',
                              'taxonomy_sub':'domain_sub'}, axis=1)
  dftables0 = dftables0.set_index('table_id', drop=False)

  #%%
  dfdiagnostic = diagnosticador._get_diagnostic(dftables0, reglas)
  columns_multilevel = pd.MultiIndex.from_tuples(zip(dftables0.columns, ['Columna']*dfdiagnostic.shape[1]))
  dftables0_columns_original = dftables0.columns
  dftables0.columns = columns_multilevel
  dfoutput = dftables0.merge(dfdiagnostic, left_index=True, right_index=True)#.sort_index(axis=1)
  #%%
  # ordenar
  columns_ordenadas = []
  for col in dftables0_columns_original:
    subcolumns = dfoutput[col].columns
    columna_ordenada = list(zip([col]*len(subcolumns), subcolumns))
    columns_ordenadas += columna_ordenada

  dfoutput = dfoutput[columns_ordenadas]

  @st.cache_data
  def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True)
    writer.save()
    processed_data = output.getvalue()
    return processed_data
  
  df_xlsx = to_excel(dfoutput)

  today = str(datetime.today())
  st.download_button(label='📥 Descargar diagnóstico',
                                  data=df_xlsx ,
                                  file_name= f'Diagnostico_{today}.xlsx')


# %%

# AgGrid(dfoutput.droplevel(0, axis=1))
