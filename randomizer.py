import random

class Randomizer:

	def get_random_color(self, count):
		result = []
		for i in range(0, count):
			r = random.randrange(0, 255, 1)
			g = random.randrange(0, 255, 1)
			b = random.randrange(0, 255, 1)
			if r > 220 and g > 220 and b > 220:
				r = random.randrange(0, 150, 1)
				b = random.randrange(50, 100, 1)
			result.append((r, g, b)) 	
		return result

	def get_random_block_numbers(self, time):
		seconds = time/1000
		if (time < 1000):
			seconds = 50
		elif (seconds < 100):
			seconds = time/100

		base = random.randrange(int(150 * ((seconds/100 + 1))), int(175 * (seconds / 25)), 1)
		# print base
		big_int = random.randrange(int(base * 1.5), int(base * 2.3), 2)
		# print big_int
		small_int = random.randrange(int(base * 0.80), int(base * 1.2), 1)
		# print small_int
		random_int = random.randrange(small_int, big_int - (base / 10), 10)
		# print random_int
		
		numbers = [base, big_int, small_int, random_int, random_int * 2]
		random.shuffle(numbers)

		return numbers