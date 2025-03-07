# マインクラフト風バイオーム & 構造物生成 + 座標表示 (Java版 & 統合版対応)

import random
import matplotlib.pyplot as plt
import noise
import numpy as np

# シード値設定
def set_seed(seed):
    random.seed(seed)
    np.random.seed(int(seed) % (2**32))

# バイオーム生成関数 (Java版 & 統合版対応)
def generate_biomes(seed, version='java', size=100):
    set_seed(seed)
    scale = 100.0 if version == 'java' else 80.0  # 統合版はやや小さめのスケール感
    world = np.zeros((size, size))
    
    for x in range(size):
        for y in range(size):
            base = int(seed) if version == 'java' else int(seed) * 2
            value = noise.pnoise2(x/scale, y/scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=size, repeaty=size, base=base)
            world[x][y] = value
    
    return world

# バイオームの分類
def classify_biomes(world):
    biomes = np.zeros_like(world, dtype=object)
    
    for x in range(world.shape[0]):
        for y in range(world.shape[1]):
            val = world[x][y]
            if val < -0.2: biomes[x][y] = ('海', 'blue', 'Ocean.png')
            elif val < 0.0: biomes[x][y] = ('砂漠', 'yellow', 'Desert.png')
            elif val < 0.2: biomes[x][y] = ('平原', 'green', 'Plains.png')
            elif val < 0.4: biomes[x][y] = ('森林', 'darkgreen', 'Forest.png')
            elif val < 0.6: biomes[x][y] = ('山', 'brown', 'Mountain.png')
            else: biomes[x][y] = ('雪原', 'white', 'Snow.png')
    
    return biomes

# 構造物を追加する関数
def add_structures(biomes, village_chance=0.02, fortress_chance=0.01):
    size = biomes.shape[0]
    structures = np.zeros_like(biomes, dtype=object)
    
    for x in range(size):
        for y in range(size):
            biome, color, image = biomes[x][y]
            if biome in ['平原', '森林', '砂漠'] and random.random() < village_chance:
                structures[x][y] = ('村', 'orange', 'https://pokemogukunns.github.io/minecraftpe/img/Village.png')
            elif biome in ['山', '雪原'] and random.random() < fortress_chance:
                structures[x][y] = ('要塞', 'red', 'https://pokemogukunns.github.io/minecraftpe/img/Fortress.png')
            else:
                structures[x][y] = (biome, color, f'https://pokemogukunns.github.io/minecraftpe/img/{image}')
    
    return structures

# 座標表示のクリックイベント
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        biome, structure, image = biomes_with_structures[x][y]
        print(f'座標: ({x}, {y}) -> {biome} ({structure}) - 画像: {image}')
        plt.annotate(f'{biome} ({x}, {y})', (x, y), color='black', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
        plt.draw()

# 可視化
def plot_biomes(biomes):
    color_map = np.vectorize(lambda x: x[1])(biomes)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(color_map)
    plt.title('Minecraft風バイオーム & 構造物生成 (Java版 & 統合版対応)')
    
    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()

# 実行
seed = input('シード値を入力してください: ')
version = input('バージョンを選択してください (java/bedrock): ').strip().lower()
if version not in ['java', 'bedrock']:
    print('無効なバージョンです。デフォルトでJava版を使用します。')
    version = 'java'

world = generate_biomes(seed, version)
biomes = classify_biomes(world)
biomes_with_structures = add_structures(biomes)
plot_biomes(biomes_with_structures)
