# ==========================================
# Module: Astar Path Finder
# File: executor/Astar_pathfinder.py
# ==========================================
# 🧩 功能概述：
#   - 实现 A* 算法进行路径规划；
#   - 提供最优路径搜索功能；
# ==========================================

from PIL import Image
import numpy as np
import heapq
import matplotlib.pyplot as plt


def image_preprocess(image):
    """纯红像素是起点，纯绿像素是终点，纯黑是障碍物，其余为可通行区域"""
    # 只找纯红和纯绿像素的质心作为起点终点即可

    img_array = np.array(image)
    height, width, _ = img_array.shape
    start = np.array([0, 0], dtype=np.float32)
    start_count = 0
    stop = np.array([0, 0], dtype=np.float32)
    stop_count = 0

    for y in range(height):
        for x in range(width):
            r, g, b = img_array[y, x]
            if r > 127 and r > g and r > b:
                start += np.array([x, y])
                start_count += 1
            elif g > 127 and g > r and g > b:
                stop += np.array([x, y])
                stop_count += 1

    start = (start / start_count).astype(np.int32) if start_count > 0 else None
    stop = (stop / stop_count).astype(np.int32) if stop_count > 0 else None

    if start is None or stop is None:
        print("❌ No start point or stop point found in the image.")

    return start, stop


def distance(pos, stop):
    """启发式评分函数，使用欧氏距离"""
    return np.linalg.norm(pos - stop)


def Astar_pathfinder(image: Image.Image) -> list:
    """使用 A* 算法进行路径规划"""
    if image is None:
        print("❌ No image provided.")
        return []
    start, stop = image_preprocess(image)
    if start is None or stop is None:
        return []

    # 优先队列，以距离排序
    active_queue = []
    visited_list = set()
    step = 30.0
    directions = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            directions.append(np.array([dx, dy]) / np.linalg.norm(np.array([dx, dy])) * step)

    heapq.heappush(active_queue, (distance(start, stop), [list(start)]))
    visited_list.add(tuple(start))
    while len(active_queue) > 0:
        _, path = heapq.heappop(active_queue)
        current_pos = path[-1]
        # 动态可视化
        if len(path) and False:
            plt.clf()
            plt.imshow(image)
            path_array = np.array(path)
            plt.plot(path_array[:, 0], path_array[:, 1], color='blue', linewidth=1)
            plt.axis('off')
            plt.pause(0.0001)

        for direction in directions:
            new_pos = (current_pos + direction).astype(np.int32)
            x, y = new_pos
            if x < 0 or x >= image.width or y < 0 or y >= image.height:
                continue

            r, g, b = image.getpixel((x, y))
            flag_collide = False # 路径碰撞检测，逐像素检测
            for step_check in range(1, int(step)+1, 1):
                check_pos = (current_pos + direction / np.linalg.norm(direction) * step_check).astype(np.int32)
                cx, cy = check_pos
                cr, cg, cb = image.getpixel((cx, cy))
                if cr < 50 and cg < 50 and cb < 50:
                    flag_collide = True
                    break
            if flag_collide:
                continue

            if g > 127 and g > r and g > b:  # 绿色终点
                print("✅ Path found!")
                return path + [new_pos]

            flag_visited = False
            for visited in visited_list:
                if np.linalg.norm(np.array(new_pos) - np.array(visited)) < step / 2:
                    flag_visited = True
                    break
            if flag_visited:
                continue
            visited_list.add(tuple(new_pos))
            path_copy = path.copy()
            path_copy.append(list(new_pos))
            heapq.heappush(active_queue, (distance(new_pos, stop) + (len(path) - 1) * step, path_copy))

    print("❌ No path found.")
    return []


if __name__ == '__main__':
    # 测试用例
    image_path = "test/astar_test.png"
    image = Image.open(image_path).convert("RGB")

    path = Astar_pathfinder(image)
    print("Path steps:", len(path))

    # 可视化路径
    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    if len(path) > 0:
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], color='blue', linewidth=2)
    plt.axis('off')
    plt.show()
