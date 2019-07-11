import hashlib
import requests # pylint: disable=F0401

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(last_proof):
        """
        Simple Proof of Work Algorithm
        - Find a number p' such that hash(pp') contains 4 leading
        zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """

        print('Starting search for new proof')
        proof = 0
        while valid_proof(last_proof, proof) is False:
            proof += 1
        print('Found new proof:' + str(proof))
        return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 4
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == "00000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        res = requests.get('http://localhost:5000/last_proof')
        res = res.json()
        print(res)
        new_proof = proof_of_work(res['proof'])
        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post('http://localhost:5000/mine', json={'proof': new_proof})
        print(response.json()['message'])
        if response.json()['message'] == 'New Block Forged':
            coins_mined += 1
            print("coins mined: ", coins_mined)
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,

        
        # print the message from the server.
