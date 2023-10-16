import pandas as pd
from datetime import datetime

# @st.cache_data
def _rules(list_subdomains, list_domains, list_uos_acronims, list_cod_process, list_fuentes_datos_cods):
    def _oseert01_1(date_created):
          # fecha de creación no en futuro
          today = datetime.today()
          try:
            date = pd.to_datetime(date_created)
          except:
            return False
          return date<=today

    def _oseert01_2(date_created):
      """
      dd/mm/yyyy
      """
      try:
        datetime.strptime(date_created, "%Y-%m-%d")
        return True
      except:
        return False

    def _oseert01_3(date_created):
      return not pd.isna(date_created)

    #################
    def _oseert02_1(date_modified):
      # fecha de creación no en futuro
      today = datetime.today()
      try:
        date = pd.to_datetime(date_modified)
      except:
        return False
      return date<=today

    def _oseert02_2(date_modified):
      """
      dd/mm/yyyy
      """
      try:
        datetime.strptime(date_modified, "%Y-%m-%d")
        return True
      except:
        return False

    def _oseert02_3(row):
      # ojo acá debe aplicar un applymap
      # fecha de creación no en futuro
      date_modified = pd.to_datetime(row['date_modified'])
      date_created = pd.to_datetime(row['date_created'])
      return date_modified<=date_created

    def _oseert02_4(date_modified):
      return not pd.isna(date_modified)

    #####################

    def _oseert03_1(table_file_type):
      return not pd.isna(table_file_type)

    def _oseert03_2(table_file_type):
      return table_file_type in ['base de datos','archivo']


    ##############
    def _oseert04_1(field):
      return not pd.isna(field)

    def _oseert04_2(row):
      if (row['table_file_type']=='base de datos') & (row['table_file_format'] in ['sql']):
        return True
      elif (row['table_file_type']=='archivo') & (row['table_file_format'] in ['xlsx','csv','dta','txt','dbf','pdf','pptx','docsx']):
        return True
      else:
        return False
    #################
    def _oseert05_1(field):
      return not pd.isna(field)

    def _oseert05_2(field): #, list_fuentes_datos_cods)#=self.list_fuentes_datos_cods):
      return field in list_fuentes_datos_cods
    ######################
    def _oseert06_1(field):
      return not pd.isna(field)

    #################
    def _oseert07_1(field):
      return not pd.isna(field)

    def _oseert07_2(column):
      # esto debe ser aplicado a toda la columna de table_id
      return ~column.duplicated(False)

    ################
    def _oseert08_1(field):
      return not pd.isna(field)

    ###################
    def _oseert10_1(field):
      return not pd.isna(field)

    ###############
    def _oseert11_1(field):
      return not pd.isna(field)

    def _oseert11_2(field): #, list_cod_process=self.list_cod_process):
      return field in list_cod_process

    ###############
    def _oseert12_1(field):
      return not pd.isna(field)
    ###############
    def _oseert13_1(field):
      return not pd.isna(field)

    def _oseert13_2(field): #, list_uos_acronims=self.list_uos_acronims):
      return field in list_uos_acronims

    ##############
    def _oseert14_1(field):
      return not pd.isna(field)

    ##############
    def _oseert15_1(field):
      return not pd.isna(field)

    def _oseert15_2(field): #, list_uos_acronims=self.list_uos_acronims):
      return field in list_uos_acronims

    ###############
    def _oseert16_1(field):
      return not pd.isna(field)

    ###############
    def _oseert17_1(field):
      return not pd.isna(field)

    def _oseert17_2(field):
      dominios_minedu = ['minedu.gob.pe']#, 'edu.gob.pe']
      # Dividir el correo electrónico en nombre de usuario y dominio
      partes = field.split('@')
      if len(partes) == 2:
        dominio = partes[1].lower()
        if dominio in dominios_minedu:
          return True
      return False

    #############
    def _oseert18_1(field):
      return not pd.isna(field)

    def _oseert18_2(field):
      return field in ['validado','por validar']

    ##############
    def _oseert19_1(field):
      return not pd.isna(field)

    def _oseert19_2(field): #, list_domains=self.list_domains):
      return field in list_domains

    ##############
    def _oseert20_1(field):
      return not pd.isna(field)

    def _oseert20_2(field): #, list_subdomains=self.list_subdomains):
      return field in list_subdomains
    ############

    def _oseert21_1(field):
      return not pd.isna(field)

    ###########
    def _oseert23_1(field):
      return not pd.isna(field)

    ##############
    def _oseert24_1(field):
      return not pd.isna(field)

    ################################
    # def _get_reglas():
    dict_reglas = {'_oseert01_1':{'fun':_oseert01_1,'type':'field','cname':'date_created'},
      '_oseert01_2':{'fun':_oseert01_2,'type':'field','cname':'date_created'},
      '_oseert01_3':{'fun':_oseert01_3,'type':'field','cname':'date_created'},
      '_oseert02_1':{'fun':_oseert02_1,'type':'field','cname':'date_modified'},
      '_oseert02_2':{'fun':_oseert02_2,'type':'field','cname':'date_modified'},
      '_oseert02_3':{'fun':_oseert02_3,'type':'row','cname':'date_modified'},
      '_oseert02_4':{'fun':_oseert02_4,'type':'field','cname':'date_modified'},
      '_oseert03_1':{'fun':_oseert03_1,'type':'field','cname':'table_file_type'},
      '_oseert03_2':{'fun':_oseert03_2,'type':'field','cname':'table_file_type'},
      '_oseert04_1':{'fun':_oseert04_1,'type':'field','cname':'table_file_format'},
      '_oseert04_2':{'fun':_oseert04_2,'type':'row','cname':'table_file_format'},
      '_oseert05_1':{'fun':_oseert05_1,'type':'field','cname':'source_cod'},
      '_oseert05_2':{'fun':_oseert05_2,'type':'field','cname':'source_cod'},
      '_oseert06_1':{'fun':_oseert06_1,'type':'field','cname':'system_cod'},
      '_oseert07_1':{'fun':_oseert07_1,'type':'field','cname':'table_id'},
      '_oseert07_2':{'fun':_oseert07_2,'type':'column','cname':'table_id'},
      '_oseert08_1':{'fun':_oseert08_1,'type':'field','cname':'table_name'},
      '_oseert10_1':{'fun':_oseert10_1,'type':'field','cname':'table_description'},
      '_oseert11_1':{'fun':_oseert11_1,'type':'field','cname':'process_cod'},
      '_oseert11_2':{'fun':_oseert11_2,'type':'field','cname':'process_cod'},
      '_oseert12_1':{'fun':_oseert12_1,'type':'field','cname':'strategy'},
      '_oseert13_1':{'fun':_oseert13_1,'type':'field','cname':'data_declare'},
      '_oseert13_2':{'fun':_oseert13_2,'type':'field','cname':'data_declare'},
      '_oseert14_1':{'fun':_oseert14_1,'type':'field','cname':'data_owner_org'},
      '_oseert15_1':{'fun':_oseert15_1,'type':'field','cname':'data_owner_uo'},
      '_oseert15_2':{'fun':_oseert15_2,'type':'field','cname':'data_owner_uo'},
      '_oseert16_1':{'fun':_oseert16_1,'type':'field','cname':'data_owner_name'},
      '_oseert17_1':{'fun':_oseert17_1,'type':'field','cname':'data_owner_contact'},
      '_oseert17_2':{'fun':_oseert17_2,'type':'field','cname':'data_owner_contact'},
      '_oseert18_1':{'fun':_oseert18_1,'type':'field','cname':'data_ownership_status'},
      '_oseert18_2':{'fun':_oseert18_2,'type':'field','cname':'data_ownership_status'},
      '_oseert19_1':{'fun':_oseert19_1,'type':'field','cname':'domain'},
      '_oseert19_2':{'fun':_oseert19_2,'type':'field','cname':'domain'},
      '_oseert20_1':{'fun':_oseert20_1,'type':'field','cname':'domain_sub'},
      '_oseert20_2':{'fun':_oseert20_2,'type':'field','cname':'domain_sub'},
      '_oseert21_1':{'fun':_oseert21_1,'type':'field','cname':'data_steward_name'},
      '_oseert23_1':{'fun':_oseert23_1,'type':'field','cname':'storage'},
      '_oseert24_1':{'fun':_oseert24_1,'type':'field','cname':'table_type'}
      }
    return dict_reglas