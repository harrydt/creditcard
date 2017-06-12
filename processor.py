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
        return self._produce_summary()

    def _add(self, name, card_number, limit):
        '''
        This method is used to add a new credit for a given name
        All new cards start with $0 balance
        '''
        if not verify(card_number) or not self._verify_unique_card_number(card_number):
            # Invalid/Existing card number
            self.summary[name] = "error"
            return 
        if name in self.accounts:
            # Add new card to existing user
            self.accounts[name].append({
                "card_number": card_number,
                "limit": int(limit[1:]),
                "balance": 0
            })
        else:
            # Initiate new user and new card
            self.accounts[name] = [{
                "card_number": card_number,
                "limit": int(limit[1:]),
                "balance": 0
            }]

    def _charge(self, name, amount):
        '''This method is used for applying a charge to existing account'''
        if name not in self.accounts:
            # User doesn't exist
            return

        int_amount = int(amount[1:])
        if self._get_capacity(name) < int_amount:
            # Ignore overcharge
            return
        
        # Start charging cards
        # "Charge" command doesn't specify which card, but it's logical to
        # distribute the charge among cards that a user owns.
        leftover = int_amount

        for i in range(0, len(self.accounts[name])):
            if leftover <= 0:
                break
            capacity = self.accounts[name][i]['limit'] - \
                     self.accounts[name][i]['balance']
            if capacity < leftover:
                self.accounts[name][i]['balance'] = - \
                        self.accounts[name][i]['limit']
                leftover = leftover - self.accounts[name][i]['limit']
            else:
                self.accounts[name][i]['balance'] += leftover
                leftover = 0

    def _credit(self, name, amount): 
        '''This method is used for decreasing balance) on an account'''
        if name not in self.accounts:
            # User doesn't exist
            return
        
        # Since "Credit" command doesn't specify which card, and there's
        # a chance that a user would want negative balance on certain card,
        # This credit will be applied to the first card for now
        # TODO revisit implementation
        if self.accounts[name]:
            self.accounts[name][0]['balance'] -= int(amount[1:])


    def _verify_unique_card_number(self, card_number):
        '''Naive implementation to check if card number is already in shelve'''
        for name in self.accounts:
            for i in range(0, len(self.accounts[name])): 
                if card_number == self.accounts[name][i]['card_number']:
                    return False
        return True

    def _get_capacity(self, name):
        '''Get total leftover capacity from all cards of a user'''
        capacity = 0
        for i in range(0, len(self.accounts[name])):
            capacity += self.accounts[name][i]['limit'] - \
                        self.accounts[name][i]['balance']
            
        return capacity

    def _produce_summary(self):
        summary_str = ""
        for name in self.accounts:
            balance = sum(card['balance'] for card in self.accounts[name])
            self.summary[name]= balance
        for name in sorted(self.summary):
            if self.summary[name] != "error":
                summary_str += "{}: ${}\n".format(name, self.summary[name])
            else:
                summary_str += "{}: {}\n".format(name, self.summary[name])
        return summary_str
