import mysql.connector as mysql
# from database import cursor, db
from mysql.connector import errorcode
import json
from key_generator.key_generator import generate
import bcrypt
from ecdsa import SigningKey, NIST256p
# from config import db, cursor
import itertools
import json
from database import db, cursor, db1, cursor1, db2, cursor2, db3, cursor3, db4, cursor4, db5, cursor5
import hashlib
# , db1, cursor1, db2, cursor2, db3, cursor3, db4, cursor4, db5, cursor5


DB_NAME = ['evote1']
TABLES = {}
TABLES['password'] = (
    "CREATE TABLE `password`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`email_id` varchar(30) NOT NULL,"
    "`password` varchar(250) NOT NULL,"
    "`voter_id` varchar(250) NOT NULL,"
    "`private_key` varchar(250) NOT NULL,"
    "`public_key` varchar(250) NOT NULL,"
    "`voted_id` varchar(250) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)
TABLES['votes'] = (
    "CREATE TABLE `votes`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`voter_id` varchar(250) NOT NULL,"
    "`private_key` varchar(250) NOT NULL,"
    "`voted_to` varchar(50) NOT NULL,"
    "`signature` varchar(250) NOT NULL,"
    "`timestamp` varchar(250) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)

TABLES['block'] = (
    "CREATE TABLE `block`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`previous_hash` varchar(250) NOT NULL,"
    "`proof` varchar(250) NOT NULL,"
    "`timestamp` varchar(250) NOT NULL,"
    "`data` varchar(10000) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)

TABLES['orphan'] = (
    "CREATE TABLE `orphan`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`vote` varchar(10000) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)


TABLES['minevote'] = "CREATE TABLE `minevote`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`data` varchar(10000) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)


# class CreateDatabase():

def create_database():
    for name in DB_NAME:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {name}")
        print('database created')


def create_tables():
    for name in DB_NAME:
        cursor.execute(f"USE {name}")
        for table_name in TABLES:
            table_description=TABLES[table_name]
            try:
                print(f"{table_name} is created!")
                cursor.execute(table_description)
            except mysql.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Already exists')
                else:
                    print(err.msg)


class AddToDatabase():

    def add_email_voter_id(self):

        for i in range(1, 122):
            id=1504000+i
            self.voter_id=generate(seed = id)
            self.email_id=f"u{id}@student.cuet.ac.bd"
            self.sql=(
                "INSERT INTO password(email_id, voter_id) VALUES (%s,%s)")
            cursor.execute(self.sql, (self.email_id, self.voter_id.get_key(),))
        db.commit()

    def add_priv_pub_key(self, priv, pub, voter_id):
        self.voter_id=voter_id
        self.priv=priv
        self.pub=pub
        self.sql=(
            "UPDATE password SET private_key= %s, public_key=%s WHERE voter_id = %s")
        cursor.execute(self.sql, (self.priv, self.pub, self.voter_id,))
        db.commit()

    def add_password(self, email, passd):
        self.email=email
        self.passd=passd.encode('ascii')
        self.sql=(
            "UPDATE password SET password= %s WHERE email_id = %s")
        self.password=bcrypt.hashpw(self.passd, bcrypt.gensalt())
        cursor.execute(self.sql, (self.password, self.email,))
        db.commit()

    def add_voted_id(self, voted, voter_id):
        self.voter_id=voter_id
        self.voted=voted
        self.sql=("UPDATE password SET voted_id= %s WHERE voter_id = %s")
        cursor.execute(self.sql, (self.voted, self.voter_id,))
        db.commit()


class VoteDatabase():
    def add_votes(self, voter_id, voted_to, priv, signature, timestamp):
        self.voter_id=voter_id
        self.voted_to=voted_to
        self.priv=priv
        self.signature=signature
        self.timestamp=timestamp
        self.sql=(
            "INSERT INTO votes (voter_id, voted_to, private_key, timestamp, signature) VALUES(%s,%s,%s,%s,%s)")
        cursor.execute(self.sql, (self.voter_id, self.voted_to,
                       self.priv, self.timestamp, self.signature,))
        db.commit()

    def load_voter_id(self):
        self.sql=("SELECT voter_id FROM votes")
        cursor.execute(self.sql)
        self.result=cursor.fetchall()
        return [self.row['voter_id'] for self.row in self.result]

    def minevote(self, previous_hash, proof, timestamp, data):
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s)")
        cursor.execute(self.sql, (self.previous_hash, self.proof,
                                  self.timestamp, self.data,))
        db.commit()

    def minevote1(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (id,previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s,%s)")
        cursor1.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data,))
        db1.commit()

    def minevote2(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (id,previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s,%s)")
        cursor2.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data,))
        db2.commit()

    def minevote3(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (id,previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s,%s)")
        cursor3.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data,))
        db3.commit()

    def minevote4(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (id,previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s,%s)")
        cursor4.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data,))
        db4.commit()

    def minevote5(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        self.sql=("INSERT INTO block (id,previous_hash, proof, timestamp,data)"
                    "VALUES(%s,%s,%s,%s,%s)")
        cursor5.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data,))
        db5.commit()

    # কাজ বাকি আছে, ক্রিয়েট ব্লক বাকি

    def loadblock(self):
        self.sql=("SELECT * FROM block")
        cursor.execute(self.sql)
        self.result=cursor.fetchall()
        return self.result

    def loadblock1(self):
        self.sql=("SELECT * FROM block")
        cursor1.execute(self.sql)
        self.result=cursor1.fetchall()
        return self.result

    def loadblock2(self):
        self.sql=("SELECT * FROM block")
        cursor2.execute(self.sql)
        self.result=cursor2.fetchall()
        return self.result

    def loadblock3(self):
        self.sql=("SELECT * FROM block")
        cursor3.execute(self.sql)
        self.result=cursor3.fetchall()
        return self.result

    def loadblock4(self):
        self.sql=("SELECT * FROM block")
        cursor4.execute(self.sql)
        self.result=cursor4.fetchall()
        return self.result

    def loadblock5(self):
        self.sql=("SELECT * FROM block")
        cursor5.execute(self.sql)
        self.result=cursor5.fetchall()
        return self.result


