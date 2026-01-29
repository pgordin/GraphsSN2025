from manim import *

class Own_Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_list = {i: set() for i in range(num_vertices)}
    
    def add_edge(self, u, v):
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)
    
    def degree(self, v):
        return len(self.adj_list[v])
    
    def neighbors(self, v):
        return self.adj_list[v]

class GraphColoring(Scene):
    def construct(self):
        # set up of the graph
        vertices = list(range(11))
        edges = [
            (0, 1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
            (0,10),(1,4),(1,5),(2,5),(2,6),(3,4),(3,10),
            (4,5),(4,8),(4,10),(5,6),(5,8),(5,9),(5,10),
            (6,7),(6,9),(6,10),(7,10),(8,10),(9,10)]
        lt = {
            0: [4, 4, 0],
            1: [1.5, 2, 0],
            2: [2.5, 2, 0],
            3: [-4, 0, 0],
            4: [-2.5, 0, 0],
            5: [0, 0, 0],
            6: [2, 0, 0],
            7: [3, 0, 0],
            8: [1.5, -2, 0],
            9: [2.5, -2, 0],
            10: [4, -4, 0],
        }
        # visualization - create graph and texts
        g = Graph(
            vertices, 
            edges, 
            layout=lt, 
            vertex_config={
                "fill_color": BLACK,
                "fill_opacity": 1,
                "radius": 0.3,
                "stroke_color": WHITE,
                "stroke_width": 2
            },
            labels=True,
            label_fill_color=WHITE
        ).scale(0.8) 
        self.play(Create(g), run_time=3)
        self.wait()
        stack = Text("Stack: ", font_size=36).to_edge(UP + LEFT)  
        low_degree_vertex_label = Text("Low deg. vertex:", font_size=36).to_edge(DOWN + LEFT)
        self.play(Write(stack), Write(low_degree_vertex_label))   
        self.wait()
        graph = Own_Graph(len(vertices))
        for u, v in edges:
            graph.add_edge(u, v)
        n = graph.num_vertices
        colors = {}
        active = set(range(n))
        removal_order = []
        stack_top = stack
        stack_texts = []
        while active:
            for v in active:
                # visualization - highlight neighbors
                incident_edges = [e for e in g.edges if v in e and (e[0] in active and e[1] in active)]
                self.play(
                        g.vertices[v].animate.set_stroke(YELLOW),
                        *[g.edges[e].animate.set_stroke(YELLOW) for e in incident_edges],
                )
                # coloring algorythm
                active_degree = sum(1 for neighbor in graph.neighbors(v) 
                                  if neighbor in active)
                if active_degree <= 5:
                    # visualization - write low deg. vertex, remove it from graph and move to stack
                    low_degree_text = Integer(v, font_size=50, color=WHITE)
                    low_degree_text.next_to(low_degree_vertex_label, RIGHT, buff=0.2)
                    self.play(FadeIn(low_degree_text))
                    self.play(
                        g.vertices[v].animate.set_stroke(DARKER_GRAY),
                        *[g.edges[e].animate.set_stroke(DARKER_GRAY) for e in incident_edges],
                    )
                    self.play(low_degree_text.animate.next_to(stack_top, RIGHT, buff=0.2))
                    stack_texts.append(low_degree_text)
                    stack_top = low_degree_text
                    # algorythm part
                    low_degree_vertex = v
                    break
                else:
                    self.play(
                        g.vertices[v].animate.set_stroke(WHITE),
                        *[g.edges[e].animate.set_stroke(WHITE) for e in incident_edges],
                )
            removal_order.append(low_degree_vertex)       
            active.remove(low_degree_vertex)
        # visualization - remove text low deg. vertex
        self.play(FadeOut(low_degree_vertex_label))
        # coloring phase
        # visualization - colors
        color_palette_label = Text("Available colors", font_size=24).to_edge(LEFT).shift(2*DOWN+RIGHT)
        self.play(Write(color_palette_label))
        vertex_colors = [RED_D, GREEN_D, BLUE_D, YELLOW_D, PURPLE_B]
        color_boxes = VGroup()
        for i, color in enumerate(vertex_colors):
            box = Square(side_length=0.4)
            box.set_fill(color, opacity=1)
            box.set_stroke(WHITE, width=2)
            color_boxes.add(box)
        color_boxes.arrange(RIGHT, buff=0.2)
        color_boxes.next_to(color_palette_label, DOWN, buff=0.3)
        self.play(Create(color_boxes))
        for v in reversed(removal_order):
            # visualization - highlight top stack element, remove from stack and mark
            current_node = stack_texts.pop()
            self.play(
                Indicate(current_node, scale_factor=1.4, color=WHITE),
                Indicate(g.vertices[v], scale_factor=1, color=WHITE)
            )
            self.play(FadeOut(current_node))
            stack_top = stack_texts[-1] if stack_texts else stack
            incident_edges = [e for e in g.edges if v in e]
            neighbors = graph.neighbors(v)
            self.play(
                g.vertices[v].animate.set_stroke(WHITE)
            )
            used_colors = set()
            for neighbor in neighbors:
                if neighbor in colors:
                    # algotythm
                    used_colors.add(colors[neighbor])
                    # visualization - indicate colored neighbors and mark in color palette
                    edge = None
                    if (v, neighbor) in g.edges:
                        edge = (v, neighbor)
                    elif (neighbor, v) in g.edges:
                        edge = (neighbor, v)
                    self.play(
                        Indicate(g.vertices[neighbor], scale_factor=1, color=WHITE),
                        g.edges[edge].animate.set_stroke(WHITE),
                    )
                    self.play(
                        color_boxes[colors[neighbor]].animate.set_fill(vertex_colors[colors[neighbor]], opacity=0.3)
                    )
            for color in range(5):
                if color not in used_colors:
                    # algorythm
                    colors[v] = color
                    # visualization - indicate chosen color, color the vertex
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        g.vertices[v].animate.set_fill(vertex_colors[color]),
                        g._labels[v].animate.set_z_index(2)
                    )
                    break
            # visualization - reset color palete
            self.play(
                *[color_boxes[i].animate.set_fill(vertex_colors[i], opacity=1) for i in range(5)]
                )
        # visualization - center the graph
        self.play(
            FadeOut(stack),
            FadeOut(color_palette_label),
            FadeOut(color_boxes)
            )
        self.wait(12)

