"""
- Undirected graph
- Vertices and weighted edges
- Find shortest closed path that visits every edge at least once
- Kruskal's Algorithm
  1. sort all edges in the graph by their weight
  2. initialize a disjoint set for each vertex
  3. iterate through the sorted edges and add each edge to the MST if it doesn't form a cycle
  4. repeat until the MST contains (V-1) edges, where V is the number of vertices
"""

import pygame
import random
import sys
import math

reverse_mst = False

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("chinese postman")

colors = {
  'white': (230, 230, 230),
  'gray': (50, 50, 50),
  'black': (25, 25, 25),
  'red': (120, 20, 20),
  'green': (20, 120, 20),
  'blue': (20, 20, 120)
}

class Vertex:
  def __init__(self, key, x, y):
    self.id = key
    self.connected_to = {}
    self.x = x
    self.y = y

  def add_neighbor(self, neighbor, weight=0):
    self.connected_to[neighbor] = weight

  def get_connections(self):
    return self.connected_to.keys()

  def get_id(self):
    return self.id

  def get_weight(self, neighbor):
    return self.connected_to[neighbor]

  def draw(self, screen):
    pygame.draw.circle(screen, colors['red'], (self.x, self.y), 10)
    font = pygame.font.SysFont(None, 20)
    img = font.render(self.id, True, colors['white'])
    screen.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))

class Graph:
  def __init__(self):
    self.vert_list = {}
    self.num_vertices = 0

  def add_vertex(self, key, x, y):
    self.num_vertices += 1
    new_vertex = Vertex(key, x, y)
    self.vert_list[key] = new_vertex
    self.update_edges()
    return new_vertex

  def get_vertex(self, n):
    if n in self.vert_list:
      return self.vert_list[n]
    else:
      return None

  def add_edge(self, frm, to, cost=0):
    if frm not in self.vert_list:
      raise ValueError(f"Vertex {frm} does not exist.")
    if to not in self.vert_list:
      raise ValueError(f"Vertex {to} does not exist.")
    self.vert_list[frm].add_neighbor(self.vert_list[to], cost)
    self.vert_list[to].add_neighbor(self.vert_list[frm], cost)

  def get_vertices(self):
    return self.vert_list.keys()

  def update_edges(self):
    self.edges = []
    vertices = list(self.vert_list.values())
    for i in range(len(vertices)):
      for j in range(i + 1, len(vertices)):
        v1 = vertices[i]
        v2 = vertices[j]
        distance = math.hypot(v1.x - v2.x, v1.y - v2.y)
        self.add_edge(v1.get_id(), v2.get_id(), distance)

  def remove_vertex(self, vertex_id):
    if vertex_id in self.vert_list:
      for neighbor in list(self.vert_list[vertex_id].get_connections()):
        self.vert_list[neighbor.get_id()].connected_to.pop(self.vert_list[vertex_id], None)
      del self.vert_list[vertex_id]
      self.num_vertices -= 1
      self.update_edges()

  def renumber_vertices(self):
    new_vert_list = {}
    for i, (key, vertex) in enumerate(sorted(self.vert_list.items(), key=lambda x: int(x[0]))):
      new_id = str(i + 1)
      vertex.id = new_id
      new_vert_list[new_id] = vertex
    self.vert_list = new_vert_list
    self.update_edges()

  def draw(self, screen):
    for vertex in self.vert_list.values():
      for neighbor in vertex.get_connections():
        pygame.draw.line(screen, colors['gray'], (vertex.x, vertex.y), (neighbor.x, neighbor.y), 2)
    for vertex in self.vert_list.values():
      vertex.draw(screen)

  def __iter__(self):
    return iter(self.vert_list.values())

  def generate_vertices(self, n):
    self.num_vertices = 0
    for x in range(n):
      graph.add_vertex(str(x+1), random.randrange(width // 8, 7 * width // 8), random.randrange(height // 8, 7 * height // 8))

class DisjointSet:
  def __init__(self, vertices):
    self.parent = {v: v for v in vertices}
    self.rank = {v: 0 for v in vertices}

  def find(self, item):
    if self.parent[item] == item:
      return item
    else:
      self.parent[item] = self.find(self.parent[item])
      return self.parent[item]

  def union(self, set1, set2):
    root1 = self.find(set1)
    root2 = self.find(set2)

    if root1 != root2:
      if self.rank[root1] > self.rank[root2]:
        self.parent[root2] = root1
      else:
        self.parent[root1] = root2
        if self.rank[root1] == self.rank[root2]:
          self.rank[root2] += 1

def kruskal_mst(graph):
  edges = []
  for vertex in graph:
    for neighbor in vertex.get_connections():
      edges.append((vertex.get_weight(neighbor), vertex, neighbor))
  edges.sort(key=lambda x: x[0], reverse=reverse_mst)

  ds = DisjointSet(graph.get_vertices())
  mst = []

  for weight, vertex, neighbor in edges:
    if ds.find(vertex.get_id()) != ds.find(neighbor.get_id()):
      ds.union(vertex.get_id(), neighbor.get_id())
      mst.append((vertex, neighbor, weight))

  return mst

def draw_mst(screen, mst):
  for vertex, neighbor, weight in mst:
    pygame.draw.line(screen, colors['green'], (vertex.x, vertex.y), (neighbor.x, neighbor.y), 2)

def draw_graph(screen, graph, mst):
  for vertex in graph:
    for neighbor in vertex.get_connections():
      pygame.draw.line(screen, colors['gray'], (vertex.x, vertex.y), (neighbor.x, neighbor.y), 2)
  draw_mst(screen, mst)
  for vertex in graph:
    vertex.draw(screen)

graph = Graph()
graph.generate_vertices(10)
mst = kruskal_mst(graph)

running = True
selected_vertex = None

def get_vertex_at_pos(x, y):
  for vertex in graph:
    if math.hypot(vertex.x - x, vertex.y - y) < 10:
      return vertex
  return None

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        mouse_x, mouse_y = event.pos
        selected_vertex = get_vertex_at_pos(mouse_x, mouse_y)
        if not selected_vertex:
          graph.add_vertex(str(graph.num_vertices + 1), mouse_x, mouse_y)
          mst = kruskal_mst(graph)
      elif event.button == 3:
        mouse_x, mouse_y = event.pos
        selected_vertex = get_vertex_at_pos(mouse_x, mouse_y)
        if selected_vertex:
          graph.remove_vertex(selected_vertex.get_id())
          graph.renumber_vertices()
          graph.update_edges()
          mst = kruskal_mst(graph)
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        selected_vertex = None
    elif event.type == pygame.MOUSEMOTION:
      if selected_vertex:
        selected_vertex.x, selected_vertex.y = event.pos
        graph.update_edges()
        mst = kruskal_mst(graph)
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        graph.vert_list = {}
        graph.generate_vertices(random.randrange(2, 10))
        mst = kruskal_mst(graph)
      elif event.key == pygame.K_e:
        reverse_mst = not reverse_mst
        mst = kruskal_mst(graph)
        draw_mst(screen, mst)
      elif event.key == pygame.K_c:
        graph.vert_list = {}
        graph.generate_vertices(0)
        mst = kruskal_mst(graph)
    elif event.type == pygame.VIDEORESIZE:
      width, height = event.size
      screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

  screen.fill(colors['black'])
  draw_graph(screen, graph, mst)
  pygame.display.flip()

pygame.quit()
sys.exit()