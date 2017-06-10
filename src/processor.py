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
        if name not in self.accounts:
            # User doesn't exist
            return

        int_amount = int(amount[1:])
        if self._get_limit(name) < int_amount:
            # Ignore overcharge
            return
        
        # Start charging cards
        leftover = int_amount

        for i in range(0, len(self.accounts[name])):
            if leftover <= 0:
                break
            capacity = self.accounts[name][i]['limit'] \
                    - self.accounts['name'][i]['balance']
            if capacity < leftover:
                self.accounts[name][i]['balance'] = \
                        self.account['name'][i]['limit']
                leftover = leftover - self.accounts[name][i]['limit']
            else:
                self.accounts[name][i]['balance'] = \ 
                    self.accounts[name][i]['balance'] + leftover
                leftover = 0

    def _credit(self, name, amount): 
        pass

    def _verify_unique_card_number(self, card_number):
        '''Naive implementation to check if card number is already in shelve'''
        for name in self.accounts:
            if card_number == self.accounts[name]['card_number']:
                return False
        return True

    def _get_capacity(self, name):
        '''Get total leftover capacity from all cards of a user'''
        capacity = 0
        for card in self.accounts[name]:
            capacity = capacity + (card['limit'] - card['balance'])

        return capacity

    def _produce_summary(self):
        summary_str = ""
        sorted_summary = sorted(self.summary)

        for name in sorted_summary:
            if sorted_summary[name] == "error":
                balance = "error"
            else:
                balance = sum([balance for card['balance'] in self.accounts[name]])
                balance = "${:d}".format(balance)

            summary_str += "%s: %s".format(name, balance)

        return summary_str
