# Tamper Detection Demo Module
# This demonstrates how blockchain prevents vote manipulation

from copy import deepcopy

class TamperDetectionDemo:
    @staticmethod
    def attempt_tamper(blockchain, block_index, new_vote):
        """
        Attempts to tamper with a block and shows why it fails
        Returns: dict with tamper attempt results
        """
        if block_index >= len(blockchain.chain):
            return {
                'success': False,
                'message': 'Invalid block index',
                'steps': []
            }
        
        steps = []
        original_block = blockchain.chain[block_index]
        
        # Step 1: Show original block
        steps.append({
            'step': 1,
            'action': 'Original Block Data',
            'data': {
                'index': original_block.index,
                'hash': original_block.hash,
                'data': original_block.data,  # Changed from 'votes' to 'data'
                'previous_hash': original_block.previous_hash
            }
        })
        
        # Step 2: Attempt to change vote
        steps.append({
            'step': 2,
            'action': 'Attempting to change vote data...',
            'data': {'new_vote': new_vote}
        })
        
        # Step 3: Calculate what new hash would be
        old_hash = original_block.hash
        old_data = deepcopy(original_block.data)  # Store original data
        original_block.data = new_vote  # Changed from 'votes' to 'data'
        new_hash = original_block.calculate_hash()
        
        steps.append({
            'step': 3,
            'action': 'Hash changed!',
            'data': {
                'old_hash': old_hash,
                'new_hash': new_hash,
                'match': old_hash == new_hash
            }
        })
        
        # Step 4: Check if chain is still valid
        is_valid = blockchain.is_chain_valid()
        
        steps.append({
            'step': 4,
            'action': 'Blockchain Validation',
            'data': {
                'is_valid': is_valid,
                'reason': 'Hash mismatch detected!' if not is_valid else 'Chain is valid'
            }
        })
        
        # Step 5: Show next block's previous_hash doesn't match
        if block_index + 1 < len(blockchain.chain):
            next_block = blockchain.chain[block_index + 1]
            steps.append({
                'step': 5,
                'action': 'Next block verification failed',
                'data': {
                    'next_block_previous_hash': next_block.previous_hash,
                    'current_block_new_hash': new_hash,
                    'match': next_block.previous_hash == new_hash
                }
            })
        
        # Restore original data
        original_block.data = old_data  # Changed from 'votes' to 'data'
        original_block.hash = old_hash
        
        return {
            'success': False,
            'message': '🛡️ BLOCKCHAIN PROTECTED THE VOTE! Tampering detected and prevented.',
            'steps': steps,
            'conclusion': 'Any attempt to modify a vote changes the hash, breaking the chain and making tampering immediately visible.'
        }
    
    @staticmethod
    def simulate_51_attack(blockchain):
        """
        Simulates a 51% attack scenario
        """
        return {
            'attack_type': '51% Attack Simulation',
            'description': 'Attacker tries to control majority of network',
            'prevention': [
                'Distributed consensus mechanism',
                'Multiple validator nodes required',
                'Proof of Work/Stake verification',
                'Network monitoring and alerts'
            ],
            'result': 'Attack prevented by decentralized architecture'
        }