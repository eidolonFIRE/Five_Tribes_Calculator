import pygame

class Button:
	def __init__(self, rect, color, text, size, shape, handler, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.text = text
		self.shape = shape
		self.handler = handler
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
		if self.handler != None:
			self.handler()

#==============================================================================

class List:
	def __init__(self, rect, color, text, size, handler, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.text = text
		self.size = size
		self.handler = handler
		self.layers = layers
	def draw(self, display):
		pygame.draw.rect(display, (20,20,20), [self.x,self.y,self.w,self.h])
		drawy = self.size
		#font = pygame.font.Font(None, self.size * 4 / 3)
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
		if self.handler != None:
			index = (int(pos[1] - self.y - self.size / 2) / self.size)
			if index < len(self.text) and index >= 0:
				self.handler(index)

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
		pygame.draw.polygon(display, (0,0,0),
			[(self.x + self.w / 20    , self.y + self.h / 2          ),
			 (self.x + self.w / 5     , self.y + self.h / 10         ),
			 (self.x + self.w / 5     , self.y + self.h - self.h / 10)])
		pygame.draw.polygon(display, (0,0,0),
			[(self.x + self.w * 19 / 20  , self.y + self.h / 2          ),
			 (self.x + self.w * 4 / 5    , self.y + self.h / 10         ),
			 (self.x + self.w * 4 / 5    , self.y + self.h - self.h / 10)])
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
		if self.handler != None:
			if pos[0] < self.x + self.w / 2:
				self.value = self.value - 1
				self.forceLimit()
			else:
				self.value = self.value + 1
				self.forceLimit()
			self.handler(self.value)

#==============================================================================

class CheckBox:
	def __init__(self, rect, isChecked, color, text, textSize, handler, layers):
		self.x = rect[0]
		self.y = rect[1]
		self.w = rect[2]
		self.h = rect[3]
		self.color = color
		self.text = text
		self.textSize = textSize
		self.handler = handler
		self.layers = layers
		self.checked = isChecked
	def draw(self, display):
		pygame.draw.rect(display, self.color, [self.x,self.y,self.w,self.h])
		pygame.draw.rect(display, (0,0,0),
			[self.x + self.w / 10, self.y + self.h / 10,
			 self.h * 8/10, self.h * 8/10])
		if self.checked:
			pygame.draw.rect(display, (255,255,255),
				[self.x + self.w / 10 + self.h * 1/10, self.y + self.h * 2/10,
				 self.h * 6/10, self.h * 6/10])
		font = pygame.font.Font(None, self.textSize)
		text = font.render(self.text, 1, (255,255,255))
		textpos = (
			-text.get_rect().center[0] + self.x + self.w * 5/10, 
			-text.get_rect().center[1] + self.y + self.h * 5/10)
		display.blit(text, textpos)
	def down(self, pos):
		if self.handler != None:
			if self.checked:
				self.checked = False
			else:
				self.checked = True
			self.handler(self.checked)


#==============================================================================

class GUI:
	def __init__(self, display):
		self.objects = {}
		self.mode = "edit"
		self.display = display
		self.sprites = {}
	def draw(self):
		for key in self.objects:
			if self.mode in self.objects[key].layers or "all" in self.objects[key].layers:
				self.objects[key].draw(self.display)
	def mouseDown(self, pos):
		for key in self.objects:
			if self.mode in self.objects[key].layers or "all" in self.objects[key].layers:
				if pos[0] > self.objects[key].x \
				and pos[0] < self.objects[key].x + self.objects[key].w \
				and pos[1] > self.objects[key].y \
				and pos[1] < self.objects[key].y + self.objects[key].h:
					self.objects[key].down(pos)
