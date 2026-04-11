from core import RuneUtils

from abc import ABC
from abc import abstractmethod
import sympy
from enum import Enum
from core import ProcessedText
import os
import itertools

# Autokey modes
AutokeyMode = Enum('AutokeyMode', [ 'PLAINTEXT', 'CIPHERTEXT', 'ALT_START_PLAINTEXT', 'ALT_START_CIPHERTEXT', 'ALT_MOBIUS_START_PLAINTEXT', 'ALT_MOBIUS_START_CIPHERTEXT' ])

class MathUtils(object):
    """
        Math utilities.
    """

    # Fibonacci primes cache
    _FIBO_PRIMES_CACHE = None

    @staticmethod
    def get_all_subsets(li):
        """
            Gets all subsets of a given list.
        """

        # Get all subsets
        return itertools.chain.from_iterable(itertools.combinations(li, r) for r in range(len(li) + 1))

    @staticmethod
    def find_next_prime(prev_prime):
        """
            Finds the next prime number.
        """

        # Return the next prime
        return sympy.nextprime(prev_prime)

    @staticmethod
    def mobius(n):
        """
            Defines Mobius function.
        """

        # Use sympy
        return sympy.mobius(n)

    @staticmethod
    def totient(n):
        """
            Defines the Totient function.
        """

        # Use sympy
        return sympy.totient(n)

    @staticmethod
    def sqrt(num):
        """
            Square root of the given number.
        """

        # Use sympy
        return sympy.sqrt(num)

    @staticmethod
    def is_square(num):
        """
            Indicates if the given number is a square.
        """

        # Rule out negatives
        if num < 0:
            return False

        # See if the square root is an integer
        return sympy.sqrt(num).is_Integer

    @staticmethod
    def gen_primes(first_value=2, indices_apart=1):
        """
            A generator for primes.
        """

        # Generate primes forever
        assert indices_apart > 0, Exception(f'Invalid argument for indices apart between primes: {indices_apart}')
        curr_prime = first_value
        while True:
            yield curr_prime
            for i in range(indices_apart):
                curr_prime = MathUtils.find_next_prime(curr_prime)

    @staticmethod
    def gen_totients(start_at_0=False):
        """
            Generate totients as a sequence.
        """

        # Optionally start at 0
        if start_at_0:
            yield 0

        # Generate forever
        n = 1
        while True:
            yield MathUtils.totient(n)
            n += 1

    @staticmethod
    def gen_fibonacci(start_a=1, start_b=1):
        """
            Generates Fibonacci sequences.
        """

        # Generate forever
        val_a, val_b = start_a, start_b
        while True:
            yield val_b
            val_a, val_b = val_b, val_a + val_b

    @classmethod
    def get_fibo_primes(cls):
        """
            Gets primes indecex by the Fibonacci sequence.
            Since generating those is CPU-intenstive, it was pre-generated in a file "fibo_primes.txt".
        """

        # Get from cache
        if cls._FIBO_PRIMES_CACHE is None:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fibo_primes.txt')
            with open(path, 'r') as fp:
                cls._FIBO_PRIMES_CACHE = list(map(int, [ elem for elem in fp.read().split('\n') if len(elem) > 0 ]))

        # Create an iterator
        return iter(cls._FIBO_PRIMES_CACHE)

    @abstractmethod
    def matrix_to_spiral_stream(matrix, repeat=False):
        """
            Creates a repeating stream from a given square matrix.
            Can optionally repeat the pattern indefinitely.
        """

        # Define directions
        dirs = [ (1, 0), (0, 1), (-1, 0), (0, -1) ]
        size = matrix.rows

        # Optionally repeat forever
        while True:

            # Find the midpoint
            x, y = (size - 1) // 2, (size - 1) // 2

            # Start right
            count = 0
            dir_index = 0
            steps_left = 1
            visited = 0
            dir_changes_even = False
            curr_step_size = 1

            # Return entire matrix
            while visited < size * size:

                # Yield the current point
                yield matrix.row(y)[x]
                visited += 1

                # Change direction if we are out of steps
                if steps_left == 0:
                    dir_index = (dir_index + 1) % len(dirs)
                    if dir_changes_even:
                        curr_step_size += 1
                    steps_left = curr_step_size
                    dir_changes_even = not dir_changes_even

                # Walk direction
                x, y = (x + dirs[dir_index][0], y + dirs[dir_index][1])
                steps_left -= 1

            # Break out unless repeating
            if not repeat:
                break

