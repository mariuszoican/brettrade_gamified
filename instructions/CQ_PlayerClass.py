class Player(BasePlayer):
    cq1 = models.StringField(
        label="class Player(BasePlayer):
    cq1 = models.StringField(
        label="If you do not sell the stock and the price crashes, you receive:",
        choices=["Zero",
                 "The stock price just before the crash",
                 "The stock price at the beginning of the round",
                 ],
        widget=widgets.RadioSelect
    )

    cq2 = models.StringField(
        label="If you do not sell the asset and the price does not crash, you receive"
        choices=["Zero",
                 "The stock price at the end of the round",
                 "The stock price at the beginning of the round",
                 ],
        widget=widgets.RadioSelect
    )

    cq3 = models.StringField(
        label="If the stock price has not yet crashed, the probability that it will crash at the next update is",
        choices=["Larger: I expect a crash at some point in the round.",
                 "Unchanged: The timing of a potential crash does not depend on past price updates.",
                 "Smaller: The stock has proven to be a good investment",
                 ],
        widget=widgets.RadioSelect
    )

    cq4 = models.StringField(
        label="Your total bonus payment for the experiment depends on:",
        choices=["The sum of payoffs across all rounds",
                 "Your payoff in a randomly selected round",
                 "Your payoff in a randomly selected round and your correct answers in the post-experimental quiz",
                 ],
        widget=widgets.RadioSelect
    )

    def cq1_error_message(self, value):
        if value != 'Zero':
            return 'Wrong answer!'

    def cq2_error_message(self, value):
        if value != 'The stock price at the end of the round':
            return 'Wrong answer!'

    def cq3_error_message(self, value):
        if value != 'Unchanged: The timing of a potential crash does not depend on past price updates.':
            return 'Wrong answer!'

    def cq4_error_message(self, value):
        if value != 'Your payoff in a randomly selected round and your correct answers in the post-experimental quiz':
            return 'Wrong answer!'