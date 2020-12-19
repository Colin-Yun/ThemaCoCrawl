class CoInfo:
    def __init__(self, thema, co_name, co_oview, avls, b_profit, b_profit_rate, forign_rate, per):  #avsl : aggregate value of listed stock(시가총액)
        self.thema = thema
        self.co_name = co_name
        self.co_oview = co_oview
        self.avls = avls
        self.b_profit = b_profit
        self.b_profit_rate = b_profit_rate
        self.forign_rate = forign_rate
        self.per = per


class ThemaInfo:
    def __init__(self, url, thema_name):
        self.url = url
        self.thema_name = thema_name


'''
class WebAccess:

    def get_page(self, ):
    
'''