class GraphFlip(Scene):
    def construct(self):
        vertices = list(range(11))
        edges = [(0, 1), (0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,10),(1,4),(1,5),(2,5),(2,6),(3,4),(3,10),(4,5),(4,8),(4,10),(5,6),(5,8),(5,9),(5,10),(6,7),(6,9),(6,10),(7,10),(8,10),(9,10)]
        lt = {
            0: [4, 4, 0],
            1: [1.5, 2, 0],
            2: [2.5, 2, 0],
            3: [-4, 0, 0],
            4: [-2.5, 0, 0],
            5: [0, 0, 0],
            6: [2, 0, 0],
            7: [3, 0, 0],
            8: [1.5, -2, 0],
            9: [2.5, -2, 0],
            10: [4, -4, 0],
        }
        g = Graph(
            vertices, 
            edges, 
            layout=lt, 
            vertex_config={
                "fill_color": BLACK,
                "fill_opacity": 1,
                "radius": 0.3,
                "stroke_color": WHITE,
                "stroke_width": 2
            }
        ).scale(0.8)
        self.add(g)
        self.wait(4)
        self.play(Rotate(g, angle=-PI/2))
        self.wait(3)

class GraphColoring4Colors(Scene):
    def construct(self):
        vertices = list(range(11))
        edges = [
            (0,1),(0,9),(0,10),(1,2),(1,3),(1,4),(8,9),
            (1,9),(1,10),(2,4),(2,9),(3,4),(3,10),(8,10),
            (4,5),(4,6),(4,7),(4,9),(4,10),(5,7),(9,10),
            (5,9),(6,7),(6,10),(7,8),(7,9),(7,10),
        ]
        lt = {
            10: [4, -4, 0],
            3: [2, -1.5, 0],
            6: [2, -2.5, 0],
            0: [0, 4, 0],
            1: [0, 2.5, 0],
            4: [0, 0, 0],
            7: [0, -2, 0],
            8: [0, -3, 0],
            2: [-2, -1.5, 0],
            5: [-2, -2.5, 0],
            9: [-4, -4, 0],
        }
        g = Graph(
            vertices, 
            edges, 
            layout=lt, 
            vertex_config={
                "fill_color": BLACK,
                "fill_opacity": 1,
                "radius": 0.3,
                "stroke_color": WHITE,
                "stroke_width": 2
            },
            labels=True,
            label_fill_color=WHITE,
        ).scale(0.8)
        for label in g._labels.values():
            label.set_opacity(0)
        self.add(g)
        self.wait(2)
        for label in g._labels.values():
            self.play(label.animate.set_opacity(1), run_time=0.3)
        self.wait(2)
        self.play(g.animate.to_edge(RIGHT))
        stack = Text("Stack: ", font_size=36).to_edge(UP + LEFT)  
        low_degree_vertex_label = Text("Low deg. vertex:", font_size=36).to_edge(DOWN + LEFT)
        self.play(Write(stack), Write(low_degree_vertex_label))   
        self.wait(2)
        graph = Own_Graph(len(vertices))
        for u, v in edges:
            graph.add_edge(u, v)
        n = graph.num_vertices
        colors = {}
        active = set(range(n))
        removal_order = []
        stack_top = stack
        stack_texts = []
        while active:
            for v in active:
                active_degree = sum(1 for neighbor in graph.neighbors(v) 
                                  if neighbor in active)
                incident_edges = [e for e in g.edges if v in e and (e[0] in active and e[1] in active)]
                self.play(
                        g.vertices[v].animate.set_stroke(YELLOW),
                        *[g.edges[e].animate.set_stroke(YELLOW) for e in incident_edges],
                )
                if active_degree <= 5:
                    low_degree_text = Integer(v, font_size=50, color=WHITE)
                    low_degree_text.next_to(low_degree_vertex_label, RIGHT, buff=0.2)
                    self.play(FadeIn(low_degree_text))
                    self.play(
                        g.vertices[v].animate.set_stroke(DARKER_GRAY),
                        *[g.edges[e].animate.set_stroke(DARKER_GRAY) for e in incident_edges],
                    )
                    self.play(low_degree_text.animate.next_to(stack_top, RIGHT, buff=0.2))
                    stack_texts.append(low_degree_text)
                    stack_top = low_degree_text
                    
                    low_degree_vertex = v
                    break
                else:
                    self.play(
                        g.vertices[v].animate.set_stroke(WHITE),
                        *[g.edges[e].animate.set_stroke(WHITE) for e in incident_edges],
                )
            removal_order.append(low_degree_vertex)       
            active.remove(low_degree_vertex)
        self.play(FadeOut(low_degree_vertex_label))
        color_palette_label = Text("Available colors", font_size=24).to_edge(LEFT).shift(2*DOWN+RIGHT)
        self.play(Write(color_palette_label))
        color_boxes = VGroup()      
        vertex_colors = [RED_D, GREEN_D, BLUE_D, YELLOW_D, PURPLE_B]
        for i, color in enumerate(vertex_colors):
            box = Square(side_length=0.4)
            box.set_fill(color, opacity=1)
            box.set_stroke(WHITE, width=2)
            color_boxes.add(box)
        color_boxes.arrange(RIGHT, buff=0.2)
        color_boxes.next_to(color_palette_label, DOWN, buff=0.3)
        self.play(Create(color_boxes))
        for v in reversed(removal_order):
            current_node = stack_texts.pop()
            self.play(
                Indicate(current_node, scale_factor=1.4, color=WHITE),
                Indicate(g.vertices[v], scale_factor=1, color=WHITE)
            )
            self.play(FadeOut(current_node))
            stack_top = stack_texts[-1] if stack_texts else stack
            neighbors = graph.neighbors(v)
            used_colors = set()
            incident_edges = [e for e in g.edges if v in e]
            self.play(
                g.vertices[v].animate.set_stroke(WHITE)
            )
            for neighbor in neighbors:
                if neighbor in colors:
                    used_colors.add(colors[neighbor])
                    edge = None
                    if (v, neighbor) in g.edges:
                        edge = (v, neighbor)
                    elif (neighbor, v) in g.edges:
                        edge = (neighbor, v)
                    self.play(
                        Indicate(g.vertices[neighbor], scale_factor=1, color=WHITE),
                        g.edges[edge].animate.set_stroke(WHITE),
                    )
                    self.play(
                        color_boxes[colors[neighbor]].animate.set_fill(vertex_colors[colors[neighbor]], opacity=0.3)
                    )
            for color in range(5):
                if color not in used_colors:
                    colors[v] = color
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        Indicate(color_boxes[color],1,WHITE),
                    )
                    self.play(
                        g.vertices[v].animate.set_fill(vertex_colors[color]),
                        g._labels[v].animate.set_z_index(2)
                    )
                    break
            self.play(
                *[color_boxes[i].animate.set_fill(vertex_colors[i], opacity=1) for i in range(5)]
                )            
        self.play(
            FadeOut(stack),
            FadeOut(color_palette_label),
            FadeOut(color_boxes),
            g.animate.center()
        )
        self.wait(5)
        self.play(
            Uncreate(g)
        )
