import string

class Vote:
    def __init__(self):
        self.votes = {}

        # Initialize the vote counts for each option (A to Z)
        for option in string.ascii_uppercase:
            self.votes[option] = 0

    def updateVotes(self, vote):
        if vote in self.votes:
            self.votes[vote] += 1
            print(f"Vote received: {vote}")
        else:
            print("Invalid vote option.")

    def displayVotes(self):
        for option, count in self.votes.items():
            print(f"Option {option}: {count} votes")