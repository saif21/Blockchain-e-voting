from sql import ReplaceData, VoteDatabase
import json
from database import db, cursor, db1, cursor1, db2, cursor2, db3, cursor3, db4, cursor4, db5, cursor5
# longest_chain = chain
# smaller_chain = self.get_chain()

replaceBlock = ReplaceData()


class Replace():
    def __init__(self):
        self.orphan_block = []

    # obtaining orphan block
    def get_orphan_block(self, longest_chain, smaller_chain):
        self.longest_chain = longest_chain
        self.smaller_chain = smaller_chain

        for i in range(len(self.smaller_chain)):
            if self.longest_chain[i]['proof'] != self.smaller_chain[i]['proof']:
                self.orphan_block = smaller_chain[i:]
        return self.orphan_block

    # orphan_block(longest_chain, smaller_chain)

    # obtaining orphan block votes and add to orphan DB
    def add_to_orphanDB(self):
        if self.orphan_block:
            for j in self.orphan_block:
                replaceBlock.add_vote_to_orphan_DB(j['vote'])

    def update_block_db1(self, longest_chain):
        self.longest_chain = longest_chain
        self.sql1 = ("DELETE FROM block")
        cursor1.execute(self.sql1)
        db1.commit()
        for k in longest_chain:
            index = k['index']
            previous_hash = k['previous_hash']
            proof = k['proof']
            timestamp = k['timestamp']
            data = json.dumps(k['votes'])
            # print("Time:", timestamp)
            replaceBlock.update_block1(
                index, previous_hash, proof, timestamp, data)

    def update_block_db2(self, longest_chain):
        self.longest_chain = longest_chain
        self.sql1 = ("DELETE FROM block")
        cursor2.execute(self.sql1)
        db2.commit()
        self.longest_chain = longest_chain
        for k in longest_chain:
            index = k['index']
            previous_hash = k['previous_hash']
            proof = k['proof']
            timestamp = k['timestamp']
            data = json.dumps(k['votes'])
            replaceBlock.update_block2(
                index, previous_hash, proof, timestamp, data)

    def update_block_db3(self, longest_chain):
        self.longest_chain = longest_chain
        self.sql1 = ("DELETE FROM block")
        cursor3.execute(self.sql1)
        db3.commit()
        self.longest_chain = longest_chain
        for k in longest_chain:
            index = k['index']
            previous_hash = k['previous_hash']
            proof = k['proof']
            timestamp = k['timestamp']
            data = json.dumps(k['votes'])
            replaceBlock.update_block3(
                index, previous_hash, proof, timestamp, data)

    def update_block_db4(self, longest_chain):
        self.longest_chain = longest_chain
        self.sql1 = ("DELETE FROM block")
        cursor4.execute(self.sql1)
        db4.commit()
        self.longest_chain = longest_chain
        for k in longest_chain:
            index = k['index']
            previous_hash = k['previous_hash']
            proof = k['proof']
            timestamp = k['timestamp']
            data = json.dumps(k['votes'])
            replaceBlock.update_block4(
                index, previous_hash, proof, timestamp, data)

    def update_block_db5(self, longest_chain):
        self.longest_chain = longest_chain
        self.sql1 = ("DELETE FROM block")
        cursor5.execute(self.sql1)
        db5.commit()
        self.longest_chain = longest_chain
        for k in longest_chain:
            index = k['index']
            previous_hash = k['previous_hash']
            proof = k['proof']
            timestamp = k['timestamp']
            data = json.dumps(k['votes'])
            replaceBlock.update_block5(
                index, previous_hash, proof, timestamp, data)


vote = VoteDatabase()


class LongestChain():

    def __init__(self):
        self.evote1 = vote.loadblock1()
        self.evote2 = vote.loadblock2()
        self.evote3 = vote.loadblock3()
        self.evote4 = vote.loadblock4()
        self.evote5 = vote.loadblock5()

        self.evote1_chain = []
        self.evote2_chain = []
        self.evote3_chain = []
        self.evote4_chain = []
        self.evote5_chain = []

    def get_chain(self, chains):
        self.chains = chains
        self.chain = []  # need change to loadblock1-5
        for i in chains:
            d = {}
            d['index'] = i['id']
            d['previous_hash'] = i['previous_hash']
            d['proof'] = i['proof']
            d['timestamp'] = i['timestamp']
            d['votes'] = json.loads(i['data'])
            self.chain.append(d)
        return self.chain

    def longest_chain(self):
        self.evote1_chain = self.get_chain(self.evote1)
        self.evote2_chain = self.get_chain(self.evote2)
        self.evote3_chain = self.get_chain(self.evote3)
        self.evote4_chain = self.get_chain(self.evote4)
        self.evote5_chain = self.get_chain(self.evote5)
        list1 = [self.evote1_chain, self.evote2_chain,
                 self.evote3_chain, self.evote4_chain, self.evote5_chain]
        longest_list = max(len(elem) for elem in list1)
        longest = None
        for i in list1:
            if len(i) == longest_list:
                longest = i
        return longest
