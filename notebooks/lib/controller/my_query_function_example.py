#Example my_query_function
#Programmer: Tim Tyree
#Date: 6.24.2021
imMatchFlag=1
vpltTrial=1  # as stimulus was presented
output_folder=f'selecting_imMatchFlag_{imMatchFlag}'
def my_query_function(df):
    boo =(df.vpltTrial==vpltTrial)
    boo&=df.imMatchFlag==imMatchFlag
    return boo
