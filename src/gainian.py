import akshare as ak
import datetime

date = datetime.datetime.now().strftime("%Y%m%d")
stock_board_concept_name_em_df = ak.stock_board_concept_name_em()
stock_board_concept_name_em_df.to_csv('E:\\股票概念\\{}.csv'.format(date), encoding='utf_8_sig')