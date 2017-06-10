from luhn import verify

class Processor:
    def __init__(self, accounts):
        self.accounts = accounts
        self.summary = {}

    def process(self, commands):
        for command in commands:
            if "Add" == command[0]:
                self._add(
                        name=command[1], 
                        card_number=command[2], 
                        limit=command[3]
                        )
            elif "Charge" == command[0]:
                self._charge(
                        name=command[1],
                        amount=command[2]
                        )
            elif "Credit" == command[0]:
                self._credit(
                        name=command[1],
                        amount=command[2]
                        )
        #return sorted(summary)

    def _add(self, name, card_number, limit):
        '''
        This method is used to add a new credit for a given name
        All new cards start with $0 balance
        '''
        if not verify(card_number) or not verify_unique_card_number(card_number):
            # Invalid/Existing card number
            self.summary[name] = "error"
            return 

        if name in self.accounts:
            # Add new card to existing user
            self.accounts[name].append({
                "card_number": card_number,
                "limit": limit,
                "balance": 0
            })
        else:
            # Initiate new user and new card
            self.accounts[name] = [{
                "card_number": card_number,
                "limit": limit,
                "balance": 0
            }]

    def _charge(self, name, amount):
        '''This method is used for applying a charge to existing account'''
        int_amount = int(amount[1:])
        if self._get_balance(name) < int_amount:
            # Ignore overcharge
            return
        else:
            # Start charging cards
            leftover = int_amount

            for i in range(0, len(self.accounts[name])):
                if leftover <= 0:
                    break
                if self.accounts[name][i]['balance'] < leftover:
                    self.accounts[name][i]['balance'] = 0
                    leftover = leftover - self.accounts[name][i]['balance']
                else:
                    self.accounts[name][i]['balance'] = 
                        self.accounts[name][i]['balance'] - leftover
                    leftover = 0

    def _credit(self, name, amount): 
        pass

    def _verify_unique_card_number(self, card_number):
        '''Naive implementation to check if card number is already in shelve'''
        for name in self.accounts:
            if card_number == self.accounts[name]['card_number']:
                return False
        return True

    def _get_balance(self, name):
        '''Get total current balance from all cards of a user'''
        balance = 0
        for card in self.accounts[name]:
            balance = balance + card['balance'] 

        return balance
