import sys
import psycopg2
import uuid
import psycopg2.extras


def insert_data_DN1():
    conn = psycopg2.connect(database="postgres", user="test", password="gbase;123", host="100.0.0.88", port="5432")
    cur = conn.cursor()
    value = ('dd3fc0c0304811ee972db76ac7fd2030', 'INYNO62272619911241379', '20230616263344047', '300203',
             '2023061626334404720230725', '12400001', 'CNY', 'F02102030101', '8033228076', '庞合一', 2,
             '20230725', '20230713', '20230713', '91.81', '0.01', '0.01', '0.01364', ' ', '96400001', 'etl',
             '2023-07-28 14:11:07', 'etl', '2023-07-28 14:11:07', 'etl', '2023-07-28 14:11:07', '16700002',
             '20230713', '97500002', '97500002', '20230727')

    data = []
    for x in range(1000000):
        data.append(value)

    # 构造INSERT语句
    insert_query = """insert into acc_loan_int_acct_dtl(id,int_acct,loan_no,tx_code,plan_id,int_type,curr_type,prod_no,
    cust_no,cust_name,cycl_no,stmt_date,int_date,act_date,loan_bal,rat,calt_int_amt,int_amt,is_fp,net_type,net_user_no,
    inst_date,inst_user_no,updt_date,updt_psn,txhp_time,acct_type,orig_int_date,in_mark,txs_type,busi_date) VALUES %s"""

    # 使用mogrify方法构造批量插入语句
    for x in range(2000):
        psycopg2.extras.execute_values(cur, insert_query, data)

        # 提交事务
        conn.commit()


def insert_data_otherDN():
    conn = psycopg2.connect(database="postgres", user="test", password="gbase;123", host="100.0.0.88", port="5432")
    cur = conn.cursor()

    data = []
    for x in range(10000):
        ID = uuid.uuid1()
        value = (f'{ID}', 'INYNO62272619911241379', '20230616263344047', '300203',
                 '2023061626334404720230725', f'{str(12400001 + x)}', 'CNY', 'F02102030101', '8033228076', '庞合一', 2,
                 '20230725', '20230713', '20230713', '91.81', '0.01', '0.01', '0.01364', ' ', '96400001', 'etl',
                 '2023-07-28 14:11:07', 'etl', '2023-07-28 14:11:07', 'etl', '2023-07-28 14:11:07', '16700002',
                 '20230713', '97500002', '97500002', '20230727')
        data.append(value)

    # 构造INSERT语句
    insert_query = """insert into acc_loan_int_acct_dtl(id,int_acct,loan_no,tx_code,plan_id,int_type,curr_type,prod_no,
        cust_no,cust_name,cycl_no,stmt_date,int_date,act_date,loan_bal,rat,calt_int_amt,int_amt,is_fp,net_type,net_user_no,
        inst_date,inst_user_no,updt_date,updt_psn,txhp_time,acct_type,orig_int_date,in_mark,txs_type,busi_date) VALUES %s"""

    # 使用mogrify方法构造批量插入语句
    for x in range(2000):
        psycopg2.extras.execute_values(cur, insert_query, data)

        # 提交事务
        conn.commit()


if __name__ == '__main__':
    insert_data_DN1()