class TransformerBase(ABC):
    """
        Base class for transformers.
    """

    @abstractmethod
    def transform(self, processed_text):
        """
            Transforms a processed text.
        """
        pass

    def __init__(self, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Saves the alphabet
        assert len(alphabet_prefix) == len([ c for c in alphabet_prefix if RuneUtils.is_rune(c) ]), Exception(f'Invalid alphabet prefix: {alphabet_prefix}')
        assert len(alphabet_prefix) == len(set(alphabet_prefix)), Exception(f'Repeating elements in alphabet prefix are forbidden: {alphabet_prefix}')
        self._alphabet = alphabet_prefix + ''.join([ RuneUtils.rune_at(i) for i in range(RuneUtils.size()) if RuneUtils.rune_at(i) not in alphabet_prefix ])

class ShiftTransformer(TransformerBase):
    """
        Shift (Caesar) transformer.
    """

    def __init__(self, shift, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Saves the shift value
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._shift = shift % len(self._alphabet)

    def transform(self, processed_text):
        """
            Trandforms runes.
        """

        # Performs the shift transformation
        processed_text.set_runes([ self._alphabet[(self._alphabet.index(rune) + self._shift) % len(self._alphabet)] for rune in processed_text.get_runes() ])

class AtbashTransformer(TransformerBase):
    """
        Atbash transformer.
    """

    def transform(self, processed_text, alphabet_prefix=''):
        """
            Transforms runes.
        """

        # Performs Atbash transformation
        super().__init__(alphabet_prefix=alphabet_prefix)
        processed_text.set_runes([ self._alphabet[len(self._alphabet) - self._alphabet.index(rune) - 1] for rune in processed_text.get_runes() ])

class AutokeyTransformer(TransformerBase):
    """
        Autokey cipher decryption.
    """

    def __init__(self, key, mode, use_gp=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
            The key should be in runes.
            The mode is one of the aforementioned AutokeyMode values.
            The GP boolean indicates whether to use primes on the index as an intermediate step in keystream extension.
        """

        # Save the key indices
        super().__init__(alphabet_prefix=alphabet_prefix)
        assert len(key) > 0, Exception('Empty key')
        self._key_indices = [ self._alphabet.index(rune) for rune in key ]

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

        # Save the mode
        self._mode = mode
        self._use_gp = False

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Save state based on mode
        extend_to_plaintext = self._mode in (AutokeyMode.PLAINTEXT, AutokeyMode.ALT_START_PLAINTEXT, AutokeyMode.ALT_MOBIUS_START_PLAINTEXT)

        # Performs an autokey decryption
        result = []
        key_index = 0
        rune_index = -1
        ciphertext_extension_index = 0
        mob_value = None
        running_key_indices = self._key_indices[:]
        ciphertext = processed_text.get_runes()
        for rune in ciphertext:
            rune_index += 1

            # Handle Mobius function and change state accrdingly
            if self._mode in (AutokeyMode.ALT_MOBIUS_START_PLAINTEXT, AutokeyMode.ALT_MOBIUS_START_CIPHERTEXT):
                mob_value = MathUtils.mobius(rune_index + 1)
                extend_to_plaintext = (AutokeyMode.ALT_MOBIUS_START_PLAINTEXT and mob_value == 1) or (AutokeyMode.ALT_MOBIUS_START_CIPHERTEXT and mob_value == 0)

            # Treat mobius value of 0 just like an interrupt index
            if rune_index in self._interrupt_indices or mob_value == 0:
                new_index = self._alphabet.index(rune)
            else:
                new_index = (self._alphabet.index(rune) - running_key_indices[key_index]) % len(self._alphabet)
                key_index += 1

                # Extend the keystream from either plaintext or ciphertext
                if extend_to_plaintext:
                    running_key_indices.append(new_index)
                else:
                    running_key_indices.append(self._alphabet.index(ciphertext[ciphertext_extension_index]))
                    ciphertext_extension_index += 1

                # Using GP mode we extend the running keystream with the GP value of the lastly added value
                if self._use_gp:
                    running_key_indices[-1] = GP_PRIMES[running_key_indices[-1]] % len(self._alphabet)

                # Update whether to extend the keystream to plaintext if needed
                if self._mode in (AutokeyMode.ALT_START_PLAINTEXT, AutokeyMode.ALT_START_CIPHERTEXT):
                    extend_to_plaintext = not extend_to_plaintext

            # Add the new rune
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class AutokeyMobiusTransformer(TransformerBase):

    def __init__(self, keys, mode, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the keys
        super().__init__(alphabet_prefix=alphabet_prefix)
        assert len(keys) == 3, Exception('Expecting three keys')
        self._keys = keys[:]

        # Save the interrupters and the mode
        self._interrupt_indices = interrupt_indices
        self._mode = mode

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Split by runes
        rune_chunks = [ '' ] * 3
        interrupt_indices = [ set() ] * 3
        rune_index = 0
        for rune in processed_text.get_runes():
            
            # Use 1-based indexing
            rune_index += 1

            # Append to the right ciphertext chunk and map Mobius function from { -1, 0, 1 } to { 0, 1, 2 }
            fixed_index = MathUtils.mobius(rune_index) + 1
            rune_chunks[fixed_index] += rune

            # Save interrupt indices
            if rune_index - 1 in self._interrupt_indices:
                interrupt_indices[fixed_index].add(len(rune_chunks[fixed_index]) - 1)

        # Run each transformer seperately
        pt_chunks = [ None ] * 3
        for i in range(3):
            transformer = AutokeyTransformer(self._keys[i], self._mode, interrupt_indices[i])
            pt_chunks[i] = ProcessedText(rune_chunks[i])
            transformer.transform(pt_chunks[i])

        # Merge results
        results = []
        pt_runes = [ pt.get_runes() for pt in pt_chunks ]
        rune_index = 0
        for rune in processed_text.get_runes():
            rune_index += 1
            fixed_index = MathUtils.mobius(rune_index) + 1
            results.append(pt_runes[fixed_index].pop(0)) 
        processed_text.set_runes(results)

class VigenereTransformer(TransformerBase):
    """
        Vigenere cipher decryption.
    """

    def __init__(self, key, interrupt_indices=set(), grouping_size=1, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the key indices
        super().__init__(alphabet_prefix=alphabet_prefix)
        assert len(key) > 0, Exception('Empty key')
        self._key_indices = [ self._alphabet.index(rune) for rune in key ]
        assert len([ i for i in self._key_indices if i < 0 ]) == 0, Exception('Invalid key')

        # Save the grouping size
        assert grouping_size >= 1, Exception(f'Invalid grouping size {grouping_size}')
        self._grouping_size = grouping_size

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

        # Build the alphabet
        assert len([ c for c in alphabet_prefix if c in self._alphabet ]) == len(alphabet_prefix), Exception(f'Invalid alphabet: {alphabet_prefix}')

    def transform(self, processed_text):
        """
            transforms runes.
        """

        # Performs Vigenere decryption
        result = []
        key_index = 0
        rune_index = -1
        curr_group_size = 1
        decrypted_in_group = 0
        for rune in processed_text.get_runes():
            rune_index += 1
            if rune_index in self._interrupt_indices:
                new_index = self._alphabet.index(rune)
            else:
                new_index = (self._alphabet.index(rune) - self._key_indices[key_index]) % len(self._alphabet)
                decrypted_in_group += 1
                if decrypted_in_group == curr_group_size:
                    key_index = (key_index + 1) % len(self._key_indices)
                    decrypted_in_group = 0
                    curr_group_size += 1
                    if curr_group_size > self._grouping_size:
                        curr_group_size = 1
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class TotientPrimeTransformer(TransformerBase):
    """
        Substructs or adds the totient of primes (i.e. p-1) from each index.
        You can also call the totient function recusrively, if needed, or not call it at all.
        Optiomally turns primes into emirps (Decimal-reversed primes).
    """

    def __init__(self, add=False, interrupt_indices=set(), tot_calls=1, emirp=False, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the action and the number of totient calls
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._add = add
        self._tot_calls = tot_calls
        self._emirp = emirp

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Substract or adds the totient of each prime
        result = []
        curr_prime = 2
        rune_index = -1
        for rune in processed_text.get_runes():
            rune_index += 1
            if rune_index in self._interrupt_indices:
                new_index = self._alphabet.index(rune)
            else:
                val = int(str(curr_prime)[::-1]) if self._emirp else curr_prime
                for i in range(self._tot_calls):
                    val = MathUtils.totient(val)
                if not self._add:
                    val *= -1
                new_index = (self._alphabet.index(rune) + val) % len(self._alphabet)
                curr_prime = MathUtils.find_next_prime(curr_prime)
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class TotientFibTransformer(TransformerBase):
    """
        Substructs or adds the totient of the Fibonacci sequence from each index.
        You can also call the totient function recusrively, if needed, or not call it at all.
    """

    def __init__(self, add=False, interrupt_indices=set(), tot_calls=1, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the action and the number of totient calls
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._add = add
        self._tot_calls = tot_calls

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Substract or adds the totient of each element in the Fibonacci sequence 
        result = []
        fib_a, fib_b = 1, 1
        rune_index = -1
        for rune in processed_text.get_runes():
            rune_index += 1
            if rune_index in self._interrupt_indices:
                new_index = self._alphabet.index(rune)
            else:
                val = fib_a
                for i in range(self._tot_calls):
                    val = MathUtils.totient(val)
                if not self._add:
                    val *= -1
                new_index = (self._alphabet.index(rune) + val) % len(self._alphabet)
                fib_a, fib_b = fib_b, fib_a + fib_b
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class MobiusTotientPrimeTransformer(TransformerBase):
    """
        Substructs or adds to Mobius function of the totient of primes (i.e. p-1), times a either the totient or the prime, from each index.
    """

    def __init__(self, add=False, use_prime_as_base=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the action
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._add = add
        self._use_prime_as_base = use_prime_as_base

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Substract or adds the value of each prime
        result = []
        curr_prime = 2
        rune_index = -1
        for rune in processed_text.get_runes():
            rune_index += 1
            if rune_index in self._interrupt_indices:
                new_index = self._alphabet.index(rune)
            else:
                tot = MathUtils.totient(curr_prime)
                if self._use_prime_as_base:
                    val = (MathUtils.mobius(tot) * curr_prime) % len(self._alphabet)
                else:
                    val = (MathUtils.mobius(tot) * tot) % len(self._alphabet)
                if not self._add:
                    val *= -1
                new_index = (self._alphabet.index(rune) + val) % len(self._alphabet)
                curr_prime = MathUtils.find_next_prime(curr_prime)
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class ReverseTransformer(TransformerBase):
    """
        Reverses the processed text.
    """

    def __init__(self, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(alphabet_prefix=alphabet_prefix)

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Reverses runes
        processed_text.set_runes(processed_text.get_runes()[::-1])

class KeystreamTransformer(TransformerBase):
    """
        Uses a keystream to either add or substruct from each rune value.
        Keystream is assumed to be infinite or sufficiently long - but generally will give up and only transform the first N runes if finite.
    """

    def __init__(self, add=False, keystream=None, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save the keystream and the action
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._keystream = keystream
        self._add = add

        # Save the interrupters
        self._interrupt_indices = interrupt_indices

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Runs the keystream
        result = []
        rune_index = -1
        orig_runes = processed_text.get_runes()
        try:
            for rune in orig_runes:
                rune_index += 1
                if rune_index in self._interrupt_indices:
                    result.append(rune)
                else:
                    val = next(self._keystream)
                    if not self._add:
                        val *= -1
                    result.append(self._alphabet[(self._alphabet.index(rune) + val) % len(self._alphabet)])

            # Set the result
            processed_text.set_runes(result)
        except StopIteration:

            # Extend results as much as possible
            result = (result + orig_runes)[:len(orig_runes)]
            processed_text.set_runes(result)

class Page15FuncPrimesTransformer(KeystreamTransformer):
    """
        Treats abs(3301 - p) for all primes p as a keystream transformer.
        That function was derived from Page 15's square matrix, which works on primes indexed by the Fibonacci sequence.
    """

    def __init__(self, add=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(add=add, keystream=map(lambda x:abs(3301-x), MathUtils.gen_primes()), interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class TotientKeystreamTransformer(KeystreamTransformer):
    """
        Uses the Totient of naturals as a sequence. Can optionally also include tot(0) = 0 (which is normally undefined).
    """

    def __init__(self, add=False, start_at_0=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(add=add, keystream=MathUtils.gen_totients(start_at_0), interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class FiboPrimesTransformer(KeystreamTransformer):
    """
        Uses the primes indexed by Fibonacci sequence (2, 3, 5, 17, 11, 17, 23) as a keystream.
        This information was derived from Page 15's square matrix, which works on primes indexed by the Fibonacci sequence.
    """

    def __init__(self, add=False, emirp=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        keystream = map(lambda x:int(str(x)[::-1]), MathUtils.get_fibo_primes()) if emirp else MathUtils.get_fibo_primes()
        super().__init__(add=add, keystream=keystream, interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class Page15FiboPrimesTransformer(KeystreamTransformer):
    """
        Treats abs(3301 - primes[fib[i]]) as a keystream.
        This information was derived from Page 15's square matrix, which works on primes indexed by the Fibonacci sequence.
    """

    def __init__(self, add=False, emirp=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        keystream = map(lambda x:abs(3301-int(str(x)[::-1])), MathUtils.get_fibo_primes()) if emirp else map(lambda x:abs(3301-x), MathUtils.get_fibo_primes())
        super().__init__(add=add, keystream=keystream, interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class SpiralSquareKeystreamTransformer(KeystreamTransformer):
    """
        Given a square matrix, uses its values as a keystream in a clockwise spiral shape from its center.
        This pattern was erived from Page 15's square matrix.
    """

    def __init__(self, matrix, add=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(add=add, keystream=MathUtils.matrix_to_spiral_stream(matrix, repeat=True), interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class PrimesIndicesApartTransformer(KeystreamTransformer):
    """
        The first few pages of Liber Primus part 1 (solved pages) have page numbers that are 107, 167, 229.
        That corresponds to primes that are 11-indices apart, and can be turned into a keystream.
    """

    def __init__(self, indices_apart=11, start_value=107, add=False, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(add=add, keystream=MathUtils.gen_primes(first_value=start_value, indices_apart=indices_apart), interrupt_indices=interrupt_indices, alphabet_prefix=alphabet_prefix)

class HillCipherTransformer(TransformerBase):
    """
        Runs Hill Cipher on runes.
    """

    def __init__(self, matrix, padding='ᚠ', inverse=True, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Saves the matrix and the padding
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._matrix = matrix.inv_mod(len(self._alphabet)) if inverse else matrix
        assert len(padding) == 1, Exception('Invalid padding length')
        assert padding[0] in self._alphabet, Exception(f'Padding must be a rune: {padding}')
        self._padding = padding[0]

    def transform(self, processed_text):
        """
            Transforms runes.
        """
        
        # Iterate runes in groups
        result = []
        runes = processed_text.get_runes()
        for i in range(0, len(runes), self._matrix.rows):

            # Get the chunk and optionally extend with padding
            chunk = (''.join(runes[i:i+self._matrix.rows]) + (self._padding * self._matrix.rows))[:self._matrix.rows]
            chunk = [ self._alphabet.index(rune) for rune in chunk ]

            # Work on transposed matrix
            new_chunk = self._matrix * sympy.Matrix(chunk)
            new_chunk = [ self._alphabet[num % len(self._alphabet)] for num in new_chunk ]
            result.extend(new_chunk)

        # Set the result
        processed_text.set_runes(result[:len(runes)])

class FibonacciKeystreamTransformer(TransformerBase):
    """
        Creates a keystream out of Fibonacci sequence.
    """

    def __init__(self, add=False, start_a=0, start_b=1, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save members
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._interrupt_indices = interrupt_indices
        self._add = add

        # Saves the sequence
        self._sequence = [ start_a, start_b ]

    def transform(self, processed_text):
        """
            Transforms runes.
        """
        
        # Extend sequence
        runes = processed_text.get_runes()
        while len(self._sequence) < len(runes):
            self._sequence.append(self._sequence[-1] + self._sequence[-2])

        # Apply sequence
        result = []
        rune_index = 0
        seq_index = 0
        for rune in runes:
            if rune_index in self._interrupt_indices:
                result.append(rune)
            else:
                val = self._sequence[seq_index]
                if not self._add:
                    val = -val
                result.append(self._alphabet[(self._alphabet.index(rune) + val) % len(self._alphabet)])

        # Apply result
        processed_text.set_runes(result)

class ModInvTransformer(TransformerBase):
    """
        Performs modular inverse of each rune.
        Also attempts to use a shift counter that is increased every time we hit the first rune.
    """

    def __init__(self, use_shift_counter=False, alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save members
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._use_shift_counter = use_shift_counter

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Iterate runes
        result = []
        shift_value = 0
        for rune in processed_text.get_runes():
            
            # Performs modular inverse
            curr_index = self._alphabet.index(rune)
            if curr_index == 0:
                new_index = curr_index
                if self._use_shift_counter:
                    shift_value += 1
            else:
                new_index = pow(curr_index, -1, len(self._alphabet)) + shift_value
            result.append(self._alphabet[new_index])

        # Set the result
        processed_text.set_runes(result)

class AutokeyGpTransformer(TransformerBase):
    """
        Uses the GP value of the previous plaintext or ciphertext in an Autokey fashion.
    """

    def __init__(self, add=False, use_plaintext=True, primer_value=0, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Save members
        super().__init__(alphabet_prefix=alphabet_prefix)
        self._add = add
        self._use_plaintext = use_plaintext
        self._primer_value = primer_value
        self._interrupt_indices = interrupt_indices

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Iterate runes
        result = []
        last_value = self._primer_value
        for rune in processed_text.get_runes():

            # Generate the new rune index
            curr_index = self._alphabet.index(rune)
            new_index = curr_index + last_value if self._add else curr_index - last_value
            new_index %= len(self._alphabet)
            result.append(self._alphabet[new_index])

            # Update last value
            last_value = curr_index if self._use_plaintext else new_index
            last_value = RuneUtils.gp_at(last_value)

        # Set the result
        processed_text.set_runes(result)

class AlbertiTransformer(TransformerBase):
    """
        Runs an Alberti cipher.
    """

    def __init__(self, period, periodic_increment=1, initial_shift=0, interrupt_indices=set(), alphabet_prefix=''):
        """
            Creates an instance.
        """

        # Validations
        super().__init__(alphabet_prefix=alphabet_prefix)
        assert periodic_increment > 0, Exception('Periodic increment must be a positive integer')
        assert periodic_increment < len(self._alphabet), Exception('Periodic increment too big')
        assert period > 0, Exception('Period must be strictly positive')

        # Save members
        self._mobile_disk = list(range(len(self._alphabet)))
        self._interrupt_indices = interrupt_indices
        self._period = period
        self._periodic_increment = periodic_increment

        # Use the initial shift
        self._mobile_disk = self._mobile_disk[initial_shift:] + self._mobile_disk[:initial_shift]

    def transform(self, processed_text):
        """
            Transforms runes.
        """

        # Save the mobile disk
        mobile_disk = self._mobile_disk[:]
        mobile_counter = 0

        # Iterate runes
        result = []
        rune_index = -1
        for rune in processed_text.get_runes():
            rune_index += 1
            if rune_index in self._interrupt_indices:
                result.append(rune)
                continue
            result.append(self._alphabet[mobile_disk.index(self._alphabet.index(rune))])
            mobile_counter += 1
            if mobile_counter == self._period:
                mobile_counter = 0
                mobile_disk = mobile_disk[self._periodic_increment:] + mobile_disk[:self._periodic_increment]

        # Yield results
        processed_text.set_runes(result)

class UnsolvedTransformer(TransformerBase):
    """
        Marks the processed text as unsolved.
    """

    def __init__(self):
        """
            Creates an instance.
        """

        # Call super
        super().__init__()

    def transform(self, processed_text):
        """
            Sets the processed text as unsolved.
        """

        # Sets as unsolved
        processed_text.set_unsolved()

