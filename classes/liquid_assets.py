

class LiquidAssets:
    def __init__(self):

        # Definiera kostnader
        self.start_value = 20
        self.cost_bfish = 1
        self.cost_pfish = 2
        self.cost_shark = 5
        self.cost_hook = 2
        self.cost_carrot = 1

        # Definiera inkomst
        self.income_egg_bonus = 2
        self.income_bfish = 3
        self.income_pfish = 5
        self.income_shark = 10
        self.income_swish = 25

        # Den viktigaste variabeln
        self.liquid_assets = self.start_value

    def status(self):
        # returnera pegavärdet
        return self.liquid_assets

    def cant_buy(self):
        pass

    def buy_bfish(self):
        if self.liquid_assets >= self.cost_bfish:
            self.liquid_assets -= self.cost_bfish
        else:
            self.cant_buy()

    def buy_pfish(self):
        if self.liquid_assets >= self.cost_pfish:
            self.liquid_assets -= self.cost_pfish
        else:
            self.cant_buy()
