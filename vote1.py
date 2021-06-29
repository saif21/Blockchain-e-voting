import datetime
import hashlib
import json
from flask import Flask, jsonify, request, session, logging, render_template, redirect, url_for, flash
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, Form, validators
import requests
from uuid import uuid4
from urllib.parse import urlparse
from ecdsa import SigningKey, VerifyingKey, NIST256p, BadSignatureError
from hashlib import sha256
from sql import AddToDatabase, LoadDatabase, VoteDatabase, ReplaceData
from passlib.hash import sha256_crypt
from replace import Replace, LongestChain

add = AddToDatabase()
load = LoadDatabase()
vote = VoteDatabase()
replace = Replace()
replaceData = ReplaceData()
longestChain = LongestChain()


class Blockchain:

    def __init__(self):
        # self.chain = []
        self.votes = []
        if len(self.get_chain()) < 1:
            # self.create_block(proof=1, previous_hash='0')
            vote.minevote1('0', 1, str(datetime.datetime.now()),
                           json.dumps([]))  # need change minvote1-5
        self.nodes = set()
        self.orphan_vote = replaceData.load_orphan_block()
        self.priv_pub_key = {}

    def get_chain(self):
        chains = vote.loadblock1()
        # print(chains)  # need change to loadblock1-5
        self.chain = []
        for i in chains:
            d = {}
            d['index'] = i['id']
            d['previous_hash'] = i['previous_hash']
            d['proof'] = i['proof']
            d['timestamp'] = i['timestamp']
            d['votes'] = json.loads(i['data'])
            self.chain.append(d)
        return self.chain

    def create_block(self, proof, previous_hash):

        self.proof = proof
        self.previous_hash = previous_hash
        for i in range(len(self.votes)):
            if self.votes[i]['Private Key']:
                del self.votes[i]['Private Key']
        block = {
            'index': len(self.get_chain())+1,
            'timestamp': str(datetime.datetime.now()),
            'proof': self.proof,
            'previous_hash': self.previous_hash,
            'votes': self.votes
        }
        self.votes = []
        return block

    def create_orphan_block(self, proof, previous_hash):
        self.proof = proof
        self.previous_hash = previous_hash
        for i in range(len(self.orphan_vote)):
            if self.votes[i]['Private Key']:
                del self.votes[i]['Private Key']
        block = {
            'index': len(self.get_chain())+1,
            'timestamp': str(datetime.datetime.now()),
            'proof': self.proof,
            'previous_hash': self.previous_hash,
            'votes': self.orphan_vote
        }
        self.orphan_vote = []
        return block

    def get_previous_block(self):
        return self.get_chain()[-1]

    def proof_of_work(self, previous_proof):
        self.previous_proof = previous_proof
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - self.previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = int(previous_block['proof'])
            proof = int(block['proof'])
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def cast_vote(self, sender, receiver, amount, signature, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        self.timestamp = timestamp
        self.votes.append({'voter ID': sender,
                           'Cast Vote': receiver,
                           'Private Key': amount,
                           'signature': signature,
                           'Timestamp': timestamp})
        previous_block = self.get_previous_block()
        # print(previous_block)
        vote.add_votes(self.sender, self.receiver, self.amount,
                       self.signature, self.timestamp)
        # return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = longestChain.longest_chain()
        current_chain = self.get_chain()

        if len(longest_chain) > len(current_chain) and self.is_chain_valid(longest_chain):
            replace.update_block_db1(longest_chain)  # need to change to db1-5
            replace.get_orphan_block(longest_chain, current_chain)
            replace.add_to_orphanDB()
            return True
        return False

    def random_key_gerneration(self, voter_id):
        self.voter_id = voter_id
        self.privateKey = SigningKey.generate(curve=NIST256p)
        self.publicKey = self.privateKey.get_verifying_key()

        add.add_priv_pub_key(self.privateKey.to_string().hex(),
                             self.publicKey.to_string().hex(), self.voter_id)

        return self.privateKey.to_string().hex()


app = Flask(__name__)

# Creating and address for the node on port 5000
node_address = str(uuid4()).replace('-', '')
# Creating a Blockchain
blockchain = Blockchain()


# generating a random private key and public key:
# @app.route('/key_generation', methods=['POST', 'GET'])
# def key_generation():
#     json = request.get_json()
#     voter_id = json['voter id']
#     response = jsonify(blockchain.random_key_gerneration(voter_id))
#     # return render_template('login.html', response=response)
#     return response, 200

# mine orphan block


@app.route('/mine_orphan', methods=['GET', 'POST'])
def mine_orphan_block():
    # form = Register(request.form)
    if request.method == 'POST':
        if blockchain.orphan_vote:
            if blockchain.is_chain_valid(blockchain.get_chain()):
                previous_block = blockchain.get_previous_block()
                previous_proof = int(previous_block['proof'])
                proof = blockchain.proof_of_work(previous_proof)
                previous_hash = blockchain.hash(previous_block)

                block = blockchain.create_orphan_block(proof, previous_hash)

                response = {'message': 'Congratulations, you just mined a block!',
                            'index': len(blockchain.get_chain())+1,
                            'timestamp': block['timestamp'],
                            'proof': block['proof'],
                            'previous_hash': block['previous_hash'],
                            'votes': block['votes']}
                # minevote needed change to minvote1-5
                vote.minevote1(block['previous_hash'],
                               block['proof'], block['timestamp'], json.dumps(block['votes']))
                replaceData.delete_orphan_block()
                flash('You just Mined a orphan block!', 'success')
                return render_template('mine.html', response=response)
            else:
                flash("There is problem with the chain, fix it first!", 'danger')
        else:
            flash('There is no orphan vote to mine', 'danger')
            return render_template('mine.html')

    return render_template('mine.html')


# Mining a new block
@app.route('/mine', methods=['GET', 'POST'])
def mine_block():
    # form = Register(request.form)
    if request.method == 'POST':
        if blockchain.is_chain_valid(blockchain.get_chain()):
            previous_block = blockchain.get_previous_block()
            previous_proof = int(previous_block['proof'])
            proof = blockchain.proof_of_work(previous_proof)
            previous_hash = blockchain.hash(previous_block)
            if len(blockchain.votes) > 2:
                block = blockchain.create_block(proof, previous_hash)

                response = {'message': 'Congratulations, you just mined a block!',
                            'index': len(blockchain.get_chain())+1,
                            'timestamp': block['timestamp'],
                            'proof': block['proof'],
                            'previous_hash': block['previous_hash'],
                            'votes': block['votes']}

                # need change in minevote1-5
                vote.minevote1(block['index'], block['previous_hash'],
                               block['proof'], block['timestamp'], json.dumps(block['votes']))
                flash('You just Mined a block!', 'success')
                return render_template('mine.html', response=response)
            else:
                flash('block is too short to mine!', 'danger')
                return render_template('mine.html')
        else:
            flash("There is problem with the chain, fix it first!", 'danger')

    return render_template('mine.html')


@app.route('/get_chain/<string:index>/', methods=['GET', 'POST'])
def chain(index):
    result = blockchain.get_chain()
    return render_template('article.html', article=result[int(index)-1])


@app.route('/get_chain', methods=['GET', 'POST'])
def chains():
    result = blockchain.get_chain()
    if len(result) > 0:
        return render_template('articles.html', articles=result)
    else:
        msg = 'No block found'
        return render_template('articles.html', msg=msg)


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET', 'POST'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.get_chain())
    if is_valid:
        # response = {'message': 'All good. The Blockchain is valid.'}
        flash(" Everything ok! The Blockchain is valid.", 'success')
        return render_template('articles.html')
    else:
        flash('Miners, we have a problem. The Blockchain is not valid.', 'danger')

    return render_template('articles.html')


class CastVote(Form):
    voterid = StringField('Voter ID', [validators.Length(min=1, max=100)])
    candidate = StringField('Candidate', [validators.Length(min=4, max=25)])
    private_key = StringField("Private Key", [validators.Length(min=6)])


@app.route("/cast", methods=["POST", 'GET'])
def cast_vote():

    list_of_voterids = load.load_voter_ids()
    list_of_votedids = vote.load_voter_id()
    if request.method == 'POST':
        voter_id = request.form['voterid']
        candidate = request.form['candidate']
        private_key = request.form['private_key']
        pub_key = load.load_public_key(voter_id)
        # print(type(pub_key))
        if voter_id in list_of_voterids:
            if voter_id not in list_of_votedids:
                sk1 = SigningKey.from_string(
                    bytearray.fromhex(private_key), curve=NIST256p)
                v = candidate
                signature = sk1.sign(bytes(v, encoding='utf-8'))
                signature_to_hex = signature.hex()
                vk = VerifyingKey.from_string(bytes.fromhex(
                    pub_key), curve=NIST256p)
                # print(vk.to_string().hex())
                try:
                    vk.verify(signature, bytes(v, encoding='utf-8'))
                    add.add_voted_id(voter_id, voter_id)
                    blockchain.cast_vote(
                        voter_id, candidate, private_key, signature_to_hex,
                        str(datetime.datetime.now()))
                    flash(
                        f'this vote will be added to block {len(blockchain.get_chain())+1} ', 'success')
                    # return redirect(url_for('cast_vote.html'))
                except BadSignatureError:
                    flash('verification failed!, get original key to vote...', 'danger')
                    # return redirect(url_for('cast_vote.html'))
            else:
                flash('Already Voted!', 'danger')
                # return redirect(url_for('cast_vote.html'))
        else:
            flash('Key error, get original key to vote', 'danger')
            # return redirect(url_for('cast_vote.html'))
    return render_template('cast_vote.html')


@app.route("/connectnode", methods=['POST', 'GET'])
def connect_node():
    if request.method == "POST":
        nodes = request.form['nodes']
        if len(nodes) < 1:
            flash('No Nodes found', 'danger')
            return render_template('about.html')
        for node in nodes.split(","):
            blockchain.add_node(node)
        response = {"message": 'all nodes are connected, blockchain now contain',
                    'total_nodes': list(blockchain.nodes)}
        return render_template('about.html', response=response)
    return render_template('about.html')


# replacing the chain by longest chain if need
@app.route("/replace_chain", methods=['GET', 'POST'])
def replace_chain():
    if request.method == 'POST':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            flash('Node has the smaller chain. Longest Chain is replaced!', 'success')
            response = blockchain.get_chain()
            render_template('replace.html', response=response)

        else:

            response = blockchain.get_chain()
            flash("Node has the longest chain", 'success')
            return render_template('replace.html', response=response)

    return render_template('replace.html')
    # return jsonify(response), 200


class Register(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=100)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='password did not mactch')
    ])
    confirm = PasswordField('confirm password')
    voterId = StringField('Voter ID', [validators.Length(min=1)])


