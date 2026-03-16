#!/usr/bin/env python3
"""XOR filter — space-efficient probabilistic set membership."""
import hashlib, random, sys, struct

class XorFilter:
    def __init__(self, keys):
        keys = list(set(keys)); n = len(keys)
        self.size = max(4, int(n * 1.23) + 32)
        self.seed = 0; self.table = None
        for attempt in range(100):
            self.seed = random.randint(0, 2**32-1)
            if self._build(keys): return
        raise RuntimeError("Failed to construct XOR filter")
    def _h(self, key, idx):
        data = struct.pack("<II", self.seed, idx) + key.encode()
        return int(hashlib.md5(data).hexdigest(), 16) % self.size
    def _fp(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest()[:2], 16) | 1
    def _build(self, keys):
        self.table = [0] * self.size
        for key in keys:
            h0, h1, h2 = self._h(key, 0), self._h(key, 1), self._h(key, 2)
            fp = self._fp(key)
            self.table[h0] ^= fp; self.table[h1] ^= fp; self.table[h2] ^= fp
        return True
    def __contains__(self, key):
        if not self.table: return False
        h0, h1, h2 = self._h(key, 0), self._h(key, 1), self._h(key, 2)
        fp = self._fp(key)
        return (self.table[h0] ^ self.table[h1] ^ self.table[h2]) & 0xFF == fp & 0xFF

if __name__ == "__main__":
    items = sys.argv[1:] or ["cat","dog","fish"]
    xf = XorFilter(items)
    for i in items + ["elephant"]: print(f"{i}: {'yes' if i in xf else 'no'}")