class LoadDatabase:
    # def __init__(self, email_id):
    #     self.email_id = email_id

    def load_email_id(self):
        self.sql=("SELECT email_id FROM password ")
        cursor.execute(self.sql)
        self.result=cursor.fetchall()
        return [self.row['email_id'] for self.row in self.result]

    def load_password(self, email_id):
        self.email_id=email_id
        self.sql=("SELECT password FROM password WHERE email_id= %s")
        cursor.execute(self.sql, (self.email_id,))
        self.result=cursor.fetchone()
        return self.result

    def load_voter_id(self, email_id):
        self.email_id=email_id
        self.sql=("SELECT voter_id FROM password WHERE email_id = %s")
        cursor.execute(self.sql, (self.email_id,))
        self.result=cursor.fetchone()
        return self.result['voter_id']

    def load_voter_ids(self):
        self.sql=("SELECT voter_id FROM password")
        cursor.execute(self.sql)
        self.result=cursor.fetchall()
        return [self.row['voter_id'] for self.row in self.result]

    def load_voted_ids(self):
        self.sql=("SELECT voted_id FROM votes")
        cursor.execute(self.sql)
        self.result=cursor.fetchall()
        return [self.row['voter_id'] for self.row in self.result]

    def load_priv_pub_key(self):
        # self.voter_id = voter_id
        self.sql=(
            "SELECT private_key,public_key FROM password ")
        cursor.execute(self.sql,)
        self.result=cursor.fetchall()
        self.list_res=[list((self.row[0], self.row[1]))
                         for self.row in self.result]
        return sum(self.list_res, [])

    def load_public_key(self, voter_id):
        self.voter_id = voter_id
        self.sql = ("SELECT public_key FROM password WHERE voter_id=%s")
        cursor.execute(self.sql, (self.voter_id,))
        self.result = cursor.fetchone()
        return self.result['public_key']

    def load_private_key(self, voter_id):
        self.voter_id = voter_id
        self.sql = ("SELECT private_key FROM password WHERE voter_id=%s")
        cursor.execute(self.sql, (self.voter_id,))
        self.result = cursor.fetchone()
        return self.result['private_key']


