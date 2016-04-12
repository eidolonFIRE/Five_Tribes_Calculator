import pygame

class Button:
	def __init__(self, rect, color, text, size, shape, method_click, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.text = text
		self.shape = shape
		self.method_click = method_click
		self.layers = layers
		self.size = size
	def draw(self, display):
		if self.shape == "rect":
			pygame.draw.rect(display, self.color, [self.x,self.y,self.w,self.h])
		if self.shape == "ellipse":
			pygame.draw.circ(display, self.color, [self.x,self.y,self.w,self.h])
		font = pygame.font.Font(None, self.size)
		text = font.render(self.text, 1, (0,0,0))
		textpos = (
			-text.get_rect().center[0] + self.x + self.w * 5/10, 
			-text.get_rect().center[1] + self.y + self.h * 5/10)
		display.blit(text, textpos)
	def down(self, pos):
		self.method_click()

#==============================================================================

class List:
	def __init__(self, rect, color, text, size, method_select, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.text = text
		self.size = size
		self.method_select = method_select
		self.layers = layers
	def draw(self, display):
		pygame.draw.rect(display, (20,20,20), [self.x,self.y,self.w,self.h])
		drawy = self.size
		#font = pygame.font.Font("monospace", self.size * 4 / 3)
		font = pygame.font.SysFont("monospace", self.size, bold = True)
		for line in self.text:
			text = font.render(line, 1, self.color)
			textpos = (
				#-text.get_rect().center[0] + self.x         + self.w * 5/10, 
				self.x,
				-text.get_rect().center[1] + self.y + drawy)
			display.blit(text, textpos)
			drawy = drawy + self.size
	def down(self, pos):
		index = (int(pos[1] - self.y - self.size / 2) / self.size)
		if index < len(self.text) and index >= 0:
			self.method_select(index)

#==============================================================================

class ValueBox:
	def __init__(self, rect, color, limit, textSize, handler, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.limit = limit
		self.textSize = textSize
		self.handler = handler
		self.layers = layers
		self.value = 0
	def draw(self, display):
		pygame.draw.rect(display, self.color, [self.x,self.y,self.w,self.h])
		font = pygame.font.Font(None, self.textSize)
		text = font.render(str(self.value), 1, (0,0,0))
		textpos = (
			-text.get_rect().center[0] + self.x + self.w * 5/10, 
			-text.get_rect().center[1] + self.y + self.h * 5/10)
		display.blit(text, textpos)
	def forceLimit(self):
		if self.value > self.limit[1]:
			self.value = self.limit[1]
		if self.value < self.limit[0]:
			self.value = self.limit[0]
	def down(self, pos):
		if pos[0] < self.x + self.w / 2:
			self.value = self.value - 1
			self.forceLimit()
		else:
			self.value = self.value + 1
			self.forceLimit()
		self.handler(self.value)

#==============================================================================

class GUI:
	def __init__(self, display):
		self.objects = {}
		self.mode = "edit"
		self.display = display
	def draw(self):
		for key in self.objects:
			if self.mode in self.objects[key].layers:
				self.objects[key].draw(self.display)
	def addButton(self, name, rect, color, text, size, shape, method_click, layers):
		self.objects[name] = Button(rect, color, text, size, shape, method_click, layers)
	def addList(self, name, rect, color, text, size, method_select, layers):
		self.objects[name] = List(rect, color, text, size, method_select, layers)
	def addValueBox(self, name, rect, color, limit, textSize, handler, layers):
		self.objects[name] = ValueBox(rect, color, limit, textSize, handler, layers)
	def mouseDown(self, pos):
		for key in self.objects:
			if self.mode in self.objects[key].layers:
				if pos[0] > self.objects[key].x \
				and pos[0] < self.objects[key].x + self.objects[key].w \
				and pos[1] > self.objects[key].y \
				and pos[1] < self.objects[key].y + self.objects[key].h:
					self.objects[key].down(pos)