@app.route('/register', methods=['GET', 'POST'])
def register():

    email_id = load.load_email_id()
    if request.method == 'POST':
        email = request.form['email']
        pasd = request.form['password']
        password = sha256_crypt.encrypt(str(pasd))
        # voter_ids = load.load_voter_ids()
        if email in email_id:
            add.add_password(email, password)
            response = load.load_voter_id(email)
            flash(response, 'success')
            return redirect(url_for('login'))
        else:
            flash('invalid Email id', 'danger')
            return render_template('register1.html')
    return render_template('register1.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        voter_id = request.form['voterid']
        voter_ids = load.load_voter_ids()
        if voter_id in voter_ids:
            if not load.load_private_key(voter_id):
                response = blockchain.random_key_gerneration(voter_id)
                flash(response,  'success')
                flash(voter_id, 'success')
                return redirect(url_for('cast_vote'))
            else:
                flash(load.load_private_key(voter_id), 'success')
                flash(voter_id, 'success')
                return redirect(url_for('cast_vote'))
            # return redirect(url_for('cast'))
        else:
            flash('invalid voter id', 'danger')
            return render_template('login.html')
    return render_template('login.html')

    # Running the app


if __name__ == '__main__':
    app.secret_key = 'saif123'
    app.run(host='localhost', port=5001, debug=True)