class ReplaceData():

    # DB function for inserting vote to orphan DB
    def add_vote_to_orphan_DB(self, vote):
        self.vote = vote
        self.sql = ("INSERT INTO orphan(vote) VALUES (%s)")
        cursor.execute(self.sql, (self.vote,))
        db.commit()

    def load_orphan_block(self):
        self.sql = ("SELECT * FROM orphan")
        cursor.execute(self.sql)
        self.result = cursor.fetchall()
        return [self.row['vote'] for self.row in self.result]

    def delete_orphan_block(self):
        self.sql = ("TRUNCATE TABLE orphan")
        cursor.execute(self.sql)
        db.commit()

    # DB function to update longest chain

    # def update_block1(self, id, previous_hash, proof, timestamp, data):
    #     self.id = id
    #     self.previous_hash = previous_hash
    #     self.proof = proof
    #     self.timestamp = timestamp
    #     self.data = data
    #     self.sql = (
    #         "UPDATE block SET previous_hash=%s, proof=%s, timestamp=%s,data=%s WHERE id=%s ")
    #     cursor1.execute(self.sql, (self.id, self.previous_hash, self.proof,
    #                                self.timestamp, self.data,))
    #     db1.commit()

    def update_block1(self, id, previous_hash, proof, timestamp, data):
        self.id = id
        self.previous_hash = previous_hash
        self.proof = proof
        self.timestamp = timestamp
        self.data = data
        # print("ID:", self.timestamp)
        # self.sql1 = ("TRUNCATE TABLE block")
        self.sql = (
            "INSERT INTO block(id, previous_hash,proof,timestamp,data) VALUES(%s,%s,%s,%s,%s) ")
        # cursor1.execute(self.sql1)
        cursor1.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data, ))
        db1.commit()

    def update_block2(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        # print("ID:", self.timestamp)
        # self.sql1 = ("TRUNCATE TABLE block")
        self.sql=(
            "INSERT INTO block(id, previous_hash,proof,timestamp,data) VALUES(%s,%s,%s,%s,%s) ")
        # cursor1.execute(self.sql1)
        cursor2.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data, ))
        db2.commit()

    def update_block3(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        # print("ID:", self.timestamp)
        # self.sql1 = ("TRUNCATE TABLE block")
        self.sql=(
            "INSERT INTO block(id, previous_hash,proof,timestamp,data) VALUES(%s,%s,%s,%s,%s) ")
        # cursor1.execute(self.sql1)
        cursor3.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data, ))
        db3.commit()

    def update_block4(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        # print("ID:", self.timestamp)
        # self.sql1 = ("TRUNCATE TABLE block")
        self.sql=(
            "INSERT INTO block(id, previous_hash,proof,timestamp,data) VALUES(%s,%s,%s,%s,%s) ")
        # cursor1.execute(self.sql1)
        cursor4.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data, ))
        db4.commit()

    def update_block5(self, id, previous_hash, proof, timestamp, data):
        self.id=id
        self.previous_hash=previous_hash
        self.proof=proof
        self.timestamp=timestamp
        self.data=data
        # print("ID:", self.timestamp)
        # self.sql1 = ("TRUNCATE TABLE block")
        self.sql=(
            "INSERT INTO block(id, previous_hash,proof,timestamp,data) VALUES(%s,%s,%s,%s,%s) ")
        # cursor1.execute(self.sql1)
        cursor5.execute(self.sql, (self.id, self.previous_hash, self.proof,
                                   self.timestamp, self.data, ))
        db5.commit()


# alter database
class AlterVote():

    def load_block(self, id):
        self.id=id
        self.sql=("SELECT * FROM block WHERE id=%s")
        cursor1.execute(self.sql, (self.id,))
        self.result=cursor1.fetchone()
        return self.result

    def load_vote_data(self, id):
        self.id=id
        self.sql=("SELECT data FROM block WHERE id=%s")
        cursor1.execute(self.sql, (self.id,))
        self.result=cursor1.fetchone()
        return self.result['data']

    def get_chain(self):
        chains=self.load_block(3)
        # print(chains)  # need change to loadblock1-5

        d={}
        d['index']=chains['id']
        d['previous_hash']=chains['previous_hash']
        d['proof']=chains['proof']
        d['timestamp']=chains['timestamp']
        d['votes']=json.loads(chains['data'])
        return d

    def get_vote(self):
        self.votes=json.loads(self.load_vote_data(3))
        self.vote=[]  # need change to loadblock1-5
        for i in self.votes:
            d={}
            d['voter ID']=i['voter ID']
            d['Cast Vote']=i['Cast Vote']
            d['signature']=i['signature']
            d['Timestamp']=i['Timestamp']

            self.vote.append(d)
        return self.vote

    def forge_vote(self):
        self.votes=self.get_vote()
        for i in self.votes:
            i['Cast Vote']="candidate 2"
        return self.votes

    def forge_block(self):
        chains=self.load_block(3)
        # print(chains)  # need change to loadblock1-5

        d={}
        d['index']=chains['id']
        d['previous_hash']=chains['previous_hash']
        d['proof']=chains['proof']
        d['timestamp']=chains['timestamp']
        d['votes']=json.dumps(self.forge_vote())
        return d

    def proof_of_work(self, previous_proof):
        self.previous_proof=previous_proof
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(
                str(new_proof ** 2 - self.previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof=True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block=json.dumps(block, sort_keys = True).encode()
        v=hashlib.sha256(encoded_block).hexdigest()
        # print(type(v))
        # hash_operation = hashlib.sha256(
        #     str(int(v, 16) ** 2 - 10 ** 2).encode()).hexdigest()
        # if hash_operation[:4] == '0000':
        #     return hash_operation
        proof=0
        while not v[0:2] == '00':
            proof += 1
        return proof
        # return hash(encoded_block)
        # return hashlib.sha256(encoded_block).hexdigest()


class OrphanVote():

    def get_all_vote_data(self):
        self.sql=("SELECT data FROM block")
        cursor1.execute(self.sql)
        self.result=cursor1.fetchall()
        return [self.row['data'] for self.row in self.result]

    def voter_id_from_block(self):
        ids=[]
        for i in self.get_all_vote_data()[1:]:
            ids.append((self.get_all_vote_data()['Voter ID']))
            # if len(i) > 10:
            #     ids.append(i['Voter ID'])

        return ids





def delete_data():
    sql=("DELETE FROM block")
    cursor3.execute(sql)
    db3.commit()


def alter_table():
    sql="DROP TABLE password"
    sql1="DROP TABLE votes"
    cursor1.execute(sql)
    cursor1.execute(sql1)
    db1.commit()
