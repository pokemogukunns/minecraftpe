# マインクラフト風バイオーム & 構造物生成 (Pythonプロトタイプ)

import random
import matplotlib.pyplot as plt
import noise
import numpy as np

# シード値設定
def set_seed(seed):
    random.seed(seed)
    np.random.seed(int(seed) % (2**32))

# バイオーム生成関数
def generate_biomes(seed, size=100):
    set_seed(seed)
    scale = 100.0
    world = np.zeros((size, size))
    
    for x in range(size):
        for y in range(size):
            value = noise.pnoise2(x/scale, y/scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=size, repeaty=size, base=int(seed))
            world[x][y] = value
    
    return world

# バイオームの分類
def classify_biomes(world):
    biomes = np.zeros_like(world, dtype=object)
    
    for x in range(world.shape[0]):
        for y in range(world.shape[1]):
            val = world[x][y]
            if val < -0.2: biomes[x][y] = ('海', 'blue')
            elif val < 0.0: biomes[x][y] = ('砂漠', 'yellow')
            elif val < 0.2: biomes[x][y] = ('平原', 'green')
            elif val < 0.4: biomes[x][y] = ('森林', 'darkgreen')
            elif val < 0.6: biomes[x][y] = ('山', 'brown')
            else: biomes[x][y] = ('雪原', 'white')
    
    return biomes

# 構造物を追加する関数
def add_structures(biomes, village_chance=0.02, fortress_chance=0.01):
    size = biomes.shape[0]
    structures = np.zeros_like(biomes, dtype=object)
    
    for x in range(size):
        for y in range(size):
            biome, color = biomes[x][y]
            if biome in ['平原', '森林', '砂漠'] and random.random() < village_chance:
                structures[x][y] = ('村', 'orange')
            elif biome in ['山', '雪原'] and random.random() < fortress_chance:
                structures[x][y] = ('要塞', 'red')
            else:
                structures[x][y] = (biome, color)
    
    return structures

# 可視化
def plot_biomes(biomes):
    color_map = np.vectorize(lambda x: x[1])(biomes)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(color_map)
    plt.title('Minecraft風バイオーム & 構造物生成')
    plt.show()

# 実行
seed = input('シード値を入力してください: ')
world = generate_biomes(seed)
biomes = classify_biomes(world)
biomes_with_structures = add_structures(biomes)
plot_biomes(biomes_with_structures)
